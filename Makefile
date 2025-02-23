up:
	docker-compose up -d

build-dev:
	docker-compose up --build -d

build-backend:
	docker-compose up webserver scheduler postgres

down:
	docker-compose down

build-prod:
	docker-compose up --build webserver scheduler -d

check-dev-db:
	docker-compose exec -T postgres-dev psql -U admin -d admin -c "SELECT * FROM ski_weather.location;"

check-cw-table:
	docker-compose exec -T postgres-dev psql -U admin -d admin -c "SELECT id, temp, snow_1h FROM ski_weather.current_weather LIMIT 100;"


check-hf-table:
	docker-compose exec -T postgres-dev psql -U admin -d admin -c "SELECT id, dt, temp, snow_1h FROM ski_weather.hourly_forecast LIMIT 100;"

check-a-table:
	docker-compose exec -T postgres-dev psql -U admin -d admin -c "SELECT sender_name, description FROM ski_weather.weather_alerts LIMIT 100;"