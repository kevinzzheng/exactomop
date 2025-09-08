# Exact-OMOP

An extended OMOP (Observational Medical Outcomes Partnership) Common Data Model implementation specifically designed for comprehensive cancer research and clinical trial matching. This system extends the standard OMOP CDM with specialized oncology models to support precision medicine initiatives.

## 🎯 OMOP Extension Categories

Exact-OMOP extends the standard OMOP CDM and the standard OMOP Oncology Extension with four major categories of cancer-specific enhancements:

### 🧪 **Labs & Biomarkers Extensions**
Comprehensive laboratory and biomarker data integration for precision oncology:
- **Enhanced Measurement Model**: Extended with cancer-specific biomarker fields
- **Biomarker Measurement Model**: Dedicated biomarker tracking with actionability
- **Molecular Test Model**: Standardized molecular diagnostic test results
- **Biospecimen Collection Model**: Research-grade sample lifecycle management

### 🧬 **Genomics Extensions** 
Advanced genomic and molecular profiling capabilities:
- **Genomic Variant Model**: Comprehensive variant annotation and clinical significance
- **Mutation Tracking**: Temporal mutation evolution and acquired resistance
- **Multi-Platform Support**: NGS, PCR, FISH, IHC data integration
- **Actionability Framework**: Direct links to targeted therapy recommendations

### 💊 **Treatment Lines & Regimens Extensions**
Sophisticated treatment sequencing and outcome tracking:
- **Treatment Regimen Model**: Multi-drug protocol management with enforced data quality
- **Treatment Line Model**: Sequential therapy progression tracking
- **Treatment Line Eligibility Model**: Complex multi-criteria eligibility assessment
- **Clinical Trial Integration**: Seamless trial matching and enrollment tracking

### 🏥 **Behavioral & Social Determinants Extensions**
Comprehensive social and behavioral health factor integration:
- **Social Determinants Model**: Housing, food security, access barriers
- **Behavioral Factors Model**: Lifestyle, substance use, health behaviors
- **Psychosocial Assessment**: Mental health, social support networks
- **Health Equity Metrics**: Disparities tracking and intervention monitoring

---

## 🧪 Labs & Biomarkers Extensions

### Enhanced Measurement Model
Extended the core OMOP Measurement table with cancer-specific biomarker fields:

#### **Immunohistochemistry (IHC) Fields**
```sql
-- Standardized IHC scoring methods
ihc_score                VARCHAR(20)    -- 0, 1+, 2+, 3+ intensity
percent_positive_cells   DECIMAL(5,2)   -- Percentage of positive cells (0-100)
allred_proportion       INTEGER         -- Allred proportion score (0-5)
allred_intensity        INTEGER         -- Allred intensity score (0-3)  
allred_total            INTEGER         -- Combined Allred score (0-8)
h_score                 INTEGER         -- H-score calculation (0-300)
```

#### **Protein Expression Analysis**
```sql
-- Quantitative protein measurements
expression_level        VARCHAR(20)    -- HIGH, MODERATE, LOW, ABSENT
pdl1_tumor_proportion_score    DECIMAL(5,2)   -- PD-L1 TPS (0-100)
pdl1_combined_positive_score   DECIMAL(5,2)   -- PD-L1 CPS (0-100)
pdl1_immune_cell_score         DECIMAL(5,2)   -- PD-L1 IC score (0-100)
```

#### **FISH Analysis**
```sql
-- Fluorescence in situ hybridization
fish_ratio              DECIMAL(8,4)   -- Signal ratio (e.g., HER2/CEP17)
fish_signal_count       INTEGER        -- Average signal count per cell
fish_interpretation     VARCHAR(50)    -- POSITIVE, NEGATIVE, EQUIVOCAL
```

#### **Tumor Microenvironment**
```sql
-- Immune infiltration metrics
til_percentage          DECIMAL(5,2)   -- Tumor-infiltrating lymphocytes %
til_density            VARCHAR(20)    -- HIGH, MODERATE, LOW, ABSENT
```

#### **Genomic Instability Markers**
```sql
-- Homologous recombination deficiency
hrd_score              INTEGER         -- HRD score (0-100)
hrd_status             VARCHAR(20)     -- DEFICIENT, PROFICIENT, UNKNOWN

-- Microsatellite instability
msi_status             VARCHAR(20)     -- MSI-HIGH, MSI-LOW, MSS, UNKNOWN

-- Tumor mutational burden
tmb_score              DECIMAL(8,2)    -- Mutations per megabase
tmb_status             VARCHAR(20)     -- HIGH, INTERMEDIATE, LOW
```

