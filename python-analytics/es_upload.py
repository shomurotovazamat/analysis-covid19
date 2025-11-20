import pandas as pd
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import BulkIndexError
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
from tqdm import tqdm
import os

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
es = Elasticsearch("http://localhost:9200", request_timeout=300)

TABLES = [
    "country_wise_latest",
    "covid_complete",
    "day_wise",
    "full_grouped",
    "usa_country",
    "worldometr_data"
]

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(",", "").str.strip()
            df[col] = df[col].replace(["inf", "-inf", "nan", ""], None)
        if col.lower() in {"confirmed", "deaths", "recovered", "active", "new_cases", "new_deaths", "new_recovered"}:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        elif col.lower() in {"deaths_per_100_cases", "recovered_per_100_cases", "deaths_per_100_recovered", "week_increase"}:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df = df.replace([pd.NA, pd.NaT, np.nan, float('inf'), float('-inf')], None)
    return df

def create_index(index_name: str, df: pd.DataFrame):
    props = {}
    for col in df.columns:
        if col.lower() in {"confirmed", "deaths", "recovered", "active", "new_cases", "new_deaths", "new_recovered"}:
            props[col] = {"type": "long"}
        elif col.lower() in {"deaths_per_100_cases", "recovered_per_100_cases", "deaths_per_100_recovered", "week_increase"}:
            props[col] = {"type": "float"}
        else:
            props[col] = {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    es.indices.create(index=index_name, body={"mappings": {"properties": props}})
    print(f"{index_name} картографирование создано")

def bulk_with_logging(es, actions, chunk_size=5_000):
    success, failed = 0, 0
    actions = list(actions)
    total = len(actions)
    pbar = tqdm(total=total, desc="Отправка")

    for i in range(0, total, chunk_size):
        chunk = actions[i:i + chunk_size]
        try:
            for ok, result in helpers.parallel_bulk(es, chunk, thread_count=4, chunk_size=1_000):
                if ok:
                    success += 1
                else:
                    failed += 1
            pbar.update(len(chunk))
        except BulkIndexError as e:
            failed += len(e.errors)
            for err in e.errors:
                print("ошибка", err)
    pbar.close()
    print(f"{success:} документ загружен, {failed:} ошибка")

def load_table_to_es(table_name: str):
    index_name = table_name.lower()
    print(f"{table_name} загрузка таблицы...")
    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
    df = clean_dataframe(df)
    print(f"{len(df):,} ряды")
    create_index(index_name, df)
    actions = [{"_index": index_name, "_source": row.dropna().to_dict()} for _, row in df.iterrows()]
    bulk_with_logging(es, actions)
    print(f"{table_name} законченный")

if __name__ == "__main__":
    for tbl in TABLES:
        load_table_to_es(tbl)