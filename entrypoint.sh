#!/bin/sh
# Exit immediately if a command exits with a non-zero status.
set -e

# It's generally recommended to create migrations during development and commit them.
# For production, you might only want 'migrate'.
python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input

#gunicorn setupfolder.wsgi:application --bind 0.0.0.0:8080
# For production, consider specifying the number of workers, e.g., --workers 4
uvicorn setup.asgi:application --host 0.0.0.0 --port 8080