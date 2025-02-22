#!/bin/bash
echo "Fixing permissions for Postgres data..."

chown -R postgres:postgres /var/lib/postgresql/data
chmod -R 700 /var/lib/postgresql/data

if [ -d "/pgdata" ]; then
  chown -R postgres:postgres /pgdata
  chmod -R 700 /pgdata
fi

exec "$@"
