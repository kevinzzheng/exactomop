# Safety Scoring Feature Documentation

## Overview

The Safety Scoring feature provides a quantitative framework for evaluating and comparing the safety profiles of clinical trial arms in the EXACTOMOP system. This feature computes standardized safety metrics based on adverse event data, enabling data-driven decision-making in clinical trial selection and patient matching.

## Table of Contents

1. [Concept & Methodology](#concept--methodology)
2. [Mathematical Formulas](#mathematical-formulas)
3. [Data Models](#data-models)
4. [Management Command](#management-command)
5. [API Endpoints](#api-endpoints)
6. [Frontend Components](#frontend-components)
7. [Use Cases](#use-cases)
8. [Interpretation Guide](#interpretation-guide)
9. [Configuration](#configuration)
10. [Examples](#examples)

---

## Concept & Methodology

### Background

Clinical trial safety evaluation requires systematic assessment of adverse events (AEs) across different treatment arms. The Safety Scoring system provides a unified metric that:

- Weights adverse events by severity (CTCAE grades 1-5)
- Normalizes for patient exposure time (person-years)
- Produces an interpretable 0-100 score (higher = safer)
- Enables objective comparison across trial arms

### Key Components

1. **Person-Years Calculation**: Measures total patient exposure time
2. **Adverse Event Counting**: Counts unique patients experiencing AEs by grade
3. **Weighted Event Burden (WEB)**: Severity-weighted AE metric
4. **Event-Adjusted Incidence Rate (EAIR)**: Rate of AEs per person-year
5. **Safety Score**: Normalized 0-100 metric incorporating WEB

---

## Mathematical Formulas

### 1. Person-Years

```
person_years = n_patients × (follow_up_months / 12)
```

**Alternative (when follow_up_months not available):**
```
days_followup = data_cut_date - enrollment_start_date
person_years = n_patients × (days_followup / 365.25)
```

**Example:**
- 100 patients followed for 12 months = 100 person-years
- 50 patients followed for 24 months = 100 person-years

### 2. Adverse Event Counts

Count **unique patients** experiencing events by CTCAE grade:

- **e1_2_count**: Patients with Grade 1-2 AEs (mild to moderate)
- **e3_4_count**: Patients with Grade 3-4 AEs (severe to life-threatening)
- **e5_count**: Patients with Grade 5 AEs (death)

**Note:** A single patient with multiple AEs of different grades is counted in multiple categories.

### 3. Weighted Event Burden (WEB)

```
WEB = (1 × e1_2_count) + (10 × e3_4_count) + (100 × e5_count)
```

**Rationale:**
- Grade 1-2 events: Weight = 1 (baseline)
- Grade 3-4 events: Weight = 10 (10× more severe)
- Grade 5 events: Weight = 100 (100× more severe)

**Example:**
```
e1_2 = 20 patients
e3_4 = 5 patients
e5 = 1 patient

WEB = (1 × 20) + (10 × 5) + (100 × 1)
    = 20 + 50 + 100
    = 170
```

### 4. Event-Adjusted Incidence Rate (EAIR)

```
EAIR = patients_with_any_AE / person_years
```

**Example:**
```
30 patients with AEs / 100 person-years = 0.30 events per person-year
```

**Interpretation:**
- EAIR = 0.10: Low incidence (10% annual rate)
- EAIR = 0.30: Moderate incidence (30% annual rate)
- EAIR = 0.50+: High incidence (50%+ annual rate)

### 5. Safety Score

```
Safety_Score = 100 / (1 + WEB/H)
```

Where:
- **H** = WEB threshold parameter (default: 15)
- **WEB** = Weighted Event Burden (calculated above)

**Properties:**
- Range: 0 to 100
- Higher score = safer profile
- Score of 100 = no adverse events (WEB = 0)
- Score approaches 0 as WEB increases

**Example Calculations:**

| WEB | Safety Score (H=15) | Risk Category |
|-----|-------------------|---------------|
| 0 | 100.0 | Low Risk |
| 7.5 | 66.7 | Moderate Risk |
| 15 | 50.0 | Elevated Risk |
| 30 | 33.3 | High Risk |
| 60 | 20.0 | High Risk |
| 150 | 9.1 | High Risk |

---

## Data Models

### 1. TrialArm

Represents a treatment arm within a clinical trial.

**Key Fields:**
```python
- trial_arm_id: Primary key
- nct_number: ClinicalTrials.gov identifier
- arm_name: Descriptive name (e.g., "Arm A: Drug X + Chemo")
- arm_code: Short code (e.g., "ARM_A")
- arm_type: EXPERIMENTAL | ACTIVE_COMPARATOR | PLACEBO_COMPARATOR
- status: ACTIVE | COMPLETED | ENDED | SUSPENDED | TERMINATED
- n_patients: Number enrolled
- follow_up_months: Average follow-up duration
- enrollment_start_date: Start of enrollment
- last_data_cut: Date of last safety data snapshot
```

**Database Table:** `trial_arm`

### 2. AdverseEvent

Tracks individual adverse events for patients in trial arms.

**Key Fields:**
```python
- adverse_event_id: Primary key
- person: Foreign key to Person
- trial_arm: Foreign key to TrialArm
- event_name: AE name (e.g., "Neutropenia")
- event_date: Date of occurrence
- grade: CTCAE grade (1-5)
- serious: Boolean (SAE flag)
- relationship_to_treatment: Causality assessment
- outcome: Resolution status
```

**Database Table:** `adverse_event`

### 3. TrialArmSafetyMetrics

Stores computed safety scores for trial arms.

**Key Fields:**
```python
- safety_metrics_id: Primary key
- trial_arm: Foreign key to TrialArm
- data_cut_date: Date of data snapshot
- person_years: Computed exposure time
- n_patients: Number of patients included
- e1_2_count: Grade 1-2 patient count
- e3_4_count: Grade 3-4 patient count
- e5_count: Grade 5 patient count
- total_ae_count: Total number of AEs
- patients_with_any_ae: Patients experiencing ≥1 AE
- eair: Event-Adjusted Incidence Rate
- web: Weighted Event Burden
- safety_score: Overall safety score (0-100)
- web_threshold_h: H parameter used
- computation_date: When computed
```

**Database Table:** `trial_arm_safety_metrics`

**Unique Constraint:** `(trial_arm, data_cut_date)` - prevents duplicate computations

---

## Management Command

### compute_safety_scores

Django management command to compute safety scores for trial arms.

#### Basic Usage

```bash
# Compute for all eligible arms
python manage.py compute_safety_scores

# Force recomputation (even if already computed this month)
python manage.py compute_safety_scores --force

# Compute for specific trial arm
python manage.py compute_safety_scores --trial-arm-id=123

# Dry run (show what would be computed)
python manage.py compute_safety_scores --dry-run

# Verbose output
python manage.py compute_safety_scores --verbosity=2
```

#### Eligibility Criteria

The command processes trial arms that:
1. Have `status` in ['ACTIVE', 'ENDED', 'COMPLETED']
2. Have NOT been computed in the current month (unless `--force`)
3. Have sufficient data (n_patients > 0, follow_up data available)

#### Output Example

```
Starting safety score computation with WEB threshold H=15.0
Found 5 trial arm(s) to process

Arm A: Experimental Drug X (ARM_A):
  Person-years: 125.50
  Grade 1-2 count: 15
  Grade 3-4 count: 8
  Grade 5 count: 1
  EAIR: 0.1912
  WEB: 115.00
  Safety Score: 56.60

Created safety metrics for ARM_A (Score: 56.60)

============================================================
Successfully computed: 5
Errors: 0
```

#### Error Handling

Common errors and solutions:

**Error:** "Cannot compute person-years: missing follow_up_months"
- **Solution:** Ensure `follow_up_months` is set OR `enrollment_start_date` and `last_data_cut` are populated

**Error:** "Invalid person-years (0)"
- **Solution:** Check that `n_patients > 0` and follow-up duration > 0

---

## API Endpoints

### GET /api/trial-arms/

List all trial arms with safety metrics.

**Query Parameters:**
- `status`: Filter by status (ACTIVE, COMPLETED, etc.)
- `nct_number`: Filter by NCT number
- `min_safety_score`: Minimum safety score threshold
- `page`: Page number (pagination)
- `page_size`: Results per page (max 100)

**Response:**
```json
{
  "count": 10,
  "next": "http://api/trial-arms/?page=2",
  "previous": null,
  "results": [
    {
      "trial_arm_id": 1,
      "nct_number": "NCT12345678",
      "arm_name": "Arm A: Drug X + Standard Care",
      "arm_code": "ARM_A",
      "arm_type": "EXPERIMENTAL",
      "status": "ACTIVE",
      "n_patients": 100,
      "follow_up_months": "12.00",
      "safety_score": 75.5,
      "web": 25.0,
      "eair": 0.35,
      "safety_category": "MODERATE_RISK",
      "latest_safety_metrics": { /* full metrics object */ }
    }
  ]
}
```

### GET /api/trial-arms/{id}/

Get specific trial arm with detailed safety metrics.

**Response:**
```json
{
  "trial_arm_id": 1,
  "arm_name": "Arm A: Drug X + Standard Care",
  /* ... other fields ... */
  "latest_safety_metrics": {
    "safety_metrics_id": 10,
    "data_cut_date": "2024-01-15",
    "person_years": "100.00",
    "n_patients": 100,
    "e1_2_count": 20,
    "e3_4_count": 5,
    "e5_count": 1,
    "total_ae_count": 45,
    "patients_with_any_ae": 26,
    "eair": "0.2600",
    "web": "125.00",
    "safety_score": "54.55",
    "safety_category": "ELEVATED_RISK"
  }
}
```

### GET /api/trial-arms/{id}/safety-metrics/

Get all historical safety metrics for a trial arm.

**Response:**
```json
[
  {
    "safety_metrics_id": 10,
    "data_cut_date": "2024-01-15",
    "safety_score": "54.55",
    /* ... */
  },
  {
    "safety_metrics_id": 9,
    "data_cut_date": "2023-12-15",
    "safety_score": "58.20",
    /* ... */
  }
]
```

### GET/POST /api/trial-matching/

Find matching trials with safety scoring.

**GET Query Parameters:**
- `status`: Filter by status (default: ACTIVE)
- `min_safety_score`: Minimum acceptable safety score
- `max_results`: Limit number of results (default: 25)

**POST Request Body:**
```json
{
  "person_id": 123,
  "diagnosis": "Breast Cancer",
  "stage": "III",
  "min_safety_score": 60,
  "max_results": 10
}
```

**Response:**
```json
[
  {
    "trial_arm": { /* trial arm object */ },
    "match_score": 0.85,
    "match_reasons": ["Biomarker match", "Stage appropriate"],
    "safety_score": 75.5,
    "safety_category": "MODERATE_RISK",
    "web": 25.0,
    "eair": 0.35,
    "recommended": true
  }
]
```

### GET /api/adverse-events/

List adverse events.

**Query Parameters:**
- `grade`: Filter by CTCAE grade (1-5)
- `serious`: Filter by serious flag (true/false)
- `trial_arm_id`: Filter by trial arm
- `person_id`: Filter by person

**Response:**
```json
{
  "count": 45,
  "results": [
    {
      "adverse_event_id": 1,
      "person": 123,
      "trial_arm": 1,
      "event_name": "Neutropenia",
      "event_date": "2023-06-15",
      "grade": 3,
      "serious": true,
      "relationship_to_treatment": "PROBABLE",
      "outcome": "RECOVERED"
    }
  ]
}
```

---

## Frontend Components

### SafetyScoreBadge

Compact badge displaying safety score with color-coded risk level.

**React Usage:**
```jsx
import SafetyScoreBadge from './components/SafetyScoreBadge';

<SafetyScoreBadge 
  safetyScore={75.5} 
  web={25.0} 
  eair={0.35} 
  size="md"
/>
```

**Vue Usage:**
```vue
<SafetyScoreBadge 
  :safety-score="75.5" 
  :web="25.0" 
  :eair="0.35" 
  size="md"
/>
```

**Features:**
- Color-coded by risk (green/yellow/orange/red)
- Interactive tooltip with detailed metrics
- Responsive and accessible

### TrialArmSafetyCard

Comprehensive card showing all safety information for a trial arm.

**React Usage:**
```jsx
import TrialArmSafetyCard from './components/TrialArmSafetyCard';

<TrialArmSafetyCard 
  trialArm={trialArmData} 
  onSelect={(arm) => console.log('Selected:', arm)}
/>
```

**Features:**
- Displays trial arm metadata
- Shows safety score badge
- Visualizes AE breakdown by grade
- Shows enrollment and follow-up metrics
- Click-to-select functionality

---

## Use Cases

### 1. Clinical Trial Selection

**Scenario:** Identify safest available trials for a newly diagnosed patient.

**Workflow:**
1. Query active trials with minimum safety threshold
2. Filter by disease indication and eligibility
3. Rank by safety score
4. Present top matches to clinician

**API Call:**
```bash
GET /api/trial-matching/?status=ACTIVE&min_safety_score=70
```

### 2. Comparative Safety Analysis

**Scenario:** Compare safety profiles of multiple arms within a trial.

**Workflow:**
1. Retrieve all arms for a specific NCT number
2. Display side-by-side safety metrics
3. Highlight differences in AE profiles
4. Generate comparative report

**API Call:**
```bash
GET /api/trial-arms/?nct_number=NCT12345678
```

### 3. Safety Monitoring & Alerts

**Scenario:** Monitor trial arms for declining safety scores.

**Workflow:**
1. Schedule monthly `compute_safety_scores`
2. Compare current score to previous month
3. Alert if score drops by >10 points
4. Flag for safety review

**Implementation:**
```bash
# Cron job (monthly)
0 0 1 * * python manage.py compute_safety_scores
```

### 4. Patient Counseling

**Scenario:** Explain safety profile to patient considering trial enrollment.

**Workflow:**
1. Display TrialArmSafetyCard for recommended trial
2. Show AE breakdown by grade
3. Explain safety score in patient-friendly terms
4. Compare to standard-of-care safety

**UI Integration:**
```jsx
<TrialArmSafetyCard trialArm={recommendedTrial} />
<PatientEducationPanel safetyScore={trial.safety_score} />
```

### 5. Regulatory Reporting

**Scenario:** Generate safety summaries for IRB/DSMB review.

**Workflow:**
1. Export safety metrics for all active arms
2. Include time-series trends
3. Highlight arms with declining scores
4. Attach raw AE data

**Export:**
```bash
GET /api/safety-metrics/?trial_arm_id=123&format=csv
```

---

## Interpretation Guide

### Safety Score Ranges

| Score Range | Risk Category | Color Code | Interpretation |
|-------------|--------------|------------|----------------|
| 80-100 | **Low Risk** | 🟢 Green | Favorable safety profile; few or mild AEs |
| 60-79 | **Moderate Risk** | 🟡 Yellow | Acceptable safety; some moderate/severe AEs |
| 40-59 | **Elevated Risk** | 🟠 Orange | Concerning safety; notable severe AEs |
| 0-39 | **High Risk** | 🔴 Red | Significant safety concerns; many severe AEs |

### WEB Interpretation

| WEB Range | Severity Level | Typical Profile |
|-----------|---------------|-----------------|
| 0-10 | Minimal | Very few AEs, mostly grade 1-2 |
| 11-30 | Low-Moderate | Mix of mild/moderate AEs, rare severe |
| 31-75 | Moderate-High | Multiple severe AEs or few fatal events |
| 76+ | High | Many severe AEs and/or multiple fatal events |

### EAIR Interpretation

| EAIR Range | Incidence Level | Meaning |
|------------|----------------|---------|
| < 0.20 | Low | <20% of patients experience AEs annually |
| 0.20-0.50 | Moderate | 20-50% annual AE rate |
| 0.51-1.00 | High | 51-100% annual AE rate |
| > 1.00 | Very High | Patients averaging >1 AE per year |

### Clinical Decision Framework

**When Safety Score ≥ 70:**
- Generally safe for patient enrollment
- Standard monitoring protocols
- Appropriate for most eligible patients

**When Safety Score 50-69:**
- Acceptable with enhanced monitoring
- Careful patient selection
- Detailed informed consent
- More frequent safety assessments

**When Safety Score < 50:**
- Rigorous eligibility screening
- Reserved for patients with limited alternatives
- Intensive safety monitoring
- Consider alternative trials if available

---

## Configuration

### Django Settings

Add to `settings.py`:

```python
# Safety Scoring Configuration
SAFETY_WEB_THRESHOLD = 15.0  # Default H parameter
```

**Environment Variable:**
```bash
export SAFETY_WEB_THRESHOLD=15.0
```

### Adjusting WEB Threshold (H)

The H parameter controls score sensitivity:

- **Higher H (e.g., 20):** More lenient scoring, higher scores overall
- **Lower H (e.g., 10):** Stricter scoring, lower scores overall

**Effect on Scores:**

| WEB | H=10 | H=15 | H=20 |
|-----|------|------|------|
| 10 | 50.0 | 60.0 | 66.7 |
| 20 | 33.3 | 42.9 | 50.0 |
| 30 | 25.0 | 33.3 | 40.0 |

**Recommendation:** Use default H=15 unless institutional standards require adjustment.

---

## Examples

### Example 1: Low-Risk Trial Arm

**Scenario:** Early-phase immunotherapy trial

**Data:**
- n_patients: 50
- follow_up_months: 6
- e1_2_count: 8 (fatigue, nausea)
- e3_4_count: 1 (grade 3 rash)
- e5_count: 0

**Calculations:**
```
person_years = 50 × (6/12) = 25
WEB = (1 × 8) + (10 × 1) + (100 × 0) = 18
safety_score = 100 / (1 + 18/15) = 45.45
```

**Result:** Score 45.5 = Elevated Risk (due to short follow-up)

### Example 2: Moderate-Risk Trial Arm

**Scenario:** Combination chemotherapy trial

**Data:**
- n_patients: 200
- follow_up_months: 18
- e1_2_count: 120 (various mild AEs)
- e3_4_count: 25 (neutropenia, infections)
- e5_count: 2 (treatment-related deaths)

**Calculations:**
```
person_years = 200 × (18/12) = 300
WEB = (1 × 120) + (10 × 25) + (100 × 2) = 570
safety_score = 100 / (1 + 570/15) = 2.56
```

**Result:** Score 2.6 = High Risk (significant safety concerns)

### Example 3: API Integration Example

**Full workflow with Python:**

```python
import requests

# Get trial arms with minimum safety score
response = requests.get(
    'http://api.example.com/api/trial-arms/',
    params={
        'status': 'ACTIVE',
        'min_safety_score': 60,
        'page_size': 10
    }
)

trial_arms = response.json()['results']

# Filter and sort
safe_trials = [
    arm for arm in trial_arms 
    if arm['safety_score'] >= 70
]

safe_trials.sort(key=lambda x: x['safety_score'], reverse=True)

# Display results
for arm in safe_trials:
    print(f"{arm['arm_name']}: Score {arm['safety_score']}")
    print(f"  WEB: {arm['web']}, EAIR: {arm['eair']}")
    print(f"  Risk: {arm['safety_category']}\n")
```

---

## Best Practices

### 1. Data Quality

- **Ensure Complete AE Reporting:** Incomplete data biases scores upward
- **Standardize CTCAE Grading:** Consistent grading across sites
- **Regular Data Cuts:** Monthly or quarterly for active trials
- **Validate Person-Years:** Check follow-up calculations

### 2. Computation Frequency

- **Active Trials:** Monthly recomputation
- **Completed Trials:** Final computation at study closure
- **Interim Analyses:** Align with DSMB meeting schedule

### 3. Interpretation

- **Context Matters:** Compare within disease indication
- **Consider Population:** Sicker patients → more AEs expected
- **Trend Analysis:** Look at score changes over time
- **Don't Use Alone:** Combine with efficacy and other factors

### 4. Clinical Integration

- **Incorporate into EMR:** Display in trial matching workflows
- **Train Staff:** Educate clinicians on interpretation
- **Document Decisions:** Record how scores influenced enrollment
- **Patient Education:** Translate scores to understandable language

---

## Troubleshooting

### Issue: Safety scores not computing

**Symptoms:** Command runs but creates no metrics

**Diagnosis:**
1. Check trial arm status: Must be ACTIVE/ENDED/COMPLETED
2. Verify data cut date: Must not already be computed this month
3. Confirm follow-up data: Needs `follow_up_months` OR enrollment dates

**Solution:**
```bash
# Force recomputation
python manage.py compute_safety_scores --force --verbosity=2
```

### Issue: Unexpectedly low scores

**Symptoms:** All scores < 30 despite few AEs

**Diagnosis:**
1. Check H parameter: May be too low
2. Verify WEB calculation: Look for data entry errors
3. Review AE counts: Ensure not double-counting patients

**Solution:**
```python
# settings.py
SAFETY_WEB_THRESHOLD = 20.0  # Increase from 15
```

### Issue: Missing safety data in API

**Symptoms:** `latest_safety_metrics` is null

**Diagnosis:**
1. Safety scores not yet computed for this arm
2. No data cut within valid time range

**Solution:**
```bash
python manage.py compute_safety_scores --trial-arm-id=<ID>
```

---

## Future Enhancements

### Planned Features

1. **Time-Series Visualization:** Plot safety score trends over time
2. **Predictive Modeling:** Forecast future safety scores based on enrollment
3. **Comparative Benchmarking:** Compare to historical trial data
4. **Automated Alerts:** Email notifications for score drops
5. **Multi-Arm Stratification:** Subgroup analysis by demographics
6. **Integration with FAERS:** Import real-world AE data

### Research Directions

- Validate scoring algorithm against clinical outcomes
- Develop disease-specific H parameters
- Incorporate patient-reported outcomes (PROs)
- Machine learning for AE prediction

---

## References

1. **CTCAE v5.0** - Common Terminology Criteria for Adverse Events
   - https://ctep.cancer.gov/protocoldevelopment/electronic_applications/ctc.htm

2. **ICH E2A** - Clinical Safety Data Management
   - https://www.ich.org/page/efficacy-guidelines

3. **FDA Guidance** - Safety Reporting Requirements for IND and BA/BE Studies
   - https://www.fda.gov/regulatory-information/search-fda-guidance-documents

4. **OMOP CDM** - Observational Medical Outcomes Partnership Common Data Model
   - https://ohdsi.org/data-standardization/

---

## Support & Contact

For questions or issues:

- **GitHub Issues:** https://github.com/cancerbot-org/exactomop/issues
- **Documentation:** https://github.com/cancerbot-org/exactomop
- **Email:** support@exactomop.org

---

**Document Version:** 1.0  
**Last Updated:** October 2025  
**Authors:** EXACTOMOP Development Team