#### **Circulating Tumor DNA (ctDNA)**
```sql
-- Liquid biopsy measurements
ctdna_detected         BOOLEAN         -- ctDNA presence
ctdna_allele_frequency DECIMAL(8,4)    -- Variant allele frequency
ctdna_copy_number      DECIMAL(8,2)    -- Copy number variations
```

### Biomarker Measurement Model
Dedicated tracking for actionable biomarkers with clinical decision support:

```python
class BiomarkerMeasurement(models.Model):
    # Core measurement link
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    # Biomarker classification
    biomarker_category = models.CharField(max_length=20, choices=BiomarkerCategoryChoices.choices)
    biomarker_name = models.CharField(max_length=100)
    
    # Clinical actionability
    actionable_status = models.CharField(max_length=30, choices=[
        ('FDA_APPROVED', 'FDA Approved Indication'),
        ('GUIDELINE_RECOMMENDED', 'Guideline Recommended'), 
        ('INVESTIGATIONAL', 'Investigational/Clinical Trial'),
        ('NOT_ACTIONABLE', 'Not Currently Actionable')
    ])
    
    # Associated therapies
    targeted_therapies = models.TextField(blank=True)  # JSON list of drugs
    resistance_mechanisms = models.TextField(blank=True)
    
    # Temporal tracking
    measurement_date = models.DateField()
    test_method = models.CharField(max_length=50)
    laboratory_name = models.CharField(max_length=100)
```

### Molecular Test Model
Standardized molecular diagnostic test management:

```python
class MolecularTest(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    # Test identification
    test_name = models.CharField(max_length=100)
    test_type = models.CharField(max_length=30, choices=[
        ('NGS_PANEL', 'Next Generation Sequencing Panel'),
        ('PCR', 'Polymerase Chain Reaction'),
        ('FISH', 'Fluorescence In Situ Hybridization'),
        ('IHC', 'Immunohistochemistry'),
        ('FLOW_CYTOMETRY', 'Flow Cytometry'),
        ('KARYOTYPE', 'Karyotype Analysis')
    ])
    
    # Platform details
    platform_name = models.CharField(max_length=100)
    panel_version = models.CharField(max_length=50)
    genes_tested = models.TextField()  # JSON list of genes
    
    # Quality metrics
    sample_type = models.CharField(max_length=50)
    sample_quality = models.CharField(max_length=20)
    coverage_metrics = models.TextField(blank=True)  # JSON quality data
    
    # Results and interpretation
    test_result = models.TextField()  # Structured or unstructured results
    clinical_interpretation = models.TextField()
    variants_detected = models.IntegerField(default=0)
```

### Biospecimen Collection Model
Research-grade sample lifecycle management:

```python
class BiospecimenCollection(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    # Sample identification
    specimen_id = models.CharField(max_length=50, unique=True)
    parent_specimen_id = models.CharField(max_length=50, blank=True)
    
    # Collection details
    collection_date = models.DateTimeField()
    collection_method = models.CharField(max_length=50)
    anatomical_site = models.CharField(max_length=100)
    
    # Sample characteristics
    specimen_type = models.CharField(max_length=50, choices=[
        ('BLOOD', 'Whole Blood'),
        ('PLASMA', 'Plasma'),
        ('SERUM', 'Serum'),
        ('TISSUE_FRESH', 'Fresh Tissue'),
        ('TISSUE_FFPE', 'FFPE Tissue'),
        ('URINE', 'Urine'),
        ('CSF', 'Cerebrospinal Fluid'),
        ('SALIVA', 'Saliva')
    ])
    
    # Processing and storage
    processing_date = models.DateTimeField(null=True)
    storage_temperature = models.CharField(max_length=20)
    biobank_id = models.CharField(max_length=50)
    
    # Quality and research use
    sample_quality = models.CharField(max_length=20)
    research_consented = models.BooleanField(default=False)
```

---

## 🧬 Genomics Extensions

### Genomic Variant Model
Comprehensive variant annotation with clinical significance tracking:

