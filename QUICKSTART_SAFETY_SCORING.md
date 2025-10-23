# Quick Start Guide - Safety Scoring Feature

Get the Safety Scoring feature up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- PostgreSQL (or SQLite for development)
- Git

## Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/exactomop.git
cd exactomop
```

## Step 2: Set Up Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Mac/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure Database

### Option A: Use SQLite (Development)

No configuration needed! Django will create `db.sqlite3` automatically.

### Option B: Use PostgreSQL (Production)

Create `setenv.sh`:

```bash
#!/bin/bash
export DATABASE_URL="postgresql://user:password@localhost:5432/exactomop"
export DJANGO_SECRET_KEY="your-secret-key-here"
export DJANGO_DEBUG="1"
export SAFETY_WEB_THRESHOLD="15.0"
```

Then:

```bash
source setenv.sh
```

## Step 4: Run Migrations

```bash
python manage.py migrate
```

You should see:
```
Running migrations:
  Applying omop.0001_initial... OK
  Applying omop.0002_safety_scoring_models... OK
```

## Step 5: Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

## Step 6: Create Sample Data

### Option A: Via Django Shell

```bash
python manage.py shell
```

```python
from omop.models import Person
from omop.models_safety import TrialArm, AdverseEvent
from datetime import date

# Create a person
person = Person.objects.create(
    person_id=1,
    gender_concept_id=8507,
    year_of_birth=1970,
    month_of_birth=6,
    day_of_birth=15
)

# Create a trial arm
arm = TrialArm.objects.create(
    nct_number='NCT12345678',
    arm_name='Arm A: Experimental Drug X',
    arm_code='ARM_A',
    arm_type='EXPERIMENTAL',
    status='ACTIVE',
    enrollment_start_date=date(2023, 1, 1),
    last_data_cut=date(2024, 1, 1),
    n_patients=100,
    follow_up_months=12.0
)

# Create an adverse event
ae = AdverseEvent.objects.create(
    person=person,
    trial_arm=arm,
    event_name='Nausea',
    event_date=date(2023, 6, 1),
    grade=2,
    serious=False
)

print(f"Created trial arm: {arm}")
print(f"Created adverse event: {ae}")
```

### Option B: Load Synthetic Data

```bash
# If available
python manage.py loaddata sample_safety_data.json
```

## Step 7: Compute Safety Scores

```bash
python manage.py compute_safety_scores --verbosity=2
```

Expected output:
```
Starting safety score computation with WEB threshold H=15.0
Found 1 trial arm(s) to process

Arm A: Experimental Drug X (ARM_A):
  Person-years: 100.00
  Grade 1-2 count: 1
  Grade 3-4 count: 0
  Grade 5 count: 0
  EAIR: 0.0100
  WEB: 1.00
  Safety Score: 93.75

Created safety metrics for ARM_A (Score: 93.75)

============================================================
Successfully computed: 1
```

## Step 8: Start Development Server

```bash
python manage.py runserver
```

## Step 9: Explore the API

Open your browser and visit:

### Browsable API
- http://127.0.0.1:8000/api/
- http://127.0.0.1:8000/api/trial-arms/
- http://127.0.0.1:8000/api/trial-matching/
- http://127.0.0.1:8000/api/adverse-events/
- http://127.0.0.1:8000/api/safety-metrics/

### Django Admin
- http://127.0.0.1:8000/admin/
- Login with your superuser credentials
- Navigate to:
  - Trial Arms
  - Adverse Events
  - Trial Arm Safety Metrics

## Step 10: Test the Feature

### Via API (curl)

```bash
# Get all trial arms
curl http://127.0.0.1:8000/api/trial-arms/

# Get trial matching results
curl http://127.0.0.1:8000/api/trial-matching/?min_safety_score=60

# Get safety metrics
curl http://127.0.0.1:8000/api/safety-metrics/
```

### Via Python

```python
import requests

