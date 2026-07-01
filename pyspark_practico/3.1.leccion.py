# Inicialización
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import shutil, os

spark = (
    SparkSession.builder
    .appName("partitioning-demo")
    .getOrCreate()
)

# Creamos un DataFrame de ejemplo relativamente grande
# Generaremos datos sintéticos para simular un dataset de ventas
n_rows = 1000000  # 1 millón de filas
data = [(i % 1000, f"producto_{i%100}", i*0.1) for i in range(n_rows)]
cols = ["region_id", "producto", "importe"]

df = spark.createDataFrame(data, cols)

# Observamos cuántas particiones tiene por defecto
print(f"Número inicial de particiones: {df.rdd.getNumPartitions()}")

# Guardamos el DataFrame en disco para ver los archivos físicos
output_path = "/tmp/particionamiento_demo"

# Borramos si existía antes
if os.path.exists(output_path):
    shutil.rmtree(output_path)

df.write.mode("overwrite").parquet(output_path)

# Revisamos cuántos archivos se generaron
print("Archivos generados inicialmente:")
print(len(os.listdir(output_path)))

# Reducimos el número de particiones con coalesce()
df_coalesced = df.coalesce(2)
df_coalesced.write.mode("overwrite").parquet(output_path + "_coalesce")

print("Archivos tras coalesce(2):")
print(len(os.listdir(output_path + "_coalesce")))

# Aumentamos el número de particiones con repartition()
df_repart = df.repartition(50)
df_repart.write.mode("overwrite").parquet(output_path + "_repart50")

print("Archivos tras repartition(50):")
print(len(os.listdir(output_path + "_repart50")))

# Medimos el tiempo de escritura para ver el impacto
import time

start = time.time()
df.coalesce(1).write.mode("overwrite").parquet(output_path + "_uno")
print("Tiempo coalesce(1):", round(time.time() - start, 2), "s")

start = time.time()
df.repartition(100).write.mode("overwrite").parquet(output_path + "_cien")
print("Tiempo repartition(100):", round(time.time() - start, 2), "s")
