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

plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=df, x='Confirmed', y='Deaths',
    hue='WHO Region', alpha=0.9, palette='Set2', s=80, edgecolor='black'
)
plt.xscale('log')
plt.yscale('log')
plt.title("Соотношение между подтвержденными случаями и смертями (логарифмическая шкала)", fontsize=14)
plt.xlabel("Подтвержденные случаи (журнал)")
plt.ylabel("Смерти (журнал)")
plt.legend(title="Регион", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()