# 1) Imports
from pyspark.sql import SparkSession
from time import time
from pyspark.storagelevel import StorageLevel

spark = SparkSession.builder.appName("cache-demo").getOrCreate()
sc = spark.sparkContext

# 2) Leer datos (ejemplo con Parquet delta)
df = spark.read.parquet("/ruta/a/tu/parquet")
# Opcional: reducir columnas antes de cachear (buena práctica)
df_small = df.select("id","timestamp","valor").filter("timestamp >= '2024-01-01'")

# 3) Medir sin cache
t0 = time()
n = df_small.groupBy("id").count().collect()   # ejemplo de acción
t1 = time()
print("Tiempo sin cache:", t1 - t0)

# 4) Cachear y medir
df_small_cached = df_small.cache()  # atajo; por DataFrame, por defecto MEMORY_AND_DISK_DESER
# Alternativa explícita:
# df_small_cached = df_small.persist(StorageLevel.MEMORY_AND_DISK)
# O para ahorrar memoria usando serialización:
# df_small_cached = df_small.persist(StorageLevel.MEMORY_AND_DISK_SER)

# Forzar materialización:
df_small_cached.count()  # primera acción que crea los bloques en cache

t0 = time()
n2 = df_small_cached.groupBy("id").count().collect()
t1 = time()
print("Tiempo con cache (segunda acción):", t1 - t0)

# 5) Comprobar estado y ocupación
print("is_cached:", df_small_cached.is_cached)
print("storageLevel:", df_small_cached.storageLevel)  # muestra el StorageLevel actual

# Información desde el driver:
for rdd_id, rdd in sc.getPersistentRDDs().items():
    print("RDD id:", rdd_id, "->", rdd.name())

# 6) Limpiar cuando termines
df_small_cached.unpersist(blocking=True)  # bloquear hasta que se borren bloques
# o para todo:
spark.catalog.clearCache()
