import os
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import current_timestamp, lit

spark = SparkSession.builder \
    .appName("WindowDemo") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.hudi.catalog.HoodieCatalog") \
    .config("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension") \
    .config("spark.jars.packages", "org.apache.hudi:hudi-spark3.5-bundle_2.12:0.15.0") \
    .getOrCreate()

# 1. Crear datos de prueba simulados
data = [
    ("101", "Usuario_A", "Activo", "2026-07-20"),
    ("102", "Usuario_B", "Inactivo", "2026-07-20"),
    ("103", "Usuario_C", "Activo", "2026-07-19")
]
columns = ["id_usuario", "nombre", "estado", "fecha"]

df = spark.createDataFrame(data, schema=columns)

# Añadir una columna de timestamp para el precombine
df_final = df.withColumn("ts_actualizacion", current_timestamp())
df_final.show(truncate=False)
# 2. Definir rutas y nombres
table_name = "tabla_usuarios_hudi"
path_destino = f"file://{os.getcwd()}/datos_hudi" # o ruta local "file:///tmp/hudi_usuarios"

# 3. Mapear las configuraciones de Hudi
hudi_options = {
    'hoodie.table.name': table_name,
    'hoodie.datasource.write.recordkey.field': 'id_usuario',      # Clave Primaria
    'hoodie.datasource.write.partitionpath.field': 'fecha',         # Columna de partición
    'hoodie.datasource.write.precombine.field': 'ts_actualizacion',# Resolución de duplicados
    'hoodie.datasource.write.operation': 'upsert',                  # Operación por defecto
    'hoodie.datasource.write.table.type': 'COPY_ON_WRITE'           # COPY_ON_WRITE o MERGE_ON_READ
}

# 4. Escritura del DataFrame
df_final.write \
    .format("hudi") \
    .options(**hudi_options) \
    .mode("append") \
    .save(path_destino)

print("Escritura en Apache Hudi completada con éxito.")