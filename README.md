# Ski-Resort-Weather


[Link to Application]([http://ski-resort-weather.com](http://ski-resort-weather.com/public/dashboard/6f9e1bf5-a3ac-4764-b298-69a6ecd642bc))

A fully deployed dashboard in AWS that gives live weather updates for ski resorts.

## Tools and Technologies
- Airflow: Orchestration with DAGs
- Metabase: Dashboarding capabilities
- Postgres: local db for storing Airflow and Metabase metadata
- AWS EC2: Linux server that hosts Airflow and Metabase
- AWS RDS: Postgres instance for storing weather data
- Terraform: IaC Tool for deploying AWS resources
- [Openweathermap](https://openweathermap.org/): Data Source for free live weather.


## Setup

### API Credentials:

Go to https://openweathermap.org, make a free account with the [One Call API](https://openweathermap.org/api/one-call-3).

### Setup AWS infrastructure with Terraform:
1. 
```
cd terraform
terraform init
terraform plan
terraform apply
```
2. Setup a Security Group for the EC2 instance that allows ssh access, and personal access over ports 3000 and 8080, and full access over port 80 for http requests.
3. Additionally, ensure there is a connection between the EC2 instance and the RDS instance.

### Linux Server Setup:
1. SSH into the EC2 server.

2. Run the following commands:
```
sudo yum update -y
sudo yum install git -y
git clone https://github.com/lderr4/ski-resort-weather.git
sudo yum install docker -y
sudo yum install make -y
sudo service docker start
sudo chkconfig docker on
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo usermod -aG docker ec2-user
cd ski-resort-weather
touch .env
vim .env
```
3. Copy Paste the following sensitive information into the .env file:
```
OPENWEATHERMAP_API_KEY=
AIRFLOW__WEBSERVER__SECRET_KEY=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```
3. Exit and reenter the ssh tunnel
4. Run these final commands
```
chmod 600 .env
sudo dnf install postgresql15 -y
PGPASSWORD="password" psql -h <DATABASASE-ENDPOINT> -U postgres -d postgres -f /sql/init.sql # make sure to set password and endpoint
docker-compose up metabase airflow postgres --build
```
5. (optional) If hosting on a domain run the following commands:
```
sudo yum install nginx -y
cd /etc/nginx/conf.d
sudo touch server_name.conf
sudo vim server_name.conf
```
Paste the following into the file:
```

listen 80;
server_name my-url.com www.my-url.com;

server {
    listen 80;
    server_name ski-resort-weather.com www.ski-resort-weather.com;
    location / {
        proxy_pass http://localhost:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port 80;
    }
}
```
Finally run this final command:
```
sudo systemctl start nginx
```








