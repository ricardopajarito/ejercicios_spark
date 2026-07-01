# 1. Crear la sesión de Spark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Mini-lab ETL corto") \
    .getOrCreate()

# 2. Leer el fichero CSV
df = spark.read.csv("transactions.csv", header=True, inferSchema=True)

# 3. Mostrar las primeras filas y el esquema
df.show(5)
df.printSchema()

# 4. Eliminar filas con valores nulos en columnas críticas
df_clean = df.dropna(subset=["transaction_id", "user_id", "amount", "transaction_date"])

df_clean.show(5, truncate=False)

# # 5. Filtrar solo transacciones con amount > 100
# df_filtered = df_clean.filter(df_clean.amount > 100)

# # 6. Guardar los resultados en Parquet particionando por country
# df_filtered.write \
#     .mode("overwrite") \
#     .partitionBy("country") \
#     .parquet("output/transactions_parquet")

# # 7. (Opcional) Leer el parquet para verificar
# df_result = spark.read.parquet("output/transactions_parquet")
# df_result.show(5)
# df_result.printSchema()