```python
class GenomicVariant(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    observation = models.ForeignKey(Observation, null=True, on_delete=models.SET_NULL)
    
    # Variant identification
    gene_symbol = models.CharField(max_length=20)  # HUGO nomenclature
    chromosome = models.CharField(max_length=2)
    position_start = models.BigIntegerField()
    position_end = models.BigIntegerField()
    
    # Variant details
    variant_type = models.CharField(max_length=20, choices=[
        ('SNV', 'Single Nucleotide Variant'),
        ('INDEL', 'Insertion/Deletion'),
        ('CNV', 'Copy Number Variant'),
        ('FUSION', 'Gene Fusion'),
        ('REARRANGEMENT', 'Chromosomal Rearrangement'),
        ('SV', 'Structural Variant')
    ])
    
    # Nomenclature
    hgvs_genomic = models.CharField(max_length=200)    # g.notation
    hgvs_coding = models.CharField(max_length=200)     # c.notation  
    hgvs_protein = models.CharField(max_length=200)    # p.notation
    
    # Clinical significance
    clinical_significance = models.CharField(max_length=30, choices=[
        ('PATHOGENIC', 'Pathogenic'),
        ('LIKELY_PATHOGENIC', 'Likely Pathogenic'),
        ('VUS', 'Variant of Uncertain Significance'),
        ('LIKELY_BENIGN', 'Likely Benign'),
        ('BENIGN', 'Benign')
    ])
    
    # Actionability
    actionable_status = models.CharField(max_length=30, choices=[
        ('FDA_APPROVED', 'FDA Approved Biomarker'),
        ('GUIDELINE_RECOMMENDED', 'Guideline Recommended'),
        ('INVESTIGATIONAL', 'Investigational'),
        ('NOT_ACTIONABLE', 'Not Currently Actionable')
    ])
    
    # Quantitative metrics
    allele_frequency = models.DecimalField(max_digits=8, decimal_places=4)
    read_depth = models.IntegerField(null=True)
    copy_number = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    
    # Biomarker status for matching
    biomarker_status = models.CharField(max_length=20, choices=[
        ('POSITIVE', 'Biomarker Positive'),
        ('NEGATIVE', 'Biomarker Negative'), 
        ('HIGH', 'High Expression/Level'),
        ('LOW', 'Low Expression/Level'),
        ('UNKNOWN', 'Unknown/Not Tested')
    ])
    
    # Resistance and evolution
    resistance_mechanism = models.CharField(max_length=100, blank=True)
    acquisition_timing = models.CharField(max_length=20, choices=[
        ('GERMLINE', 'Germline'),
        ('SOMATIC_PRIMARY', 'Somatic - Primary Tumor'),
        ('SOMATIC_ACQUIRED', 'Somatic - Acquired Resistance'),
        ('UNKNOWN', 'Unknown Timing')
    ])
```

### Multi-Platform Integration Support

#### **Next Generation Sequencing (NGS)**
- Comprehensive panel testing (Foundation Medicine, Guardant360, etc.)
- Whole exome/genome sequencing integration
- Tumor-normal paired analysis
- Liquid biopsy ctDNA analysis

#### **Targeted Testing Platforms** 
- PCR-based hotspot testing
- Real-time PCR quantification
- Droplet digital PCR (ddPCR)
- Single-gene FISH analysis

#### **Protein-Based Testing**
- Immunohistochemistry integration
- Flow cytometry results
- Mass spectrometry proteomics
- Western blot validation

---

## 💊 Treatment Lines & Regimens Extensions

### Treatment Regimen Model
Comprehensive multi-drug treatment protocol management with enforced data quality:

