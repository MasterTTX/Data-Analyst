import pandas as pd
import pandasql as ps

# 8	Скачайте данные в CSV и откройте их в Python

# Загружаем первый датафрейм (Ответы на форму) из Google Sheets
sheet_id = "1jN7Oaozo6f3ih2EGKhcjIW_DRtujwApXPntoQ0lUo1k"
gid = "1312725914"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

df_full = pd.read_csv(csv_url)

# Выбираем диапазон B1:N21
df = df_full.iloc[0:21, 1:14]

print("Ответы на форму:")
print(df)

# Загружаем второй датафрейм city.csv из базы данных World-db
conn_str = "postgresql://netology:NetoSQL2019@84.201.177.166:19001/world-db"

# Загружаем данные из таблицы city в DataFrame
df_city = pd.read_sql("SELECT * FROM city", conn_str)

print("\nДанные по городам из базы World-db:")
print(df_city.head())

# 9	При помощи SQL и Python получите датафрейм с названием города и его населением из таблицы City
query = """
SELECT name, population
FROM df_city
"""
df_city_selected = ps.sqldf(query, locals())
print("\nДатафрейм с названием города и его населением:")
print(df_city_selected.head())

# 10 - 1 При помощи Python соедините данные из выгруженного CSV файла (пункт 8) и таблицы с населением города

# в первом датафрейме df есть столбец Town с названиями городов
# переименовываем столбец name в датафрейме df_city_selected
df_city_renamed = df_city_selected[['name', 'population']].rename(columns={'name': 'Town'})

# Объединяем датафреймы по названию города с left join
df_merged = df.merge(df_city_renamed, on='Town', how='left')

print("\nИтоговый датафрейм: Ответы на форму с population:")
print(df_merged)

# 10 - 2 Сгруппируйте итоговый датафрейм по странам

# Удаляем лишние пробелы из названий столбцов
df_merged.columns = df_merged.columns.str.strip()
# Группируем по странам
grouped = df_merged.groupby("Страна")
print(grouped.size().reset_index(name="Количество записей"))

# 10 - 3 рассчитайте среднюю численность населения в городах, в которых вы отдыхали
avg_population = df_merged['population'].mean()
print(f"\nСредняя численность населения в городах, в которых вы отдыхали: {avg_population:.0f}")