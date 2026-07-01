from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import broadcast

spark = SparkSession.builder.appName("Lección 2.2").getOrCreate()

customers = spark.createDataFrame(
    [(1,"Ana","ES"), (2,"Luis","ES"), (3,"Marta","FR")],
    ["customer_id","name","country"]
)

orders = spark.createDataFrame(
    [(101,1,100.0,"2025-09-01"),
     (102,2, 50.0,"2025-09-02"),
     (103,1, 25.0,"2025-09-03"),
     (104,4, 10.0,"2025-09-04")],
    ["order_id","customer_id","amount","order_date"]
)

# Select y withColumn
orders.select("order_id","amount").show()
orders.select(F.col("order_id"), (F.col("amount")*1.21).alias("amount_vat")).show()
orders.withColumn("amount_vat", F.round(F.col("amount")*1.21,2)).show()

# Filter
orders.filter(F.col("amount") > 30).show()
orders.where("amount > 30 AND order_date >= '2025-09-01'").show()

# Aggregations
orders.groupBy("customer_id").agg(
    F.count("*").alias("n_orders"),
    F.sum("amount").alias("total_amount"),
    F.avg("amount").alias("avg_amount"),
    F.max("amount").alias("max_amount")
).show()

# Joins
orders.join(customers, on="customer_id", how="inner").show()
customers.join(orders, on="customer_id", how="left").show()
orders.join(customers, on="customer_id", how="full").show()

# Broadcast example
orders.join(broadcast(customers), on="customer_id", how="inner").show()
