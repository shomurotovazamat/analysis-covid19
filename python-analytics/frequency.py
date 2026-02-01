import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
from dotenv import load_dotenv
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

plt.figure(figsize=(12, 8))
sns.histplot(df['Recovered / 100 Cases'], bins=20, kde=True, color='blue')
plt.xlabel("Коэффициент восстановления (%)")
plt.ylabel("Частота")
plt.title("Распределение показателей восстановления по странам")
plt.show()
