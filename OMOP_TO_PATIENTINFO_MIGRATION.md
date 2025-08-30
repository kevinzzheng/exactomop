# OMOP to PatientInfo Migration Guide

This document describes the data migration script that transforms OMOP CDM data into the PatientInfo model for clinical trial matching and research applications.

## Overview

The `migrate_omop_to_patientinfo` management command extracts data from multiple OMOP tables and consolidates it into a single PatientInfo record per patient. This creates a denormalized, research-friendly view of patient data that's optimized for clinical trial eligibility screening and phenotypic analysis.

## Data Sources and Mappings

### 1. Demographics (Person Table)

| OMOP Field | PatientInfo Field | Mapping Logic |
|------------|-------------------|---------------|
| `year_of_birth` | `patient_age` | Calculated: current_year - birth_year |
| `gender_concept_id` | `gender` | 8532→F, 8507→M, 8521→O, 8551→U |
| `ethnicity_concept_id` | `ethnicity` | 38003563→Hispanic, 38003564→Not Hispanic |
| `primary_language_concept_id` | `languages` | 4182347→en, 4182503→es, etc. |
| `location_id` | `country`, `region`, `postal_code` | From related Location table |

### 2. Disease Information (ConditionOccurrence Table)

| OMOP Field | PatientInfo Field | Mapping Logic |
|------------|-------------------|---------------|
| `primary_site_concept_id` | `disease` | Maps cancer site concepts to disease names |
| `ajcc_clinical_stage` | `stage` | Direct mapping |
| `ajcc_clinical_t_stage` | `tumor_stage` | TNM staging components |
| `ajcc_clinical_n_stage` | `nodes_stage` | TNM staging components |
| `ajcc_clinical_m_stage` | `distant_metastasis_stage` | TNM staging components |
| `estrogen_receptor_status` | `estrogen_receptor_status` | Breast cancer specific |
| `progesterone_receptor_status` | `progesterone_receptor_status` | Breast cancer specific |
| `her2_status` | `her2_status` | Breast cancer specific |

### 3. Laboratory Data (Measurement Table)

Laboratory values are mapped using LOINC codes and measurement names:

| Lab Test | PatientInfo Field | LOINC Codes |
|----------|-------------------|-------------|
| Hemoglobin | `hemoglobin_level` | 718-7, 30313-1 |
| Platelet Count | `platelet_count` | 26515-7, 777-3 |
| White Blood Cell Count | `white_blood_cell_count` | 26464-8, 6690-2 |
| Absolute Neutrophil Count | `absolute_neutrophile_count` | 26499-4, 751-8 |
| Serum Creatinine | `serum_creatinine_level` | 2160-0, 38483-4 |
| Serum Calcium | `serum_calcium_level` | 17861-6, 2000-8 |
| Total Bilirubin | `serum_bilirubin_level_total` | 1975-2, 42719-5 |
| Albumin | `albumin_level` | 1751-7, 61151-7 |
| AST | `liver_enzyme_levels_ast` | 1920-8, 30239-8 |
| ALT | `liver_enzyme_levels_alt` | 1742-6, 16324-6 |
| Weight | `weight` | 29463-7, 3141-9 |
| Height | `height` | 8302-2, 3137-7 |
| Systolic BP | `systolic_blood_pressure` | 8480-6 |
| Diastolic BP | `diastolic_blood_pressure` | 8462-4 |

### 4. Clinical Observations (Observation Table)

| OMOP Field | PatientInfo Field | Mapping Logic |
|------------|-------------------|---------------|
| `performance_score_type=ECOG` | `ecog_performance_status` | Direct numeric value |
| `performance_score_type=KARNOFSKY` | `karnofsky_performance_score` | Direct numeric value |
| `pregnancy_status` | `no_pregnancy_or_lactation_status` | Inverted boolean |
| `menopausal_status` | `menopausal_status` | Direct mapping |
| `infectious_disease_type=HIV` | `hiv_status`, `no_hiv_status` | Status-based mapping |
| `infectious_disease_type=HBV` | `hepatitis_b_status`, `no_hepatitis_b_status` | Status-based mapping |
| `infectious_disease_type=HCV` | `hepatitis_c_status`, `no_hepatitis_c_status` | Status-based mapping |
| `smoking_status` | `no_tobacco_use_status`, `tobacco_use_details` | Status and details |
| `consent_capability` | `consent_capability` | Boolean mapping |
| `mental_health_status` | `no_mental_health_disorder_status` | Inverted boolean |
| `caregiver_status` | `caregiver_availability_status` | Direct mapping |

### 5. Treatment History (TreatmentRegimen and TreatmentLine Tables)

| OMOP Source | PatientInfo Field | Mapping Logic |
|-------------|-------------------|---------------|
| `TreatmentLine.count()` | `therapy_lines_count` | Count of treatment lines |
| Line 1 regimens | `first_line_therapy`, `first_line_date`, `first_line_outcome` | First line data |
| Line 2 regimens | `second_line_therapy`, `second_line_date`, `second_line_outcome` | Second line data |
| Line 3+ regimens | `later_therapy`, `later_date`, `later_outcome` | Later line data |
| All regimens | `prior_therapy` | Concatenated regimen names |
| Latest regimen | `last_treatment` | Most recent end/start date |
| Progression events | `relapse_count` | Count of progression discontinuations |
| Poor responses | `treatment_refractory_status` | Based on response patterns |

