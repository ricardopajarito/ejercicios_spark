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

# 2) Definir la ventana particionada por región
#    Esto indica que los cálculos se harán "dentro" de cada región, sin mezclar Norte y Sur
w_region = Window.partitionBy("region")

# 3) Calcular el total de ventas por región usando sum() como función de ventana
df_total = df.withColumn("total_region", F.sum("ventas").over(w_region))

# 4) Calcular el ranking de productos dentro de cada región según las ventas (descendente)
df_rank = df_total.withColumn("ranking", F.rank().over(w_region.orderBy(F.desc("ventas"))))

# 5) Calcular el porcentaje que representa cada producto dentro del total de su región
df_final = (
    df_rank
    .withColumn(
        "pct_region",
        F.round(F.col("ventas") / F.col("total_region") * 100, 2)
    )
)

print("Resultado final:")
df_final.show()

# 6) (Opcional) Mostrar solo columnas relevantes en el reporte final
df_final.select("region", "producto", "ventas", "total_region", "ranking", "pct_region").show()
