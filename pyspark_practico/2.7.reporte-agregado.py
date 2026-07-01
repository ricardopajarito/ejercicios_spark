# 0) Imports y SparkSession
from pyspark.sql import SparkSession, functions as F, Window

spark = (
    SparkSession.builder
    .appName("lab-ventanas")
    .getOrCreate()
)

# 1) Crear DataFrame de ejemplo
data = [
    ("Norte", "A", 1200),
    ("Norte", "B", 800),
    ("Norte", "C", 400),
    ("Sur", "A", 1000),
    ("Sur", "B", 500),
    ("Sur", "C", 500)
]
cols = ["region", "producto", "ventas"]

df = spark.createDataFrame(data, cols)

print("Datos de entrada:")
df.show()

# 2) Tareas:
# - Define una ventana particionada por región.
# - Calcula el total de ventas por región.
# - Calcula el ranking por producto (de mayor a menor venta).
# - Calcula el porcentaje del producto sobre el total de su región.

