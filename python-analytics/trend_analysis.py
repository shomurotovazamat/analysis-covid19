# Построены глобальные и страновые тренды с использованием 7-дневных скользящих средних для более плавной визуализации.
# Использованы подграфики для отображения отдельных трендов по подтверждённым случаям, смертям и выздоровлениям с течением времени.
import numpy as np
import pandas as pd
import warnings
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sqlalchemy import create_engine
import os

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

warnings.filterwarnings('ignore')
db_connection_str = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_connection_str)

query = "SELECT * FROM full_grouped"
df = pd.read_sql(query, engine)

# Функция построения трендов
def plot_trend_analysis(df, country=None):
    # Set the style for seaborn
    sns.set(style="whitegrid")

    # Преобразуйте «Date» в datetime, если это еще не сделано
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Сводные данные, если конкретная страна не указана
    if country:
        df = df[df['Country/Region'] == country]
    else:
        df = df.groupby('Date').agg({
            'Confirmed': 'sum',
            'Deaths': 'sum',
            'Recovered': 'sum'
        }).reset_index()
    # Рассчитать скользящие средние
    df['Confirmed_MA'] = df['Confirmed'].rolling(window=7).mean()
    df['Deaths_MA'] = df['Deaths'].rolling(window=7).mean()
    df['Recovered_MA'] = df['Recovered'].rolling(window=7).mean()

    # Построение сюжета
    plt.figure(figsize=(14, 7))

    # Тенденция подтвержденных случаев
    plt.subplot(3, 1, 1)
    sns.lineplot(data=df, x='Date', y='Confirmed_MA', color='blue', label='Подтвержденные случаи')
    plt.title(f'Тенденция подтвержденных случаев с течением времени' if not country else f'Тенденция подтвержденных случаев в {country}')
    plt.xlabel('Дата')
    plt.ylabel('Количество случаев')
    plt.legend()
    # Тенденция смертности
    plt.subplot(3, 1, 2)
    sns.lineplot(data=df, x='Date', y='Deaths_MA', color='red', label='Смерти')
    plt.title(f'Тенденция смертности с течением времени' if not country else f'Тенденция смертности в {country}')
    plt.xlabel('Дата')
    plt.ylabel('Количество смертей')
    plt.legend()
    # Тенденция к восстановлению
    plt.subplot(3, 1, 3)
    sns.lineplot(data=df, x='Date', y='Recovered_MA', color='green', label='выздоровления')
    plt.title(f'Тенденция выздоровления с течением времени' if not country else f'Тенденция к выздоровлению {country}')
    plt.xlabel('Дата')
    plt.ylabel('Количество выздоровлений')
    plt.legend()

    plt.tight_layout()
    plt.show()

plot_trend_analysis(df)