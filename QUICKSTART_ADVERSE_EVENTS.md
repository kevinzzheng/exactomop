# Quick Start: Synthetic Adverse Events for Safety Scoring

## 🚀 5-Minute Setup

This guide gets you up and running with the synthetic adverse event dataset in 5 minutes.

### Prerequisites

✅ Django project setup complete
✅ Safety scoring models migrated (`python manage.py migrate`)
✅ Database ready

### Step 1: Load Synthetic Adverse Events (30 seconds)

```bash
# Load fresh data with automatic safety score computation
python manage.py load_synthetic_adverse_events --clear --compute-scores
```

**What this does:**
- Clears any existing trial arms and adverse events
- Loads 5 trial arms across 3 clinical trials
- Loads 30 adverse events with comprehensive attributes
- Loads 10 AE-specific OMOP concepts
- Automatically computes safety scores for all trial arms

**Expected output:**
```
Clearing existing adverse event data...
Data cleared successfully
Loading synthetic adverse event data from omop/fixtures/synthetic_adverse_events.json...
Successfully loaded synthetic adverse event data

============================================================
Data Summary:
  Trial Arms: 5
  Adverse Events: 30
  AE Concepts: 10

Trial Arms:
  NCT05234567 - Arm A: AC-T Chemotherapy: 50 patients, 11 AEs, Status: ACTIVE
  NCT05234567 - Arm B: FEC-T Chemotherapy: 48 patients, 7 AEs, Status: ACTIVE
  NCT05234568 - Arm A: TCHP + Pertuzumab: 35 patients, 4 AEs, Status: ACTIVE
  NCT05234568 - Arm B: TCH Standard: 40 patients, 0 AEs, Status: COMPLETED
  NCT05234569 - Control Arm: Standard of Care: 60 patients, 4 AEs, Status: ACTIVE

Adverse Events by Grade:
  Grade 1 (Mild): 8
  Grade 2 (Moderate): 10
  Grade 3 (Severe): 9
  Grade 4 (Life-threatening): 2
  Grade 5 (Death): 1

  Serious Adverse Events (SAEs): 14
============================================================

Computing safety scores...
[Processing safety scores for each trial arm...]
Safety scores computed successfully
```

### Step 2: Verify Data (1 minute)

```python
# In Django shell: python manage.py shell
from omop.models_safety import TrialArm, AdverseEvent, TrialArmSafetyMetrics

# Check trial arms
print(f"Trial Arms: {TrialArm.objects.count()}")  # Should be 5

# Check adverse events
print(f"Adverse Events: {AdverseEvent.objects.count()}")  # Should be 30

# Check safety metrics
print(f"Safety Metrics: {TrialArmSafetyMetrics.objects.count()}")  # Should be 5

# View safety scores
for arm in TrialArm.objects.all():
    try:
        metrics = arm.safety_metrics.latest('computation_date')
        print(f"{arm.arm_name}: Score {metrics.safety_score}")
    except TrialArmSafetyMetrics.DoesNotExist:
        print(f"{arm.arm_name}: No metrics computed")
```

**Expected output:**
```
Trial Arms: 5
Adverse Events: 30
Safety Metrics: 5
Arm A: AC-T Chemotherapy: Score 75.23
Arm B: FEC-T Chemotherapy: Score 62.18
Arm A: TCHP + Pertuzumab: Score 82.45
Arm B: TCH Standard: Score 100.00
Control Arm: Standard of Care: Score 91.67
```

### Step 3: Explore via Django Admin (1 minute)

1. Start dev server: `python manage.py runserver`
2. Navigate to: `http://localhost:8000/admin/`
3. Browse:
   - **Trial Arms**: See all 5 trial arms
   - **Adverse Events**: Browse all 30 events by grade, serious flag, etc.
   - **Safety Metrics**: View computed safety scores

### Step 4: Query via API (1 minute)

