# 1. Импорт необходимых библиотек
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Загрузка данных
url = "https://u.netology.ru/backend/uploads/lms/attachments/files/data/51789/FPS_hw_1_df_1_bank_customer.xlsx?_gl=1*1859vvr*_gcl_au*MjQ1NTkwMDcwLjE3NDc0Njc3NjY."

# Чтение Excel-файла
df = pd.read_excel(url)

# Просмотр первых строк
df.head()

# 3. Расчёт статистик по возрасту
age = df['Age']

print("Статистики по возрасту клиентов банка:\n")
print(f"Среднее арифметическое: {age.mean():.2f}")
print(f"Стандартное отклонение: {age.std():.2f}")
print(f"Минимум: {age.min()}")
print(f"25-й персентиль: {age.quantile(0.25)}")
print(f"50-й персентиль (медиана): {age.median()}")
print(f"75-й персентиль: {age.quantile(0.75)}")
print(f"Максимум: {age.max()}")

# 4. Построение гистограммы плотности распределения возраста
plt.figure(figsize=(10, 6))
sns.histplot(age, kde=True, bins=30, color='skyblue')
plt.title('Распределение возраста клиентов банка')
plt.xlabel('Возраст')
plt.ylabel('Плотность')
plt.grid(True)
plt.show()

# Выводы:
# Средний возраст клиентов составляет 39.35 лет, а медиана — 39.27 лет - распределение достаточно симметрично
# Распределение нормальное - но с лёгкой асимметрией в сторону старших возрастов. Большинство клиентов — в возрасте от 30 до 45 лет.
# Нет резких скачков или провалов - что говорит о достаточной репрезентативности выборки по возрасту.