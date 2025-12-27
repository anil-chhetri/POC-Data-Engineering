#!/bin/bash
set -e

# source .env if you really want to double-ensure it’s loaded
# set -a; [ -f /docker-entrypoint-initdb.d/.env ] && source /docker-entrypoint-initdb.d/.env; set +a

PARQUET_FILE="/opt/parquet/*.parquet"
JSON_FILE="/tmp/data.json"
TARGET_TABLE="all_data"

echo "→ Converting Parquet to JSON via DuckDB..."
duckdb -c "COPY (SELECT *, filename as file_name FROM read_parquet('${PARQUET_FILE}', filename=true)) TO '${JSON_FILE}' (FORMAT JSON);"

echo "→ Preparing Postgres schema..."
psql -v ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" \
  --password <<-EOSQL

  CREATE TABLE IF NOT EXISTS ${TARGET_TABLE} (
    data JSONB
  );
  COPY ${TARGET_TABLE}(data) FROM '${JSON_FILE}';

EOSQL

echo "→ Loaded all rows into table '${TARGET_TABLE}' as one JSONB value."