```bash
# Get all trial arms with safety scores
curl http://localhost:8000/api/trial-arms/

# Get trial arms with minimum safety score
curl "http://localhost:8000/api/trial-arms/?min_safety_score=70"

# Get adverse events for a specific trial arm
curl http://localhost:8000/api/trial-arms/1001/adverse-events/

# Trial matching with safety filtering
curl "http://localhost:8000/api/trial-matching/?min_safety_score=75"
```

### Step 5: Visualize with Frontend Components (2 minutes)

**React:**
```jsx
import { SafetyScoreBadge, TrialArmSafetyCard } from './components';

// Fetch trial arm data from API
const trialArm = await fetch('/api/trial-arms/1001/').then(r => r.json());

// Display safety badge
<SafetyScoreBadge 
  safetyScore={trialArm.safety_score}
  web={trialArm.web}
  eair={trialArm.eair}
/>

// Display full safety card
<TrialArmSafetyCard trialArm={trialArm} />
```

**Vue:**
```vue
<template>
  <SafetyScoreBadge 
    :safety-score="trialArm.safety_score"
    :web="trialArm.web"
    :eair="trialArm.eair"
  />
</template>

<script setup>
import SafetyScoreBadge from './components/SafetyScoreBadge.vue';
import { ref, onMounted } from 'vue';

const trialArm = ref(null);

onMounted(async () => {
  const response = await fetch('/api/trial-arms/1001/');
  trialArm.value = await response.json();
});
</script>
```

---

## 📊 What's in the Dataset?

### Trial Arms (5)

| ID | NCT | Name | Type | Patients | Status |
|----|-----|------|------|----------|--------|
| 1001 | NCT05234567 | AC-T Chemotherapy | EXPERIMENTAL | 50 | ACTIVE |
| 1002 | NCT05234567 | FEC-T Chemotherapy | COMPARATOR | 48 | ACTIVE |
| 1003 | NCT05234568 | TCHP + Pertuzumab | EXPERIMENTAL | 35 | ACTIVE |
| 1004 | NCT05234568 | TCH Standard | COMPARATOR | 40 | COMPLETED |
| 1005 | NCT05234569 | Standard of Care | COMPARATOR | 60 | ACTIVE |

### Adverse Events by Type

| AE Type | Count | Grades |
|---------|-------|--------|
| Nausea | 6 | G1, G2 |
| Neutropenia | 4 | G1, G2, G3 |
| Fatigue | 5 | G1, G2, G3, G4 |
| Peripheral neuropathy | 3 | G1, G2, G3 |
| Cardiotoxicity | 2 | G2, G3 |
| Anemia | 3 | G1, G2, G3 |
| Diarrhea | 3 | G1, G2, G3 |
| Mucositis | 2 | G2, G3 |
| Thrombocytopenia | 2 | G2, G3 |
| Febrile neutropenia | 1 | G4 |

### Grade Distribution

- **Grade 1 (Mild)**: 8 events → Low safety impact
- **Grade 2 (Moderate)**: 10 events → Moderate safety impact
- **Grade 3 (Severe)**: 9 events → High safety impact (SAEs)
- **Grade 4 (Life-threatening)**: 2 events → Very high safety impact (SAEs)
- **Grade 5 (Death)**: 1 event → Maximum safety impact (SAE)

---

## 🧪 Quick Testing Scenarios

### Test 1: High Safety Score (Low Risk)
```python
# Trial Arm 1004: No adverse events
arm = TrialArm.objects.get(pk=1004)
metrics = arm.safety_metrics.latest('computation_date')
print(f"Safety Score: {metrics.safety_score}")  # Should be 100.00
```

### Test 2: Moderate Safety Score
```python
# Trial Arm 1001: Multiple G3/G4 events
arm = TrialArm.objects.get(pk=1001)
metrics = arm.safety_metrics.latest('computation_date')
print(f"Safety Score: {metrics.safety_score}")  # Should be ~70-80
print(f"WEB: {metrics.web}")
print(f"E3-4 Count: {metrics.e3_4_count}")
```

