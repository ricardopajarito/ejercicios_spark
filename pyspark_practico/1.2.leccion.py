from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("mi_app_local") \
    .master("local[*]") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

print(spark.version)   # comprueba la versión de Spark desde Python

# ejemplo rápido para probar
df = spark.createDataFrame([(1, "a"), (2, "b")], ["id", "valor"])
df.show()
