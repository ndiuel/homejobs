web: gunicorn prod:app --workers=5
release: python manage.py db upgrade && python manage.py add_admin_roles