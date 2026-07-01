from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("temp-views-demo").getOrCreate()

# 1) crear DataFrame de ejemplo
data = [
    (1, "Alice", "sales", 1000),
    (2, "Bob", "sales", 1500),
    (3, "Carmen", "eng", 2000),
    (4, "Diego", "eng", 1800),
]
cols = ["id","name","dept","salary"]
df = spark.createDataFrame(data, cols)
df.show()

# 2) crear vista temporal local
df.createOrReplaceTempView("empleados")

# 3) ejecutar consulta SQL
res = spark.sql("""
  SELECT dept, AVG(salary) as avg_sal, COUNT(*) as cnt
  FROM empleados
  GROUP BY dept
  ORDER BY avg_sal DESC
""")
res.show()

# 4) comprobar tablas/vistas en catálogo
print(spark.catalog.listTables())

# 5) cachear la vista si conviene
spark.catalog.cacheTable("empleados")
print("is cached:", spark.catalog.isCached("empleados"))

# 6) explicar plan de una consulta
spark.sql("SELECT * FROM empleados WHERE salary > 1200").explain(True)

# 7) crear global temp view
df.createGlobalTempView("empleados_global")
spark.sql("SELECT * FROM global_temp.empleados_global").show()

# 8) limpiar
spark.catalog.dropTempView("empleados")
# si usas global_temp, puedes DROP VIEW con nombre cualificado
spark.sql("DROP VIEW IF EXISTS global_temp.empleados_global")
