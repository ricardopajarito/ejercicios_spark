from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F

spark = SparkSession.builder \
    .appName("WindowDemo") \
    .getOrCreate()

# data_bi = [
#     ("10/10/2025", "10/10/2025", "02/01/2025", "FG23962", 9394.00),
#     ("10/10/2025", "10/10/2025", "02/01/2025", "FG23963",   1020.99),
#     ("10/10/2025", "10/10/2025", "02/01/2025",  "FG23964", 236.42),
#     ("10/10/2025", "10/10/2025", "02/01/2025",  "FG23964",  236.42),
#     ("10/10/2025", "10/10/2025", "02/01/2025",  "FG23964",  236.42),
#     ("10/10/2025", "10/10/2025", "02/01/2025", "FS186821",   239.84),
#     ("10/10/2025", "10/10/2025", "02/01/2025",  "FS186822", 198.27),
#     ("10/10/2025", "10/10/2025", "02/01/2025",  "FS186825", 156.49),
#     ("10/10/2025", "10/10/2025", "03/01/2025",  "FS186825",  156.49),
#     ("10/10/2025", "10/10/2025", "03/01/2026",  "FS186825",  156.49),
#     ("10/10/2025", "10/10/2025", "03/01/2026",  "FS186825",  156.49),
#     ("10/10/2026", "10/10/2025", "03/01/2026",  "FS186825",  156.49),
#     ("10/10/2028", "10/10/2025", "03/01/2026",  "FS186825",  156.49),
#     ("10/10/2027", "10/10/2025", "03/01/2026",  "FS186827",  157.49),
#     ("10/10/2024", "10/10/2025", "03/01/2026",  "FS186827",  157.49),
# ]

# data_nsccap = [
#     ("10/10/2025", "02/01/2025", "FG23962", 9394.00),
#     ("10/10/2025", "02/01/2025", "FG23963",   1020.99),
#     ("10/10/2025", "02/01/2025",  "FG23964", 236.42),
#     ("10/10/2025", "02/01/2025",  "FG23964",  236.42),
#     ("10/10/2025", "02/01/2025",  "FG23964",  236.42),
#     ("10/10/2025", "02/01/2025", "FS186821",   239.84),
#     ("10/10/2025", "02/01/2025",  "FS186822", 198.27),
#     ("10/10/2025", "02/01/2025",  "FS186825", 156.49),
#     ("10/10/2025", "03/01/2025",  "FS186825",  156.49),
#     ("10/10/2025", "03/01/2026",  "FS186825",  156.49),
#     ("2024-10-10", "03/01/2026",  "FS186825",  156.49),
# ]
# cols = ["LOADDATE_DATE", "FechaExtraccion","FechaFactura","Factura","Venta"]
# df_bi = spark.createDataFrame(data_bi, cols)

print("Datos de BI")
# df_bi.show(truncate=False)

# leer de un archivo csv de ejemplo
df_bi = spark.read.csv("assets/BIDMS_2015_REF_VTAS.csv", header=True, inferSchema=True, sep=",")
df_bi.printSchema()
df_bi.show(5, truncate=False)

# df_nsccap = spark.createDataFrame(data_nsccap, cols)

# agregar la columna LOADDATE_DATE ya que no esta en el csv de df_bi, con un valor fijo para simular que todas las filas de NSCCAP tienen la misma fecha de carga
df_bi = df_bi.withColumn("LOADDATE_DATE", F.lit("2025-10-10"))
df_bi.show(5, truncate=False)

# Detectar duplicados ignorando LOADDATE_DATE, y quedarnos con el registro más reciente por el campo LOADDATE_DATE
# Primero convertimos LOADDATE_DATE a tipo date para ordenar correctamente por antigüedad.
df_bi = df_bi.withColumn(
    "LOADDATE_DATE_PARSED",
    F.coalesce(
        F.to_date("LOADDATE_DATE", "dd/MM/yyyy"),
        F.to_date("LOADDATE_DATE", "yyyy-MM-dd")
    )
)

key_cols = ["Factura", "FechaFactura", "FechaExtraccion", "Venta"]
w = Window.partitionBy(*key_cols).orderBy(F.desc("LOADDATE_DATE_PARSED"))

df_filtrado = df_bi.withColumn("orden", F.row_number().over(w)).filter(F.col("orden") == 1).drop("orden")

print("Datos de BI filtrados (manteniendo la fila más reciente por LOADDATE_DATE)")
df_filtrado.show(5, truncate=False)

# Opcional: mostrar todos los registros que pertenecen a grupos duplicados ignorando LOADDATE_DATE
df_duplicados = df_bi.withColumn("dup_count", F.count("*").over(Window.partitionBy(*key_cols))).filter(F.col("dup_count") > 1).drop("dup_count")
print("Registros duplicados ignorando LOADDATE_DATE")
df_duplicados.show(5, truncate=False)

# registros_faltantes = df_filtrado.join(
#     df_nsccap,
#     on=cols, 
#     how="left_anti"
# )

# print("Registros faltantes")
# registros_faltantes.show(truncate=False)





# escribirlos en un csv de forma local haciendo repartition para controlar el número de ficheros de salida
# (registros_faltantes
#  .repartition(2)   # objetivo: controlar número de ficheros de salida
#  .write
#  .option("compression", "zstd")  # prueba zstd, snappy o lz4 según tu caso
#  .mode("overwrite")
#  .parquet("/datos/processed/transactions_parquet/"))

