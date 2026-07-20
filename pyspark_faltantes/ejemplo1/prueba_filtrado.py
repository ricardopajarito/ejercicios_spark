import os
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F
from pyspark.sql.functions import col, trim, regexp_replace, when, to_date, date_format

spark = SparkSession.builder \
    .appName("WindowDemo") \
    .getOrCreate()

load_date_start = os.getenv("LOAD_DATE_START", "2025-01-01")
load_date_end = os.getenv("LOAD_DATE_END", "2025-01-30")

data_nsccap = [
    # ("31/07/2025 00:00:00", "02/01/2025", "FG23962", 9394.00),
    ("31/07/2026", "02/01/2027", "FG23962", 9394.00),
    ("10/10/2025", "02/01/2025", "FG23963",   1020.99),
    ("10/10/2025", "02/01/2025",  "FG23964", 236.42),
    ("10/10/2025", "02/01/2025",  "FG23964",  236.42),
    ("10/10/2025", "02/01/2025",  "FG23964",  236.42),
    ("10/10/2025", "02/01/2025", "FS186821",   239.84),
    ("10/10/2025", "02/01/2025",  "FS186822", 198.27),
    ("10/10/2025", "02/01/2025",  "FS186825", 156.49),
    # ("2025-09-01", "03/01/2025",  "FS186825",  156.49),
    # ("2026-09-01 21:02", "03/01/2026",  "FS186825",  156.49),
    # ("08/08/2025", "03/01/2026",  "FS186825",  156.49),
]

cols_nsccap = ["FechaExtraccion", "FechaFactura", "Factura", "Venta"]

df_nsccap = spark.createDataFrame(data_nsccap, cols_nsccap)

df_nsccap = df_nsccap.withColumn(
    "FechaFactura_uniforme",
    F.coalesce(
        F.date_format(F.expr("try_to_timestamp(FechaFactura, 'dd/MM/yyyy HH:mm:ss')"), "yyyy-MM-dd"),
        F.date_format(F.expr("try_to_timestamp(FechaFactura, 'dd/MM/yyyy')"), "yyyy-MM-dd"),
        F.date_format(F.expr("try_to_timestamp(FechaFactura, 'yyyy-MM-dd HH:mm')"), "yyyy-MM-dd"),
        F.date_format(F.expr("try_to_timestamp(FechaFactura, 'yyyy-MM-dd')"), "yyyy-MM-dd")
    )
)

df_nsccap.show(truncate=False)

df_nsccap = df_nsccap.where(col("FechaFactura_uniforme").between(load_date_start, load_date_end))

print("Datos de NSCCAP filtrados")
df_nsccap.show(truncate=False)