```python
class TreatmentRegimen(models.Model):
    regimen_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    # OMOP vocabulary integration (REQUIRED)
    regimen_concept = models.ForeignKey(Concept, on_delete=models.PROTECT)
    
    # Regimen identification (REQUIRED)
    regimen_name = models.CharField(max_length=200)      # e.g., "FOLFOX", "TCH"
    regimen_code = models.CharField(max_length=50)       # Standard abbreviation
    
    # Timing (REQUIRED)
    regimen_start_date = models.DateField()
    regimen_end_date = models.DateField(null=True, blank=True)
    
    # Treatment line context (REQUIRED)
    treatment_line = models.ForeignKey('TreatmentLine', null=True, on_delete=models.SET_NULL)
    line_number = models.IntegerField()                  # 1, 2, 3, etc.
    
    # Regimen characteristics (REQUIRED)
    regimen_type = models.CharField(max_length=30, choices=[
        ('CHEMOTHERAPY', 'Chemotherapy'),
        ('IMMUNOTHERAPY', 'Immunotherapy'), 
        ('TARGETED_THERAPY', 'Targeted Therapy'),
        ('HORMONE_THERAPY', 'Hormone Therapy'),
        ('COMBINATION', 'Combination Therapy'),
        ('MAINTENANCE', 'Maintenance Therapy')
    ])
    
    # Intent and setting (REQUIRED)
    treatment_intent = models.CharField(max_length=30, choices=[
        ('CURATIVE', 'Curative'),
        ('PALLIATIVE', 'Palliative'),
        ('ADJUVANT', 'Adjuvant'),
        ('NEOADJUVANT', 'Neoadjuvant'),
        ('MAINTENANCE', 'Maintenance')
    ])
    
    treatment_setting = models.CharField(max_length=20, choices=[
        ('INPATIENT', 'Inpatient'),
        ('OUTPATIENT', 'Outpatient'),
        ('AMBULATORY', 'Ambulatory')
    ])
    
    # Cycle management (REQUIRED)
    cycles_planned = models.IntegerField()               # Expected cycles
    cycles_completed = models.IntegerField(null=True)   # Actual cycles
    cycle_length_days = models.IntegerField()           # 14, 21, 28 days typical
    
    # Response assessment
    best_response = models.CharField(max_length=20, choices=[
        ('CR', 'Complete Response'),
        ('PR', 'Partial Response'), 
        ('SD', 'Stable Disease'),
        ('PD', 'Progressive Disease'),
        ('NE', 'Not Evaluable'),
        ('MR', 'Mixed Response')
    ], blank=True)
    
    response_assessment_date = models.DateField(null=True)
    progression_date = models.DateField(null=True)
    
    # Discontinuation tracking
    regimen_discontinued = models.BooleanField(default=False)
    discontinuation_reason = models.CharField(max_length=50, choices=[
        ('COMPLETED', 'Completed as Planned'),
        ('PROGRESSION', 'Disease Progression'),
        ('TOXICITY', 'Unacceptable Toxicity'),
        ('PATIENT_CHOICE', 'Patient Choice'),
        ('DEATH', 'Death'),
        ('OTHER', 'Other Reason')
    ], blank=True)
    
    # Clinical trial integration
    clinical_trial = models.ForeignKey('ClinicalTrial', null=True, on_delete=models.SET_NULL)
```

### Treatment Line Model
Sequential therapy management for complex cancer treatment journeys:

```python
class TreatmentLine(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    # Line identification
    line_number = models.IntegerField()                  # 1st, 2nd, 3rd line, etc.
    line_start_date = models.DateField()
    line_end_date = models.DateField(null=True)
    
    # Line characteristics
    line_type = models.CharField(max_length=20, choices=[
        ('FIRST_LINE', 'First-line Therapy'),
        ('SECOND_LINE', 'Second-line Therapy'),
        ('THIRD_LINE', 'Third-line Therapy'),
        ('FOURTH_PLUS', 'Fourth-line or Later'),
        ('MAINTENANCE', 'Maintenance Therapy'),
        ('SALVAGE', 'Salvage Therapy')
    ])
    
    # Clinical context
    treatment_intent = models.CharField(max_length=30)
    performance_status = models.CharField(max_length=20)
    disease_status_start = models.CharField(max_length=30)
    
    # Outcomes
    best_response = models.CharField(max_length=20)
    progression_date = models.DateField(null=True)
    progression_type = models.CharField(max_length=30, null=True)
    
    # Next line rationale
    line_end_reason = models.CharField(max_length=50, choices=[
        ('COMPLETED', 'Treatment Completed'),
        ('PROGRESSION', 'Disease Progression'),
        ('TOXICITY', 'Unacceptable Toxicity'),
        ('PATIENT_CHOICE', 'Patient/Family Choice'),
        ('DEATH', 'Patient Death'),
        ('LOST_FOLLOWUP', 'Lost to Follow-up')
    ])
```

### Treatment Line Eligibility Model
Complex multi-criteria eligibility assessment framework:

```python
class TreatmentLineEligibility(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    treatment_line = models.ForeignKey(TreatmentLine, on_delete=models.CASCADE)
    
    # Eligibility assessment
    assessment_date = models.DateField()
    overall_eligible = models.BooleanField()
    
    # Performance status criteria
    ecog_performance_status = models.IntegerField(null=True)
    karnofsky_score = models.IntegerField(null=True)
    
    # Laboratory criteria
    adequate_organ_function = models.BooleanField(default=True)
    hemoglobin_adequate = models.BooleanField(default=True)
    platelet_count_adequate = models.BooleanField(default=True)
    liver_function_adequate = models.BooleanField(default=True)
    renal_function_adequate = models.BooleanField(default=True)
    
    # Disease-specific criteria
    measurable_disease = models.BooleanField(null=True)
    prior_therapy_count = models.IntegerField(default=0)
    radiation_washout_period = models.BooleanField(default=True)
    
    # Biomarker requirements
    required_biomarkers_present = models.BooleanField(null=True)
    excluding_biomarkers_absent = models.BooleanField(null=True)
    
    # Exclusion criteria
    active_infection = models.BooleanField(default=False)
    pregnant_or_nursing = models.BooleanField(default=False)
    uncontrolled_comorbidities = models.BooleanField(default=False)
    
    # Eligibility reasoning
    eligibility_details = models.TextField(blank=True)
    exclusion_reasons = models.TextField(blank=True)
```

