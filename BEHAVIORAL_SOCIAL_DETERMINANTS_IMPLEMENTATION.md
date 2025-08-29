# Behavioral, Social Determinants & Demographics Extensions for Comprehensive Patient Care

## Overview
This implementation addresses critical behavioral, social determinants, and demographic factors that are essential for comprehensive patient assessment and care planning. These extensions enable detail# Trial eligibility indexes
CREATE INDEX ON observation (risk_assessment_date);patient profiling while maintaining OMOP CDM compliance.

## Key Patient Assessment Areas Addressed

### Behavioral Factors
- **Smoking Status**: Comprehensive smoking history and cessation tracking
- **Substance Use**: Alcohol and substance use assessment for safety monitoring
- **Reproductive Health**: Contraceptive use and pregnancy status tracking

### Social Determinants
- **Caregiver Support**: Social support system assessment
- **Transportation**: Access to healthcare services
- **Living Situation**: Social environment and support network

### Demographics & Health Status
- **Reproductive Health**: Pregnancy status and menstrual health
- **Infectious Disease**: Disease screening and vaccination status

## Enhanced Choice Classes

### 1. Smoking and Tobacco Use
```python
# SmokingStatusChoices
NEVER_SMOKER = 'never_smoker'
CURRENT_SMOKER = 'current_smoker'
FORMER_SMOKER = 'former_smoker'
PASSIVE_SMOKER = 'passive_smoker'

# TobaccoProductChoices
CIGARETTES = 'cigarettes'
E_CIGARETTES = 'e_cigarettes'
CIGARS = 'cigars'
PIPE = 'pipe'
CHEWING_TOBACCO = 'chewing_tobacco'
```

### 2. Substance Use Assessment
```python
# SubstanceUseChoices
ALCOHOL = 'alcohol'
ILLICIT_DRUGS = 'illicit_drugs'
PRESCRIPTION_MISUSE = 'prescription_misuse'
MARIJUANA = 'marijuana'
OPIOIDS = 'opioids'

# AlcoholUseChoices
NEVER = 'never'
LIGHT = 'light'          # 1-7 drinks/week
MODERATE = 'moderate'    # 8-14 drinks/week
HEAVY = 'heavy'          # > 14 drinks/week
BINGE = 'binge'          # Binge drinking pattern
```

### 3. Reproductive Health
```python
# ContraceptiveMethodChoices
HORMONAL_ORAL = 'hormonal_oral'
HORMONAL_INJECTION = 'hormonal_injection'
IUD_HORMONAL = 'iud_hormonal'
IUD_COPPER = 'iud_copper'
BARRIER_CONDOM = 'barrier_condom'
STERILIZATION = 'sterilization'

# PregnancyStatusChoices
NOT_PREGNANT = 'not_pregnant'
PREGNANT = 'pregnant'
POSSIBLY_PREGNANT = 'possibly_pregnant'
LACTATING = 'lactating'
POSTPARTUM = 'postpartum'

# MenopausalStatusChoices
PREMENOPAUSAL = 'premenopausal'
PERIMENOPAUSAL = 'perimenopausal'
POSTMENOPAUSAL = 'postmenopausal'
POSTMENOPAUSAL_SURGICAL = 'postmenopausal_surgical'
```

### 4. Infectious Disease Status
```python
# InfectiousDiseaseStatusChoices
NEGATIVE = 'negative'
POSITIVE_ACTIVE = 'positive_active'
POSITIVE_TREATED = 'positive_treated'
POSITIVE_CHRONIC = 'positive_chronic'
IMMUNE = 'immune'           # Vaccinated/Natural immunity
```

### 5. Social Support Assessment
```python
# CaregiverStatusChoices
AVAILABLE_FAMILY = 'available_family'
AVAILABLE_PROFESSIONAL = 'available_professional'
LIMITED_SUPPORT = 'limited_support'
NO_CAREGIVER = 'no_caregiver'
SELF_CARE = 'self_care'

# ConsentCapabilityChoices
CAPABLE = 'capable'
IMPAIRED = 'impaired'
GUARDIAN_REQUIRED = 'guardian_required'
FLUCTUATING = 'fluctuating'
```

