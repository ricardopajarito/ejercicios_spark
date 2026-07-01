# 1. Crear la sesión de Spark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Mini-lab ETL corto") \
    .getOrCreate()

# 2. Leer el fichero CSV (añade las opciones necesarias)
df = spark.read.____("data/transactions.csv", ____=True, ____=True)

# 3. Mostrar las primeras filas y el esquema
df.____(5)
df.____()

# 4. Eliminar filas con valores nulos en columnas críticas
df_clean = df.____(subset=["transaction_id", "user_id", "amount", "transaction_date"])

# 5. Filtrar solo transacciones con amount > 100
df_filtered = df_clean.____(df_clean.amount > ____)

# 6. Guardar los resultados en Parquet particionando por country
df_filtered.write \
    .mode("____") \
    .____("country") \
    .____("output/transactions_parquet")

# 7. (Opcional) Leer el parquet para verificar
df_result = spark.read.____("output/transactions_parquet")
df_result.show(5)
