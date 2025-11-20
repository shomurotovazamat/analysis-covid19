# Новые случаи заболевания, смерти и выздоровления
# Каково ежедневное количество новых случаев заболевания, смертей и выздоровлений по странам
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

df_full_grouped = df.sort_values(['Country/Region', 'Date'])

df_full_grouped['Daily New Cases'] = df_full_grouped.groupby('Country/Region')['Confirmed'].diff().fillna(0)
df_full_grouped['Daily New Deaths'] = df_full_grouped.groupby('Country/Region')['Deaths'].diff().fillna(0)
df_full_grouped['Daily New Recoveries'] = df_full_grouped.groupby('Country/Region')['Recovered'].diff().fillna(0)

country = 'Kazakhstan'

sample_country = df_full_grouped[df_full_grouped['Country/Region'] == country]

plt.figure(figsize=(14, 8))
sns.lineplot(x='Date', y='Daily New Cases', data=sample_country, label='Ежедневно несколько случаев')
sns.lineplot(x='Date', y='Daily New Deaths', data=sample_country, label='Ежедневные новые смерти', color='red')
sns.lineplot(x='Date', y='Daily New Recoveries', data=sample_country, label='Ежедневные новые выздоровления',
             color='green')
plt.title('Ежедневные данные о новых случаях заболевания, смертях и выздоровлениях в Kazakhstan')
plt.xlabel('Дата')
plt.ylabel('Ежедневные подсчеты')
plt.legend()
plt.xticks(rotation=45)
plt.show()
