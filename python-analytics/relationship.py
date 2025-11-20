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

plt.figure(figsize=(8,6))
sns.scatterplot(
    x="Deaths / 100 Cases",
    y="Recovered / 100 Cases",
    data=df,
    hue="WHO Region",
    size="Confirmed",
    sizes=(35, 500),
    alpha=0.7,
    palette="tab10"
)

plt.title("Связь между уровнем смертности и уровнем выздоровления")
plt.xlabel("Число смертей на 100 случаев (%)")
plt.ylabel("Выздоровело на 100 случаев (%)")
plt.grid(True, linestyle="--", alpha=0.5)
# plt.legend(title="WHO Region", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.show()