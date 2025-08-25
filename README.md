# Exact-OMOP

Scripts to populate the EXACT clinical trial matching system with patients stored in an extended OMOP schema

## Quickstart Setup
Be sure setenv.sh has DATABASE_URL set (export DATABASE_URL=<URL to postgres>)
```bash
source setenv.sh 
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run migrations & start
python omop_site/manage.py makemigrations
python omop_site/manage.py migrate
python omop_site/manage.py createsuperuser
python omop_site/manage.py runserver
```
Visit http://127.0.0.1:8000/ for the browser and /admin/ for Django admin.

