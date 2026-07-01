# 1) imports y SparkSession (recordatorio mínimo)
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

spark = SparkSession.builder.appName("leccion_1_3").getOrCreate()

# 2) lectura rápida con inferSchema (útil en desarrollo)

# si el CSV usa otro separador, cambiar sep
df = spark.read.csv("1.3.sales.csv", header=True, inferSchema=True, sep=",")
df.printSchema()
df.show(5, truncate=False)

# 3) schema explícito (recomendado en producción)
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("date", StringType(), True),
    StructField("product", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("quantity", IntegerType(), True)
])

df_fixed = spark.read.csv("1.3.sales.csv", header=True, schema=schema, sep=",")
df_fixed.printSchema()

# 4) convertir date (si hace falta)
df_fixed = df_fixed.withColumn("date", F.to_date(F.col("date"), "yyyy-MM-dd"))

# solo seleccionar columnas que necesitamos
df_sel = df_fixed.select("id", "product", "price", "quantity")
df_sel.show(3)

# 5) crear columna total y filtrar ventas > 100
df_tot = df_fixed.withColumn("total", F.col("price") * F.col("quantity"))
df_filtered = df_tot.filter(F.col("total") > 100)

# 6) mostrar resultado final (proyección)
df_filtered.select("id", "date", "product", "total").show(10)
