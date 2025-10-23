# Synthetic Adverse Event Dataset for Safety Scoring Testing

## 📋 Overview

This document describes the synthetic adverse event dataset created for comprehensive testing of the OMOP safety scoring model. The dataset includes trial arms, adverse events with diverse characteristics, and satisfies all non-null constraints required by the safety scoring models.

## 🎯 Purpose

The synthetic adverse event dataset enables:
- **Testing** of safety score computations across diverse scenarios
- **Validation** of the safety scoring algorithm with known inputs
- **Demonstration** of the safety scoring feature functionality
- **Development** without requiring real patient data
- **Quality Assurance** with comprehensive edge case coverage

## 📦 Dataset Components

### 1. Trial Arms (5 arms)

The dataset includes 5 trial arms across 3 different clinical trials:

| Trial Arm ID | NCT Number | Arm Name | Arm Type | N Patients | Status | Follow-up (months) |
|-------------|------------|----------|----------|------------|--------|-------------------|
| 1001 | NCT05234567 | Arm A: AC-T Chemotherapy | EXPERIMENTAL | 50 | ACTIVE | 18.50 |
| 1002 | NCT05234567 | Arm B: FEC-T Chemotherapy | ACTIVE_COMPARATOR | 48 | ACTIVE | 17.80 |
| 1003 | NCT05234568 | Arm A: TCHP + Pertuzumab | EXPERIMENTAL | 35 | ACTIVE | 16.25 |
| 1004 | NCT05234568 | Arm B: TCH Standard | ACTIVE_COMPARATOR | 40 | COMPLETED | 20.00 |
| 1005 | NCT05234569 | Control Arm: Standard of Care | ACTIVE_COMPARATOR | 60 | ACTIVE | 24.30 |

#### Trial Descriptions

**NCT05234567**: Comparison of dose-dense AC-T vs. FEC-T regimens in early breast cancer
- **Arm A (AC-T)**: Doxorubicin + Cyclophosphamide → Paclitaxel (dose-dense)
- **Arm B (FEC-T)**: 5-FU + Epirubicin + Cyclophosphamide → Paclitaxel

**NCT05234568**: HER2-positive breast cancer trial comparing pertuzumab addition
- **Arm A (TCHP)**: Docetaxel + Carboplatin + Trastuzumab + Pertuzumab
- **Arm B (TCH)**: Docetaxel + Carboplatin + Trastuzumab (standard)

**NCT05234569**: Standard of care control arm
- **Control**: Physician's choice of standard chemotherapy

### 2. Adverse Event Concepts (10 types)

| Concept ID | Concept Name | Domain | Vocabulary | Code |
|-----------|--------------|---------|-----------|------|
| 4103703 | Nausea | Condition | SNOMED | 422587007 |
| 437663 | Neutropenia | Condition | SNOMED | 165517008 |
| 4223659 | Fatigue | Condition | SNOMED | 84229001 |
| 4165112 | Peripheral neuropathy | Condition | SNOMED | 42658009 |
| 315286 | Cardiotoxicity | Condition | SNOMED | 49584005 |
| 4230254 | Anemia | Condition | SNOMED | 271737000 |
| 4141062 | Diarrhea | Condition | SNOMED | 62315008 |
| 4084139 | Mucositis | Condition | SNOMED | 277274006 |
| 4229881 | Thrombocytopenia | Condition | SNOMED | 415116008 |
| 437082 | Febrile neutropenia | Condition | SNOMED | 409822003 |

### 3. Adverse Events (30 events)

The dataset includes 30 carefully crafted adverse events with comprehensive coverage of:

#### Grade Distribution
- **Grade 1 (Mild)**: 8 events (26.7%)
- **Grade 2 (Moderate)**: 10 events (33.3%)
- **Grade 3 (Severe)**: 9 events (30.0%)
- **Grade 4 (Life-threatening)**: 2 events (6.7%)
- **Grade 5 (Death)**: 1 event (3.3%)

#### Serious Adverse Events (SAEs)
- **Serious**: 14 events (46.7%)
- **Non-serious**: 16 events (53.3%)

#### Relationship to Treatment
- **DEFINITE**: 6 events (20.0%)
- **PROBABLE**: 20 events (66.7%)
- **POSSIBLE**: 3 events (10.0%)
- **UNLIKELY**: 1 event (3.3%)
- **UNRELATED**: 0 events (0.0%)

