CREATE SCHEMA IF NOT EXISTS ski_weather;
SET search_path TO ski_weather;

CREATE TABLE IF NOT EXISTS location(
    id SERIAL PRIMARY KEY,
    resort_name TEXT,
    pass_name TEXT,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    timezone TEXT,
    timezone_offset INT,
    link_to_livecam TEXT,
    UNIQUE(resort_name, pass_name, lat, lon)

);

CREATE TABLE IF NOT EXISTS current_weather(
    id SERIAL PRIMARY KEY,
    location_id INT,
    dt TIMESTAMP,
    temp DOUBLE PRECISION,
    feels_like DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    dew_point DOUBLE PRECISION,
    clouds DOUBLE PRECISION,
    uvi DOUBLE PRECISION,
    wind_speed DOUBLE PRECISION,
    wind_gust DOUBLE PRECISION,
    rain_1h DOUBLE PRECISION,
    snow_1h DOUBLE PRECISION,
    main VARCHAR(50),
    "description" TEXT,
    FOREIGN KEY (location_id) REFERENCES location(id)
);

CREATE TABLE IF NOT EXISTS hourly_forecast(
    id SERIAL PRIMARY KEY,
    current_weather_id INT,
    location_id INT,
    dt TIMESTAMP,
    temp DOUBLE PRECISION,
    feels_like DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    dew_point DOUBLE PRECISION,
    clouds DOUBLE PRECISION,
    uvi DOUBLE PRECISION,
    wind_speed DOUBLE PRECISION,
    wind_gust DOUBLE PRECISION,
    pop DOUBLE PRECISION,
    rain_1h DOUBLE PRECISION,
    snow_1h DOUBLE PRECISION,
    main VARCHAR(50),
    "description" TEXT,
    FOREIGN KEY (current_weather_id) REFERENCES current_weather(id),
    FOREIGN KEY (location_id) REFERENCES location(id),
    UNIQUE (dt, location_id)
);

CREATE TABLE IF NOT EXISTS daily_forecast(
    id SERIAL PRIMARY KEY,
    "date" DATE,
    location_id INT,
    current_weather_id INT,
    pressure DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    dew_point DOUBLE PRECISION,
    clouds DOUBLE PRECISION,
    uvi DOUBLE PRECISION,
    wind_speed DOUBLE PRECISION,
    wind_gust DOUBLE PRECISION,
    summary TEXT,
    pop DOUBLE PRECISION,
    rain DOUBLE PRECISION,
    snow DOUBLE PRECISION,
    main VARCHAR(50),
    "description" TEXT,
    min_temp DOUBLE PRECISION,
    max_temp DOUBLE PRECISION,
    day_temp DOUBLE PRECISION,
    day_feels_like DOUBLE PRECISION,
    FOREIGN KEY (current_weather_id) REFERENCES current_weather(id),
    FOREIGN KEY (location_id) REFERENCES location(id),
    UNIQUE ("date", location_id)
);

CREATE TABLE IF NOT EXISTS weather_alerts (
    id SERIAL PRIMARY KEY, 
    location_id INT,
    sender_name TEXT,
    event TEXT,
    start TIMESTAMP,
    "end" TIMESTAMP,
    description TEXT,

    FOREIGN KEY (location_id) REFERENCES location(id),
    UNIQUE(sender_name, event, start, "end") 

);

INSERT INTO location (resort_name, pass_name, lat, lon, timezone, timezone_offset, link_to_livecam) VALUES
('Winter Park', 'Ikon', 39.8765, -105.7658, 'America/Denver', -25200, 'https://www.winterparkresort.com/the-mountain/mountain-cams'),
('Copper Mountain', 'Ikon', 39.4937, -106.1594, 'America/Denver', -25200, 'https://www.coppercolorado.com/the-mountain/webcams'),
('Eldora', 'Ikon', 39.9375, -105.584, 'America/Denver', -25200, 'https://www.eldora.com/the-mountain/webcams/snow-stake-cam'),
('Steamboat Springs', 'Ikon', 40.4662, -106.7809, 'America/Denver', -25200, 'https://www.steamboat.com/the-mountain/live-cams'),
('Palisades Tahoe', 'Ikon', 39.1911, -120.2557, 'America/Los_Angeles', -28800, 'https://www.palisadestahoe.com/mountain-information/webcams'),
('Big Sky', 'Ikon', 45.2931, -111.3629, 'America/Denver', -25200, 'https://www.bigskyresort.com/current-conditions/webcams'),
('Northstar', 'Epic', 39.2567, -120.1334, 'America/Los_Angeles', -28800, 'https://www.northstarcalifornia.com/the-mountain/mountain-conditions/mountain-cams.aspx'),
('Crystal', 'Ikon', 46.9348, -121.4838, 'America/Los_Angeles', -28800, 'https://www.crystalmountainresort.com/the-mountain/mountain-report-and-webcams/webcams'),
('Jackson', 'Ikon', 43.5946, -110.8461, 'America/Denver', -25200, 'https://www.jacksonhole.com/live-mountain-cams'),
('Breckenridge', 'Epic', 39.4789, -106.0784, 'America/Denver', -25200, 'https://www.breckenridge.com/the-mountain/mountain-conditions/mountain-cams.aspx'),
('Vail', 'Epic', 39.6198, -106.3696, 'America/Denver', -25200, 'https://www.vail.com/the-mountain/mountain-conditions/mountain-cams.aspx'),
('Stratton', 'Ikon', 43.11, -72.9103, 'America/New_York', -18000, 'https://www.stratton.com/the-mountain/webcams'),
('Whistler', 'Epic', 50.0735, -122.9594, 'America/Vancouver', -28800, 'https://www.whistlerblackcomb.com/the-mountain/mountain-conditions/mountain-cams.aspx'),
('Charmonix', 'Ikon', 45.9698, 6.879, 'Europe/Paris', 3600, 'https://en.chamonix.com/webcams');


    