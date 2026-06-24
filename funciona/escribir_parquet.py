import os
from pyspark.sql import SparkSession

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "assets", "archivo.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

spark = SparkSession.builder \
    .appName("CsvToParquet") \
    .getOrCreate()

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"No se encontró el archivo CSV en: {CSV_PATH}")

print(f"Leyendo CSV desde: {CSV_PATH}")
df = spark.read.option("header", "true").option("inferSchema", "true").csv(CSV_PATH)

print(f"Escribiendo Parquet en: {OUTPUT_DIR}")
df.write.mode("overwrite").parquet(OUTPUT_DIR)

spark.stop()


