from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F

spark = SparkSession.builder \
    .appName("WindowDemo") \
    .getOrCreate()

data = [
    (1, "sales", "Alice", 70000, "2024-05-01"),
    (2, "sales", "Bob",   80000, "2024-06-01"),
    (3, "eng",   "Carol", 95000, "2024-05-21"),
    (4, "eng",   "Dave",  95000, "2024-06-01"),
    (5, "sales", "Eve",   80000, "2024-04-15"),
    (6, "eng",   "Frank", 87000, "2024-06-02")
]
cols = ["id","department","name","salary","hired_date"]
df = spark.createDataFrame(data, cols)

# Top 3 por department
w = Window.partitionBy("department").orderBy(F.desc("salary"), F.desc("hired_date"))
df_with_rn = df.withColumn("rn", F.row_number().over(w))
top3 = df_with_rn.filter(F.col("rn") <= 3).orderBy("department","rn")
top3.show(truncate=False)

# Comparación rank vs dense_rank
df_rank = df.withColumn("rank", F.rank().over(w)) \
            .withColumn("dense_rank", F.dense_rank().over(w)) \
            .orderBy("department", F.desc("salary"), "name")
df_rank.show(truncate=False)

# Dedupe: quedarnos con la última fila por ID (ejemplo)
events = [
    (1, "u1", "2024-06-01 10:00", "A"),
    (2, "u1", "2024-06-02 11:00", "B"),
    (3, "u2", "2024-05-30 09:00", "C")
]
events_cols = ["evt_id","user_id","event_time","payload"]
events_df = spark.createDataFrame(events, events_cols) \
                 .withColumn("event_time", F.to_timestamp("event_time"))
w2 = Window.partitionBy("user_id").orderBy(F.desc("event_time"))
df_latest = events_df.withColumn("rn", F.row_number().over(w2)) \
                     .filter(F.col("rn") == 1) \
                     .drop("rn")
df_latest.show(truncate=False)