response = requests.get('http://127.0.0.1:8000/api/trial-arms/')
data = response.json()

for arm in data['results']:
    print(f"Arm: {arm['arm_name']}")
    print(f"Safety Score: {arm['safety_score']}")
    print(f"Category: {arm['safety_category']}")
    print()
```

### Via Admin Interface

1. Go to http://127.0.0.1:8000/admin/
2. Click "Trial Arms"
3. Click on your trial arm
4. View the computed safety metrics
5. Click "Safety Metrics" to see historical data

## Common Tasks

### Recompute Safety Scores

```bash
# Force recomputation
python manage.py compute_safety_scores --force

# Specific trial arm
python manage.py compute_safety_scores --trial-arm-id=1
```

### Add More Adverse Events

```python
from omop.models_safety import AdverseEvent, TrialArm
from omop.models import Person
from datetime import date

person = Person.objects.get(person_id=1)
arm = TrialArm.objects.get(arm_code='ARM_A')

AdverseEvent.objects.create(
    person=person,
    trial_arm=arm,
    event_name='Fatigue',
    event_date=date(2023, 7, 1),
    grade=3,
    serious=True
)

# Recompute after adding events
from django.core.management import call_command
call_command('compute_safety_scores', force=True)
```

### Run Tests

```bash
python manage.py test omop.tests.test_safety_scores
```

## Integration with Frontend

### React

```bash
cd frontend
npm install
```

```jsx
import SafetyScoreBadge from './components/SafetyScoreBadge';

function App() {
  return (
    <SafetyScoreBadge 
      safetyScore={93.75} 
      web={1.0} 
      eair={0.01} 
    />
  );
}
```

### Vue

```bash
cd frontend
npm install vue@3
```

```vue
<template>
  <SafetyScoreBadge 
    :safety-score="93.75" 
    :web="1.0" 
    :eair="0.01" 
  />
</template>

<script setup>
import SafetyScoreBadge from './components/SafetyScoreBadge.vue';
</script>
```

## Configuration

### Adjust WEB Threshold

In `omop_site/settings.py` or via environment:

```python
# settings.py
SAFETY_WEB_THRESHOLD = 20.0  # Default is 15.0

# OR via environment
export SAFETY_WEB_THRESHOLD=20.0
```

Higher threshold = more lenient scoring (higher scores)
Lower threshold = stricter scoring (lower scores)

## Troubleshooting

### "No module named 'rest_framework'"

```bash
pip install djangorestframework
```

### "relation 'trial_arm' does not exist"

```bash
python manage.py migrate
```

### Safety scores not computing

Check trial arm status:
```python
from omop.models_safety import TrialArm

arm = TrialArm.objects.get(arm_code='ARM_A')
print(f"Status: {arm.status}")  # Must be ACTIVE, ENDED, or COMPLETED
print(f"Patients: {arm.n_patients}")  # Must be > 0
print(f"Follow-up: {arm.follow_up_months}")  # Must be set
```

### API returns empty results

```bash
# Check if data exists
python manage.py shell
>>> from omop.models_safety import TrialArm
>>> TrialArm.objects.all().count()

# Compute safety scores if needed
python manage.py compute_safety_scores --force
```

## Next Steps

1. **Read Full Documentation:** `docs/SAFETY_SCORING.md`
2. **Explore API:** Use browsable API at `/api/`
3. **Add Real Data:** Import your clinical trial data
4. **Customize Frontend:** Modify React/Vue components
5. **Set Up Production:** Configure PostgreSQL and deploy

## Need Help?

- **Documentation:** `docs/SAFETY_SCORING.md`
- **Implementation Summary:** `SAFETY_SCORING_FEATURE.md`
- **GitHub Issues:** Report bugs and request features
- **Tests:** Run tests to understand expected behavior

---

**You're now ready to use the Safety Scoring feature!** 🎉

For detailed documentation on formulas, interpretation, and use cases, see `docs/SAFETY_SCORING.md`.

