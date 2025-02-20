from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from weather_etl.load_weather import get_resort_weather_response_data
from weather_etl.export_weather import export_current_weather, export_hourly_forecast, export_daily_forecast, export_alerts
from weather_etl.transform_weather import transform_current_weather, transform_alerts, transform_daily_forecast, transform_hourly_forecast
from utils import get_location_dict

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2025, 2, 3, 5, 26)
}

with DAG(
    'weather_data_ETL',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False
) as dag:
    load_location_map = PythonOperator(
        task_id="get_location_dict",
        python_callable=get_location_dict
    )

    load_weather_data = PythonOperator(
        task_id="load_weather",
        python_callable=get_resort_weather_response_data
    )
    transform_current_data = PythonOperator(
        task_id="transform_current_weather",
        python_callable=transform_current_weather
    )
    export_current_data = PythonOperator(
        task_id="export_current_weather",
        python_callable=export_current_weather
    )

    transform_alerts_data = PythonOperator(
        task_id = "transform_alerts",
        python_callable=transform_alerts
    )
    transform_hourly_data = PythonOperator(
        task_id = "transform_hourly",
        python_callable=transform_hourly_forecast
    )
    transform_daily_data = PythonOperator(
        task_id = "transform_daily",
        python_callable=transform_daily_forecast
    )
    export_hourly_data = PythonOperator(
        task_id = "export_hourly_forecast",
        python_callable=export_hourly_forecast
    )
    export_daily_data = PythonOperator(
        task_id="export_daily_forecast",
        python_callable=export_daily_forecast
    )
    export_weather_alerts = PythonOperator(
        task_id="export_weather_alerts",
        python_callable=export_alerts
    )
    load_location_map >> load_weather_data >> transform_current_data >> export_current_data >> [transform_daily_data, transform_alerts_data, transform_hourly_data] >> export_hourly_data >> export_daily_data >> export_weather_alerts