### Clinical Trial Integration

```python
class ClinicalTrial(models.Model):
    # Trial identification
    nct_number = models.CharField(max_length=20, unique=True)
    official_title = models.TextField()
    protocol_number = models.CharField(max_length=50)
    
    # Trial characteristics
    trial_phase = models.CharField(max_length=20)
    trial_type = models.CharField(max_length=30)
    primary_purpose = models.CharField(max_length=30)
    
    # Status and timeline
    overall_status = models.CharField(max_length=30)
    enrollment_start_date = models.DateField(null=True)
    enrollment_end_date = models.DateField(null=True)
    
    # Population
    target_enrollment = models.IntegerField(null=True)
    cancer_types = models.TextField()  # JSON list
    
    # Eligibility criteria
    inclusion_criteria = models.TextField()
    exclusion_criteria = models.TextField()
    biomarker_requirements = models.TextField(blank=True)
    
    # Intervention details
    intervention_type = models.CharField(max_length=30)
    investigational_agents = models.TextField(blank=True)
    control_arm_description = models.TextField(blank=True)
```

---

## 🏥 Behavioral & Social Determinants Extensions

### Social Determinants Tracking

#### **Core Social Determinants Model**
```python
class SocialDeterminant(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    # Assessment details
    assessment_date = models.DateField()
    assessment_method = models.CharField(max_length=50)
    
    # Socioeconomic factors
    annual_household_income = models.CharField(max_length=20, choices=[
        ('UNDER_25K', 'Under $25,000'),
        ('25K_50K', '$25,000 - $50,000'),
        ('50K_75K', '$50,000 - $75,000'),
        ('75K_100K', '$75,000 - $100,000'),
        ('OVER_100K', 'Over $100,000'),
        ('DECLINED', 'Declined to Answer')
    ])
    
    education_level = models.CharField(max_length=30, choices=[
        ('LESS_THAN_HS', 'Less than High School'),
        ('HIGH_SCHOOL', 'High School Graduate'),
        ('SOME_COLLEGE', 'Some College'),
        ('COLLEGE_GRADUATE', 'College Graduate'),
        ('GRADUATE_DEGREE', 'Graduate Degree')
    ])
    
    employment_status = models.CharField(max_length=30, choices=[
        ('EMPLOYED_FULL', 'Employed Full-time'),
        ('EMPLOYED_PART', 'Employed Part-time'),
        ('UNEMPLOYED', 'Unemployed'),
        ('RETIRED', 'Retired'),
        ('DISABLED', 'Disabled'),
        ('STUDENT', 'Student')
    ])
    
    # Housing and environment
    housing_status = models.CharField(max_length=30, choices=[
        ('OWNS_HOME', 'Owns Home'),
        ('RENTS', 'Rents'),
        ('LIVES_WITH_FAMILY', 'Lives with Family/Friends'),
        ('HOMELESS', 'Homeless'),
        ('ASSISTED_LIVING', 'Assisted Living'),
        ('NURSING_HOME', 'Nursing Home')
    ])
    
    housing_quality = models.CharField(max_length=20, choices=[
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor')
    ])
    
    neighborhood_safety = models.CharField(max_length=20, choices=[
        ('VERY_SAFE', 'Very Safe'),
        ('SAFE', 'Safe'),
        ('SOMEWHAT_SAFE', 'Somewhat Safe'),
        ('UNSAFE', 'Unsafe')
    ])
    
    # Access to care
    health_insurance_status = models.CharField(max_length=30, choices=[
        ('PRIVATE', 'Private Insurance'),
        ('MEDICARE', 'Medicare'),
        ('MEDICAID', 'Medicaid'),
        ('UNINSURED', 'Uninsured'),
        ('OTHER_GOVERNMENT', 'Other Government'),
        ('MULTIPLE', 'Multiple Types')
    ])
    
    transportation_barriers = models.BooleanField(default=False)
    distance_to_care_miles = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    
    # Food security
    food_security_status = models.CharField(max_length=20, choices=[
        ('SECURE', 'Food Secure'),
        ('INSECURE_LOW', 'Low Food Security'),
        ('INSECURE_VERY_LOW', 'Very Low Food Security')
    ])
    
    # Social support
    social_support_score = models.IntegerField(null=True)  # 0-100 scale
    lives_alone = models.BooleanField(null=True)
    primary_caregiver_available = models.BooleanField(null=True)
```

