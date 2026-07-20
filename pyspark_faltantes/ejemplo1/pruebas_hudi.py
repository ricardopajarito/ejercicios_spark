import os
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F
from pyspark.sql.functions import col, trim, regexp_replace, when, to_date, date_format

spark = SparkSession.builder \
    .appName("WindowDemo") \
    .getOrCreate()

# Leer el archivo o directorio Parquet
df = spark.read.parquet("../assets/8b67f00d-384d-4122-ac17-a316affa7650-0_0-552-3082_20260329114448659.parquet")

print(df.schema.json())

df.createOrReplaceTempView("servventas")
res = spark.sql("""
  SELECT *
  FROM servventas
    WHERE DIRECCION != null OR FECHAENTREGA1 != 'null'
    LIMIT 10
""")
# res = res.withColumn("Columna_Prueba", F.lit(None).cast("string"))

# Mostrar los primeros registros
res.show(truncate=False)

res.coalesce(1).write.option("header", "true").csv("../output/direccion_no_null.csv")

