# Exact-OMOP

Scripts to ppulate the EXACT clinical trial matching system with data from OMOP types

## Quickstart Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run migrations & start
python omop_site/manage.py makemigrations
python omop_site/manage.py migrate
python omop_site/manage.py createsuperuser
python omop_site/manage.py runserver
```
Visit http://127.0.0.1:8000/ for the browser and /admin/ for Django admin.

