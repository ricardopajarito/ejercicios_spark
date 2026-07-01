from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, col, expr, rand, floor

spark = SparkSession.builder.appName("joins-demo").getOrCreate()

# 1) comprobar umbrales/particiones
print("autoBroadcastJoinThreshold:", spark.conf.get("spark.sql.autoBroadcastJoinThreshold"))
print("shuffle.partitions:", spark.conf.get("spark.sql.shuffle.partitions"))

# 2) crear datos de ejemplo
lookup = spark.createDataFrame([(1, "A"), (2, "B"), (3, "C")], ["id", "label"])
big = spark.range(0, 2_000_000).withColumn("id", (col("id") % 3) + 1)

# 3) join sin forzar (posible shuffle)
j1 = big.join(lookup, "id", "inner")
j1.explain(True)   # mira si aparece SortMergeJoin o BroadcastHashJoin

# 4) forzar broadcast (si lookup cabe)
j2 = big.join(broadcast(lookup), "id", "inner")
j2.explain(True)   # deberías ver BroadcastHashJoin

# 5) ejemplo sencillo de salting (para claves skew)
n_salts = 8
big_salted = big.withColumn("salt", floor(rand() * n_salts))
lookup_salted = lookup.crossJoin(spark.range(0, n_salts).withColumnRenamed("id", "salt"))
joined_salted = big_salted.join(lookup_salted, ["id", "salt"])
joined_salted.explain(True)
