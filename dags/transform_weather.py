from constants import alerts_cols, daily_forecast_cols, current_weather_cols, hourly_forecast_cols
import pandas as pd
from typing import Dict, List

def transform_current_weather(**kwargs):

    responses = kwargs['ti'].xcom_pull(task_ids="load_weather", key="responses")
    transformed_current_weather = []

    for response in responses:
        current_weather = get_current_weather(response)
        transformed_current_weather.append(current_weather)

    
    
    kwargs['ti'].xcom_push(key="current_weather_list", value=transformed_current_weather)


def transform_hourly_forecast(**kwargs):
    responses = kwargs['ti'].xcom_pull(task_ids="load_weather", key="responses")
    foreign_key_map = kwargs['ti'].xcom_pull(task_ids="export_current_weather", key="foreign_key_map")
    print(foreign_key_map)
    hourly_forecast = []
    
    for response in responses:
        hf = get_hourly_forecast(response, foreign_key_map)
        hourly_forecast.extend(hf)
    
    kwargs['ti'].xcom_push(key="hourly_forecast_list", value=hourly_forecast)




def transform_daily_forecast(**kwargs):

    responses = kwargs['ti'].xcom_pull(task_ids="load_weather", key="responses")
    foreign_key_map = kwargs['ti'].xcom_pull(task_ids="export_current_weather", key="foreign_key_map")


    daily_forecast = []
    
    for response in responses:
        df = get_daily_forecast(response, foreign_key_map)
        daily_forecast.extend(df)
    
    kwargs['ti'].xcom_push(key="daily_forecast_list", value=daily_forecast)



def transform_alerts(**kwargs):
    responses = kwargs['ti'].xcom_pull(task_ids="load_weather", key="responses")
    alerts = []
    
    for response in responses:
        alert = get_alerts(response)
        alerts.extend(alert)

    kwargs['ti'].xcom_push(key="alerts_list", value=alerts)





def get_current_weather(response: Dict) -> Dict: 
    current = response["current"]

    current_weather_raw = {
        key: current_weather_cols[key](current.get(key, None) or 0) for key in current_weather_cols
    }
    current_weather_raw["rain_1h"] = float(current.get("rain", {}).get("1h", 0))
    current_weather_raw['snow_1h'] = float(current.get("snow", {}).get("1h", 0))
    current_weather_raw['main'] = str(current.get("weather", [{}])[0].get("main", ""))
    current_weather_raw['description'] = str(current.get("weather", [{}])[0].get("description", ""))
    current_weather_raw['location_id'] = int(response['location_id'])
    return current_weather_raw

def get_hourly_forecast(response: Dict, foreign_key_map: Dict) -> List[Dict[str, any]]:
    
    hourly = response["hourly"]

    hourly_forecast_raw = []
    location_id = int(response['location_id'])
    current_weather_id = foreign_key_map[str(location_id)]


    for forecast in hourly:
        data = {}
        data = {key: hourly_forecast_cols[key](forecast.get(key, None) or 0) for key in hourly_forecast_cols}

        data["rain_1h"] = float(forecast.get("rain", {}).get("1h", 0))
        data['snow_1h'] = float(forecast.get("snow", {}).get("1h", 0))
        data['main'] = str(forecast.get("weather", [{}])[0].get("main", ""))
        data['description'] = str(forecast.get("weather", [{}])[0].get("description", ""))
        data['location_id'] = location_id
        data['current_weather_id'] = current_weather_id
        hourly_forecast_raw.append(data)
    return hourly_forecast_raw

def get_daily_forecast(response: Dict, foreign_key_map: Dict) -> List[Dict[str, any]]:

    daily = response["daily"]
    location_id = response['location_id']

    current_weather_id = foreign_key_map[str(location_id)]

    daily_forecast_raw = []


    for forecast in daily:
        data = {}
        data = {key: daily_forecast_cols[key](forecast.get(key, None) or 0) for key in daily_forecast_cols}


        data['main'] = str(forecast.get("weather", [{}])[0].get("main", ""))
        data['description'] = str(forecast.get("weather", [{}])[0].get("description", ""))

        data["min_temp"] = float(forecast.get("temp", [{}]).get("min", 0))
        data["max_temp"] = float(forecast.get("temp", [{}]).get("max", 0))
        data["day_temp"] = float(forecast.get("temp", [{}]).get("day", 0))
        data["day_feels_like"] = float(forecast.get("feels_like", [{}]).get("day", 0))
        data['location_id'] = location_id
        data['current_weather_id'] = current_weather_id

        daily_forecast_raw.append(data)

    return daily_forecast_raw

def get_alerts(response: Dict) -> List[Dict[str, any]]:

    if 'alerts' not in response:
        return []
    
    alerts = response['alerts']
    location_id = response['location_id']

    alerts_raw = []
    for alert in alerts:
        data = {}
        data = {key: alerts_cols[key](alert.get(key, 0)) for key in alerts_cols}
        data['location_id'] = location_id
        alerts_raw.append(data)
    return alerts_raw