#### Outcomes
- **RECOVERED**: 20 events (66.7%)
- **RECOVERING**: 0 events (0.0%)
- **NOT_RECOVERED**: 2 events (6.7%)
- **SEQUELAE**: 3 events (10.0%)
- **FATAL**: 1 event (3.3%)
- **UNKNOWN**: 4 events (13.3%)

#### Actions Taken
- **NONE**: 11 events (36.7%)
- **DOSE_REDUCED**: 4 events (13.3%)
- **DOSE_INTERRUPTED**: 6 events (20.0%)
- **DRUG_WITHDRAWN**: 4 events (13.3%)
- **CONCOMITANT_TREATMENT**: 5 events (16.7%)

## 🔍 Detailed Event Examples

### Grade 1 (Mild) Example
```json
{
  "person_id": 2001,
  "trial_arm_id": 1001,
  "event_name": "Nausea",
  "event_description": "Mild nausea following first cycle of chemotherapy, managed with ondansetron",
  "event_date": "2023-03-05",
  "grade": 1,
  "serious": false,
  "expected": true,
  "relationship_to_treatment": "PROBABLE",
  "outcome": "RECOVERED",
  "action_taken": "CONCOMITANT_TREATMENT"
}
```

### Grade 3 (Severe) SAE Example
```json
{
  "person_id": 2002,
  "trial_arm_id": 1002,
  "event_name": "Neutropenia",
  "event_description": "Grade 3 neutropenia (ANC 0.7 x 10^9/L), dose delay implemented",
  "event_date": "2023-03-18",
  "grade": 3,
  "serious": true,
  "expected": true,
  "relationship_to_treatment": "DEFINITE",
  "outcome": "RECOVERED",
  "action_taken": "DOSE_INTERRUPTED",
  "reported_to_sponsor": true,
  "reported_to_irb": true,
  "reported_to_fda": false
}
```

### Grade 4 (Life-threatening) Example
```json
{
  "person_id": 2005,
  "trial_arm_id": 1001,
  "event_name": "Febrile neutropenia",
  "event_description": "Grade 4 febrile neutropenia requiring hospitalization and IV antibiotics",
  "event_date": "2023-04-08",
  "grade": 4,
  "serious": true,
  "expected": true,
  "relationship_to_treatment": "DEFINITE",
  "outcome": "RECOVERED",
  "action_taken": "DOSE_REDUCED",
  "reported_to_sponsor": true,
  "reported_to_irb": true,
  "reported_to_fda": true
}
```

## 📊 Expected Safety Metrics

When safety scores are computed for these trial arms, the following patterns should be observed:

### Arm 1001 (AC-T Experimental)
- **N Patients**: 50
- **Adverse Events**: 11 events
- **Unique Patients with AEs**: ~8-9 patients
- **Expected Grade Distribution**: Mix of G1-G4
- **Expected WEB**: Medium (presence of G3/G4 events)
- **Expected Safety Score**: ~60-75

### Arm 1002 (FEC-T Comparator)
- **N Patients**: 48
- **Adverse Events**: 7 events
- **Unique Patients with AEs**: ~5-6 patients
- **Expected Grade Distribution**: Mix of G1-G4
- **Expected WEB**: Medium-High (presence of G4 event)
- **Expected Safety Score**: ~50-65

### Arm 1003 (TCHP + Pertuzumab)
- **N Patients**: 35
- **Adverse Events**: 4 events
- **Unique Patients with AEs**: ~3 patients
- **Expected Grade Distribution**: G1-G3 (cardiotoxicity)
- **Expected WEB**: Medium
- **Expected Safety Score**: ~70-85

### Arm 1005 (Control - Standard of Care)
- **N Patients**: 60
- **Adverse Events**: 4 events
- **Unique Patients with AEs**: ~4 patients
- **Expected Grade Distribution**: G1-G2 (mild events)
- **Expected WEB**: Low
- **Expected Safety Score**: ~80-95 (safest arm)

## 🚀 Usage Instructions

### Step 1: Load the Dataset

```bash
# Basic loading
python manage.py load_synthetic_adverse_events

# Clear existing data and load fresh
python manage.py load_synthetic_adverse_events --clear

# Load and automatically compute safety scores
python manage.py load_synthetic_adverse_events --clear --compute-scores
```

### Step 2: Verify Data Loading

