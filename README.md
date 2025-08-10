# Django OMOP Starter (Postgres)

Minimal Django project with core OMOP tables and simple list/detail views.
Configured for PostgreSQL via environment variables.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Set Postgres env vars (example)
export PGDATABASE=omop
export PGUSER=postgres
export PGPASSWORD=yourpassword
export PGHOST=127.0.0.1
export PGPORT=5432

# Run migrations & start
python omop_site/manage.py makemigrations
python omop_site/manage.py migrate
python omop_site/manage.py createsuperuser
python omop_site/manage.py runserver
```
Visit http://127.0.0.1:8000/ for the browser and /admin/ for Django admin.

> Schema is simplified for demo purposes. Extend models to match full OMOP CDM.