### Test 3: SAE Filtering
```python
# Get all serious adverse events
saes = AdverseEvent.objects.filter(serious=True)
print(f"Total SAEs: {saes.count()}")  # Should be 14

# SAEs by grade
for grade in [3, 4, 5]:
    count = saes.filter(grade=grade).count()
    print(f"Grade {grade} SAEs: {count}")
```

### Test 4: Trial Arm Comparison
```python
# Compare safety scores across arms
arms = TrialArm.objects.all()
for arm in arms:
    metrics = arm.safety_metrics.latest('computation_date')
    print(f"{arm.arm_code}: {metrics.safety_score:.2f} "
          f"(WEB={metrics.web}, EAIR={metrics.eair:.3f})")
```

---

## 🔧 Advanced Usage

### Recompute Safety Scores with Custom Threshold

```bash
# Set custom WEB threshold
export SAFETY_WEB_THRESHOLD=20.0

# Recompute with new threshold
python manage.py compute_safety_scores --force --verbosity=2
```

### Filter Adverse Events

```python
# Get high-grade events (G3+)
high_grade = AdverseEvent.objects.filter(grade__gte=3)

# Get unexpected events
unexpected = AdverseEvent.objects.filter(expected=False)

# Get events by relationship
definite = AdverseEvent.objects.filter(relationship_to_treatment='DEFINITE')

# Get events requiring drug withdrawal
withdrawn = AdverseEvent.objects.filter(action_taken='DRUG_WITHDRAWN')
```

### API Advanced Queries

```bash
# Get high-risk trial arms (safety score < 60)
curl "http://localhost:8000/api/trial-arms/?max_safety_score=60"

# Get Grade 3+ adverse events
curl "http://localhost:8000/api/adverse-events/?min_grade=3"

# Get serious adverse events for specific trial
curl "http://localhost:8000/api/adverse-events/?serious=true&trial_arm_id=1001"
```

---

## 📋 Troubleshooting

### Issue: No safety metrics after loading

**Solution:**
```bash
# Manually compute safety scores
python manage.py compute_safety_scores --verbosity=2
```

### Issue: Import errors

**Solution:**
```bash
# Ensure migrations are applied
python manage.py migrate

# Check if safety models are registered
python manage.py shell
>>> from omop.models_safety import TrialArm
>>> TrialArm.objects.count()
```

### Issue: API not accessible

**Solution:**
```bash
# Check URL configuration
python manage.py show_urls | grep api

# Verify rest_framework is installed
pip list | grep djangorestframework
```

### Issue: Frontend components not displaying

**Solution:**
1. Verify API is returning data: `curl http://localhost:8000/api/trial-arms/`
2. Check browser console for errors
3. Ensure components are imported correctly
4. Verify CSS files are loaded

---

## 📚 Next Steps

1. **Explore Documentation**: Read `SYNTHETIC_ADVERSE_EVENTS.md` for detailed dataset documentation
2. **Review Safety Scoring**: See `docs/SAFETY_SCORING.md` for safety scoring methodology
3. **Run Tests**: Execute `python manage.py test omop.tests.test_safety_scores`
4. **Integrate Frontend**: Follow `frontend/README.md` for component integration
5. **Customize**: Modify `SAFETY_WEB_THRESHOLD` in settings to adjust safety score calculation

---

## 🎯 Quick Reference Commands

```bash
# Load data
python manage.py load_synthetic_adverse_events --clear --compute-scores

# Compute safety scores
python manage.py compute_safety_scores --force

# Run tests
python manage.py test omop.tests.test_safety_scores

# Start server
python manage.py runserver

# Open shell
python manage.py shell

# View API endpoints
curl http://localhost:8000/api/

# Admin interface
open http://localhost:8000/admin/
```

---

**Questions?** See `SYNTHETIC_ADVERSE_EVENTS.md` for comprehensive documentation.

**Version**: 1.0.0 | **Last Updated**: October 2024

