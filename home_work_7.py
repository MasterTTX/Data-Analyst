import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Загрузка данных из файла 'insurance.csv'
file_id = '1qNFH5zT7cgBw8f4yHTQMPsTelPE5XaCJ'
download_url = f'https://drive.google.com/uc?id={file_id}'

df = pd.read_csv(download_url)

# Просмотр первых строк таблицы
print ("\nПросмотр первых строк таблицы:")
print(df.head())
print ("* "*40)
df.info()
print ("* "*40)
print(df.describe())
print ("* "*40)

# Заменяем пол и курение на числа
df['sex']=df['sex'].map({'male':1, 'female':0})
df['smoker']=df['smoker'].map({'yes':1,'no':0})
print ("\nПросмотр первых строк таблицы:")
print(df.head())
print ("* "*40)
df = pd.get_dummies(df, columns=['region'])

# Показывать все столбцы
pd.set_option('display.max_columns', None)
print ("\nПросмотр первых строк таблицы:")
print(df.head())

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Формируем признаки и целевую переменную
X = df.drop('charges', axis=1)  # признаки
y = df['charges']               # целевая переменная

# Разбиваем данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# random_state=42 - фиксируем "зерно случайности"
# Создаем модель линейной регрессии
model = LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None)
# copy_X=True — исходные данные не изменяются, создаётся их копия
# fit_intercept=True - Добавлять свободный член βо -  (intercept) У = βо + β1X1 + β2х2 + ... + βnxn
# n_jobs=None - Сколько потоков (CPU) использовать для обучения. использовать один поток

# обучаем модель линейной регрессии
model.fit(X_train, y_train)

# Предсказываем значения на тестовой выборке
y_pred = model.predict(X_test)

print ("* "*40)
# Вычисляем среднеквадратичную ошибку
mse = mean_squared_error(y_test, y_pred)
print(f"Среднеквадратичная ошибка (MSE): {mse:.2f}")
rmse = np.sqrt(mse)  # вычисляем корень из MSE
print(f"Средняя ошибка в долларах (RMSE): {rmse:.2f} $")

# Выводим коэффициенты модели
print("\nКоэффициенты модели:")
for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature}: {coef:.4f}")

print(f"Свободный член (βо): {model.intercept_:.4f}")

# Данные по конкретному человеку
data = [{
    "age": 20,
    "sex": 1,
    "bmi": 30,
    "children": 2,
    "smoker": 1,
    "region_northeast": 0,
    "region_northwest": 0,
    "region_southeast": 1,
    "region_southwest": 0
}]

# Преобразуем в DataFrame
person_df = pd.DataFrame(data)

# Делаем предсказание
predicted_charge = model.predict(person_df)

print(f"Предсказанная стоимость страховки для данного человека: ${predicted_charge[0]:.2f}")