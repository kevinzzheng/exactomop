# Synthetic Breast Cancer Patient Data

This document describes the synthetic breast cancer patient dataset created for testing the OMOP TreatmentRegimen model with comprehensive non-null constraints.

## Dataset Overview

- **15 synthetic patients** with breast cancer
- **26 treatment regimens** across multiple treatment lines
- **26 treatment lines** (1-3 lines per patient)
- **45 biomarker measurements** (ER, PR, HER2 status)
- **20 OMOP concepts** supporting all referenced data

## Treatment Regimens Included

### Chemotherapy Regimens
- **AC-T**: Doxorubicin + Cyclophosphamide → Docetaxel (8 cycles, 21-day cycles)
- **FEC-T**: Fluorouracil + Epirubicin + Cyclophosphamide → Docetaxel (6 cycles, 21-day cycles)

### Combination Therapy Regimens  
- **TCH**: Docetaxel + Carboplatin + Trastuzumab (6 cycles, 21-day cycles)
- **TCHP**: Docetaxel + Carboplatin + Trastuzumab + Pertuzumab (6 cycles, 21-day cycles)

### Hormone Therapy Regimens
- **Tamoxifen**: Daily oral therapy (60 cycles, 30-day cycles)
- **Anastrozole**: Daily oral therapy (60 cycles, 30-day cycles)

## Breast Cancer Subtypes Represented

1. **Hormone Receptor Positive**: ER+/PR+ cancers
2. **HER2 Positive**: HER2+ cancers (may also be hormone positive)
3. **Triple Negative**: ER-/PR-/HER2- cancers
4. **Hormone Positive + HER2 Positive**: ER+/PR+/HER2+ cancers

## Data Characteristics

### Treatment Lines
- **Line 1**: 15 patients (all patients receive first-line therapy)
- **Line 2**: 8 patients (53% progress to second-line)
- **Line 3**: 3 patients (20% require third-line therapy)

### Treatment Responses
- **Complete Response (CR)**: 19% of regimens
- **Partial Response (PR)**: 46% of regimens  
- **Stable Disease (SD)**: 27% of regimens
- **Progressive Disease (PD)**: 8% of regimens

### Treatment Settings
- **Outpatient**: Most common setting
- **Ambulatory**: Day treatment units
- **Inpatient**: For complex cases

### Treatment Intents
- **Neoadjuvant**: Pre-surgical treatment
- **Adjuvant**: Post-surgical treatment
- **Palliative**: Symptom management
- **Curative**: Intent to cure

## TreatmentRegimen Model Fields Populated

All synthetic TreatmentRegimen entries include complete data for:

### Required Fields (Non-Nullable)
- `regimen_concept_id`: Valid OMOP concept ID
- `regimen_name`: Standard regimen name
- `regimen_code`: Standard abbreviation
- `line_number`: Treatment line (1, 2, or 3)
- `regimen_type`: CHEMOTHERAPY, COMBINATION, HORMONE_THERAPY
- `treatment_intent`: ADJUVANT, NEOADJUVANT, PALLIATIVE, CURATIVE
- `treatment_setting`: OUTPATIENT, INPATIENT, AMBULATORY
- `cycles_planned`: Number of planned treatment cycles
- `cycle_length_days`: Length of each cycle (typically 21 or 30 days)

### Optional Fields (May be Null)
- `regimen_end_date`: Calculated based on cycles completed
- `treatment_line_id`: Links to TreatmentLine record
- `cycles_completed`: May be less than planned due to toxicity/progression
- `best_response`: CR, PR, SD, or PD
- `response_assessment_date`: Typically 60 days after start
- `progression_date`: Only if disease progresses
- `regimen_discontinued`: Boolean flag
- `discontinuation_reason`: COMPLETED, TOXICITY, PROGRESSION, etc.

## Sample Patient Journeys

### Patient 2002 (Multi-line Treatment)
1. **Line 1**: FEC-T → PR response (7/7 cycles completed)
2. **Line 2**: AC-T → PR response (8/9 cycles completed) 
3. **Line 3**: FEC-T → CR response (2/4 cycles completed)

### Patient 2003 (HER2+ with Targeted Therapy)
1. **Line 1**: TCHP → PR response (5/6 cycles completed)
2. **Line 2**: FEC-T → PD response (7/7 cycles completed)
3. **Line 3**: FEC-T → SD response (4/6 cycles completed)

## Loading the Data

Use the Django management command to load the synthetic data:

```bash
# Load data (keeping existing data)
python manage.py load_synthetic_breast_cancer_data

# Clear existing data and load fresh
python manage.py load_synthetic_breast_cancer_data --clear
```

## Validation

All TreatmentRegimen entries have been validated to ensure:
- ✅ All required fields are populated with realistic values
- ✅ Concept IDs reference valid OMOP concepts
- ✅ Treatment sequences follow clinical logic
- ✅ Response patterns are realistic for each regimen type
- ✅ JSON structure is valid and loadable

This synthetic dataset provides comprehensive test data for validating the TreatmentRegimen model with non-null constraints while representing realistic breast cancer treatment patterns.
