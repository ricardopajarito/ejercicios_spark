from pyspark.sql import SparkSession

spark = (SparkSession.builder
         .appName("rdd_vs_dataframe_demo")
         .getOrCreate())

ruta_csv = "2.1-usuarios.csv"

# ---------------------------------------------------------------
# 3. Ejemplo con RDD
# ---------------------------------------------------------------
print("===== EJEMPLO CON RDD =====")

# Leer el CSV como RDD
rdd = spark.sparkContext.textFile(ruta_csv)

# Obtener cabecera
header = rdd.first()

# Quitar cabecera
rdd_no_header = rdd.filter(lambda row: row != header)

# Dividir las columnas por coma
rdd_split = rdd_no_header.map(lambda row: row.split(","))

# Filtrar los usuarios mayores de 30 años
rdd_mayores30 = rdd_split.filter(lambda x: int(x[2]) > 30)

# Contar cuántos son
total_mayores30 = rdd_mayores30.count()

print(f"Usuarios mayores de 30 años (RDD): {total_mayores30}")

# ---------------------------------------------------------------
# 4. Ejemplo con DataFrame
# ---------------------------------------------------------------

# Leer el CSV como DataFrame
df = spark.read.csv(ruta_csv, header=True, inferSchema=True)

# Filtrar los mayores de 30
df_mayores30 = df.filter(df.edad > 30)

# Contar
total_df_mayores30 = df_mayores30.count()

print(f"Usuarios mayores de 30 años (DataFrame): {total_df_mayores30}")

# Mostrar algunos resultados
df_mayores30.show()
