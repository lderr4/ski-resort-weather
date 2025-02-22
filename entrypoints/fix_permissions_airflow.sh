#!/bin/bash
echo "Fixing permissions..."
chown -R 50000:50000 /opt/airflow/dags /opt/airflow/logs
chmod -R 755 /opt/airflow/dags /opt/airflow/logs
exec "$@"