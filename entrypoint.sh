#!/bin/sh
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec gunicorn beyond_health.wsgi:application --bind 0.0.0.0:${PORT:-8000}