### 6. Genomic Data (GenomicVariant and BiomarkerMeasurement Tables)

| OMOP Source | PatientInfo Field | Mapping Logic |
|-------------|-------------------|---------------|
| `GenomicVariant` records | `genetic_mutations` | JSON array of mutation data |
| BRCA1/2, PALB2, ATM variants | `hrd_status` | Pathogenic variants → DEFICIENT |
| PD-L1 biomarker | `pd_l1_tumor_cels`, `pd_l1_assay` | Numeric result and method |
| Ki-67 biomarker | `ki67_proliferation_index` | Numeric result |

### 7. Social and Behavioral Data (SocialDeterminant, HealthBehavior, PsychosocialAssessment)

| OMOP Source | PatientInfo Field | Mapping Logic |
|-------------|-------------------|---------------|
| `SocialDeterminant.housing_status` | `geographic_exposure_risk_details` | Housing information |
| `HealthBehavior.smoking_status` | `no_tobacco_use_status`, `tobacco_use_details` | Smoking data |
| `HealthBehavior.alcohol_use` | `no_substance_use_status`, `substance_use_details` | Alcohol data |
| `PsychosocialAssessment.depression_severity` | `no_mental_health_disorder_status` | Mental health status |

## Usage

### Basic Migration

```bash
# Migrate all persons
python manage.py migrate_omop_to_patientinfo

# Clear existing PatientInfo records first
python manage.py migrate_omop_to_patientinfo --clear

# Migrate specific persons only
python manage.py migrate_omop_to_patientinfo --person-ids 1001,1002,1003

# Dry run to see what would be migrated
python manage.py migrate_omop_to_patientinfo --dry-run
```

### Testing the Migration

```bash
# Run the test script
python test_migration.py

# This will:
# 1. Check for OMOP data availability
# 2. Run a dry-run migration
# 3. Migrate a subset of persons
# 4. Validate the results
```

### Command Options

| Option | Description |
|--------|-------------|
| `--clear` | Delete all existing PatientInfo records before migration |
| `--person-ids` | Comma-separated list of specific person IDs to migrate |
| `--dry-run` | Show what would be migrated without making changes |
| `--verbosity` | Control output verbosity (0=minimal, 1=normal, 2=verbose) |

## Data Quality Considerations

### 1. Missing Data Handling

- The script gracefully handles missing OMOP data
- Fields are only populated when source data exists
- Default values are applied for critical fields (e.g., disease='multiple myeloma')

### 2. Data Validation

- Numeric conversions are wrapped in try/catch blocks
- Boolean mappings handle various input formats
- Date fields use appropriate fallbacks

### 3. Performance Optimization

- Uses `select_related()` and `prefetch_related()` for efficient queries
- Processes records in batches
- Implements database transactions for data consistency

### 4. Error Handling

- Individual person migration errors don't stop the entire process
- Detailed error logging for troubleshooting
- Summary statistics at completion

## Derived Fields

The script calculates several derived fields:

### BMI Calculation
```python
if weight and height:
    # Convert units to metric if necessary
    weight_kg = convert_to_kg(weight, weight_units)
    height_m = convert_to_meters(height, height_units)
    bmi = weight_kg / (height_m ** 2)
```

### Age Calculation
```python
current_year = date.today().year
death_year = person.death_datetime.year if person.death_datetime else None
reference_year = death_year or current_year
age = reference_year - person.year_of_birth
```

## Integration with Clinical Trial Matching

The migrated PatientInfo records are optimized for clinical trial eligibility screening:

1. **Structured Data**: All relevant patient data in a single record
2. **Standardized Values**: Consistent formatting for eligibility checks
3. **Research-Ready**: Includes genomic, biomarker, and social determinant data
4. **Performance**: Fast queries for large patient populations

## Monitoring and Maintenance

### Regular Migration Updates

```bash
# Update PatientInfo for new OMOP data
python manage.py migrate_omop_to_patientinfo --verbosity=2

# Check for data inconsistencies
python manage.py validate_patient_info
```

### Data Quality Checks

After migration, validate:

1. **Completeness**: Check for expected field populations
2. **Consistency**: Verify calculated fields (BMI, age)
3. **Referential Integrity**: Ensure Person↔PatientInfo relationships
4. **Clinical Logic**: Validate medical data relationships

## Troubleshooting

### Common Issues

1. **No OMOP Data**: Load synthetic data first with `load_synthetic_breast_cancer_data`
2. **Permission Errors**: Ensure database write permissions
3. **Memory Issues**: Process in smaller batches using `--person-ids`
4. **Data Type Errors**: Check for unexpected data formats in source tables

### Debug Mode

```bash
# Enable detailed logging
python manage.py migrate_omop_to_patientinfo --verbosity=2 --person-ids 1001

# Check specific person's data
python manage.py shell
>>> from omop.models import Person, PatientInfo
>>> person = Person.objects.get(person_id=1001)
>>> patient_info = PatientInfo.objects.get(person=person)
>>> print(patient_info.__dict__)
```

## Future Enhancements

1. **Real-time Sync**: Trigger PatientInfo updates when OMOP data changes
2. **Delta Updates**: Only migrate changed records
3. **Data Versioning**: Track PatientInfo update history
4. **Custom Mappings**: Configurable field mapping rules
5. **Quality Metrics**: Built-in data quality scoring
