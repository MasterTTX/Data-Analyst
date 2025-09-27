import os
from datetime import date, datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window

# Кодировка
if os.name == "nt": os.system("chcp 65001 > nul")

os.environ["JAVA_HOME"] = r"C:\Program Files\Eclipse Adoptium\jdk-17.0.16.8-hotspot"
os.environ["PYSPARK_PYTHON"] = r"C:\Python\Python313\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Python\Python313\python.exe"

spark = SparkSession.builder.appName("COVID Analysis").getOrCreate()

csv_file = r"C:\Python\pyspark\covid-data.csv"

df = spark.read.option("header", "true").option("inferSchema", "true").csv(csv_file)
print("Количество строк:", df.count())

df = df.withColumn("date", F.to_date("date", "yyyy-MM-dd"))

min_max = df.select(
    F.min("date").alias("min_date"),
    F.max("date").alias("max_date")
).collect()[0]

print("Первая дата:", min_max["min_date"])
print("Последняя дата:", min_max["max_date"])

# # # # Выберите 15 стран с наибольшим процентом переболевших на 31 марта (в выходящем датасете необходимы колонки: iso_code, страна, процент переболевших)
cutoff_date = date(2021, 3, 31)
cutoff_str = cutoff_date.strftime("%Y-%m-%d")

print(f"\nЗаписи до {cutoff_str}.")

df_cut = df.filter(F.col("date") <= F.to_date(F.lit(cutoff_str), "yyyy-MM-dd"))

df_max = df_cut.groupBy("iso_code", "location").agg(
    F.max(F.coalesce(F.col("total_cases"), F.lit(0))).alias("max_cases"),
    F.max(F.col("population")).alias("population")
)

df_max = df_max.filter((F.col("population").isNotNull()) & (F.col("population") > 0))

df_max = df_max.withColumn(
    "percent_infected",
    (F.col("max_cases").cast("double") / F.col("population").cast("double")) * 100.0
)

top15 = df_max.select(
    "iso_code",
    F.col("location").alias("страна"),
    F.round("percent_infected", 6).alias("процент_переболевших")
).orderBy(F.desc("процент_переболевших")).limit(15)

print(f"\nTop 15 стран по проценту переболевших (до {cutoff_date}):")
top15.show(truncate=False)

# # # # Top 10 стран с максимальным зафиксированным кол-вом новых случаев за последнюю неделю марта 2021 в отсортированном порядке по убыванию
last_week_start = datetime(2021, 3, 25)
last_week_end = datetime(2021, 3, 31)

df_last_week = df.filter(
    (F.col("date") >= F.lit(last_week_start.strftime("%Y-%m-%d"))) &
    (F.col("date") <= F.lit(last_week_end.strftime("%Y-%m-%d")))
)

df_top10_new_cases = df_last_week.groupBy("location").agg(
    F.max(F.coalesce(F.col("new_cases"), F.lit(0))).alias("max_new_cases")
)

window_rank = Window.orderBy(F.desc("max_new_cases"))
top10_new_cases = df_top10_new_cases.select(
    F.row_number().over(window_rank).alias("номер"),
    F.col("location").alias("страна"),
    "max_new_cases"
).orderBy(F.desc("max_new_cases")).limit(10)

print("\nTop 10 стран по максимальному числу новых случаев (25–31 марта 2021):")
top10_new_cases.show(truncate=False)

# # # # Посчитайте изменение случаев относительно предыдущего дня в России за последнюю неделю марта 2021.
df_russia = df.filter(
    (F.col("location") == "Russia") &
    (F.col("date") >= F.lit("2021-03-25")) &
    (F.col("date") <= F.lit("2021-03-31"))
).select("date", "new_cases")

window_russia = Window.orderBy("date")
df_russia = df_russia.withColumn("yesterday_cases", F.lag("new_cases").over(window_russia))
df_russia = df_russia.withColumn("delta", F.col("new_cases") - F.col("yesterday_cases"))

df_russia_result = df_russia.select(
    F.col("date").alias("число"),
    F.col("yesterday_cases").alias("новых_случаев_вчера"),
    F.col("new_cases").alias("новых_случаев_сегодня"),
    F.col("delta").alias("дельта")
).orderBy("число")

print("\nИзменение случаев в России за (25–31 марта 2021):")
df_russia_result.show(truncate=False)

spark.stop()
