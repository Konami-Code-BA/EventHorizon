release: python manage.py migrate
web: gunicorn project_name.wsgi --bind 0.0.0.0:$PORT