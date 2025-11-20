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

plt.figure(figsize=(12, 8))
sns.boxplot(x=df['WHO Region'], y=df['Deaths / 100 Cases'], palette='coolwarm')
plt.xlabel("WHO Region")
plt.ylabel("Уровень смертности (%)")
plt.title("Уровень смертности в регионах")
plt.xticks(rotation=45)
plt.show()