## Enhanced Observation Model

The OMOP Observation model has been significantly enhanced with behavioral and social determinants fields:

### Smoking and Tobacco Assessment
- `smoking_status`: Current smoking status (SmokingStatusChoices)
- `tobacco_product_type`: Type of tobacco product used
- `pack_years`: Pack-years of smoking history
- `smoking_cessation_date`: Date smoking was stopped

### Substance Use Assessment  
- `substance_use_category`: Category of substance use
- `alcohol_use_level`: Level of alcohol consumption
- `drinks_per_week`: Average drinks per week
- `substance_use_details`: Detailed use patterns

### Reproductive Health Assessment
- `contraceptive_method`: Current contraceptive method
- `pregnancy_status`: Current pregnancy status
- `pregnancy_test_date`: Date of pregnancy test
- `last_menstrual_period`: Date of last menstrual period
- `menopausal_status`: Menopausal status
- `menopause_age`: Age at menopause
- `lactation_status`: Currently breastfeeding

### Infectious Disease Assessment
- `infectious_disease_type`: Type of infectious disease
- `infectious_disease_status`: Disease status
- `infection_test_date`: Date of testing
- `infection_test_result`: Detailed test results
- `vaccination_status`: Vaccination history

### Social Support Assessment
- `caregiver_status`: Caregiver availability and type
- `caregiver_relationship`: Relationship to caregiver
- `social_support_score`: Quantitative support assessment
- `lives_alone`: Patient lives alone
- `transportation_access`: Reliable transportation available

### Cognitive and Mental Health
- `consent_capability`: Capability for informed consent
- `mental_health_status`: Mental health disorder status
- `cognitive_assessment_score`: Cognitive screening scores
- `depression_screening_score`: Depression screening (PHQ-9, etc.)
- `anxiety_screening_score`: Anxiety screening (GAD-7, etc.)

### Geographic and Environmental Factors
- `geographic_risk_category`: Geographic risk exposure type
- `endemic_disease_exposure`: Endemic disease exposure history
- `occupational_exposure`: Occupational hazard exposure
- `environmental_toxin_exposure`: Environmental toxin exposure

### Clinical Trial Eligibility
- `eligible_for_trials`: General trial eligibility
- `contraindication_reason`: Specific exclusion reasons
- `risk_assessment_date`: Date of comprehensive assessment
- `behavioral_data_complete`: Assessment completeness flag

## New Vocabulary Models

### 1. BehavioralVocabulary
Standardizes behavioral observations for clinical trials:

**Key Features**:
- Links behavioral assessments to OMOP concepts
- Maps to LOINC/SNOMED codes
- Tracks clinical relevance and assessment methodologies
- Provides clinical cutoffs and thresholds

**Example Usage**:
```python
smoking_vocab = BehavioralVocabulary.objects.create(
    observation_type='smoking_status',
    observation_name='Smoking History Assessment',
    loinc_code='72166-2',
    clinical_cutoffs={'pack_years_threshold': 10}
)
```

### 2. SocialDeterminantsVocabulary
Maps social factors affecting trial participation:

**Key Features**:
- Categorizes social determinants of health
- Maps to ICD-10 Z-codes for social factors
- Tracks impact on health outcomes and treatment compliance
- Provides intervention options
- Defines health impact levels

**Example Usage**:
```python
caregiver_vocab = SocialDeterminantsVocabulary.objects.create(
    determinant_category='Social Support',
    determinant_name='Caregiver Availability',
    z_code='Z74.1',
    health_impact_level='HIGH'
)
```

### 3. InfectiousDiseaseVocabulary
Standardizes infectious disease assessments:

**Key Features**:
- Maps diseases to ICD-10/SNOMED codes
- Tracks monitoring requirements for patient safety
- Defines standard diagnostic tests
- Provides geographic risk information
- Outlines treatment considerations

**Example Usage**:
```python
hiv_vocab = InfectiousDiseaseVocabulary.objects.create(
    disease_name='Human Immunodeficiency Virus',
    pathogen_type='VIRUS',
    icd10_code='Z21',
    requires_monitoring=True
)
```

## Patient Assessment Examples

