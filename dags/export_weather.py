import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values


def export_current_weather(**kwargs):

    transformed_data = kwargs['ti'].xcom_pull(task_ids="transform_current_weather", key="current_weather_list")
    
    DB_CONFIG = {
        "dbname": "admin",
        "user": "admin",
        "password": "admin",
        "host": "postgres-dev",
        "port": "5432",  # Default is 5432
    }

    df = pd.DataFrame(transformed_data)
    df["dt"] = df["dt"].apply(lambda x: datetime.fromtimestamp(x))
    location_ids = df['location_id'].tolist()
    print(df.columns)

    insert_sql = """
    INSERT INTO ski_weather.current_weather (
        dt, temp, feels_like, pressure, humidity, dew_point, clouds, uvi, wind_speed, wind_gust, rain_1h, snow_1h, main, description, location_id
    ) VALUES %s
    RETURNING id;
    """

    records = list(df.itertuples(index=False, name=None))

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        execute_values(cursor, insert_sql, records)

        returned_id = [row[0] for row in cursor.fetchall()]

        foreign_key_map = {l_id: r_id for l_id, r_id in zip(location_ids, returned_id)}
        
        kwargs['ti'].xcom_push(key="foreign_key_map", value=foreign_key_map)

        conn.commit()
        print("Data inserted successfully!")

    except Exception as e:
        print("Error inserting data:", e)

    finally:
        cursor.close()
        conn.close()

def export_hourly_forecast(**kwargs):
    transformed_data = kwargs['ti'].xcom_pull(task_ids="transform_hourly", key="hourly_forecast_list")
    
    DB_CONFIG = {
        "dbname": "admin",
        "user": "admin",
        "password": "admin",
        "host": "postgres-dev",
        "port": "5432",  # Default is 5432
    }

    df = pd.DataFrame(transformed_data)
    df["dt"] = df["dt"].apply(lambda x: datetime.fromtimestamp(x))

    print(df.columns)


    insert_sql = """
    INSERT INTO ski_weather.hourly_forecast (
        dt, temp, feels_like, pressure, humidity, dew_point, clouds, uvi, wind_speed, wind_gust, pop, rain_1h, snow_1h, main, description, location_id, current_weather_id
    ) VALUES %s;
    """

    records = list(df.itertuples(index=False, name=None))

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        execute_values(cursor, insert_sql, records)

        conn.commit()
        print("Data inserted successfully!")

    except Exception as e:
        print("Error inserting data:", e)

    finally:
        cursor.close()
        conn.close()



def export_daily_forecast(**kwargs):
    transformed_data = kwargs['ti'].xcom_pull(task_ids="transform_daily", key="daily_forecast_list")
    
    DB_CONFIG = {
        "dbname": "admin",
        "user": "admin",
        "password": "admin",
        "host": "postgres-dev",
        "port": "5432",  # Default is 5432
    }

    df = pd.DataFrame(transformed_data)
    df["dt"] = df["dt"].apply(lambda x: datetime.fromtimestamp(x))

    print(df.columns)

    '''

    (['dt', 'summary', 'pressure', 'humidity', 'dew_point', 'wind_speed',
       'wind_gust', 'clouds', 'pop', 'uvi', 'rain', 'snow', 'main',
       'description', 'min_temp', 'max_temp', 'day_temp', 'day_feels_like',
       'location_id', 'current_weather_id'],
      dtype='object')
    '''

    insert_sql = """
    INSERT INTO ski_weather.daily_forecast (
        dt, summary, pressure, humidity, dew_point, wind_speed, wind_gust, clouds, pop, uvi, rain, snow, main, description, min_temp, max_temp, day_temp, day_feels_like, location_id, current_weather_id
    ) VALUES %s;
    """

    records = list(df.itertuples(index=False, name=None))

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        execute_values(cursor, insert_sql, records)

        conn.commit()
        print("Data inserted successfully!")

    except Exception as e:
        print("Error inserting data:", e)

    finally:
        cursor.close()
        conn.close()


def export_alerts(**kwargs):
    transformed_data = kwargs['ti'].xcom_pull(task_ids="transform_alerts", key="alerts_list")
    
    DB_CONFIG = {
        "dbname": "admin",
        "user": "admin",
        "password": "admin",
        "host": "postgres-dev",
        "port": "5432",  # Default is 5432
    }

    df = pd.DataFrame(transformed_data)
    df["start"] = df["start"].apply(lambda x: datetime.fromtimestamp(x))
    df["end"] = df["end"].apply(lambda x: datetime.fromtimestamp(x))

    print(df.columns)


    insert_sql = """
    INSERT INTO ski_weather.weather_alerts ( 
        sender_name,
        location_id,
        event,
        start,
        "end",
        description
    ) VALUES %s
    ON CONFLICT(sender_name, event, start, "end") DO NOTHING;
    """

    records = list(df.itertuples(index=False, name=None))

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        execute_values(cursor, insert_sql, records)

        conn.commit()
        print("Data inserted successfully!")

    except Exception as e:
        print("Error inserting data:", e)

    finally:
        cursor.close()
        conn.close()



    
    
    
    

