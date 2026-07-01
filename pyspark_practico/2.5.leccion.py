# 0) Imports y SparkSession
from pyspark.sql import SparkSession, functions as F, types as T
from pyspark.sql.functions import pandas_udf
import pandas as pd, time

spark = (
    SparkSession.builder
    .appName("udf-vs-pandasudf-demo")
    .getOrCreate()
)

# (Opcional) habilitar Arrow si tu Spark no lo activa por defecto
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

# 1) DataFrame de prueba (suficiente tamaño)
data = [("a", 1), ("bb", 2), ("ccc", 3)] * 200000   # ≈ 600k filas
df = spark.createDataFrame(data, schema=["s", "n"]).repartition(8)

# 2) UDF clásico
def length_times_n(s, n):
    if s is None:
        return None
    return len(s) * n

udf_len = F.udf(length_times_n, T.IntegerType())

t0 = time.time()
df_udf = df.withColumn("res", udf_len(F.col("s"), F.col("n")))
df_udf.count()   # Forzamos ejecución total
t_udf = time.time() - t0
print("Tiempo UDF clásico (seg):", t_udf)

# 3) Pandas UDF (vectorized)
@pandas_udf(T.IntegerType())
def length_times_n_vectorized(s: pd.Series, n: pd.Series) -> pd.Series:
    return s.str.len().fillna(0).astype(int) * n

t0 = time.time()
df_pudf = df.withColumn("res", length_times_n_vectorized(F.col("s"), F.col("n")))
df_pudf.count()
t_pudf = time.time() - t0
print("Tiempo Pandas UDF (seg):", t_pudf)

# 4) Resultado simple
print("Ratio UDF/PandasUDF:", t_udf / t_pudf)