### Behavioral Health Factors

#### **Health Behaviors Model**
```python
class HealthBehavior(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    assessment_date = models.DateField()
    
    # Tobacco use
    smoking_status = models.CharField(max_length=20, choices=[
        ('NEVER', 'Never Smoker'),
        ('FORMER', 'Former Smoker'),
        ('CURRENT', 'Current Smoker'),
        ('UNKNOWN', 'Unknown')
    ])
    pack_years = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    quit_date = models.DateField(null=True)
    
    # Alcohol use
    alcohol_use = models.CharField(max_length=20, choices=[
        ('NEVER', 'Never'),
        ('RARE', 'Rarely'),
        ('MODERATE', 'Moderate'),
        ('HEAVY', 'Heavy'),
        ('FORMER', 'Former User')
    ])
    drinks_per_week = models.IntegerField(null=True)
    
    # Physical activity
    exercise_frequency = models.CharField(max_length=20, choices=[
        ('NONE', 'No Regular Exercise'),
        ('LIGHT', 'Light Exercise'),
        ('MODERATE', 'Moderate Exercise'),
        ('VIGOROUS', 'Vigorous Exercise')
    ])
    minutes_per_week = models.IntegerField(null=True)
    
    # Diet and nutrition
    diet_quality = models.CharField(max_length=20, choices=[
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor')
    ])
    
    # Sleep patterns
    sleep_hours_per_night = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    sleep_quality = models.CharField(max_length=20, choices=[
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor')
    ])
    
    # Substance use
    illicit_drug_use = models.BooleanField(default=False)
    prescription_drug_misuse = models.BooleanField(default=False)
```

#### **Psychosocial Assessment Model**
```python
class PsychosocialAssessment(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    assessment_date = models.DateField()
    assessment_tool = models.CharField(max_length=50)  # PHQ-9, GAD-7, etc.
    
    # Mental health screening
    depression_score = models.IntegerField(null=True)
    depression_severity = models.CharField(max_length=20, choices=[
        ('NONE', 'None'),
        ('MILD', 'Mild'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe')
    ])
    
    anxiety_score = models.IntegerField(null=True)
    anxiety_severity = models.CharField(max_length=20, choices=[
        ('NONE', 'None'),
        ('MILD', 'Mild'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe')
    ])
    
    # Distress and coping
    distress_thermometer_score = models.IntegerField(null=True)  # 0-10 scale
    coping_strategies = models.TextField(blank=True)
    
    # Mental health treatment
    current_mental_health_treatment = models.BooleanField(default=False)
    psychiatric_medications = models.BooleanField(default=False)
    counseling_or_therapy = models.BooleanField(default=False)
    
    # Social factors
    relationship_status = models.CharField(max_length=20, choices=[
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('PARTNERED', 'Partnered'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed')
    ])
    
    social_isolation_risk = models.CharField(max_length=20, choices=[
        ('LOW', 'Low Risk'),
        ('MODERATE', 'Moderate Risk'),
        ('HIGH', 'High Risk')
    ])
    
    # Spiritual and cultural factors
    religious_affiliation = models.CharField(max_length=50, blank=True)
    spiritual_coping = models.BooleanField(null=True)
    cultural_considerations = models.TextField(blank=True)
```

### Health Equity and Disparities Tracking

#### **Health Equity Metrics Model**
```python
class HealthEquityMetric(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    assessment_date = models.DateField()
    
    # Access barriers
    financial_barriers = models.BooleanField(default=False)
    geographic_barriers = models.BooleanField(default=False)
    language_barriers = models.BooleanField(default=False)
    cultural_barriers = models.BooleanField(default=False)
    
    # Discrimination experiences
    healthcare_discrimination = models.BooleanField(default=False)
    discrimination_type = models.CharField(max_length=50, blank=True)
    
    # Quality measures
    care_coordination_score = models.IntegerField(null=True)  # 0-100 scale
    patient_satisfaction_score = models.IntegerField(null=True)
    
    # Intervention tracking
    social_services_referral = models.BooleanField(default=False)
    community_resources_connected = models.TextField(blank=True)
    intervention_effectiveness = models.CharField(max_length=20, blank=True)
```

