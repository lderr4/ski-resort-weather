import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
from weather_etl.constants import DB_CONFIG


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
    ) VALUES %s
        ON CONFLICT (dt, location_id) 
        DO UPDATE SET 
            temp = EXCLUDED.temp,
            feels_like = EXCLUDED.feels_like,
            pressure = EXCLUDED.pressure,
            humidity = EXCLUDED.humidity,
            dew_point = EXCLUDED.dew_point,
            clouds = EXCLUDED.clouds,
            uvi = EXCLUDED.uvi,
            wind_speed = EXCLUDED.wind_speed,
            wind_gust = EXCLUDED.wind_gust,
            pop = EXCLUDED.pop,
            rain_1h = EXCLUDED.rain_1h,
            snow_1h = EXCLUDED.snow_1h,
            main = EXCLUDED.main,
            description = EXCLUDED.description,
            current_weather_id = EXCLUDED.current_weather_id;
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
    df["dt"] = df["dt"].apply(lambda x: datetime.fromtimestamp(x).date())


    '''
    (['date', 'summary', 'pressure', 'humidity', 'dew_point', 'wind_speed',
       'wind_gust', 'clouds', 'pop', 'uvi', 'rain', 'snow', 'main',
       'description', 'min_temp', 'max_temp', 'day_temp', 'day_feels_like',
       'location_id', 'current_weather_id'],
      dtype='object')
    '''

    insert_sql = """
    INSERT INTO ski_weather.daily_forecast (
        "date", summary, pressure, humidity, dew_point, wind_speed, wind_gust, clouds, pop, uvi, rain, snow, main, description, min_temp, max_temp, day_temp, day_feels_like, location_id, current_weather_id
    ) VALUES %s
    ON CONFLICT ("date", location_id) 
    DO UPDATE SET 
        summary = EXCLUDED.summary,
        pressure = EXCLUDED.pressure,
        humidity = EXCLUDED.humidity,
        dew_point = EXCLUDED.dew_point,
        wind_speed = EXCLUDED.wind_speed,
        wind_gust = EXCLUDED.wind_gust,
        clouds = EXCLUDED.clouds,
        pop = EXCLUDED.pop,
        uvi = EXCLUDED.uvi,
        rain = EXCLUDED.rain,
        snow = EXCLUDED.snow,
        main = EXCLUDED.main,
        description = EXCLUDED.description,
        min_temp = EXCLUDED.min_temp,
        max_temp = EXCLUDED.max_temp,
        day_temp = EXCLUDED.day_temp,
        day_feels_like = EXCLUDED.day_feels_like,
        current_weather_id = EXCLUDED.current_weather_id;
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
    if not len(transformed_data ):
        print("No Values to insert")
        return
    
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
