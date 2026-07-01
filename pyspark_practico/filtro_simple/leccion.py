from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("leccion").getOrCreate()
spark.conf.set("spark.sql.debug.maxToStringFields", "1000")

df = spark.read.csv("transactions.csv", header=True, inferSchema=True, sep=",")
df.printSchema()
df.show(5, truncate=False)

# se quitan nulos en columnas críticas
df_clean = df.dropna(subset=["transaction_id", "user_id", "amount", "transaction_date"])

print("DataFrame limpio:")
df_clean.show(5, truncate=False)

df_clean_filtered = df_clean.filter(df_clean.amount > 100)

print("DataFrame filtrado:")
df_clean_filtered.show(5, truncate=False)

df_clean_filtered.write \
    .mode("overwrite") \
    .partitionBy("country") \
    .parquet("output/transactions_parquet")

# 7. (Opcional) Leer el parquet para verificar
df_result = spark.read.parquet("output/transactions_parquet")
df_result.show(5)
df_result.printSchema()




