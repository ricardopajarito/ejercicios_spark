from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F

spark = SparkSession.builder \
    .appName("WindowDemo") \
    .getOrCreate()

data_bi = [
    ("10/10/2025", "02/01/2025", "FG23962", 9394.00),
    ("10/10/2025", "02/01/2025", "FG23963",   1020.99),
    ("10/10/2025", "02/01/2025",  "FG23964", 236.42),
    ("10/10/2025", "02/01/2025",  "FG23964",  236.42),
    ("10/10/2025", "02/01/2025",  "FG23964",  236.42),
    ("10/10/2025", "02/01/2025", "FS186821",   239.84),
    ("10/10/2025", "02/01/2025",  "FS186822", 198.27),
    ("10/10/2025", "02/01/2025",  "FS186825", 156.49),
    ("10/10/2025", "03/01/2025",  "FS186825",  156.49),
    ("10/10/2025", "03/01/2026",  "FS186825",  156.49),
    ("2024-10-10", "03/01/2026",  "FS186825",  156.49),
    ("10/10/2027", "03/01/2026",  "FS186827",  157.49),
]

data_nsccap = [
    ("10/10/2025", "02/01/2025", "FG23962", 9394.00),
    ("10/10/2025", "02/01/2025", "FG23963",   1020.99),
    ("10/10/2025", "02/01/2025",  "FG23964", 236.42),
    ("10/10/2025", "02/01/2025",  "FG23964",  236.42),
    ("10/10/2025", "02/01/2025",  "FG23964",  236.42),
    ("10/10/2025", "02/01/2025", "FS186821",   239.84),
    ("10/10/2025", "02/01/2025",  "FS186822", 198.27),
    ("10/10/2025", "02/01/2025",  "FS186825", 156.49),
    ("10/10/2025", "03/01/2025",  "FS186825",  156.49),
    ("10/10/2025", "03/01/2026",  "FS186825",  156.49),
    ("2024-10-10", "03/01/2026",  "FS186825",  156.49),
]
cols = ["FechaExtraccion","FechaFactura","Factura","Venta"]
df = spark.createDataFrame(data_bi, cols)
df_nsccap = spark.createDataFrame(data_nsccap, cols)

# se estan eliminando los duplicados, pero no se esta quedando con el ultimo registro, por lo que no se esta filtrando correctamente
w = Window.partitionBy("Factura", "FechaFactura", "FechaExtraccion", "Venta").orderBy(F.desc("FechaExtraccion"))
df_filtrado = df.withColumn("orden", F.row_number().over(w)).filter(F.col("orden") == 1).drop("orden")

df_filtrado.show(truncate=False)

registros_faltantes = df_filtrado.join(
    df_nsccap,
    on=cols, 
    how="leftanti"
)

print("Registros faltantes")
registros_faltantes.show(truncate=False)



# w2 = Window.partitionBy("user_id").orderBy(F.desc("event_time"))
# df_latest = events_df.withColumn("rn", F.row_number().over(w2)) \
#                      .filter(F.col("rn") == 1) \
#                      .drop("rn")
# df_latest.show(truncate=False)
