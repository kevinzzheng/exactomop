# Treatment Line Implementation for Comprehensive Treatment Tracking

## Overview
This implementation provides comprehensive treatment line tracking following OHDSI Oncology Working Group principles and Artemis project methodologies. It enables detailed treatment history analysis and therapeutic decision support for oncology care.

## Core Models

### 1. TreatmentLine
**Purpose**: Represents a complete line of therapy for a specific cancer condition.

**Key Features**:
- OHDSI Oncology WG methodology compliance
- Configurable gap thresholds (default: 120 days)
- Combination therapy window settings (default: 30 days)
- Treatment intent tracking (curative, palliative, adjuvant, neoadjuvant)
- Automatic therapy classification (platinum-based, immunotherapy-based, targeted therapy)
- Treatment response tracking

**Example Usage**:
```python
# First-line platinum therapy for breast cancer
treatment_line = TreatmentLine.objects.create(
    person=patient,
    condition_occurrence=breast_cancer_condition,
    line_number=1,
    line_start_date=date(2023, 1, 15),
    treatment_intent='palliative',
    platinum_based=True,
    line_calculation_method='OHDSI_Oncology_WG'
)
```

### 2. TreatmentRegimen
**Purpose**: Tracks detailed regimens within a treatment line (e.g., AC followed by T in adjuvant setting).

**Key Features**:
- Sequential regimen tracking within lines
- Combination therapy identification
- Response assessment integration
- Dose modification tracking

### 3. TreatmentLineComponent
**Purpose**: Links individual drug exposures and procedures to treatment lines and regimens.

**Key Features**:
- Connects OMOP drug_exposure and procedure_occurrence to treatment context
- Drug classification tracking
- Component-level therapy flags (platinum, immunotherapy, targeted)
- Temporal relationship tracking

## OHDSI Methodology Implementation

### Gap Threshold Calculation
The implementation follows OHDSI Oncology WG standards for defining treatment line boundaries:

```python
# Default gap threshold: 120 days
# Configurable per treatment line
gap_threshold_days = 120

# Combination window: treatments starting within 30 days are grouped
combination_window_days = 30
```

### Line Calculation Methods
- `OHDSI_Oncology_WG`: Standard OHDSI methodology
- `Artemis_Project`: Artemis-specific algorithms
- `Institution_Specific`: Custom institutional rules
- `Manual_Review`: Manually curated lines

## Treatment History Analysis Examples

### Example 1: Treatment Line Sequence
```python
# Get all treatment lines for a patient's condition
treatment_lines = TreatmentLine.objects.filter(
    person=patient,
    condition_occurrence=condition
).order_by('line_number')

for line in treatment_lines:
    print(f"Line {line.line_number}: {line.primary_regimen_name}")
    print(f"  Duration: {line.line_start_date} to {line.line_end_date}")
    print(f"  Response: {line.treatment_response}")
```

### Example 2: Drug Classification Analysis
```python
# Analyze platinum exposure history
platinum_exposures = DrugExposure.objects.filter(
    person=patient,
    is_platinum_agent=True
).order_by('drug_exposure_start_date')

for exposure in platinum_exposures:
    print(f"Platinum drug: {exposure.drug_concept.concept_name}")
    print(f"  Treatment Line: {exposure.treatment_line.line_number}")
```

## Database Indexes

The implementation includes comprehensive indexing for optimal query performance:

### DrugExposure Indexes
- `treatment_line`: Fast treatment line lookups
- `drug_classification`: Quick drug class filtering
- `is_platinum_agent`, `is_immunotherapy`, `is_targeted_therapy`: Therapy type queries

### TreatmentLine Indexes
- `person`: Patient-specific queries
- `condition_occurrence`: Condition-specific treatment history
- `line_number`: Sequential line access
- `treatment_intent`: Intent-based filtering
- Therapy type flags for quick classification

## Admin Interface

Complete Django admin interface provided for:
- Treatment line management and review
- Regimen tracking and modification
- Component-level drug/procedure linking

## Integration with Existing OMOP Models

The treatment line implementation seamlessly integrates with existing OMOP models:

### Core OMOP Integration
- **Person**: Patient identification and demographics
- **Condition_Occurrence**: Cancer diagnoses and staging
- **Drug_Exposure**: Enhanced with treatment context
- **Procedure_Occurrence**: Surgical and radiation therapies
- **Measurement**: Response assessments and biomarkers

### Oncology Extension Integration
- **Episode**: Treatment episodes and care phases
- **Episode_Event**: Linking treatments to episodes

## OHDSI Compliance

This implementation maintains full OHDSI compliance while extending functionality:

### Standard Vocabularies
- Uses OMOP standard concepts for all classifications
- Maintains concept_id relationships throughout
- Supports custom concept mapping for institutional needs

### Data Provenance
- Tracks calculation methodology for each treatment line
- Maintains audit trail for treatment decisions
- Supports both automated and manual review workflows

## Future Enhancements

Planned enhancements for future releases:

### Advanced Analytics
- Treatment pattern analysis
- Response prediction modeling
- Survival outcome integration

### Clinical Decision Support
- Treatment recommendation engines
- Guideline compliance checking

### External System Integration
- EMR treatment plan import
- Clinical trial management system integration
- Regulatory reporting support

## Usage in Clinical Care

This implementation enables sophisticated treatment history analysis and clinical decision support:

### Treatment History Analysis
1. **Treatment Sequence Tracking**:
   - Complete treatment line progression
   - Response patterns across lines
   - Treatment duration and gaps

2. **Drug Classification Analysis**:
   - Platinum exposure history
   - Immunotherapy experience
   - Targeted therapy patterns

3. **Response Assessment**:
   - Treatment effectiveness tracking
   - Duration of response analysis
   - Progression patterns

### Performance Optimization
- Indexed fields enable fast treatment history queries
- Materialized views for complex treatment analytics
- Optimized queries for longitudinal analysis

This comprehensive treatment line implementation provides the foundation for sophisticated treatment history analysis and clinical decision support while maintaining full OMOP CDM compliance and following established OHDSI methodologies.
