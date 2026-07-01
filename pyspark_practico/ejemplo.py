
from pyspark.context import SparkContext
from pyspark.sql import Window
from pyspark.sql.functions import row_number, col, broadcast, coalesce
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

spark = SparkSession.builder.appName("leccion_1_4").getOrCreate()
spark.conf.set("spark.sql.debug.maxToStringFields", "1000")

df_brv_tmp = spark.read.csv("BIDMS_2015_REF_VTAS.csv", header=True, inferSchema=True, sep=",")
df_nrv_tmp = spark.read.csv("nsccap_20250907_refventas.csv", header=True, inferSchema=True, sep=",")
df_brv_tmp.printSchema()
df_brv_tmp.show(5, truncate=False)

df_brv = df_brv_tmp.withColumn("FECHAEXTRACCION2", coalesce(
    F.try_to_date(F.trim(F.col("FECHAEXTRACCION")), "dd/MM/yyyy"),
    F.try_to_date(F.trim(F.col("FECHAEXTRACCION")), "MM/dd/yyyy"),
    F.try_to_date(F.trim(F.col("FECHAEXTRACCION")), "yyyy-MM-dd"),
    F.try_to_date(F.trim(F.col("FECHAEXTRACCION")), "dd-MM-yyyy")
))
df_nrv = df_nrv_tmp.withColumn("FECHAEXTRACCION2", coalesce(
    F.try_to_date(F.trim(F.col("FECHAEXTRACCION")), "dd/MM/yyyy"),
    F.try_to_date(F.trim(F.col("FECHAEXTRACCION")), "MM/dd/yyyy"),
    F.try_to_date(F.trim(F.col("FECHAEXTRACCION")), "yyyy-MM-dd"),
    F.try_to_date(F.trim(F.col("FECHAEXTRACCION")), "dd-MM-yyyy")
))

window_spec = Window.partitionBy("FECHAEXTRACCION2", "FACTURA", "FECHAFACTURA", "VENTA").orderBy(col("FECHAEXTRACCION2").desc())
df_filtrado = df_brv.withColumn("orden", row_number().over(window_spec)).filter(col("orden") == 1).drop("orden") 

print("Registros filtrados")
df_filtrado.show(5, truncate=False)

df_filtrado.write.csv("registros_faltantes.csv", header=True, mode="overwrite")


columnas_clave = ["FECHAEXTRACCION2", "FACTURA", "FECHAFACTURA", "VENTA"]

registros_faltantes = df_nrv.join(
    broadcast(df_filtrado), 
    on=columnas_clave, 
    how="left_anti"
)

# Convertir de vuelta a DynamicFrame para la escritura en Glue
# registros_faltantes = registros_faltantes.coalesce(100)

#escribirlos en un csv de forma local
# registros_faltantes.write.csv("registros_faltantes.csv", header=True, mode="overwrite")

# registros_faltantes.show(5, truncate=False)