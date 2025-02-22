import os
resorts = [
    ("Ikon", "Winter Park", (39.87652886804281, -105.76577005628859)),
    ("Ikon", "Copper Mountain", (39.49367530426312, -106.15941614917506)),
    ("Ikon", "Eldora", (39.93747528686545, -105.58400897925249)),
    ("Ikon", "Steamboat Springs", (40.466202977197106, -106.78094073252413)),
    ("Ikon", "Palisades Tahoe", (39.19114916529031, -120.2557470349228)),
    ("Ikon", "Big Sky", (45.293131560098956, -111.36294562989895)),
    ("Epic", "Northstar", (39.25671866393303, -120.13341133625593)),
    ("Ikon", "Crystal", (46.934754314303206, -121.48384975195034)),
    ("Ikon", "Jackson", (43.594634283058724, -110.84610943388475)),
    ("Epic", "Breckenridge", (39.478861079038985, -106.07839392176015)),
    ("Epic", "Vail", (39.619779887440146, -106.36957399501661)),
    ("Ikon", "Stratton", (43.110007073773104, -72.91026718465827)),
    ("Epic", "Whistler", (50.073500220248334, -122.95937601933981)),
    ("Ikon", "Charmonix", (45.96980068114292, 6.879032518531963))
]

DB_CONFIG = {
    "dbname": os.environ.get('DB_NAME'),
    "user": os.environ.get('DB_USER'),
    "password": os.environ.get('DB_PASSWORD'),
    "host": os.environ.get('DB_HOST'),
    "port": os.environ.get('DB_PORT'),
}


alerts_cols = {
    "sender_name": str,
    "location_id": int,
    "event": str,
    "start": int,
    "end": int,
    "description": str
}

daily_forecast_cols = {
    "dt": int,
    "summary": str,
    "pressure": float,
    "humidity": float,
    "dew_point": float,
    "wind_speed": float,
    "wind_gust": float,
    "clouds": float,
    "pop": float,
    "uvi": float,
    "rain": float,
    "snow": float
}


location_cols = {"lat": float,
                 "lon": float,
                 "timezone": str,
                 "pass_name": str,
                 "resort_name": str,
                 "timezone_offset": str}


current_weather_cols = {
    "dt" : int,
    "temp": float,
    "feels_like": float,
    "pressure": float,
    "humidity": float,
    "dew_point": float,
    "clouds": float,
    "uvi": float,
    "wind_speed": float,
    "wind_gust": float,
}

hourly_forecast_cols = {
    "dt": int,
    "temp": float,
    "feels_like": float ,
    "pressure": float,
    "humidity": float,
    "dew_point": float,
    "clouds": float,
    "uvi": float,
    "wind_speed": float,
    "wind_gust": float,
    "pop": float
}