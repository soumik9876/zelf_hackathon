#!/bin/bash

echo "API SERVER RUN"
python manage.py migrate # Apply migrations

#python manage.py collectstatic
# Start the Gunicorn server
gunicorn --config gunicorn_config.py zelf_hackathon.wsgi:application