---

## 🔬 Synthetic Test Data

### Breast Cancer Dataset
Comprehensive synthetic dataset for testing and development:
- **15 synthetic patients** with diverse demographics and cancer subtypes
- **26 treatment regimens** representing real-world treatment patterns
- **Multiple treatment lines** showing disease progression and treatment evolution
- **Complete biomarker profiles** (ER, PR, HER2 status)
- **Realistic outcomes** with appropriate response rates

**Treatment Regimens Included:**
- **TCH/TCHP**: HER2-targeted combination therapy
- **AC-T/FEC-T**: Sequential chemotherapy protocols
- **Hormone Therapy**: Tamoxifen, Anastrozole for HR+ disease
- **Multi-line Progressions**: Real-world treatment sequences

Load synthetic data:
```bash
python manage.py load_synthetic_breast_cancer_data --clear
```

## 📊 Data Quality & Standards

### OMOP Vocabulary Integration
- **Standard Concepts**: Full integration with OMOP standardized vocabularies
- **Custom Extensions**: Cancer-specific vocabularies (HemOnc, ICDO-3)
- **Mapping Support**: Source-to-standard concept mapping
- **Version Control**: Vocabulary versioning and update management

### Data Validation
- **Referential Integrity**: Enforced foreign key relationships
- **Business Rules**: Cancer-specific validation logic
- **Temporal Consistency**: Date validation and sequence checking
- **Completeness Checks**: Required field validation

### Performance Optimization
- **Strategic Indexing**: Query-optimized database indexes
- **Denormalization**: Performance-critical derived fields
- **Caching**: Intelligent query result caching
- **Partitioning**: Date-based table partitioning for large datasets

## 🚀 Quickstart Setup
Be sure setenv.sh has DATABASE_URL set (export DATABASE_URL=<URL to postgres>)
```bash
source setenv.sh 
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run migrations & start
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Load synthetic test data (optional)
python manage.py load_synthetic_breast_cancer_data

# Start development server
python manage.py runserver
```
Visit http://127.0.0.1:8000/ for the browser and /admin/ for Django admin.

## 📁 Project Structure

```
exactomop/
├── omop/                           # Main OMOP application
│   ├── models.py                   # Extended OMOP data models
│   ├── views.py                    # API and web interface
│   ├── admin.py                    # Django admin configuration
│   ├── urls.py                     # URL routing
│   ├── fixtures/                   # Test data and examples
│   │   ├── breast_cancer_patients.json              # Original test dataset
│   │   └── synthetic_breast_cancer_patients.json    # Comprehensive synthetic data
│   ├── management/commands/        # Data loading and maintenance utilities
│   │   ├── load_breast_cancer_data.py               # Load original fixtures
│   │   ├── load_synthetic_breast_cancer_data.py     # Load synthetic dataset
│   │   ├── populate_patient_info.py                 # Generate patient data
│   │   ├── cleanup_patient_info.py                  # Data cleanup utilities
│   │   ├── update_patient_info.py                   # Update existing records
│   │   └── validate_patient_info.py                 # Data validation
│   ├── migrations/                 # Database schema evolution
│   ├── templates/                  # Web interface templates
│   └── templatetags/               # Custom template helpers
├── omop_site/                      # Django project configuration
├── requirements.txt                # Python dependencies
├── manage.py                       # Django management interface
└── documentation/
    ├── GENOMICS_IMPLEMENTATION.md              # Genomics extension details
    ├── BIOMARKERS_LABS_IMAGING.md              # Biomarker model documentation
    ├── TREATMENT_LINE_IMPLEMENTATION.md        # Treatment tracking details
    ├── BEHAVIORAL_SOCIAL_DETERMINANTS_IMPLEMENTATION.md  # SDOH documentation
    └── SYNTHETIC_BREAST_CANCER_DATA.md         # Test dataset documentation
```

## 🔧 Management Commands

The system includes comprehensive Django management commands for data operations:

### **Data Loading Commands**
- `load_synthetic_breast_cancer_data` - Load comprehensive synthetic test dataset
- `load_breast_cancer_data` - Load original breast cancer fixtures
- `populate_patient_info` - Generate additional patient demographics

### **Data Maintenance Commands**  
- `cleanup_patient_info` - Remove incomplete or invalid records
- `update_patient_info` - Bulk update patient demographic information
- `validate_patient_info` - Comprehensive data validation and reporting

