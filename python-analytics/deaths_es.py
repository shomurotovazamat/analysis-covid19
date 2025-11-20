import psycopg2
import pandas as pd
from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5433/covid")
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