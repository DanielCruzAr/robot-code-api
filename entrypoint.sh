#!/bin/bash
set -e

until pg_isready "${DATABASE_URL}"; do
  echo "⏳ Waiting for Postgres..."
  sleep 1
done

# Run database migrations
alembic upgrade head

# Seed test data
python -m app.utils.seed_test_data

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload