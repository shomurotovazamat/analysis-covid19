import psycopg2
import pandas as pd
from elasticsearch import Elasticsearch
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os


load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
df = pd.read_sql("SELECT * FROM country_wise_latest", engine)

es = Elasticsearch("http://localhost:9200")

resp = es.search(
    index="covid",
    size=10000,
    query={"match_all": {}}
)

top10 = df.sort_values("Deaths", ascending=False).head(10)

plt.bar(top10["Country/Region"], top10["Deaths"])
plt.xticks(rotation=45)
plt.title("10 стран с наибольшим числом подтвержденных смертей")
plt.show()