import requests
import os
import time



def get_resort_weather_response_data(**kwargs):
    responses = []

    ti = kwargs['ti']
    location_dict = ti.xcom_pull(task_ids="get_location_dict", key="location_dict")


    for latlon in location_dict:
        
        location_id = location_dict[latlon]
        lat, lon = latlon.split(",")
        lat, lon = float(lat), float(lon)
        
        response = load_data_from_api(lat, lon)
        response['location_id'] = location_id
        responses.append(response)

    
    kwargs['ti'].xcom_push(key="responses", value=responses)
    

def load_data_from_api(lat: float, lon: float):
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url).json()
    return response


