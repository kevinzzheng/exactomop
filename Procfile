web: gunicorn omop_site.wsgi:application --preload --workers=${WEB_CONCURRENCY:-2} --threads=${GUNICORN_THREADS:-4} --timeout 120 --log-file -
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
