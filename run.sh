#!/bin/bash

echo "API SERVER RUN"
python manage.py migrate # Apply migrations

# Load data from fixtures
python manage.py loaddata user/fixtures/user_data.json
python manage.py loaddata restaurant/fixtures/restaurant_data.json

python manage.py collectstatic
# Start the Gunicorn server
gunicorn --config gunicorn_config.py django_starter.wsgi:application
