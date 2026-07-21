import os
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F
from pyspark.sql.functions import col, trim, regexp_replace, when, to_date, date_format

spark = SparkSession.builder \
    .appName("WindowDemo") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.hudi.catalog.HoodieCatalog") \
    .config("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension") \
    .config("spark.jars.packages", "org.apache.hudi:hudi-spark3.5-bundle_2.12:0.15.0") \
    .getOrCreate()

path_hudi = "/Users/RChapuli/Documents/DATOS_DATOS_PRE/python-pyspark/pyspark_faltantes/ejemplo1/datos_hudi"

# Lee la carpeta usando el formato 'hudi'
df_hudi = spark.read \
    .format("hudi") \
    .load(path_hudi)

# Muestra los primeros datos cargados y el esquema
df_hudi.show(5)
df_hudi.printSchema()

