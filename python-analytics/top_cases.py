# Ваш код подключается к базе данных, загружает таблицу с данными о COVID-19, выбирает 10 стран
# с наибольшим числом подтверждённых случаев и строит для них столбчатый график. В результате
# вы получаете быстрый визуальный обзор того, какие страны сильнее всего пострадали.
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
query = "SELECT * FROM country_wise_latest"
df = pd.read_sql(query, engine)

top_newcases = df[['Country/Region', 'New cases']].sort_values(by='New cases', ascending=False).head(10)
top_newcases

plt.figure(figsize=(12, 8))
sns.barplot(data=top_newcases, x='New cases', y='Country/Region', palette="coolwarm")
plt.ylabel("Страна")
plt.xlabel("Рекордное число случаев заболевания COVID-19 по странам")
plt.show()
