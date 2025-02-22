import psycopg2
from constants import DB_CONFIG

def get_location_dict(**kwargs):
    # change to .env var eventully


    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    query = "SELECT id, lat, lon FROM ski_weather.location;"
    cur.execute(query)

    location_dict = {f"{row[1]},{row[2]}": row[0] for row in cur.fetchall()}

    cur.close()
    conn.close()
    kwargs['ti'].xcom_push(key="location_dict", value=location_dict)

    