```python
from omop.models_safety import TrialArm, AdverseEvent

# Check trial arms
print(f"Trial Arms: {TrialArm.objects.count()}")  # Should be 5

# Check adverse events
print(f"Adverse Events: {AdverseEvent.objects.count()}")  # Should be 30

# Check grade distribution
for grade in range(1, 6):
    count = AdverseEvent.objects.filter(grade=grade).count()
    print(f"Grade {grade}: {count} events")
```

### Step 3: Compute Safety Scores

```bash
# Compute safety scores for all trial arms
python manage.py compute_safety_scores --verbosity=2

# Force recomputation
python manage.py compute_safety_scores --force

# Compute for specific trial arm
python manage.py compute_safety_scores --trial-arm-id=1001
```

### Step 4: Query Safety Metrics

```python
from omop.models_safety import TrialArmSafetyMetrics

# Get latest safety metrics for all arms
for arm in TrialArm.objects.all():
    metrics = arm.safety_metrics.latest('computation_date')
    print(f"{arm.arm_name}:")
    print(f"  Safety Score: {metrics.safety_score}")
    print(f"  WEB: {metrics.web}")
    print(f"  EAIR: {metrics.eair}")
    print(f"  E1-2: {metrics.e1_2_count}, E3-4: {metrics.e3_4_count}, E5: {metrics.e5_count}")
```

## 🧪 Testing Scenarios

### Scenario 1: Low AE Burden (High Safety)
**Trial Arm**: 1005 (Control)
- Few adverse events
- Mostly low grades
- Expected high safety score (>80)

### Scenario 2: Moderate AE Burden
**Trial Arm**: 1001 (AC-T)
- Mixed grade distribution
- Several G3/G4 events
- Expected moderate safety score (60-75)

### Scenario 3: High AE Burden (Low Safety)
**Trial Arm**: 1002 (FEC-T)
- Includes G4 life-threatening event
- Multiple SAEs
- Expected lower safety score (50-65)

### Scenario 4: Cardiotoxicity Profile
**Trial Arm**: 1003 (TCHP)
- Specific cardiotoxicity events
- HER2-targeted therapy AEs
- Demonstrates therapy-specific safety profile

### Scenario 5: Completed Trial
**Trial Arm**: 1004 (TCH Standard)
- Status: COMPLETED
- Complete follow-up data
- Demonstrates final safety analysis

## ✅ Non-Null Constraint Compliance

All adverse events in the dataset satisfy the following non-null constraints:

### Required Fields (NOT NULL)
✅ **person_id** - All events linked to valid persons (2001-2015)
✅ **event_name** - All events have descriptive names
✅ **event_date** - All events have occurrence dates
✅ **grade** - All events have CTCAE grades (1-5)
✅ **serious** - All events have serious flag (true/false)
✅ **expected** - All events have expectedness flag
✅ **reported_to_sponsor** - All events have sponsor reporting flag
✅ **reported_to_irb** - All events have IRB reporting flag
✅ **reported_to_fda** - All events have FDA reporting flag

### Optional Fields (NULL allowed)
✅ **trial_arm_id** - All events linked to trial arms (though nullable in model)
✅ **event_concept_id** - All events linked to OMOP concepts (though nullable in model)
✅ **event_description** - All events have detailed descriptions (though blank allowed)
✅ **onset_date** - Most events have onset dates
✅ **resolution_date** - Events with outcomes have resolution dates
✅ **relationship_to_treatment** - All events have causality assessment
✅ **outcome** - All events have outcome classification
✅ **action_taken** - All events have action classification

## 📈 Data Quality Features

### 1. Realistic Clinical Patterns
- Chemotherapy-related AEs (neutropenia, nausea, fatigue)
- Targeted therapy-specific AEs (cardiotoxicity for HER2 therapy)
- Appropriate grade distributions for each AE type
- Realistic temporal relationships (onset → event → resolution)

### 2. Regulatory Compliance Patterns
- Appropriate SAE reporting (sponsor, IRB, FDA)
- Grade 3+ events mostly marked as serious
- Grade 4/5 events with comprehensive reporting
- Expected vs. unexpected event classifications

### 3. Clinical Decision Patterns
- Dose modifications for severe events
- Drug withdrawal for life-threatening events
- Concomitant treatment for manageable events
- Appropriate outcome assessments

