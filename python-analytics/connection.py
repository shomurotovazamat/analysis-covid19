import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

try:
    conn = psycopg2.connect(
        dbname={DB_NAME},
        user={DB_USER},
        password={DB_PASS},
        host={DB_HOST},
        port={DB_PORT}
    )

    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("PostgreSQL версия:", version)

    cur.execute("SELECT * FROM worldometr_data LIMIT 1")
    rows = cur.fetchall()
    for row in rows:
        print(row)

except Exception as e:
    print("Ошибка:", e)

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