### Example 1: Smoking History Assessment
```python
# Assess smoking history for treatment planning
smoking_obs = Observation.objects.filter(
    person=patient,
    behavioral_category='smoking_status'
).first()

if smoking_obs:
    print(f"Smoking status: {smoking_obs.smoking_status}")
    print(f"Pack-years: {smoking_obs.pack_years}")
    if smoking_obs.smoking_cessation_date:
        print(f"Quit date: {smoking_obs.smoking_cessation_date}")
```

### Example 2: Reproductive Health Assessment
```python
# Assess reproductive health status
pregnancy_obs = Observation.objects.filter(
    person=patient,
    behavioral_category='pregnancy_status'
).first()

if pregnancy_obs:
    print(f"Pregnancy status: {pregnancy_obs.pregnancy_status}")
    print(f"Contraceptive method: {pregnancy_obs.contraceptive_method}")
    print(f"Menopausal status: {pregnancy_obs.menopausal_status}")
```

### Example 3: Infectious Disease Screening
```python
# Review infectious disease screening results
infectious_obs = Observation.objects.filter(
    person=patient,
    behavioral_category='infectious_disease'
)

for obs in infectious_obs:
    print(f"{obs.infectious_disease_type}: {obs.infectious_disease_status}")
    print(f"Test date: {obs.infection_test_date}")
```

### Example 4: Social Support Assessment
```python
# Evaluate social support system
caregiver_obs = Observation.objects.filter(
    person=patient,
    behavioral_category='caregiver_status'
).first()

if caregiver_obs:
    print(f"Caregiver status: {caregiver_obs.caregiver_status}")
    print(f"Social support score: {caregiver_obs.social_support_score}")
    print(f"Transportation access: {caregiver_obs.transportation_access}")
```

## Database Indexes for Performance

Comprehensive indexing ensures fast eligibility queries:

```sql
-- Behavioral assessment indexes
CREATE INDEX ON observation (behavioral_category);
CREATE INDEX ON observation (smoking_status);
CREATE INDEX ON observation (substance_use_category);
CREATE INDEX ON observation (alcohol_use_level);

-- Reproductive health indexes
CREATE INDEX ON observation (pregnancy_status);
CREATE INDEX ON observation (menopausal_status);

-- Infectious disease indexes  
CREATE INDEX ON observation (infectious_disease_status);

-- Social determinants indexes
CREATE INDEX ON observation (caregiver_status);
CREATE INDEX ON observation (consent_capability);

-- Trial eligibility indexes
CREATE INDEX ON observation (eligible_for_trials);
CREATE INDEX ON observation (risk_assessment_date);
```

## Clinical Decision Support Features

### Patient Assessment
- Assessment completeness tracking
- Social determinants impact assessment
- Geographic risk evaluation

### Quality Assurance
- Data completeness tracking
- Assessment method validation
- Provider accountability

## Benefits for Patient Care

### 1. Comprehensive Assessment
- Standardized behavioral assessments
- Social determinants evaluation
- Demographic health tracking
- Infectious disease screening

### 2. Care Planning
- Risk factor identification
- Social support evaluation
- Safety monitoring protocols

### 3. Quality Care
- Standardized vocabulary usage
- Assessment completeness tracking
- Provider accountability

### 4. Research Enhancement
- Behavioral data harmonization
- Social determinants research
- Health equity analysis
- Outcome prediction modeling

## Future Enhancements

### Planned Extensions
- **Behavioral Pattern Analysis**: Longitudinal behavioral tracking
- **Social Determinants Interventions**: Intervention tracking and outcomes
- **Geographic Risk Modeling**: Advanced geographic risk assessment
- **Cultural Competency**: Cultural factors affecting healthcare access

### Integration Opportunities
- **Electronic Health Records**: Direct EHR data import
- **Patient-Reported Outcomes**: PRO integration for behavioral assessments
- **Clinical Decision Support**: Real-time assessment alerts
- **Population Health**: Community health monitoring and intervention

This comprehensive implementation transforms behavioral, social determinants, and demographic assessment into a standardized, queryable, and clinically actionable framework within the OMOP CDM, enabling sophisticated patient care while maintaining full OMOP compliance and supporting evidence-based clinical decision making.
