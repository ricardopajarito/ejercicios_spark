# Ejemplo PySpark: escribir parquet con compresión y activar AQE
from pyspark.sql import SparkSession

spark = (SparkSession.builder
         .appName("ejemplo_parquet_aqe")
         .config("spark.sql.adaptive.enabled", "true")
         .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
         # Umbral para convertir a shuffled hash join (bytes)
         .config("spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold", str(64 * 1024 * 1024))
         .getOrCreate())

# Leer datos (ejemplo)
df = spark.read.csv("/datos/raw/transactions.csv", header=True, inferSchema=True)

# Transformación simple
from pyspark.sql.functions import col
df_small = df.filter(col("country") == "ES")

# Escribir Parquet con compresión ZSTD (si tu Spark soporta ZSTD)
(df_small
 .repartition(200)   # objetivo: controlar número de ficheros de salida
 .write
 .option("compression", "zstd")  # prueba zstd, snappy o lz4 según tu caso
 .mode("overwrite")
 .parquet("/datos/processed/transactions_parquet/"))
