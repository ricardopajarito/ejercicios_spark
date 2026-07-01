# Ejemplo: broadcast vs normal join (PySpark)
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import broadcast
import time

spark = SparkSession.builder \
    .appName("broadcast_demo") \
    .getOrCreate()

# Datos de ejemplo (ajusta tamaños para tu cluster)
large = spark.range(0, 500000).withColumn("key", (F.col("id") % 1000)).withColumn("value", F.lit("x"))
small = spark.range(0, 1000).withColumnRenamed("id", "key").withColumn("attr", F.concat(F.lit("cat_"), F.col("key")))

# Join normal (probablemente SortMergeJoin)
t0 = time.time()
res_normal = large.join(small, "key")
res_normal.count()  # forzar ejecución
t_normal = time.time() - t0

# Join con broadcast
t0 = time.time()
res_b = large.join(broadcast(small), "key")
res_b.count()
t_broadcast = time.time() - t0

# Mostrar planes
print("Plan normal:")
res_normal.explain("formatted")
print("\nPlan broadcast:")
res_b.explain("formatted")

print(f"Tiempo normal: {t_normal:.1f}s, Tiempo broadcast: {t_broadcast:.1f}s")
