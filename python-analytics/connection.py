import psycopg2

try:
    conn = psycopg2.connect(
        dbname="covid",
        user="postgres",
        password="1234",
        host="localhost",
        port="5433"
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