### **Example Usage**
```bash
# Load synthetic data with progress reporting
python manage.py load_synthetic_breast_cancer_data --verbosity=2

# Validate all patient data
python manage.py validate_patient_info --output-format=json

# Clean up test data
python manage.py cleanup_patient_info --dry-run
```

For detailed command documentation, see [omop/management/README.md](omop/management/README.md).

## 📊 API Integration

### **RESTful API Endpoints**
The system provides comprehensive API access to all OMOP extensions:

```python
# Example API usage
GET /api/persons/                           # List all patients
GET /api/persons/{id}/treatment-regimens/   # Patient's treatment history
GET /api/persons/{id}/genomic-variants/     # Patient's genomic profile
GET /api/persons/{id}/biomarkers/           # Patient's biomarker measurements
GET /api/clinical-trials/                   # Available clinical trials
POST /api/trial-matching/                   # Automated trial matching
```

### **Clinical Trial Matching**
Automated patient-trial matching based on comprehensive criteria:

```python
from omop.models import Person, ClinicalTrial
from omop.utils import TrialMatcher

# Find eligible trials for a patient
patient = Person.objects.get(pk=123)
matcher = TrialMatcher()
eligible_trials = matcher.find_eligible_trials(patient)

# Detailed eligibility assessment
for trial in eligible_trials:
    eligibility = matcher.assess_eligibility(patient, trial)
    print(f"Trial {trial.nct_number}: {eligibility.overall_eligible}")
    print(f"Biomarker match: {eligibility.biomarker_match}")
    print(f"Prior therapy eligible: {eligibility.prior_therapy_eligible}")
```

```
exactomop/
├── omop/                           # Core OMOP models and extensions
│   ├── models.py                   # Extended OMOP data models
│   ├── admin.py                    # Django admin interface
│   ├── management/commands/        # Data loading and management
│   ├── fixtures/                   # Synthetic test datasets
│   └── migrations/                 # Database schema migrations
├── omop_site/                      # Django project configuration
├── templates/                      # Web interface templates
├── requirements.txt                # Python dependencies
├── *.md                           # Documentation files
└── example_*.py                   # Usage examples
```

## 🔧 Management Commands

### Data Loading
```bash
# Load breast cancer test data
python manage.py load_synthetic_breast_cancer_data --clear

# Load genomics test data  
python manage.py load_genomics_test_data

# Validate patient data
python manage.py validate_patient_info

# Clean up orphaned records
python manage.py cleanup_patient_info
```

### Data Analysis
```bash
# Generate treatment pattern reports
python manage.py analyze_treatment_patterns

# Export clinical trial matches
python manage.py export_trial_matches

# Generate biomarker summaries
python manage.py summarize_biomarkers
```

## 🔗 API Integration

### RESTful Endpoints
- **Patient Data**: FHIR-compatible patient resource endpoints
- **Treatment History**: Complete treatment timeline API
- **Biomarker Data**: Genomics and biomarker query interface
- **Trial Matching**: Real-time eligibility assessment API

### Clinical Trial Systems
- **EXACT Integration**: Direct API for trial matching
- **ClinicalTrials.gov**: Protocol metadata synchronization
- **CTMS Integration**: Clinical trial management system connectivity

## 📖 Documentation

- **[Treatment Line Implementation](TREATMENT_LINE_IMPLEMENTATION.md)**: Comprehensive treatment sequencing
- **[Genomics Implementation](GENOMICS_IMPLEMENTATION.md)**: Molecular data integration
- **[Biomarkers & Labs](BIOMARKERS_LABS_IMAGING.md)**: Laboratory data standards
- **[Social Determinants](BEHAVIORAL_SOCIAL_DETERMINANTS_IMPLEMENTATION.md)**: SDOH integration
- **[Synthetic Data Guide](SYNTHETIC_BREAST_CANCER_DATA.md)**: Test dataset documentation

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Add tests**: Ensure new features have comprehensive test coverage
4. **Update documentation**: Include relevant documentation updates
5. **Submit pull request**: Detailed description of changes

### Development Guidelines
- **OMOP Compliance**: All extensions must maintain OMOP CDM compatibility
- **Data Quality**: Implement appropriate validation and constraints
- **Documentation**: Comprehensive inline and external documentation
- **Testing**: Unit tests for all models and business logic

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OHDSI Community**: OMOP Common Data Model framework
- **HemOnc Vocabulary**: Cancer treatment standardization
- **EXACT Program**: Clinical trial matching inspiration
- **Cancer Research Community**: Domain expertise and validation

---

**Built for cancer researchers, by cancer researchers** 🎗️