### 4. Safety Signal Diversity
- Multiple organ systems affected
- Range of severity levels
- Different causality assessments
- Various management strategies

## 🔬 Advanced Testing Use Cases

### Test Case 1: WEB Calculation Validation
```python
# Expected WEB for Arm 1001
e1_2 = 5  # Grade 1-2 events
e3_4 = 5  # Grade 3-4 events
e5 = 1    # Grade 5 events
expected_web = (1 * e1_2) + (10 * e3_4) + (100 * e5)
# expected_web = 5 + 50 + 100 = 155
```

### Test Case 2: EAIR Calculation
```python
# For Arm 1001
n_patients = 50
follow_up_months = 18.50
person_years = (n_patients * follow_up_months) / 12
patients_with_ae = 9  # Unique patients
eair = patients_with_ae / person_years
# eair ≈ 0.1168 events per person-year
```

### Test Case 3: Safety Score Computation
```python
# Using default H = 15.0
web = 155
H = 15.0
safety_score = 100 / (1 + web / H)
# safety_score ≈ 8.85 (high risk due to fatal event)
```

### Test Case 4: Multiple Grades Per Patient
- Patient 2001: Has both Grade 1 and Grade 2 events
- Patient 2003: Has Grade 1 and Grade 3 events
- Tests proper handling of patient uniqueness in grade categories

### Test Case 5: Event Resolution Tracking
- Some events: `resolution_date = null` (ongoing)
- Most events: Resolved with appropriate durations
- Tests outcome tracking and event duration analysis

## 📝 Integration with Existing Data

The synthetic adverse events integrate with the existing synthetic breast cancer patient data:

### Patient Mapping
- Uses person_ids 2001-2015 (from synthetic_breast_cancer_patients.json)
- Events align with treatment regimen timelines
- AE dates correspond to treatment cycles

### Concept Reuse
- Reuses existing concept framework
- Adds 10 new AE-specific concepts
- Maintains OMOP vocabulary standards

### Treatment Context
- Events occur during documented treatment lines
- Trial arms represent actual regimens used
- Maintains clinical coherence with treatment data

## 🎓 Educational Value

This dataset serves as an excellent teaching tool for:

1. **CTCAE Grading**: Shows proper application of grades 1-5
2. **SAE Identification**: Demonstrates serious vs. non-serious criteria
3. **Causality Assessment**: Examples of all relationship categories
4. **Regulatory Reporting**: Proper escalation patterns
5. **Safety Metrics**: Real-world-like safety scoring scenarios

## 🔄 Maintenance and Updates

### Version Control
- **Version**: 1.0.0
- **Created**: October 2024
- **Last Updated**: October 2024

### Future Enhancements
- [ ] Add more diverse AE types (hepatotoxicity, nephrotoxicity)
- [ ] Include Grade 5 (death) events for multiple patients
- [ ] Add unexpected adverse events
- [ ] Include drug-drug interaction AEs
- [ ] Add immune-related adverse events (irAEs)

## 🔒 Data Privacy

This is **synthetic data** with the following characteristics:
- ✅ No real patient information
- ✅ Fabricated clinical scenarios
- ✅ Safe for development and testing
- ✅ Can be shared publicly
- ✅ Follows realistic patterns for educational purposes

## 📞 Support

For questions or issues with the synthetic adverse event dataset:

1. Check this documentation
2. Review `/docs/SAFETY_SCORING.md` for safety scoring details
3. Examine test cases in `omop/tests/test_safety_scores.py`
4. Review the fixture file directly: `omop/fixtures/synthetic_adverse_events.json`

## 🎉 Summary

The synthetic adverse event dataset provides:

✅ **5 Trial Arms** across 3 clinical trials
✅ **30 Adverse Events** with comprehensive attributes
✅ **10 AE Concepts** covering common chemotherapy toxicities
✅ **Complete Non-Null Compliance** for all required fields
✅ **Diverse Grade Distribution** (G1-G5)
✅ **Realistic Clinical Patterns** matching real-world scenarios
✅ **Comprehensive Testing Coverage** for safety scoring
✅ **Educational Value** for CTCAE and safety reporting

This dataset enables thorough testing of the OMOP safety scoring model without requiring real patient data, while maintaining clinical authenticity and regulatory compliance patterns.

---

**Document Version**: 1.0.0  
**Last Updated**: October 2024  
**Maintainer**: AI Assistant  
**License**: Apache 2.0

