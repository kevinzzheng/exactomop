from django.db import models

# Choice classes for standardized values (complementing exactmodels.py)
class MeasurementSourceChoices(models.TextChoices):
    LAB_RESULT = 'LAB', 'Laboratory Result'
    VITAL_SIGN = 'VITAL', 'Vital Sign'
    PATIENT_REPORTED = 'PATIENT', 'Patient Reported'
    CLINICAL_ASSESSMENT = 'CLINICAL', 'Clinical Assessment'

class ObservationSourceChoices(models.TextChoices):
    CLINICAL_EXAM = 'EXAM', 'Clinical Examination'
    IMAGING = 'IMAGING', 'Medical Imaging'
    PATHOLOGY = 'PATH', 'Pathology Report'
    GENETIC_TEST = 'GENETIC', 'Genetic Testing'

# Choice classes for PatientInfo support
class GenderChoices(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    UNKNOWN = 'UN', 'Unknown'
    EMPTY = '', 'Empty'

class WeightUnits(models.TextChoices):
    KG = 'kg', 'Kilograms'
    LB = 'lb', 'Pounds'

class HeightUnits(models.TextChoices):
    CM = 'cm', 'Centimeters'
    IN = 'in', 'Inches'

class HemoglobinUnits(models.TextChoices):
    G_DL = 'G/DL', 'g/deciliter'
    G_L = 'G/L', 'g/Liter'

class AlbuminUnits(models.TextChoices):
    G_DL = 'G/DL', 'g/deciliter'
    G_L = 'G/L', 'g/Liter'

class PlateletCountUnits(models.TextChoices):
    CELLS_UL = 'CELLS/UL', 'cells/microliter'
    CELLS_L = 'CELLS/L', 'cells/Liter'

class SerumCreatinineUnits(models.TextChoices):
    MG_DL = 'MG/DL', 'mg/dL'
    MICROMOLES_L = 'MICROMOLES/L', 'micromoles/L'

class SerumBilirubinUnits(models.TextChoices):
    MG_DL = 'MG/DL', 'mg/dL'
    MICROMOLES_L = 'MICROMOLES/L', 'micromoles/L'

class SerumCalciumUnits(models.TextChoices):
    MG_DL = 'MG/DL', 'mg/dL'
    MICROMOLES_L = 'MICROMOLES/L', 'micromoles/L'

# Additional choice classes for enhanced OMOP models
class TherapyLineChoices(models.TextChoices):
    FIRST_LINE = '1', 'First Line'
    SECOND_LINE = '2', 'Second Line'  
    THIRD_LINE = '3', 'Third Line'
    FOURTH_LINE = '4', 'Fourth Line'
    LATER_LINE = '5+', 'Later Line (5+)'

class TherapyIntentChoices(models.TextChoices):
    CURATIVE = 'CURATIVE', 'Curative'
    PALLIATIVE = 'PALLIATIVE', 'Palliative'
    ADJUVANT = 'ADJUVANT', 'Adjuvant'
    NEOADJUVANT = 'NEOADJUVANT', 'Neoadjuvant'
    MAINTENANCE = 'MAINTENANCE', 'Maintenance'
    SUPPORTIVE = 'SUPPORTIVE', 'Supportive Care'

class TreatmentResponseChoices(models.TextChoices):
    COMPLETE_RESPONSE = 'CR', 'Complete Response'
    PARTIAL_RESPONSE = 'PR', 'Partial Response'  
    STABLE_DISEASE = 'SD', 'Stable Disease'
    PROGRESSIVE_DISEASE = 'PD', 'Progressive Disease'
    NOT_EVALUABLE = 'NE', 'Not Evaluable'

class TreatmentLineStatusChoices(models.TextChoices):
    """Treatment line progression status for therapeutic tracking"""
    TREATMENT_NAIVE = 'NAIVE', 'Treatment Naive'
    PREVIOUSLY_TREATED = 'PREV_TX', 'Previously Treated'
    REFRACTORY = 'REFRACTORY', 'Refractory'
    RELAPSED = 'RELAPSED', 'Relapsed'
    RELAPSED_REFRACTORY = 'REL_REF', 'Relapsed/Refractory'

class DrugClassificationChoices(models.TextChoices):
    """Drug classifications for treatment line analysis"""
    PLATINUM_BASED = 'PLATINUM', 'Platinum-based Therapy'
    IMMUNOTHERAPY = 'IMMUNO', 'Immunotherapy'
    TARGETED_THERAPY = 'TARGETED', 'Targeted Therapy'
    CHEMOTHERAPY = 'CHEMO', 'Traditional Chemotherapy'
    HORMONE_THERAPY = 'HORMONE', 'Hormone Therapy'
    RADIATION = 'RADIATION', 'Radiation Therapy'
    STEM_CELL_TRANSPLANT = 'SCT', 'Stem Cell Transplant'
    SURGERY = 'SURGERY', 'Surgical Intervention'
    CLINICAL_TRIAL_DRUG = 'TRIAL', 'Clinical Trial Drug'

class RegimenTypeChoices(models.TextChoices):
    """Types of treatment regimens"""
    SINGLE_AGENT = 'SINGLE', 'Single Agent'
    COMBINATION = 'COMBO', 'Combination Therapy'
    SEQUENTIAL = 'SEQ', 'Sequential Therapy'
    CONCURRENT = 'CONC', 'Concurrent Therapy'
    ALTERNATING = 'ALT', 'Alternating Therapy'

class TreatmentOutcomeChoices(models.TextChoices):
    """Treatment line outcomes"""
    COMPLETED = 'COMPLETED', 'Treatment Completed'
    PROGRESSION = 'PROGRESSION', 'Disease Progression'
    TOXICITY = 'TOXICITY', 'Unacceptable Toxicity'
    PATIENT_CHOICE = 'PT_CHOICE', 'Patient Choice'
    PHYSICIAN_CHOICE = 'MD_CHOICE', 'Physician Decision'
    DEATH = 'DEATH', 'Death'
    TRANSPLANT = 'TRANSPLANT', 'Proceeded to Transplant'
    ONGOING = 'ONGOING', 'Treatment Ongoing'

# ==========================================
# BEHAVIORAL, SOCIAL DETERMINANTS & DEMOGRAPHICS
# ==========================================

# Smoking/Tobacco Use Status for Patient Demographics
class SmokingStatusChoices(models.TextChoices):
    NEVER_SMOKER = 'never_smoker', 'Never Smoker'
    CURRENT_SMOKER = 'current_smoker', 'Current Smoker'
    FORMER_SMOKER = 'former_smoker', 'Former Smoker'
    PASSIVE_SMOKER = 'passive_smoker', 'Passive Smoker (Environmental Exposure)'
    UNKNOWN = 'unknown', 'Unknown Smoking Status'

# Tobacco Product Types
class TobaccoProductChoices(models.TextChoices):
    CIGARETTES = 'cigarettes', 'Cigarettes'
    CIGARS = 'cigars', 'Cigars'
    PIPE = 'pipe', 'Pipe Tobacco'
    CHEWING_TOBACCO = 'chewing_tobacco', 'Chewing Tobacco'
    SNUFF = 'snuff', 'Snuff'
    E_CIGARETTES = 'e_cigarettes', 'Electronic Cigarettes/Vaping'
    HOOKAH = 'hookah', 'Hookah/Shisha'
    OTHER = 'other', 'Other Tobacco Product'

# Substance Use Categories
class SubstanceUseChoices(models.TextChoices):
    ALCOHOL = 'alcohol', 'Alcohol Use'
    ILLICIT_DRUGS = 'illicit_drugs', 'Illicit Drug Use'
    PRESCRIPTION_MISUSE = 'prescription_misuse', 'Prescription Drug Misuse'
    MARIJUANA = 'marijuana', 'Marijuana/Cannabis'
    OPIOIDS = 'opioids', 'Opioid Use'
    STIMULANTS = 'stimulants', 'Stimulant Use'
    SEDATIVES = 'sedatives', 'Sedative/Hypnotic Use'
    NONE = 'none', 'No Substance Use'
    UNKNOWN = 'unknown', 'Unknown'

# Alcohol Consumption Levels
class AlcoholUseChoices(models.TextChoices):
    NEVER = 'never', 'Never'
    MINIMAL = 'minimal', 'Minimal (< 1 drink/week)'
    LIGHT = 'light', 'Light (1-7 drinks/week)'
    MODERATE = 'moderate', 'Moderate (8-14 drinks/week)'
    HEAVY = 'heavy', 'Heavy (> 14 drinks/week)'
    BINGE = 'binge', 'Binge Drinking Pattern'
    FORMER_USER = 'former_user', 'Former Alcohol User'
    UNKNOWN = 'unknown', 'Unknown'

# Contraceptive Methods
class ContraceptiveMethodChoices(models.TextChoices):
    NONE = 'none', 'No Contraception'
    HORMONAL_ORAL = 'hormonal_oral', 'Oral Contraceptive Pills'
    HORMONAL_PATCH = 'hormonal_patch', 'Contraceptive Patch'
    HORMONAL_RING = 'hormonal_ring', 'Vaginal Ring'
    HORMONAL_INJECTION = 'hormonal_injection', 'Injectable Contraceptive'
    HORMONAL_IMPLANT = 'hormonal_implant', 'Contraceptive Implant'
    IUD_HORMONAL = 'iud_hormonal', 'Hormonal IUD'
    IUD_COPPER = 'iud_copper', 'Copper IUD'
    BARRIER_CONDOM = 'barrier_condom', 'Condoms'
    BARRIER_DIAPHRAGM = 'barrier_diaphragm', 'Diaphragm'
    STERILIZATION = 'sterilization', 'Surgical Sterilization'
    NATURAL_METHODS = 'natural_methods', 'Natural Family Planning'
    EMERGENCY = 'emergency', 'Emergency Contraception'
    UNKNOWN = 'unknown', 'Unknown Method'

# Pregnancy Status for Patient Demographics
class PregnancyStatusChoices(models.TextChoices):
    NOT_PREGNANT = 'not_pregnant', 'Not Pregnant (Confirmed)'
    PREGNANT = 'pregnant', 'Pregnant'
    POSSIBLY_PREGNANT = 'possibly_pregnant', 'Possibly Pregnant'
    POSTPARTUM = 'postpartum', 'Postpartum (< 6 months)'
    LACTATING = 'lactating', 'Currently Lactating'
    NOT_APPLICABLE = 'not_applicable', 'Not Applicable (Male/Postmenopausal)'
    UNKNOWN = 'unknown', 'Unknown'

# Menopausal Status
class MenopausalStatusChoices(models.TextChoices):
    PREMENOPAUSAL = 'premenopausal', 'Premenopausal'
    PERIMENOPAUSAL = 'perimenopausal', 'Perimenopausal'
    POSTMENOPAUSAL = 'postmenopausal', 'Postmenopausal'
    POSTMENOPAUSAL_NATURAL = 'postmenopausal_natural', 'Postmenopausal (Natural)'
    POSTMENOPAUSAL_SURGICAL = 'postmenopausal_surgical', 'Postmenopausal (Surgical)'
    POSTMENOPAUSAL_TREATMENT = 'postmenopausal_treatment', 'Postmenopausal (Treatment-Induced)'
    UNKNOWN = 'unknown', 'Unknown Menopausal Status'
    NOT_APPLICABLE = 'not_applicable', 'Not Applicable (Male)'

# Infectious Disease Status
class InfectiousDiseaseStatusChoices(models.TextChoices):
    NEGATIVE = 'negative', 'Negative/Not Infected'
    POSITIVE_ACTIVE = 'positive_active', 'Positive/Active Infection'
    POSITIVE_TREATED = 'positive_treated', 'Positive/Treated'
    POSITIVE_CHRONIC = 'positive_chronic', 'Positive/Chronic'
    POSITIVE_RESOLVED = 'positive_resolved', 'Positive/Resolved'
    INDETERMINATE = 'indeterminate', 'Indeterminate'
    NOT_TESTED = 'not_tested', 'Not Tested'
    IMMUNE = 'immune', 'Immune (Vaccinated/Natural)'
    UNKNOWN = 'unknown', 'Unknown Status'

# Social Support and Caregiver Status
class CaregiverStatusChoices(models.TextChoices):
    AVAILABLE_FAMILY = 'available_family', 'Family Caregiver Available'
    AVAILABLE_FRIEND = 'available_friend', 'Friend/Non-family Caregiver Available'
    AVAILABLE_PROFESSIONAL = 'available_professional', 'Professional Caregiver Available'
    LIMITED_SUPPORT = 'limited_support', 'Limited Caregiver Support'
    NO_CAREGIVER = 'no_caregiver', 'No Caregiver Available'
    SELF_CARE = 'self_care', 'Independent/Self-Care'
    UNKNOWN = 'unknown', 'Unknown Caregiver Status'

# Cognitive/Mental Health Status for Consent Capability
class ConsentCapabilityChoices(models.TextChoices):
    CAPABLE = 'capable', 'Capable of Informed Consent'
    IMPAIRED = 'impaired', 'Impaired Consent Capability'
    GUARDIAN_REQUIRED = 'guardian_required', 'Guardian/Proxy Consent Required'
    FLUCTUATING = 'fluctuating', 'Fluctuating Cognitive Status'
    ASSESSED_CAPABLE = 'assessed_capable', 'Formally Assessed as Capable'
    NOT_ASSESSED = 'not_assessed', 'Consent Capability Not Assessed'
    UNKNOWN = 'unknown', 'Unknown Consent Capability'

# Mental Health Disorder Status
class MentalHealthStatusChoices(models.TextChoices):
    NO_DISORDER = 'no_disorder', 'No Mental Health Disorder'
    DEPRESSION = 'depression', 'Depression'
    ANXIETY = 'anxiety', 'Anxiety Disorder'
    BIPOLAR = 'bipolar', 'Bipolar Disorder'
    PSYCHOTIC = 'psychotic', 'Psychotic Disorder'
    COGNITIVE_IMPAIRMENT = 'cognitive_impairment', 'Cognitive Impairment'
    SUBSTANCE_INDUCED = 'substance_induced', 'Substance-Induced Mental Disorder'
    PERSONALITY_DISORDER = 'personality_disorder', 'Personality Disorder'
    ADJUSTMENT_DISORDER = 'adjustment_disorder', 'Adjustment Disorder'
    OTHER = 'other', 'Other Mental Health Condition'
    MULTIPLE = 'multiple', 'Multiple Mental Health Conditions'
    UNKNOWN = 'unknown', 'Unknown Mental Health Status'

# Geographic Risk Exposure Categories
class GeographicRiskChoices(models.TextChoices):
    NO_RISK = 'no_risk', 'No Geographic Risk Exposure'
    ENDEMIC_DISEASE = 'endemic_disease', 'Endemic Disease Area Exposure'
    ENVIRONMENTAL_TOXIN = 'environmental_toxin', 'Environmental Toxin Exposure'
    RADIATION_EXPOSURE = 'radiation_exposure', 'Radiation Exposure Area'
    INFECTIOUS_OUTBREAK = 'infectious_outbreak', 'Infectious Disease Outbreak Area'
    OCCUPATIONAL_HAZARD = 'occupational_hazard', 'Occupational Hazard Exposure'
    CONFLICT_ZONE = 'conflict_zone', 'Conflict Zone/War Area'
    NATURAL_DISASTER = 'natural_disaster', 'Natural Disaster Area'
    HIGH_ALTITUDE = 'high_altitude', 'High Altitude Exposure'
    EXTREME_CLIMATE = 'extreme_climate', 'Extreme Climate Exposure'
    OTHER = 'other', 'Other Geographic Risk'
    UNKNOWN = 'unknown', 'Unknown Geographic Risk Status'

# Behavioral Observation Categories
class BehavioralObservationChoices(models.TextChoices):
    SMOKING_STATUS = 'smoking_status', 'Smoking/Tobacco Use Status'
    SUBSTANCE_USE = 'substance_use', 'Substance Use Assessment'
    ALCOHOL_USE = 'alcohol_use', 'Alcohol Use Assessment'
    CONTRACEPTIVE_USE = 'contraceptive_use', 'Contraceptive Use'
    PREGNANCY_STATUS = 'pregnancy_status', 'Pregnancy Status'
    MENOPAUSAL_STATUS = 'menopausal_status', 'Menopausal Status'
    INFECTIOUS_DISEASE = 'infectious_disease', 'Infectious Disease Status'
    CAREGIVER_STATUS = 'caregiver_status', 'Caregiver/Social Support'
    CONSENT_CAPABILITY = 'consent_capability', 'Consent Capability'
    MENTAL_HEALTH = 'mental_health', 'Mental Health Status'
    GEOGRAPHIC_RISK = 'geographic_risk', 'Geographic Risk Exposure'
    SOCIAL_DETERMINANT = 'social_determinant', 'Social Determinant of Health'
    REPRODUCTIVE_HEALTH = 'reproductive_health', 'Reproductive Health Status'

class PerformanceStatusChoices(models.TextChoices):
    ECOG_0 = 'ECOG_0', 'ECOG 0 - Fully active'
    ECOG_1 = 'ECOG_1', 'ECOG 1 - Restricted in strenuous activity'
    ECOG_2 = 'ECOG_2', 'ECOG 2 - Ambulatory, capable of self-care'
    ECOG_3 = 'ECOG_3', 'ECOG 3 - Limited self-care'
    ECOG_4 = 'ECOG_4', 'ECOG 4 - Completely disabled'
    KARNOFSKY_100 = 'KPS_100', 'Karnofsky 100% - Normal activity'
    KARNOFSKY_90 = 'KPS_90', 'Karnofsky 90% - Minor signs/symptoms'
    KARNOFSKY_80 = 'KPS_80', 'Karnofsky 80% - Normal activity with effort'

# OMOP Oncology Extension Choice Classes
class TumorLateralityChoices(models.TextChoices):
    RIGHT = 'R', 'Right'
    LEFT = 'L', 'Left'
    BILATERAL = 'B', 'Bilateral'
    MIDLINE = 'M', 'Midline'
    UNKNOWN = 'U', 'Unknown'
    NOT_APPLICABLE = 'N', 'Not Applicable'

class AJCCStageChoices(models.TextChoices):
    STAGE_0 = '0', 'Stage 0 (in situ)'
    STAGE_I = 'I', 'Stage I'
    STAGE_IA = 'IA', 'Stage IA'
    STAGE_IB = 'IB', 'Stage IB'
    STAGE_II = 'II', 'Stage II'
    STAGE_IIA = 'IIA', 'Stage IIA'
    STAGE_IIB = 'IIB', 'Stage IIB'
    STAGE_III = 'III', 'Stage III'
    STAGE_IIIA = 'IIIA', 'Stage IIIA'
    STAGE_IIIB = 'IIIB', 'Stage IIIB'
    STAGE_IIIC = 'IIIC', 'Stage IIIC'
    STAGE_IV = 'IV', 'Stage IV'
    STAGE_IVA = 'IVA', 'Stage IVA'
    STAGE_IVB = 'IVB', 'Stage IVB'
    UNKNOWN = 'UNK', 'Unknown'

class TStageChoices(models.TextChoices):
    TX = 'TX', 'TX - Primary tumor cannot be assessed'
    T0 = 'T0', 'T0 - No evidence of primary tumor'
    TIS = 'Tis', 'Tis - Carcinoma in situ'
    T1 = 'T1', 'T1'
    T1A = 'T1a', 'T1a'
    T1B = 'T1b', 'T1b'
    T1C = 'T1c', 'T1c'
    T2 = 'T2', 'T2'
    T2A = 'T2a', 'T2a'
    T2B = 'T2b', 'T2b'
    T3 = 'T3', 'T3'
    T3A = 'T3a', 'T3a'
    T3B = 'T3b', 'T3b'
    T4 = 'T4', 'T4'
    T4A = 'T4a', 'T4a'
    T4B = 'T4b', 'T4b'
    T4C = 'T4c', 'T4c'
    T4D = 'T4d', 'T4d'

class NStageChoices(models.TextChoices):
    NX = 'NX', 'NX - Regional lymph nodes cannot be assessed'
    N0 = 'N0', 'N0 - No regional lymph node metastasis'
    N1 = 'N1', 'N1'
    N1A = 'N1a', 'N1a'
    N1B = 'N1b', 'N1b'
    N1C = 'N1c', 'N1c'
    N2 = 'N2', 'N2'
    N2A = 'N2a', 'N2a'
    N2B = 'N2b', 'N2b'
    N2C = 'N2c', 'N2c'
    N3 = 'N3', 'N3'
    N3A = 'N3a', 'N3a'
    N3B = 'N3b', 'N3b'
    N3C = 'N3c', 'N3c'

class MStageChoices(models.TextChoices):
    MX = 'MX', 'MX - Distant metastasis cannot be assessed'
    M0 = 'M0', 'M0 - No distant metastasis'
    M1 = 'M1', 'M1 - Distant metastasis'
    M1A = 'M1a', 'M1a'
    M1B = 'M1b', 'M1b'
    M1C = 'M1c', 'M1c'

class TumorGradeChoices(models.TextChoices):
    GX = 'GX', 'GX - Grade cannot be assessed'
    G1 = 'G1', 'G1 - Well differentiated'
    G2 = 'G2', 'G2 - Moderately differentiated'
    G3 = 'G3', 'G3 - Poorly differentiated'
    G4 = 'G4', 'G4 - Undifferentiated'

class BiomarkerStatusChoices(models.TextChoices):
    POSITIVE = 'POS', 'Positive'
    NEGATIVE = 'NEG', 'Negative'
    EQUIVOCAL = 'EQU', 'Equivocal'
    UNKNOWN = 'UNK', 'Unknown'
    NOT_TESTED = 'NT', 'Not Tested'

class GenomicVariantTypeChoices(models.TextChoices):
    """Types of genomic variants for molecular profiling"""
    SNV = 'SNV', 'Single Nucleotide Variant'
    INDEL = 'INDEL', 'Insertion/Deletion'
    CNV = 'CNV', 'Copy Number Variant'
    SV = 'SV', 'Structural Variant'
    FUSION = 'FUSION', 'Gene Fusion'
    MSI = 'MSI', 'Microsatellite Instability'
    TMB = 'TMB', 'Tumor Mutational Burden'
    LOH = 'LOH', 'Loss of Heterozygosity'

class ClinicalSignificanceChoices(models.TextChoices):
    """Clinical significance classifications"""
    PATHOGENIC = 'PATH', 'Pathogenic'
    LIKELY_PATHOGENIC = 'LPATH', 'Likely Pathogenic'
    BENIGN = 'BEN', 'Benign'
    LIKELY_BENIGN = 'LBEN', 'Likely Benign'
    VUS = 'VUS', 'Variant of Uncertain Significance'
    DRUG_RESPONSE = 'DRUG', 'Drug Response'
    RISK_FACTOR = 'RISK', 'Risk Factor'
    PROTECTIVE = 'PROT', 'Protective'

class GenomicTestTypeChoices(models.TextChoices):
    """Types of genomic testing methods"""
    TARGETED_PANEL = 'PANEL', 'Targeted Gene Panel'
    WES = 'WES', 'Whole Exome Sequencing'
    WGS = 'WGS', 'Whole Genome Sequencing'
    RNA_SEQ = 'RNA', 'RNA Sequencing'
    FISH = 'FISH', 'Fluorescence In Situ Hybridization'
    IHC = 'IHC', 'Immunohistochemistry'
    PCR = 'PCR', 'Polymerase Chain Reaction'
    LIQUID_BIOPSY = 'LIQUID', 'Liquid Biopsy/ctDNA'

class MolecularAlterationChoices(models.TextChoices):
    """Common molecular alterations for therapeutic matching"""
    BRCA1_MUTATION = 'BRCA1', 'BRCA1 Mutation'
    BRCA2_MUTATION = 'BRCA2', 'BRCA2 Mutation'
    ESR1_MUTATION = 'ESR1', 'ESR1 Mutation'
    PIK3CA_MUTATION = 'PIK3CA', 'PIK3CA Mutation'
    HER2_AMPLIFICATION = 'HER2_AMP', 'HER2 Amplification'
    EGFR_MUTATION = 'EGFR', 'EGFR Mutation'
    KRAS_MUTATION = 'KRAS', 'KRAS Mutation'
    TP53_MUTATION = 'TP53', 'TP53 Mutation'
    MSI_HIGH = 'MSI_H', 'Microsatellite Instability High'
    TMB_HIGH = 'TMB_H', 'Tumor Mutational Burden High'
    PDL1_HIGH = 'PDL1_H', 'PD-L1 High Expression'
    NTRK_FUSION = 'NTRK', 'NTRK Gene Fusion'

class ImagingModalityChoices(models.TextChoices):
    """Imaging modalities for OMOP Imaging Extension"""
    CT = 'CT', 'Computed Tomography'
    MRI = 'MRI', 'Magnetic Resonance Imaging'
    PET = 'PET', 'Positron Emission Tomography'
    PET_CT = 'PET_CT', 'PET/CT'
    ULTRASOUND = 'US', 'Ultrasound'
    XRAY = 'XR', 'X-Ray'
    MAMMOGRAPHY = 'MG', 'Mammography'
    NUCLEAR = 'NM', 'Nuclear Medicine'
    FLUOROSCOPY = 'FL', 'Fluoroscopy'
    ANGIOGRAPHY = 'AG', 'Angiography'

class ImagingContrastChoices(models.TextChoices):
    """Contrast agent types for imaging"""
    NONE = 'NONE', 'No Contrast'
    IODINATED = 'IOD', 'Iodinated Contrast'
    GADOLINIUM = 'GAD', 'Gadolinium-based'
    BARIUM = 'BAR', 'Barium-based'
    MICROBUBBLE = 'MB', 'Microbubble'
    RADIOISOTOPE = 'RI', 'Radioisotope'

class TumorResponseChoices(models.TextChoices):
    """Tumor response assessment (RECIST, irRECIST)"""
    COMPLETE_RESPONSE = 'CR', 'Complete Response'
    PARTIAL_RESPONSE = 'PR', 'Partial Response'
    STABLE_DISEASE = 'SD', 'Stable Disease'
    PROGRESSIVE_DISEASE = 'PD', 'Progressive Disease'
    NOT_EVALUABLE = 'NE', 'Not Evaluable'
    MIXED_RESPONSE = 'MR', 'Mixed Response'

class BiomarkerCategoryChoices(models.TextChoices):
    """Categories of biomarkers for molecular analysis"""
    PROTEIN_EXPRESSION = 'PROTEIN', 'Protein Expression'
    GENOMIC_ALTERATION = 'GENOMIC', 'Genomic Alteration'
    IMMUNE_MARKER = 'IMMUNE', 'Immune Marker'
    METABOLIC_MARKER = 'METABOLIC', 'Metabolic Marker'
    TUMOR_BURDEN = 'BURDEN', 'Tumor Burden'
    HORMONE_RECEPTOR = 'HORMONE', 'Hormone Receptor'
    GROWTH_FACTOR = 'GROWTH', 'Growth Factor Receptor'

class LabTestCategoryChoices(models.TextChoices):
    """Laboratory test categories for standard medical care"""
    HEMATOLOGY = 'HEME', 'Hematology'
    CHEMISTRY = 'CHEM', 'Clinical Chemistry'
    IMMUNOLOGY = 'IMMUNO', 'Immunology'
    MOLECULAR = 'MOLEC', 'Molecular Diagnostics'
    TUMOR_MARKER = 'TUMOR', 'Tumor Markers'
    COAGULATION = 'COAG', 'Coagulation'
    ENDOCRINE = 'ENDO', 'Endocrine'
    CARDIOMARKER = 'CARDIO', 'Cardiac Markers'

class Location(models.Model):
    location_id = models.BigAutoField(primary_key=True)
    address_1 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=20, blank=True)
    country_concept_id = models.IntegerField(null=True, blank=True)
    
    # Extended geographic data for distance calculations (complementing PatientInfo geo_point)
    longitude = models.FloatField(blank=True, null=True, help_text="Longitude coordinate")
    latitude = models.FloatField(blank=True, null=True, help_text="Latitude coordinate") 
    
    class Meta:
        db_table = "location"
        indexes = [models.Index(fields=["zip"])]
    def __str__(self):
        return f"{self.address_1} {self.city} {self.zip}".strip()

class Concept(models.Model):
    """
    OMOP Concept model for standardized terminology
    Essential for mapping all clinical data to standard vocabularies
    """
    concept_id = models.IntegerField(primary_key=True)
    concept_name = models.CharField(max_length=255)
    domain_id = models.CharField(max_length=20, help_text="Domain (Measurement, Drug, Condition, etc.)")
    vocabulary_id = models.CharField(max_length=20, help_text="Vocabulary (SNOMED, LOINC, RxNorm, etc.)")
    concept_class_id = models.CharField(max_length=20, help_text="Concept class")
    standard_concept = models.CharField(max_length=1, blank=True, help_text="S=Standard, C=Classification")
    concept_code = models.CharField(max_length=50, help_text="Source code")
    valid_start_date = models.DateField(help_text="Date concept became valid")
    valid_end_date = models.DateField(help_text="Date concept became invalid")
    invalid_reason = models.CharField(max_length=1, blank=True, help_text="Reason concept is invalid")
    
    class Meta:
        db_table = "concept"
        indexes = [
            models.Index(fields=["concept_name"]),
            models.Index(fields=["domain_id"]),
            models.Index(fields=["vocabulary_id"]),
            models.Index(fields=["concept_class_id"]),
            models.Index(fields=["standard_concept"]),
            models.Index(fields=["concept_code"]),
        ]
    
    def __str__(self):
        return f"{self.concept_id}: {self.concept_name}"

class ConceptRelationship(models.Model):
    """
    OMOP Concept Relationship model for concept mappings
    Links source concepts to standard concepts
    """
    concept_id_1 = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='relationships_as_concept_1')
    concept_id_2 = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='relationships_as_concept_2')
    relationship_id = models.CharField(max_length=20, help_text="Type of relationship (Maps to, Is a, etc.)")
    valid_start_date = models.DateField()
    valid_end_date = models.DateField()
    invalid_reason = models.CharField(max_length=1, blank=True)
    
    class Meta:
        db_table = "concept_relationship"
        unique_together = [['concept_id_1', 'concept_id_2', 'relationship_id']]
        indexes = [
            models.Index(fields=["relationship_id"]),
            models.Index(fields=["valid_start_date"]),
        ]
    
    def __str__(self):
        return f"{self.concept_id_1} {self.relationship_id} {self.concept_id_2}"

class Vocabulary(models.Model):
    """
    OMOP Vocabulary model for terminology systems
    """
    vocabulary_id = models.CharField(max_length=20, primary_key=True)
    vocabulary_name = models.CharField(max_length=255)
    vocabulary_reference = models.CharField(max_length=255, blank=True)
    vocabulary_version = models.CharField(max_length=255, blank=True)
    vocabulary_concept_id = models.IntegerField()
    
    class Meta:
        db_table = "vocabulary"
    
    def __str__(self):
        return f"{self.vocabulary_id}: {self.vocabulary_name}"

class Person(models.Model):
    person_id = models.BigAutoField(primary_key=True)
    gender_concept_id = models.IntegerField()
    year_of_birth = models.IntegerField(null=True, blank=True)
    month_of_birth = models.IntegerField(null=True, blank=True)
    day_of_birth = models.IntegerField(null=True, blank=True)
    race_concept_id = models.IntegerField(null=True, blank=True)
    ethnicity_concept_id = models.IntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    
    # OMOP CDM extensions that complement PatientInfo
    provider_id = models.IntegerField(null=True, blank=True, help_text="Primary care provider ID")
    care_site_id = models.IntegerField(null=True, blank=True, help_text="Primary care site ID")
    person_source_value = models.CharField(max_length=50, blank=True, help_text="Source identifier")
    
 
    # Language and cultural information
    primary_language_concept_id = models.IntegerField(null=True, blank=True, help_text="Primary language concept")
    secondary_languages = models.TextField(blank=True, help_text="Additional languages (JSON array)")
    language_skill_level = models.CharField(max_length=20, blank=True, help_text="Language proficiency level")
    
    class Meta:
        db_table = "person"
        indexes = [
            models.Index(fields=["gender_concept_id"]),
            models.Index(fields=["primary_language_concept_id"]),
        ]
    def __str__(self):
        return f"Person {self.person_id}"

class ConditionOccurrence(models.Model):
    condition_occurrence_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    condition_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT, related_name='conditions',
                                         help_text="OMOP concept for the condition")
    condition_start_date = models.DateField(null=True, blank=True)
    condition_end_date = models.DateField(null=True, blank=True)
    condition_type_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                              related_name='condition_types', help_text="Type/source of condition record")
    
    # OMOP CDM extensions for clinical context
    stop_reason = models.CharField(max_length=20, blank=True, help_text="Reason condition ended")
    provider_id = models.IntegerField(null=True, blank=True, help_text="Provider who recorded condition")
    visit_occurrence_id = models.IntegerField(null=True, blank=True, help_text="Visit when condition was recorded")
    visit_detail_id = models.IntegerField(null=True, blank=True, help_text="Visit detail for condition")
    condition_source_value = models.CharField(max_length=50, blank=True, help_text="Source code for condition")
    condition_source_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                                 related_name='condition_sources', help_text="Source concept")
    condition_status_source_value = models.CharField(max_length=50, blank=True, help_text="Source status value")
    condition_status_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                                 related_name='condition_statuses', help_text="Status concept")
    
    # OMOP Oncology Extension fields for comprehensive cancer data
    # Tumor topography and laterality
    primary_site_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                           related_name='primary_sites', help_text="Primary tumor site concept (ICD-O topography)")
    tumor_laterality = models.CharField(
        max_length=10,
        choices=TumorLateralityChoices.choices,
        blank=True,
        help_text="Laterality of the tumor"
    )
    
    # Histology and morphology concepts
    histology_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                         related_name='histologies', help_text="Histology/morphology concept (ICD-O, SNOMED)")
    behavior_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                        related_name='behaviors', help_text="Tumor behavior concept (benign, malignant, etc.)")
    
    # AJCC/UICC Clinical Staging
    ajcc_clinical_stage = models.CharField(
        max_length=10,
        choices=AJCCStageChoices.choices,
        blank=True,
        help_text="AJCC clinical stage"
    )
    ajcc_clinical_t = models.CharField(
        max_length=10,
        choices=TStageChoices.choices,
        blank=True,
        help_text="AJCC clinical T stage"
    )
    ajcc_clinical_n = models.CharField(
        max_length=10,
        choices=NStageChoices.choices,
        blank=True,
        help_text="AJCC clinical N stage"
    )
    ajcc_clinical_m = models.CharField(
        max_length=10,
        choices=MStageChoices.choices,
        blank=True,
        help_text="AJCC clinical M stage"
    )
    
    # AJCC/UICC Pathologic Staging
    ajcc_pathologic_stage = models.CharField(
        max_length=10,
        choices=AJCCStageChoices.choices,
        blank=True,
        help_text="AJCC pathologic stage"
    )
    ajcc_pathologic_t = models.CharField(
        max_length=10,
        choices=TStageChoices.choices,
        blank=True,
        help_text="AJCC pathologic T stage"
    )
    ajcc_pathologic_n = models.CharField(
        max_length=10,
        choices=NStageChoices.choices,
        blank=True,
        help_text="AJCC pathologic N stage"
    )
    ajcc_pathologic_m = models.CharField(
        max_length=10,
        choices=MStageChoices.choices,
        blank=True,
        help_text="AJCC pathologic M stage"
    )
    
    # Tumor grading
    histologic_grade = models.CharField(
        max_length=10,
        choices=TumorGradeChoices.choices,
        blank=True,
        help_text="Histologic grade"
    )
    nuclear_grade = models.CharField(
        max_length=10,
        choices=TumorGradeChoices.choices,
        blank=True,
        help_text="Nuclear grade"
    )
    
    # Cancer-specific biomarkers (summary status - detailed results in Observation/Measurement)
    estrogen_receptor_status = models.CharField(
        max_length=10,
        choices=BiomarkerStatusChoices.choices,
        blank=True,
        help_text="Estrogen receptor status"
    )
    progesterone_receptor_status = models.CharField(
        max_length=10,
        choices=BiomarkerStatusChoices.choices,
        blank=True,
        help_text="Progesterone receptor status"
    )
    her2_status = models.CharField(
        max_length=10,
        choices=BiomarkerStatusChoices.choices,
        blank=True,
        help_text="HER2 status"
    )
    
    # Episode linkage for disease progression tracking
    cancer_episode = models.ForeignKey('Episode', null=True, blank=True, on_delete=models.SET_NULL,
                                      help_text="Associated cancer episode for progression tracking")
    
    # Source staging system and version
    staging_system = models.CharField(max_length=50, blank=True, help_text="Staging system used (AJCC, UICC, etc.)")
    staging_system_version = models.CharField(max_length=20, blank=True, help_text="Version of staging system")
    
    class Meta:
        db_table = "condition_occurrence"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["condition_concept"]),
            models.Index(fields=["condition_start_date"]),
            models.Index(fields=["primary_site_concept"]),
            models.Index(fields=["histology_concept"]),
            models.Index(fields=["tumor_laterality"]),
            models.Index(fields=["ajcc_clinical_stage"]),
            models.Index(fields=["ajcc_pathologic_stage"]),
            models.Index(fields=["histologic_grade"]),
            models.Index(fields=["estrogen_receptor_status"]),
            models.Index(fields=["progesterone_receptor_status"]),
            models.Index(fields=["her2_status"]),
            models.Index(fields=["cancer_episode"]),
            models.Index(fields=["staging_system"]),
        ]
    def __str__(self):
        return f"Condition {self.condition_occurrence_id} for Person {self.person.person_id}"

class Measurement(models.Model):
    measurement_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    measurement_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT, related_name='measurements', 
                                           help_text="OMOP concept for what was measured")
    measurement_datetime = models.DateTimeField(null=True, blank=True, help_text="Measurement datetime (set to midnight if only date known)")
    value_as_number = models.FloatField(null=True, blank=True)
    value_as_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT, 
                                        related_name='measurement_values', help_text="Concept for categorical values")
    unit_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT, 
                                    related_name='measurement_units', help_text="Unit concept")
    modifier_of_event_id = models.BigIntegerField(null=True, blank=True)
    modifier_of_field_concept_id = models.IntegerField(null=True, blank=True)
    
    # OMOP CDM extensions for measurement context
    measurement_type_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                                related_name='measurement_types', help_text="Type/source of measurement")
    operator_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                        related_name='measurement_operators', help_text="Operator (>, <, =, etc.)")
    range_low = models.FloatField(null=True, blank=True, help_text="Normal range low value")
    range_high = models.FloatField(null=True, blank=True, help_text="Normal range high value")
    provider_id = models.IntegerField(null=True, blank=True, help_text="Provider who ordered measurement")
    visit_occurrence_id = models.IntegerField(null=True, blank=True, help_text="Visit when measured")
    visit_detail_id = models.IntegerField(null=True, blank=True, help_text="Visit detail for measurement")
    measurement_source_value = models.CharField(max_length=50, blank=True, help_text="Source value")
    measurement_source_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                                  related_name='measurement_sources', help_text="Source concept")
    unit_source_value = models.CharField(max_length=50, blank=True, help_text="Source unit value")
    value_source_value = models.CharField(max_length=50, blank=True, help_text="Source result value")
    
    # Source classification to complement PatientInfo detailed measurements
    measurement_source = models.CharField(
        max_length=10, 
        choices=MeasurementSourceChoices.choices, 
        blank=True, 
        help_text="Source type of measurement"
    )
    
    # Extended measurement context from PatientInfo
    specimen_type = models.CharField(max_length=50, blank=True, help_text="Type of specimen (blood, urine, etc.)")
    fasting_status = models.BooleanField(null=True, blank=True, help_text="Whether patient was fasting")
    measurement_method = models.CharField(max_length=100, blank=True, help_text="Method used for measurement")
    critical_value_flag = models.BooleanField(null=True, blank=True, help_text="Whether value is critical")
    
    # Quality indicators
    measurement_quality_flag = models.CharField(max_length=20, blank=True, help_text="Quality flag for measurement")
    instrument_id = models.CharField(max_length=50, blank=True, help_text="Instrument/device used")
    lab_batch_id = models.CharField(max_length=50, blank=True, help_text="Laboratory batch identifier")
    
    # Molecular biomarker support
    biomarker_type = models.CharField(max_length=50, blank=True, 
                                     help_text="Type of biomarker (protein, genomic, metabolic)")
    assay_method = models.CharField(max_length=100, blank=True, 
                                   help_text="Specific assay method used")
    reference_range_text = models.CharField(max_length=200, blank=True,
                                           help_text="Text description of reference range")
    clinical_interpretation = models.TextField(blank=True, 
                                              help_text="Clinical interpretation of result")
    
    # External identifiers for molecular data
    loinc_code = models.CharField(max_length=20, blank=True, help_text="LOINC code for measurement")
    snomed_code = models.CharField(max_length=20, blank=True, help_text="SNOMED code for measurement")
    
    # Laboratory test categorization
    lab_test_category = models.CharField(max_length=20, choices=LabTestCategoryChoices.choices,
                                        blank=True, help_text="Laboratory test category")
    
    # Lab-specific quality indicators
    delta_check_flag = models.BooleanField(null=True, blank=True, help_text="Delta check alert flag")
    panic_value_flag = models.BooleanField(null=True, blank=True, help_text="Panic/critical value flag")
    hemolysis_flag = models.BooleanField(null=True, blank=True, help_text="Hemolysis interference flag")
    lipemia_flag = models.BooleanField(null=True, blank=True, help_text="Lipemia interference flag")
    icterus_flag = models.BooleanField(null=True, blank=True, help_text="Icterus interference flag")
    
    # Therapeutic drug monitoring
    drug_concentration = models.FloatField(null=True, blank=True, help_text="Drug concentration level")
    therapeutic_range_low = models.FloatField(null=True, blank=True, help_text="Therapeutic range lower bound")
    therapeutic_range_high = models.FloatField(null=True, blank=True, help_text="Therapeutic range upper bound")
    
    # Tumor marker specific fields
    tumor_marker_trend = models.CharField(max_length=20, choices=[
        ('INCREASING', 'Increasing'),
        ('DECREASING', 'Decreasing'),
        ('STABLE', 'Stable'),
        ('FLUCTUATING', 'Fluctuating'),
    ], blank=True, help_text="Tumor marker trend")
    
    previous_value = models.FloatField(null=True, blank=True, help_text="Previous measurement value")
    percent_change = models.FloatField(null=True, blank=True, help_text="Percent change from previous")
    
    class Meta:
        db_table = "measurement"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["measurement_concept"]),
            models.Index(fields=["measurement_datetime"]),
            models.Index(fields=["specimen_type"]),
            models.Index(fields=["critical_value_flag"]),
            models.Index(fields=["unit_concept"]),
            models.Index(fields=["lab_test_category"]),
            models.Index(fields=["loinc_code"]),
            models.Index(fields=["biomarker_type"]),
            models.Index(fields=["panic_value_flag"]),
        ]
    def __str__(self):
        return f"Measurement {self.measurement_id}"

class MeasurementConcept(models.Model):
    """
    Predefined measurement concepts commonly used in PatientInfo
    Maps PatientInfo fields to standard OMOP concepts
    """
    concept = models.OneToOneField(Concept, on_delete=models.CASCADE, primary_key=True)
    
    # PatientInfo field mappings
    patient_info_field = models.CharField(max_length=100, unique=True, 
                                         help_text="Corresponding PatientInfo field name")
    preferred_unit_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                              related_name='preferred_measurements',
                                              help_text="Preferred unit concept for this measurement")
    normal_range_low = models.FloatField(null=True, blank=True, help_text="Normal range low value")
    normal_range_high = models.FloatField(null=True, blank=True, help_text="Normal range high value")
    
    # Measurement categorization
    measurement_category = models.CharField(max_length=50, blank=True, 
                                           help_text="Category (vital_signs, lab_values, demographics)")
    required_specimen_type = models.CharField(max_length=50, blank=True,
                                             help_text="Required specimen type if applicable")
    
    class Meta:
        db_table = "measurement_concept"
        indexes = [
            models.Index(fields=["patient_info_field"]),
            models.Index(fields=["measurement_category"]),
        ]
    
    def __str__(self):
        return f"{self.patient_info_field}: {self.concept.concept_name}"

class BiomarkerMeasurement(models.Model):
    """
    Specialized model for biomarker measurements
    Extends OMOP Measurement with biomarker-specific fields
    """
    biomarker_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='biomarker_measurements')
    measurement = models.ForeignKey(Measurement, null=True, blank=True, on_delete=models.SET_NULL,
                                   help_text="Related OMOP measurement record")
    
    # Biomarker identification
    biomarker_name = models.CharField(max_length=100, help_text="Biomarker name (e.g., PD-L1, TMB, MSI)")
    biomarker_concept = models.ForeignKey(Concept, on_delete=models.PROTECT,
                                         related_name='biomarker_measurements',
                                         help_text="OMOP concept for biomarker")
    biomarker_category = models.CharField(max_length=50, choices=[
        ('PROTEIN', 'Protein Expression'),
        ('GENOMIC', 'Genomic Biomarker'),
        ('METABOLIC', 'Metabolic Biomarker'),
        ('IMMUNE', 'Immune Biomarker'),
        ('FUNCTIONAL', 'Functional Biomarker'),
        ('HORMONE_RECEPTOR', 'Hormone Receptor'),
        ('GROWTH_FACTOR', 'Growth Factor Receptor'),
        ('TUMOR_BURDEN', 'Tumor Burden Marker'),
    ], help_text="Category of biomarker")
    
    # Measurement details
    measurement_date = models.DateField(help_text="Date of biomarker measurement")
    numeric_value = models.FloatField(null=True, blank=True, help_text="Numeric biomarker value")
    categorical_value = models.CharField(max_length=50, blank=True, help_text="Categorical result")
    unit = models.CharField(max_length=50, blank=True, help_text="Unit of measurement")
    
    # Clinical interpretation
    result_interpretation = models.CharField(max_length=50, choices=[
        ('HIGH', 'High'),
        ('LOW', 'Low'),
        ('POSITIVE', 'Positive'),
        ('NEGATIVE', 'Negative'),
        ('INTERMEDIATE', 'Intermediate'),
        ('INDETERMINATE', 'Indeterminate'),
    ], blank=True, help_text="Clinical interpretation of result")
    
    # Threshold and cutoff information
    threshold_value = models.FloatField(null=True, blank=True, help_text="Clinical threshold value")
    threshold_operator = models.CharField(max_length=10, choices=[
        ('GT', 'Greater than'),
        ('GTE', 'Greater than or equal'),
        ('LT', 'Less than'),
        ('LTE', 'Less than or equal'),
        ('EQ', 'Equal to'),
    ], blank=True, help_text="Threshold comparison operator")
    
    # Assay information
    assay_name = models.CharField(max_length=200, blank=True, help_text="Specific assay used")
    assay_version = models.CharField(max_length=50, blank=True, help_text="Assay version")
    laboratory = models.CharField(max_length=200, blank=True, help_text="Testing laboratory")
    
    # Sample context
    specimen_type = models.CharField(max_length=100, blank=True, help_text="Specimen type")
    tissue_site = models.CharField(max_length=100, blank=True, help_text="Tissue site")
    collection_method = models.CharField(max_length=100, blank=True, help_text="Collection method")
    
    class Meta:
        db_table = "biomarker_measurement"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["biomarker_name"]),
            models.Index(fields=["measurement_date"]),
            models.Index(fields=["biomarker_category"]),
            models.Index(fields=["result_interpretation"]),
        ]
    
    def __str__(self):
        return f"{self.biomarker_name} for Person {self.person.person_id}: {self.result_interpretation}"

class ClinicalTrialBiomarker(models.Model):
    """
    Specialized model for key biomarkers used in research
    Focus on TMB, PD-L1, MSI, HER2, ER/PR status with standardized thresholds
    """
    biomarker_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='trial_biomarkers')
    biomarker_measurement = models.ForeignKey(BiomarkerMeasurement, null=True, blank=True, on_delete=models.SET_NULL,
                                            help_text="Related biomarker measurement")
    
    # Biomarker identification
    biomarker_type = models.CharField(max_length=50, choices=[
        ('TMB', 'Tumor Mutational Burden'),
        ('PD_L1', 'PD-L1 Expression'),
        ('MSI', 'Microsatellite Instability'),
        ('HER2_IHC', 'HER2 Immunohistochemistry'),
        ('HER2_FISH', 'HER2 Fluorescence In Situ Hybridization'),
        ('ER_STATUS', 'Estrogen Receptor Status'),
        ('PR_STATUS', 'Progesterone Receptor Status'),
        ('TIL', 'Tumor Infiltrating Lymphocytes'),
        ('BRCA_STATUS', 'BRCA Mutation Status'),
        ('NTRK_FUSION', 'NTRK Gene Fusion'),
        ('CDK4_6', 'CDK4/6 Expression'),
        ('PI3K_AKT', 'PI3K/AKT Pathway'),
    ], help_text="Type of biomarker")
    
    # Test details
    test_date = models.DateField(help_text="Date of biomarker testing")
    test_method = models.CharField(max_length=100, choices=[
        ('IHC', 'Immunohistochemistry'),
        ('FISH', 'Fluorescence In Situ Hybridization'),
        ('NGS', 'Next Generation Sequencing'),
        ('PCR', 'Polymerase Chain Reaction'),
        ('WES', 'Whole Exome Sequencing'),
        ('WGS', 'Whole Genome Sequencing'),
        ('FLOW_CYTOMETRY', 'Flow Cytometry'),
        ('ELISA', 'Enzyme-Linked Immunosorbent Assay'),
    ], help_text="Testing methodology")
    
    # Results and interpretation
    numeric_value = models.FloatField(null=True, blank=True, help_text="Numeric result value")
    unit = models.CharField(max_length=50, blank=True, help_text="Unit of measurement")
    categorical_result = models.CharField(max_length=50, choices=[
        ('POSITIVE', 'Positive'),
        ('NEGATIVE', 'Negative'),
        ('HIGH', 'High'),
        ('LOW', 'Low'),
        ('INTERMEDIATE', 'Intermediate'),
        ('EQUIVOCAL', 'Equivocal'),
        ('MSI_HIGH', 'MSI-High'),
        ('MSI_LOW', 'MSI-Low'),
        ('MSS', 'Microsatellite Stable'),
        ('HER2_0', 'HER2 0'),
        ('HER2_1PLUS', 'HER2 1+'),
        ('HER2_2PLUS', 'HER2 2+'),
        ('HER2_3PLUS', 'HER2 3+'),
        ('AMPLIFIED', 'Amplified'),
        ('NOT_AMPLIFIED', 'Not Amplified'),
    ], blank=True, help_text="Categorical interpretation")
    
    # Biomarker thresholds
    threshold_value = models.FloatField(null=True, blank=True, help_text="Threshold value used")
    threshold_description = models.CharField(max_length=200, blank=True, help_text="Description of threshold criteria")
    
    # Assay-specific details
    assay_name = models.CharField(max_length=200, blank=True, help_text="Specific assay/kit used")
    assay_manufacturer = models.CharField(max_length=200, blank=True, help_text="Assay manufacturer")
    assay_version = models.CharField(max_length=50, blank=True, help_text="Assay version")
    
    # Sample context
    specimen_type = models.CharField(max_length=100, blank=True, help_text="Specimen type tested")
    tissue_site = models.CharField(max_length=100, blank=True, help_text="Tissue site")
    tumor_content = models.FloatField(null=True, blank=True, help_text="Tumor content percentage")
    
    # Laboratory and quality
    laboratory = models.CharField(max_length=200, blank=True, help_text="Testing laboratory")
    lab_certification = models.CharField(max_length=100, blank=True, help_text="Laboratory certification")
    quality_score = models.CharField(max_length=50, blank=True, help_text="Quality assessment")
    
    # Clinical relevance
    drug_target = models.CharField(max_length=200, blank=True, help_text="Associated drug target")
    
    # External references
    loinc_code = models.CharField(max_length=20, blank=True, help_text="LOINC code")
    snomed_code = models.CharField(max_length=20, blank=True, help_text="SNOMED code")
    
    class Meta:
        db_table = "clinical_trial_biomarker"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["biomarker_type"]),
            models.Index(fields=["test_date"]),
            models.Index(fields=["categorical_result"]),
        ]
        unique_together = [['person', 'biomarker_type', 'test_date', 'assay_name']]
    
    def __str__(self):
        return f"{self.biomarker_type} for Person {self.person.person_id}: {self.categorical_result}"

class UnitConcept(models.Model):
    """
    Unit concepts for measurements
    Maps PatientInfo unit choices to OMOP concepts
    """
    concept = models.OneToOneField(Concept, on_delete=models.CASCADE, primary_key=True)
    
    # Unit categorization
    unit_type = models.CharField(max_length=50, help_text="Type of unit (weight, height, volume, etc.)")
    patient_info_choice_value = models.CharField(max_length=20, blank=True,
                                                help_text="Corresponding PatientInfo choice value")
    conversion_factor_to_standard = models.FloatField(null=True, blank=True,
                                                     help_text="Factor to convert to standard unit")
    standard_unit_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                             related_name='converted_units',
                                             help_text="Standard unit concept")
    
    class Meta:
        db_table = "unit_concept"
        indexes = [
            models.Index(fields=["unit_type"]),
            models.Index(fields=["patient_info_choice_value"]),
        ]
    
    def __str__(self):
        return f"{self.unit_type}: {self.concept.concept_name}"

class ClinicalLabTest(models.Model):
    """
    Specialized model for clinical laboratory tests 
    Focus on common safety labs with standardized normal ranges
    """
    lab_test_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='clinical_lab_tests')
    measurement = models.ForeignKey(Measurement, null=True, blank=True, on_delete=models.SET_NULL,
                                   help_text="Related OMOP measurement record")
    
    # Test identification
    test_name = models.CharField(max_length=200, help_text="Laboratory test name")
    test_concept = models.ForeignKey(Concept, on_delete=models.PROTECT,
                                    related_name='lab_tests', help_text="OMOP concept for test")
    loinc_code = models.CharField(max_length=20, blank=True, help_text="LOINC code")
    
    # Test categorization
    test_category = models.CharField(max_length=20, choices=LabTestCategoryChoices.choices,
                                    help_text="Category of laboratory test")
    organ_system = models.CharField(max_length=50, choices=[
        ('HEPATIC', 'Hepatic Function'),
        ('RENAL', 'Renal Function'),
        ('CARDIAC', 'Cardiac Function'),
        ('HEMATOLOGIC', 'Hematologic'),
        ('METABOLIC', 'Metabolic'),
        ('IMMUNOLOGIC', 'Immunologic'),
        ('ENDOCRINE', 'Endocrine'),
        ('INFECTIOUS', 'Infectious Disease'),
    ], blank=True, help_text="Primary organ system")
    
    # Test timing and context
    test_date = models.DateField(help_text="Date of laboratory test")
    collection_time = models.TimeField(null=True, blank=True, help_text="Collection time")
    fasting_status = models.BooleanField(null=True, blank=True, help_text="Fasting status required")
    
    # Results
    numeric_result = models.FloatField(null=True, blank=True, help_text="Numeric result")
    result_unit = models.CharField(max_length=50, blank=True, help_text="Result unit")
    text_result = models.CharField(max_length=200, blank=True, help_text="Text/categorical result")
    
    # Reference ranges and interpretation
    reference_range_low = models.FloatField(null=True, blank=True, help_text="Reference range low")
    reference_range_high = models.FloatField(null=True, blank=True, help_text="Reference range high")
    abnormal_flag = models.CharField(max_length=10, choices=[
        ('N', 'Normal'),
        ('H', 'High'),
        ('L', 'Low'),
        ('HH', 'Critical High'),
        ('LL', 'Critical Low'),
        ('A', 'Abnormal'),
    ], blank=True, help_text="Abnormal flag")
    
    # Grade assessment (CTCAE)
    ctcae_grade = models.IntegerField(null=True, blank=True, choices=[
        (0, 'Grade 0 - Normal'),
        (1, 'Grade 1 - Mild'),
        (2, 'Grade 2 - Moderate'),
        (3, 'Grade 3 - Severe'),
        (4, 'Grade 4 - Life-threatening'),
        (5, 'Grade 5 - Death'),
    ], help_text="CTCAE toxicity grade")
    
    # Laboratory quality
    specimen_type = models.CharField(max_length=50, blank=True, help_text="Specimen type")
    collection_method = models.CharField(max_length=100, blank=True, help_text="Collection method")
    processing_delay = models.IntegerField(null=True, blank=True, help_text="Processing delay in hours")
    
    # Analyzer and methodology
    analyzer_name = models.CharField(max_length=100, blank=True, help_text="Laboratory analyzer")
    methodology = models.CharField(max_length=100, blank=True, help_text="Testing methodology")
    laboratory_name = models.CharField(max_length=200, blank=True, help_text="Testing laboratory")
    
    # Quality flags
    hemolyzed = models.BooleanField(null=True, blank=True, help_text="Hemolyzed specimen")
    lipemic = models.BooleanField(null=True, blank=True, help_text="Lipemic specimen")
    icteric = models.BooleanField(null=True, blank=True, help_text="Icteric specimen")
    
    class Meta:
        db_table = "clinical_lab_test"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["test_date"]),
            models.Index(fields=["test_category"]),
            models.Index(fields=["abnormal_flag"]),
            models.Index(fields=["ctcae_grade"]),
            models.Index(fields=["loinc_code"]),
        ]
    
    def __str__(self):
        return f"{self.test_name} for Person {self.person.person_id}: {self.numeric_result} {self.result_unit}"

class OncologyConcept(models.Model):
    """
    Oncology-specific concept mappings for cancer terminology
    Maps cancer staging, histology, and biomarker concepts to standardized vocabularies
    """
    concept = models.OneToOneField(Concept, on_delete=models.CASCADE, primary_key=True)
    
    # Oncology category classification
    oncology_category = models.CharField(max_length=50, 
                                        help_text="Category (staging, histology, biomarker, site, grade)")
    cancer_type = models.CharField(max_length=100, blank=True,
                                  help_text="Specific cancer type this concept applies to")
    
    # Staging system mapping
    staging_system = models.CharField(max_length=50, blank=True,
                                     help_text="Staging system (AJCC, UICC, etc.)")
    staging_system_version = models.CharField(max_length=20, blank=True,
                                             help_text="Version of staging system")
    
    # ICD-O mappings for topography and morphology
    icdo_topography_code = models.CharField(max_length=10, blank=True,
                                           help_text="ICD-O topography code")
    icdo_morphology_code = models.CharField(max_length=10, blank=True,
                                           help_text="ICD-O morphology code")
    
    # Biomarker information
    biomarker_type = models.CharField(max_length=50, blank=True,
                                     help_text="Type of biomarker (protein, genetic, etc.)")
    measurement_method = models.CharField(max_length=100, blank=True,
                                         help_text="Standard measurement method")
    
    class Meta:
        db_table = "oncology_concept"
        indexes = [
            models.Index(fields=["oncology_category"]),
            models.Index(fields=["cancer_type"]),
            models.Index(fields=["staging_system"]),
            models.Index(fields=["biomarker_type"]),
        ]
    
    def __str__(self):
        return f"{self.oncology_category}: {self.concept.concept_name}"

class Observation(models.Model):
    """
    OMOP Observation model for clinical assessments and findings
    
    NOTE: Disease staging information (T, N, M stages, overall stage, tumor grade)
    should be stored as Observation records, NOT as fields in ConditionOccurrence.
    This follows OMOP CDM principles where staging represents clinical assessments
    about a condition, not properties of the condition occurrence itself.
    """
    observation_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    observation_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT, related_name='observations',
                                           help_text="OMOP concept for what was observed")
    observation_datetime = models.DateTimeField(null=True, blank=True, help_text="Observation datetime (set to midnight if only date known)")
    value_as_number = models.FloatField(null=True, blank=True)
    value_as_string = models.CharField(max_length=255, blank=True)
    value_as_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                        related_name='observation_values', help_text="Concept for categorical values")
    
    # OMOP CDM extensions for observation context
    observation_type_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                                related_name='observation_types', help_text="Type/source of observation")
    qualifier_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                         related_name='observation_qualifiers', help_text="Qualifier for observation")
    unit_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                    related_name='observation_units', help_text="Unit concept")
    provider_id = models.IntegerField(null=True, blank=True, help_text="Provider who made observation")
    visit_occurrence_id = models.IntegerField(null=True, blank=True, help_text="Visit when observed")
    visit_detail_id = models.IntegerField(null=True, blank=True, help_text="Visit detail for observation")
    observation_source_value = models.CharField(max_length=50, blank=True, help_text="Source value")
    observation_source_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                                  related_name='observation_sources', help_text="Source concept")
    unit_source_value = models.CharField(max_length=50, blank=True, help_text="Source unit value")
    qualifier_source_value = models.CharField(max_length=50, blank=True, help_text="Source qualifier value")
    
    # Source classification to complement PatientInfo clinical observations
    observation_source = models.CharField(
        max_length=10, 
        choices=ObservationSourceChoices.choices, 
        blank=True, 
        help_text="Source type of observation"
    )
    
    # Enhanced molecular and genomic observation support
    molecular_test_id = models.ForeignKey('MolecularTest', null=True, blank=True, on_delete=models.SET_NULL,
                                         related_name='observations', help_text="Related molecular test")
    genomic_variant = models.ForeignKey('GenomicVariant', null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='observations', help_text="Related genomic variant")
    
    # Clinical interpretation fields
    clinical_significance = models.CharField(max_length=100, blank=True,
                                            help_text="Clinical significance of observation")
    interpretation_code = models.CharField(max_length=50, blank=True,
                                          help_text="Standardized interpretation code")
    
    # Molecular context
    assay_type = models.CharField(max_length=100, blank=True,
                                 help_text="Type of molecular assay")
    detection_method = models.CharField(max_length=100, blank=True,
                                       help_text="Detection method used")
    
    # Extended observation context from PatientInfo
    performance_score_type = models.CharField(max_length=20, blank=True, help_text="Type of performance score (ECOG, Karnofsky)")
    genetic_test_result = models.TextField(blank=True, help_text="Genetic test results (JSON)")
    mutation_interpretation = models.TextField(blank=True, help_text="Clinical interpretation of genetic findings")
    
    # Clinical assessment extensions
    symptom_severity = models.IntegerField(null=True, blank=True, help_text="Symptom severity score (1-10)")
    functional_status = models.CharField(max_length=50, blank=True, help_text="Functional status assessment")
    quality_of_life_score = models.FloatField(null=True, blank=True, help_text="Quality of life score")
    
    # Behavioral and social observations
    substance_use_type = models.CharField(max_length=50, blank=True, help_text="Type of substance use")
    substance_use_frequency = models.CharField(max_length=50, blank=True, help_text="Frequency of substance use")
    social_support_level = models.CharField(max_length=50, blank=True, help_text="Level of social support")
    caregiver_availability = models.BooleanField(null=True, blank=True, help_text="Caregiver availability status")
    
    # Risk assessment
    infection_risk_category = models.CharField(max_length=50, blank=True, help_text="Infection risk category")
    geographic_risk_exposure = models.TextField(blank=True, help_text="Geographic risk exposure details")
    
    # ===========================================
    # BEHAVIORAL & SOCIAL DETERMINANTS EXTENSIONS
    # ===========================================
    
    # Behavioral observation category
    behavioral_category = models.CharField(
        max_length=30,
        choices=BehavioralObservationChoices.choices,
        blank=True,
        help_text="Category of behavioral/social observation"
    )
    
    # Smoking and tobacco use
    smoking_status = models.CharField(
        max_length=20,
        choices=SmokingStatusChoices.choices,
        blank=True,
        help_text="Current smoking status"
    )
    tobacco_product_type = models.CharField(
        max_length=20,
        choices=TobaccoProductChoices.choices,
        blank=True,
        help_text="Type of tobacco product used"
    )
    pack_years = models.FloatField(
        null=True,
        blank=True,
        help_text="Pack-years of smoking (packs per day × years smoked)"
    )
    smoking_cessation_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date smoking was stopped (for former smokers)"
    )
    
    # Substance use assessment
    substance_use_category = models.CharField(
        max_length=20,
        choices=SubstanceUseChoices.choices,
        blank=True,
        help_text="Category of substance use"
    )
    alcohol_use_level = models.CharField(
        max_length=15,
        choices=AlcoholUseChoices.choices,
        blank=True,
        help_text="Level of alcohol consumption"
    )
    drinks_per_week = models.IntegerField(
        null=True,
        blank=True,
        help_text="Average number of alcoholic drinks per week"
    )
    substance_use_details = models.TextField(
        blank=True,
        help_text="Detailed substance use history and patterns"
    )
    
    # Reproductive and contraceptive health
    contraceptive_method = models.CharField(
        max_length=20,
        choices=ContraceptiveMethodChoices.choices,
        blank=True,
        help_text="Current contraceptive method"
    )
    pregnancy_status = models.CharField(
        max_length=20,
        choices=PregnancyStatusChoices.choices,
        blank=True,
        help_text="Current pregnancy status"
    )
    pregnancy_test_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date of pregnancy test"
    )
    last_menstrual_period = models.DateField(
        null=True,
        blank=True,
        help_text="Date of last menstrual period"
    )
    menopausal_status = models.CharField(
        max_length=25,
        choices=MenopausalStatusChoices.choices,
        blank=True,
        help_text="Menopausal status"
    )
    menopause_age = models.IntegerField(
        null=True,
        blank=True,
        help_text="Age at menopause"
    )
    lactation_status = models.BooleanField(
        null=True,
        blank=True,
        help_text="Currently lactating/breastfeeding"
    )
    
    # Infectious disease status
    infectious_disease_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="Type of infectious disease (HIV, HBV, HCV, etc.)"
    )
    infectious_disease_status = models.CharField(
        max_length=20,
        choices=InfectiousDiseaseStatusChoices.choices,
        blank=True,
        help_text="Status of infectious disease"
    )
    infection_test_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date of infectious disease test"
    )
    infection_test_result = models.CharField(
        max_length=255,
        blank=True,
        help_text="Detailed infectious disease test result"
    )
    vaccination_status = models.CharField(
        max_length=100,
        blank=True,
        help_text="Vaccination status for relevant diseases"
    )
    
    # Social support and caregiver assessment
    caregiver_status = models.CharField(
        max_length=25,
        choices=CaregiverStatusChoices.choices,
        blank=True,
        help_text="Caregiver availability and type"
    )
    caregiver_relationship = models.CharField(
        max_length=100,
        blank=True,
        help_text="Relationship to primary caregiver"
    )
    social_support_score = models.IntegerField(
        null=True,
        blank=True,
        help_text="Quantitative social support assessment score"
    )
    lives_alone = models.BooleanField(
        null=True,
        blank=True,
        help_text="Patient lives alone"
    )
    transportation_access = models.BooleanField(
        null=True,
        blank=True,
        help_text="Has reliable transportation for medical visits"
    )
    
    # Cognitive and mental health assessment
    consent_capability = models.CharField(
        max_length=20,
        choices=ConsentCapabilityChoices.choices,
        blank=True,
        help_text="Capability to provide informed consent"
    )
    mental_health_status = models.CharField(
        max_length=25,
        choices=MentalHealthStatusChoices.choices,
        blank=True,
        help_text="Mental health disorder status"
    )
    cognitive_assessment_score = models.IntegerField(
        null=True,
        blank=True,
        help_text="Cognitive assessment score (MMSE, MoCA, etc.)"
    )
    depression_screening_score = models.IntegerField(
        null=True,
        blank=True,
        help_text="Depression screening score (PHQ-9, etc.)"
    )
    anxiety_screening_score = models.IntegerField(
        null=True,
        blank=True,
        help_text="Anxiety screening score (GAD-7, etc.)"
    )
    
    # Geographic and environmental risk factors
    geographic_risk_category = models.CharField(
        max_length=25,
        choices=GeographicRiskChoices.choices,
        blank=True,
        help_text="Category of geographic risk exposure"
    )
    endemic_disease_exposure = models.TextField(
        blank=True,
        help_text="Exposure to endemic diseases in travel/residence areas"
    )
    occupational_exposure = models.TextField(
        blank=True,
        help_text="Occupational hazard or toxin exposure history"
    )
    environmental_toxin_exposure = models.TextField(
        blank=True,
        help_text="Environmental toxin exposure details"
    )
    
    risk_assessment_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date of comprehensive risk assessment"
    )
    assessment_provider = models.CharField(
        max_length=255,
        blank=True,
        help_text="Provider who performed behavioral/social assessment"
    )
    
    # Data quality and completeness
    behavioral_data_complete = models.BooleanField(
        default=False,
        help_text="Indicates if behavioral assessment is complete"
    )
    social_data_complete = models.BooleanField(
        default=False,
        help_text="Indicates if social determinants assessment is complete"
    )
    assessment_method = models.CharField(
        max_length=100,
        blank=True,
        help_text="Method used for behavioral/social assessment (interview, questionnaire, etc.)"
    )
    
    class Meta:
        db_table = "observation"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["observation_concept"]),
            models.Index(fields=["observation_datetime"]),
            models.Index(fields=["performance_score_type"]),
            models.Index(fields=["genetic_test_result"]),
            # Behavioral and social determinants indexes
            models.Index(fields=["behavioral_category"]),
            models.Index(fields=["smoking_status"]),
            models.Index(fields=["substance_use_category"]),
            models.Index(fields=["alcohol_use_level"]),
            models.Index(fields=["pregnancy_status"]),
            models.Index(fields=["menopausal_status"]),
            models.Index(fields=["infectious_disease_status"]),
            models.Index(fields=["caregiver_status"]),
            models.Index(fields=["consent_capability"]),
            models.Index(fields=["mental_health_status"]),
            models.Index(fields=["geographic_risk_category"]),
            models.Index(fields=["eligible_for_trials"]),
            models.Index(fields=["risk_assessment_date"]),
        ]
    def __str__(self):
        return f"Observation {self.observation_id}"

class DrugExposure(models.Model):
    drug_exposure_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    drug_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT, related_name='drug_exposures',
                                    help_text="OMOP concept for the drug")
    drug_exposure_start_datetime = models.DateTimeField(null=True, blank=True, help_text="Start datetime (set to midnight if only date known)")
    drug_exposure_end_datetime = models.DateTimeField(null=True, blank=True, help_text="End datetime (set to midnight if only date known)")
    route_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                     related_name='drug_routes', help_text="Route of administration concept")
    dose = models.FloatField(null=True, blank=True)
    dose_unit_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                         related_name='drug_dose_units', help_text="Dose unit concept")
    
    # OMOP CDM extensions for drug exposure context
    verbatim_end_date = models.DateField(null=True, blank=True, help_text="Verbatim end date from source")
    drug_type_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                         related_name='drug_types', help_text="Type/source of drug record")
    stop_reason = models.CharField(max_length=20, blank=True, help_text="Reason drug was stopped")
    refills = models.IntegerField(null=True, blank=True, help_text="Number of refills")
    quantity = models.FloatField(null=True, blank=True, help_text="Quantity dispensed")
    days_supply = models.IntegerField(null=True, blank=True, help_text="Days supply")
    sig = models.TextField(blank=True, help_text="Sig/directions for use")
    lot_number = models.CharField(max_length=50, blank=True, help_text="Lot number")
    provider_id = models.IntegerField(null=True, blank=True, help_text="Prescribing provider")
    visit_occurrence_id = models.IntegerField(null=True, blank=True, help_text="Visit when prescribed")
    visit_detail_id = models.IntegerField(null=True, blank=True, help_text="Visit detail for prescription")
    drug_source_value = models.CharField(max_length=50, blank=True, help_text="Source drug value")
    drug_source_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                            related_name='drug_sources', help_text="Source drug concept")
    route_source_value = models.CharField(max_length=50, blank=True, help_text="Source route value")
    dose_unit_source_value = models.CharField(max_length=50, blank=True, help_text="Source dose unit value")
    
    # Therapy line tracking from PatientInfo
    line_of_therapy = models.IntegerField(null=True, blank=True, help_text="Line of therapy (1st, 2nd, 3rd, etc.)")
    therapy_intent = models.CharField(max_length=50, blank=True, help_text="Intent of therapy (curative, palliative, etc.)")
    therapy_regimen = models.CharField(max_length=100, blank=True, help_text="Name of therapy regimen")
    combination_therapy = models.BooleanField(null=True, blank=True, help_text="Part of combination therapy")
    
    # Treatment response and outcomes
    treatment_response = models.CharField(max_length=50, blank=True, help_text="Treatment response")
    response_assessment_date = models.DateField(null=True, blank=True, help_text="Date of response assessment")
    progression_free_survival_days = models.IntegerField(null=True, blank=True, help_text="PFS in days")
    overall_survival_days = models.IntegerField(null=True, blank=True, help_text="OS in days")
    
    # Toxicity and adverse events
    maximum_toxicity_grade = models.IntegerField(null=True, blank=True, help_text="Maximum toxicity grade observed")
    dose_modifications = models.TextField(blank=True, help_text="Dose modifications made (JSON)")
    treatment_delays = models.TextField(blank=True, help_text="Treatment delays (JSON)")
    
    # Supporting therapy indicators
    supportive_therapy = models.BooleanField(null=True, blank=True, help_text="Is this supportive therapy")
    concomitant_medication = models.BooleanField(null=True, blank=True, help_text="Is this concomitant medication")
    washout_period_required = models.BooleanField(null=True, blank=True, help_text="Requires washout period")
    
    # Enhanced treatment line tracking (OHDSI Oncology WG methodology)
    treatment_line = models.ForeignKey('TreatmentLine', null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='drug_exposures', help_text="Associated treatment line")
    treatment_regimen = models.ForeignKey('TreatmentRegimen', null=True, blank=True, on_delete=models.SET_NULL,
                                        related_name='drug_exposures', help_text="Associated regimen")
    
    # Drug classification for treatment line analysis
    drug_classification = models.CharField(max_length=50, choices=DrugClassificationChoices.choices,
                                         blank=True, help_text="Drug classification")
    is_platinum_agent = models.BooleanField(default=False, help_text="Is platinum-based agent")
    is_immunotherapy = models.BooleanField(default=False, help_text="Is immunotherapy")
    is_targeted_therapy = models.BooleanField(default=False, help_text="Is targeted therapy")
    is_novel_agent = models.BooleanField(default=False, help_text="Is investigational agent")
    
    # Regimen role
    regimen_role = models.CharField(max_length=20, choices=[
        ('PRIMARY', 'Primary Agent'),
        ('COMBINATION', 'Combination Agent'),
        ('MAINTENANCE', 'Maintenance Agent'),
        ('SUPPORTIVE', 'Supportive Care'),
        ('PREMEDICATION', 'Premedication'),
    ], blank=True, help_text="Role within regimen")
    
    # Cycle and schedule tracking
    cycle_number = models.IntegerField(null=True, blank=True, help_text="Cycle number within regimen")
    cycle_day = models.IntegerField(null=True, blank=True, help_text="Day within cycle")
    total_cycles_planned = models.IntegerField(null=True, blank=True, help_text="Total planned cycles")
    
    # Clinical trial context
    clinical_trial_drug = models.BooleanField(default=False, help_text="Administered in clinical trial")
    fda_approved_indication = models.BooleanField(null=True, blank=True, help_text="FDA approved for this indication")
    compassionate_use = models.BooleanField(default=False, help_text="Compassionate use program")
    
    # Treatment gaps (for OHDSI methodology)
    gap_before_start_days = models.IntegerField(null=True, blank=True, help_text="Gap before treatment start")
    gap_after_end_days = models.IntegerField(null=True, blank=True, help_text="Gap after treatment end")
    
    class Meta:
        db_table = "drug_exposure"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["drug_concept"]),
            models.Index(fields=["drug_exposure_start_datetime"]),
            models.Index(fields=["line_of_therapy"]),
            models.Index(fields=["therapy_intent"]),
            models.Index(fields=["treatment_response"]),
            models.Index(fields=["treatment_line"]),
            models.Index(fields=["treatment_regimen"]),
            models.Index(fields=["drug_classification"]),
            models.Index(fields=["is_platinum_agent"]),
            models.Index(fields=["is_immunotherapy"]),
            models.Index(fields=["is_targeted_therapy"]),
            models.Index(fields=["clinical_trial_drug"]),
        ]
    def __str__(self):
        return f"DrugExposure {self.drug_exposure_id}"

class ProcedureOccurrence(models.Model):
    procedure_occurrence_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    procedure_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT, related_name='procedures',
                                         help_text="OMOP concept for the procedure")
    procedure_datetime = models.DateTimeField(null=True, blank=True, help_text="Procedure datetime (set to midnight if only date known)")
    
    # OMOP CDM extensions for procedure context
    procedure_type_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                              related_name='procedure_types', help_text="Type/source of procedure")
    modifier_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                        related_name='procedure_modifiers', help_text="Modifier for procedure")
    quantity = models.IntegerField(null=True, blank=True, help_text="Quantity of procedures")
    provider_id = models.IntegerField(null=True, blank=True, help_text="Provider who performed procedure")
    visit_occurrence_id = models.IntegerField(null=True, blank=True, help_text="Visit when procedure occurred")
    visit_detail_id = models.IntegerField(null=True, blank=True, help_text="Visit detail for procedure")
    procedure_source_value = models.CharField(max_length=50, blank=True, help_text="Source procedure value")
    procedure_source_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                                 related_name='procedure_sources', help_text="Source concept")
    modifier_source_value = models.CharField(max_length=50, blank=True, help_text="Source modifier value")
    
    # Extended procedure context from PatientInfo
    procedure_outcome = models.CharField(max_length=100, blank=True, help_text="Outcome of procedure")
    procedure_location = models.CharField(max_length=100, blank=True, help_text="Anatomical location")
    procedure_laterality = models.CharField(max_length=20, blank=True, help_text="Left/Right/Bilateral")
    
    # Transplant-specific fields
    transplant_type = models.CharField(max_length=50, blank=True, help_text="Type of transplant")
    donor_type = models.CharField(max_length=50, blank=True, help_text="Donor type (autologous, allogeneic)")
    stem_cell_source = models.CharField(max_length=50, blank=True, help_text="Source of stem cells")
    conditioning_regimen = models.CharField(max_length=100, blank=True, help_text="Conditioning regimen used")
    
    # Imaging and diagnostic procedures
    imaging_modality = models.CharField(max_length=50, blank=True, help_text="Imaging modality (CT, MRI, PET)")
    contrast_used = models.BooleanField(null=True, blank=True, help_text="Whether contrast was used")
    imaging_results = models.TextField(blank=True, help_text="Imaging results summary")
    
    # Biopsy and pathology procedures
    specimen_type = models.CharField(max_length=50, blank=True, help_text="Type of specimen obtained")
    specimen_adequacy = models.CharField(max_length=50, blank=True, help_text="Specimen adequacy assessment")
    pathology_results = models.TextField(blank=True, help_text="Pathology results")
    
    # Procedure quality and complications
    procedure_success = models.BooleanField(null=True, blank=True, help_text="Whether procedure was successful")
    complications = models.TextField(blank=True, help_text="Complications during procedure")
    anesthesia_type = models.CharField(max_length=50, blank=True, help_text="Type of anesthesia used")
    
    class Meta:
        db_table = "procedure_occurrence"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["procedure_concept"]),
            models.Index(fields=["procedure_datetime"]),
            models.Index(fields=["transplant_type"]),
            models.Index(fields=["imaging_modality"]),
        ]
    def __str__(self):
        return f"Procedure {self.procedure_occurrence_id}"

class Episode(models.Model):
    """
    OMOP Episode model enhanced for oncology progression tracking
    Supports cancer diagnosis episodes, progression events, recurrence, and remission
    """
    episode_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    episode_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT, related_name='episodes',
                                       help_text="OMOP concept for the episode")
    episode_start_date = models.DateField(null=True, blank=True)
    episode_end_date = models.DateField(null=True, blank=True)
    episode_number = models.IntegerField(null=True, blank=True)
    
    # OMOP Oncology Extension for cancer episode tracking
    episode_type = models.CharField(max_length=50, blank=True, 
                                   help_text="Episode type (primary_diagnosis, progression, recurrence, remission)")
    parent_episode = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                      help_text="Parent episode for progression/recurrence tracking")
    
    # Cancer-specific episode data
    primary_cancer_condition = models.ForeignKey('ConditionOccurrence', null=True, blank=True, on_delete=models.SET_NULL,
                                                 help_text="Primary cancer condition for this episode")
    disease_status = models.CharField(max_length=50, blank=True, 
                                     help_text="Disease status (active, remission, progression, recurrence)")
    response_to_treatment = models.CharField(max_length=50, blank=True,
                                           help_text="Response to treatment (complete_response, partial_response, etc.)")
    
    # Episode source and provider information
    episode_source_value = models.CharField(max_length=50, blank=True, help_text="Source episode identifier")
    episode_source_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                              related_name='episode_sources', help_text="Source episode concept")
    
    class Meta:
        db_table = "episode"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["episode_concept"]),
            models.Index(fields=["episode_start_date"]),
            models.Index(fields=["episode_type"]),
            models.Index(fields=["parent_episode"]),
            models.Index(fields=["primary_cancer_condition"]),
        ]
    def __str__(self):
        return f"Episode {self.episode_id} ({self.episode_type})"

class EpisodeEvent(models.Model):
    episode_event_id = models.BigAutoField(primary_key=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    event_field_concept_id = models.IntegerField()
    event_id = models.BigIntegerField()
    class Meta:
        db_table = "episode_event"
        indexes = [
            models.Index(fields=["episode"]),
            models.Index(fields=["event_field_concept_id"]),
        ]
    def __str__(self):
        return f"EpisodeEvent {self.episode_event_id}"

class ClinicalTrialParticipation(models.Model):
    """
    OMOP model for clinical trial participation, complementing the Trial model in exactmodels.py
    This focuses on OMOP CDM compliance and participant tracking
    """
    participation_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='trial_participations')
    
    # Trial identification (links to exactmodels.Trial via external reference)
    trial_source_id = models.CharField(max_length=100, help_text="Reference to Trial.code in exactmodels")
    trial_concept_id = models.IntegerField(null=True, blank=True, help_text="OMOP concept for trial type")
    
    # Participation timeline
    enrollment_date = models.DateField(help_text="Date patient enrolled in trial")
    enrollment_datetime = models.DateTimeField(null=True, blank=True, help_text="Precise enrollment datetime")
    completion_date = models.DateField(null=True, blank=True, help_text="Date participation ended")
    completion_datetime = models.DateTimeField(null=True, blank=True, help_text="Precise completion datetime")
    
    # Participation details
    participation_status = models.CharField(max_length=50, blank=True, help_text="Current participation status")
    randomization_arm = models.CharField(max_length=50, blank=True, help_text="Trial arm assignment")
    withdrawal_reason = models.CharField(max_length=100, blank=True, help_text="Reason for withdrawal if applicable")
    
    # Provider and visit context
    enrolling_provider_id = models.IntegerField(null=True, blank=True, help_text="Provider who enrolled patient")
    enrollment_visit_id = models.IntegerField(null=True, blank=True, help_text="Visit when enrolled")
    
    # Source tracking
    participation_source_value = models.CharField(max_length=50, blank=True, help_text="Source participation ID")
    
    class Meta:
        db_table = "clinical_trial_participation"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["trial_source_id"]),
            models.Index(fields=["enrollment_date"]),
            models.Index(fields=["participation_status"]),
        ]
        unique_together = [['person', 'trial_source_id']]
    
    def __str__(self):
        return f"Trial Participation {self.participation_id} - Person {self.person.person_id} in {self.trial_source_id}"

class VisitOccurrence(models.Model):
    """
    OMOP visit occurrence model to track healthcare encounters
    Complements exactmodels.py by providing structured visit data
    """
    visit_occurrence_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='visits')
    
    # Visit identification and classification
    visit_concept_id = models.IntegerField(help_text="OMOP concept for visit type")
    visit_start_date = models.DateField(help_text="Visit start date")
    visit_start_datetime = models.DateTimeField(null=True, blank=True, help_text="Visit start datetime")
    visit_end_date = models.DateField(help_text="Visit end date")
    visit_end_datetime = models.DateTimeField(null=True, blank=True, help_text="Visit end datetime")
    visit_type_concept_id = models.IntegerField(help_text="Type/source of visit record")
    
    # Provider and location
    provider_id = models.IntegerField(null=True, blank=True, help_text="Primary provider for visit")
    care_site_id = models.IntegerField(null=True, blank=True, help_text="Care site where visit occurred")
    
    # Source tracking
    visit_source_value = models.CharField(max_length=50, blank=True, help_text="Source visit identifier")
    visit_source_concept_id = models.IntegerField(null=True, blank=True, help_text="Source concept ID")
    admitted_from_concept_id = models.IntegerField(null=True, blank=True, help_text="Admission source")
    admitted_from_source_value = models.CharField(max_length=50, blank=True, help_text="Source admission value")
    discharge_to_concept_id = models.IntegerField(null=True, blank=True, help_text="Discharge destination")
    discharge_to_source_value = models.CharField(max_length=50, blank=True, help_text="Source discharge value")
    
    # Preceding visit (for visit chains)
    preceding_visit_occurrence_id = models.IntegerField(null=True, blank=True, help_text="Previous visit ID")
    
    class Meta:
        db_table = "visit_occurrence"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["visit_concept_id"]),
            models.Index(fields=["visit_start_date"]),
            models.Index(fields=["provider_id"]),
        ]
    
    def __str__(self):
        return f"Visit {self.visit_occurrence_id} for Person {self.person.person_id}"

class Specimen(models.Model):
    """
    OMOP specimen model for tracking biological specimens
    Supports genetic testing and laboratory procedures from PatientInfo
    """
    specimen_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='specimens')
    
    # Core specimen information
    specimen_concept_id = models.IntegerField(help_text="OMOP concept for specimen type")
    specimen_type_concept_id = models.IntegerField(help_text="Type/source of specimen record")
    specimen_date = models.DateField(help_text="Date specimen was collected")
    specimen_datetime = models.DateTimeField(null=True, blank=True, help_text="Datetime specimen was collected")
    
    # Collection details
    anatomic_site_concept_id = models.IntegerField(null=True, blank=True, help_text="Anatomic site concept")
    disease_status_concept_id = models.IntegerField(null=True, blank=True, help_text="Disease status at collection")
    quantity = models.FloatField(null=True, blank=True, help_text="Quantity collected")
    unit_concept_id = models.IntegerField(null=True, blank=True, help_text="Unit of quantity")
    
    # Source tracking
    specimen_source_id = models.CharField(max_length=50, blank=True, help_text="Source specimen identifier")
    specimen_source_value = models.CharField(max_length=50, blank=True, help_text="Source specimen value")
    unit_source_value = models.CharField(max_length=50, blank=True, help_text="Source unit value")
    anatomic_site_source_value = models.CharField(max_length=50, blank=True, help_text="Source anatomic site")
    disease_status_source_value = models.CharField(max_length=50, blank=True, help_text="Source disease status")
    
    class Meta:
        db_table = "specimen"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["specimen_concept_id"]),
            models.Index(fields=["specimen_date"]),
        ]
    
    def __str__(self):
        return f"Specimen {self.specimen_id} for Person {self.person.person_id}"

class GenomicVariant(models.Model):
    """
    Enhanced genomic variant model for molecular profiling
    Supports HGVS, ClinVar, COSMIC, GA4GH/Sequence Ontology standards
    Links to OMOP Observation for standardized genetic testing records
    """
    variant_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='genomic_variants')
    observation = models.ForeignKey(Observation, null=True, blank=True, on_delete=models.SET_NULL, 
                                    help_text="Related OMOP observation record")
    
    # Gene and variant identification
    gene_symbol = models.CharField(max_length=20, help_text="Gene symbol (e.g., BRCA1, TP53)")
    gene_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                    related_name='gene_variants', help_text="OMOP concept for gene")
    hgvs_notation = models.CharField(max_length=200, blank=True, help_text="HGVS notation for variant")
    variant_type = models.CharField(max_length=50, choices=GenomicVariantTypeChoices.choices,
                                   blank=True, help_text="Type of variant (SNV, CNV, etc.)")
    chromosome = models.CharField(max_length=10, blank=True, help_text="Chromosome location")
    genomic_position = models.BigIntegerField(null=True, blank=True, help_text="Genomic position")
    
    # Variant details
    reference_allele = models.CharField(max_length=200, blank=True, help_text="Reference allele sequence")
    alternate_allele = models.CharField(max_length=200, blank=True, help_text="Alternate allele sequence")
    variant_allele_frequency = models.FloatField(null=True, blank=True, help_text="Variant allele frequency")
    
    # Clinical interpretation
    clinical_significance = models.CharField(max_length=50, choices=ClinicalSignificanceChoices.choices,
                                            blank=True, help_text="Clinical significance (pathogenic, benign, etc.)")
    interpretation = models.TextField(blank=True, help_text="Clinical interpretation of variant")
    
    # External database identifiers
    clinvar_id = models.CharField(max_length=50, blank=True, help_text="ClinVar variant ID")
    cosmic_id = models.CharField(max_length=50, blank=True, help_text="COSMIC variant ID") 
    dbsnp_id = models.CharField(max_length=50, blank=True, help_text="dbSNP rs ID")
    ga4gh_id = models.CharField(max_length=100, blank=True, help_text="GA4GH variant ID")
    
    # Genomic annotation
    transcript_id = models.CharField(max_length=50, blank=True, help_text="Transcript ID (e.g., ENST)")
    protein_change = models.CharField(max_length=200, blank=True, help_text="Protein change notation")
    consequence_type = models.CharField(max_length=100, blank=True, help_text="Variant consequence type")
    
    # Testing information
    test_date = models.DateField(help_text="Date of genetic testing")
    testing_method = models.CharField(max_length=100, choices=GenomicTestTypeChoices.choices,
                                     blank=True, help_text="Testing method used")
    laboratory = models.CharField(max_length=100, blank=True, help_text="Testing laboratory")
    test_kit = models.CharField(max_length=100, blank=True, help_text="Specific test kit or panel used")
    
    # Quality metrics
    read_depth = models.IntegerField(null=True, blank=True, help_text="Sequencing read depth")
    quality_score = models.FloatField(null=True, blank=True, help_text="Variant quality score")
    allele_fraction = models.FloatField(null=True, blank=True, help_text="Tumor allele fraction")
    
    # Molecular classification
    molecular_alteration = models.CharField(max_length=50, choices=MolecularAlterationChoices.choices,
                                           blank=True, help_text="Standardized molecular alteration type")
    biomarker_status = models.CharField(max_length=10, choices=BiomarkerStatusChoices.choices,
                                       blank=True, help_text="Biomarker status")
    
    # Copy number and expression data
    copy_number = models.FloatField(null=True, blank=True, help_text="Copy number value")
    expression_level = models.FloatField(null=True, blank=True, help_text="Gene expression level")
    
    class Meta:
        db_table = "genomic_variant"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["gene_symbol"]),
            models.Index(fields=["test_date"]),
            models.Index(fields=["clinical_significance"]),
            models.Index(fields=["molecular_alteration"]),
            models.Index(fields=["biomarker_status"]),
            models.Index(fields=["clinvar_id"]),
            models.Index(fields=["cosmic_id"]),
        ]
        unique_together = [['person', 'gene_symbol', 'hgvs_notation', 'test_date']]
    
    def __str__(self):
        return f"{self.gene_symbol} variant for Person {self.person.person_id}"

class GenomicConcept(models.Model):
    """
    Maps genomic terms to OMOP standard vocabulary
    Supports OHDSI Genomic Vocabulary integration
    """
    concept = models.OneToOneField(Concept, on_delete=models.CASCADE, primary_key=True)
    
    # Genomic categorization
    genomic_category = models.CharField(max_length=50, choices=[
        ('GENE', 'Gene'),
        ('VARIANT', 'Variant'),
        ('CONSEQUENCE', 'Consequence'),
        ('PATHWAY', 'Pathway'),
        ('BIOMARKER', 'Biomarker'),
        ('SIGNATURE', 'Gene Signature'),
    ], help_text="Category of genomic concept")
    
    # Gene information
    gene_symbol = models.CharField(max_length=20, blank=True, help_text="Official gene symbol")
    gene_aliases = models.TextField(blank=True, help_text="Alternative gene names/symbols")
    chromosome = models.CharField(max_length=10, blank=True, help_text="Chromosome location")
    
    # External mappings
    hgnc_id = models.CharField(max_length=20, blank=True, help_text="HGNC gene ID")
    ensembl_gene_id = models.CharField(max_length=20, blank=True, help_text="Ensembl gene ID")
    ncbi_gene_id = models.CharField(max_length=20, blank=True, help_text="NCBI Gene ID")
    
    # Clinical relevance
    clinical_actionability = models.CharField(max_length=20, choices=[
        ('HIGH', 'High'),
        ('MODERATE', 'Moderate'),
        ('LOW', 'Low'),
        ('UNKNOWN', 'Unknown'),
    ], blank=True, help_text="Clinical actionability level")
    
    therapeutic_implications = models.TextField(blank=True, 
                                              help_text="Known therapeutic implications")
    
    class Meta:
        db_table = "genomic_concept"
        indexes = [
            models.Index(fields=["genomic_category"]),
            models.Index(fields=["gene_symbol"]),
            models.Index(fields=["clinical_actionability"]),
        ]
    
    def __str__(self):
        return f"Genomic {self.genomic_category}: {self.concept.concept_name}"

class CuratedBiomarkerVocabulary(models.Model):
    """
    Curated vocabulary for biomarker and lab test standardization
    Site-specific mappings for non-standardized biomarkers used in clinical practice
    """
    vocabulary_id = models.BigAutoField(primary_key=True)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='curated_biomarkers')
    
    # Biomarker identification
    biomarker_name = models.CharField(max_length=200, help_text="Standard biomarker name")
    biomarker_aliases = models.TextField(blank=True, help_text="Alternative names/synonyms")
    biomarker_category = models.CharField(max_length=50, choices=BiomarkerCategoryChoices.choices,
                                         help_text="Biomarker category")
    
    # Standardization mappings
    loinc_code = models.CharField(max_length=20, blank=True, help_text="LOINC code if available")
    snomed_code = models.CharField(max_length=20, blank=True, help_text="SNOMED code if available")
    hgnc_gene_symbol = models.CharField(max_length=20, blank=True, help_text="HGNC gene symbol")
    
    # Clinical context
    cancer_types = models.TextField(blank=True, help_text="Applicable cancer types")
    clinical_utility = models.TextField(help_text="Clinical utility description")
    
    # Standardized thresholds
    positive_threshold = models.FloatField(null=True, blank=True, help_text="Threshold for positive result")
    high_threshold = models.FloatField(null=True, blank=True, help_text="Threshold for high expression")
    units = models.CharField(max_length=50, blank=True, help_text="Standard units")
    
    # Assay information
    preferred_assays = models.TextField(blank=True, help_text="Preferred/validated assays")
    fda_approved_assays = models.TextField(blank=True, help_text="FDA-approved companion diagnostics")
    
    # Evidence level
    evidence_level = models.CharField(max_length=20, choices=[
        ('LEVEL_1', 'Level 1 - FDA approved'),
        ('LEVEL_2A', 'Level 2A - Professional guidelines'),
        ('LEVEL_2B', 'Level 2B - Expert consensus'),
        ('LEVEL_3', 'Level 3 - Emerging evidence'),
        ('LEVEL_4', 'Level 4 - Investigational'),
    ], blank=True, help_text="Evidence level for clinical utility")
    
    # Site-specific mappings
    site_specific_codes = models.JSONField(null=True, blank=True, 
                                          help_text="Site-specific codes and mappings")
    local_reference_ranges = models.JSONField(null=True, blank=True,
                                             help_text="Local reference ranges by laboratory")
    
    # Metadata
    created_date = models.DateField(auto_now_add=True, help_text="Date added to vocabulary")
    last_updated = models.DateField(auto_now=True, help_text="Last update date")
    curator = models.CharField(max_length=200, blank=True, help_text="Curator/reviewer")
    
    class Meta:
        db_table = "curated_biomarker_vocabulary"
        indexes = [
            models.Index(fields=["biomarker_name"]),
            models.Index(fields=["biomarker_category"]),
            models.Index(fields=["loinc_code"]),
            models.Index(fields=["evidence_level"]),
        ]
        unique_together = [['biomarker_name', 'biomarker_category']]
    
    def __str__(self):
        return f"{self.biomarker_name} ({self.biomarker_category})"

# ==========================================
# BEHAVIORAL & SOCIAL DETERMINANTS VOCABULARIES
# ==========================================

class BehavioralVocabulary(models.Model):
    """
    Standardized vocabulary for behavioral observations in clinical trials
    Maps behavioral assessments to OMOP concepts for smoking, substance use, etc.
    """
    vocabulary_id = models.BigAutoField(primary_key=True)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='behavioral_concepts')
    
    # Behavioral observation identification
    observation_type = models.CharField(max_length=30, choices=BehavioralObservationChoices.choices,
                                       help_text="Type of behavioral observation")
    observation_name = models.CharField(max_length=200, help_text="Standardized observation name")
    observation_aliases = models.TextField(blank=True, help_text="Alternative names/terms")
    
    # Standardization mappings
    loinc_code = models.CharField(max_length=20, blank=True, help_text="LOINC code for observation")
    snomed_code = models.CharField(max_length=20, blank=True, help_text="SNOMED code for observation")
    icd10_code = models.CharField(max_length=10, blank=True, help_text="ICD-10 code if applicable")
    
    # Clinical trial relevance
    exclusion_criterion = models.BooleanField(default=False, 
                                             help_text="Commonly used as exclusion criterion")
    inclusion_criterion = models.BooleanField(default=False,
                                             help_text="Commonly used as inclusion criterion")
    risk_assessment_factor = models.BooleanField(default=False,
                                                help_text="Used for risk assessment")
    
    # Assessment methodology
    assessment_method = models.TextField(blank=True, help_text="Standard assessment methodology")
    validated_instruments = models.TextField(blank=True, help_text="Validated assessment instruments")
    clinical_cutoffs = models.JSONField(null=True, blank=True, 
                                       help_text="Clinical cutoffs and thresholds")
    
    # Clinical context
    applicable_populations = models.TextField(blank=True, help_text="Applicable patient populations")
    contraindications = models.TextField(blank=True, help_text="When not to assess")
    clinical_significance = models.TextField(help_text="Clinical significance description")
    
    # Metadata
    created_date = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    curator = models.CharField(max_length=200, blank=True, help_text="Curator/reviewer")
    
    class Meta:
        db_table = "behavioral_vocabulary"
        indexes = [
            models.Index(fields=["observation_type"]),
            models.Index(fields=["observation_name"]),
            models.Index(fields=["loinc_code"]),
            models.Index(fields=["exclusion_criterion"]),
            models.Index(fields=["inclusion_criterion"]),
        ]
        unique_together = [['observation_type', 'observation_name']]
    
    def __str__(self):
        return f"{self.observation_name} ({self.observation_type})"

class SocialDeterminantsVocabulary(models.Model):
    """
    Standardized vocabulary for social determinants of health
    Maps social factors affecting clinical trial participation and outcomes
    """
    vocabulary_id = models.BigAutoField(primary_key=True)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='social_determinant_concepts')
    
    # Social determinant identification
    determinant_category = models.CharField(max_length=50, help_text="Category of social determinant")
    determinant_name = models.CharField(max_length=200, help_text="Standardized determinant name")
    determinant_aliases = models.TextField(blank=True, help_text="Alternative names/terms")
    
    # Standardization mappings
    loinc_code = models.CharField(max_length=20, blank=True, help_text="LOINC code for determinant")
    snomed_code = models.CharField(max_length=20, blank=True, help_text="SNOMED code for determinant")
    z_code = models.CharField(max_length=10, blank=True, help_text="ICD-10 Z-code for social factor")
    
    # Clinical impacts
    affects_compliance = models.BooleanField(default=False,
                                            help_text="Affects treatment compliance")
    affects_outcomes = models.BooleanField(default=False,
                                          help_text="Affects clinical outcomes")
    
    # Assessment details
    assessment_method = models.TextField(blank=True, help_text="How to assess this determinant")
    screening_questions = models.JSONField(null=True, blank=True,
                                          help_text="Standard screening questions")
    intervention_options = models.TextField(blank=True, help_text="Possible interventions")
    
    # Clinical significance
    health_impact_level = models.CharField(max_length=10, choices=[
        ('HIGH', 'High Impact'),
        ('MODERATE', 'Moderate Impact'),
        ('LOW', 'Low Impact'),
        ('UNKNOWN', 'Unknown Impact'),
    ], blank=True, help_text="Level of health impact")
    
    evidence_base = models.TextField(blank=True, help_text="Evidence for health impact")
    clinical_recommendations = models.TextField(blank=True, help_text="Clinical practice recommendations")
    
    # Geographic and demographic factors
    geographic_specificity = models.CharField(max_length=100, blank=True,
                                             help_text="Geographic areas where relevant")
    demographic_specificity = models.CharField(max_length=100, blank=True,
                                              help_text="Specific demographic groups")
    
    # Metadata
    created_date = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    curator = models.CharField(max_length=200, blank=True, help_text="Curator/reviewer")
    
    class Meta:
        db_table = "social_determinants_vocabulary"
        indexes = [
            models.Index(fields=["determinant_category"]),
            models.Index(fields=["determinant_name"]),
            models.Index(fields=["z_code"]),
            models.Index(fields=["health_impact_level"]),
        ]
        unique_together = [['determinant_category', 'determinant_name']]
    
    def __str__(self):
        return f"{self.determinant_name} ({self.determinant_category})"

class InfectiousDiseaseVocabulary(models.Model):
    """
    Standardized vocabulary for infectious disease status in clinical trials
    Maps infectious disease assessments to OMOP concepts
    """
    vocabulary_id = models.BigAutoField(primary_key=True)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='infectious_disease_concepts')
    
    # Disease identification
    disease_name = models.CharField(max_length=200, help_text="Standardized disease name")
    disease_aliases = models.TextField(blank=True, help_text="Alternative names/abbreviations")
    pathogen_type = models.CharField(max_length=20, choices=[
        ('VIRUS', 'Viral'),
        ('BACTERIA', 'Bacterial'),
        ('FUNGUS', 'Fungal'),
        ('PARASITE', 'Parasitic'),
        ('PRION', 'Prion'),
        ('OTHER', 'Other'),
    ], help_text="Type of pathogen")
    
    # Standardization mappings
    icd10_code = models.CharField(max_length=10, blank=True, help_text="ICD-10 code")
    snomed_code = models.CharField(max_length=20, blank=True, help_text="SNOMED code")
    
    # Clinical trial relevance
    exclusion_criterion = models.BooleanField(default=False,
                                             help_text="Commonly used as exclusion criterion")
    requires_monitoring = models.BooleanField(default=False,
                                             help_text="Requires monitoring during treatment")
    drug_interaction_risk = models.BooleanField(default=False,
                                               help_text="Risk of drug interactions")
    
    # Testing information
    standard_tests = models.JSONField(null=True, blank=True,
                                     help_text="Standard diagnostic tests")
    test_interpretation = models.TextField(blank=True, help_text="Test result interpretation")
    screening_recommendations = models.TextField(blank=True, help_text="Screening recommendations")
    
    # Clinical management
    treatment_considerations = models.TextField(blank=True, 
                                               help_text="Treatment considerations for trials")
    monitoring_requirements = models.TextField(blank=True,
                                              help_text="Monitoring requirements")
    precautions = models.TextField(blank=True, help_text="Special precautions")
    
    # Geographic factors
    endemic_regions = models.TextField(blank=True, help_text="Geographic regions where endemic")
    travel_risk_areas = models.TextField(blank=True, help_text="Travel-related risk areas")
    
    # Metadata
    created_date = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    curator = models.CharField(max_length=200, blank=True, help_text="Curator/reviewer")
    
    class Meta:
        db_table = "infectious_disease_vocabulary"
        indexes = [
            models.Index(fields=["disease_name"]),
            models.Index(fields=["pathogen_type"]),
            models.Index(fields=["icd10_code"]),
            models.Index(fields=["exclusion_criterion"]),
            models.Index(fields=["requires_monitoring"]),
        ]
        unique_together = [['disease_name', 'pathogen_type']]
    
    def __str__(self):
        return f"{self.disease_name} ({self.pathogen_type})"

class MolecularTest(models.Model):
    """
    Represents comprehensive molecular testing panels
    Links genomic variants to standardized test reports
    """
    test_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='molecular_tests')
    observation = models.ForeignKey(Observation, null=True, blank=True, on_delete=models.SET_NULL,
                                   help_text="Related OMOP observation record")
    
    # Test identification
    test_name = models.CharField(max_length=200, help_text="Name of molecular test/panel")
    test_type = models.CharField(max_length=50, choices=GenomicTestTypeChoices.choices,
                                help_text="Type of molecular testing")
    test_date = models.DateField(help_text="Date of testing")
    
    # Laboratory information
    laboratory = models.CharField(max_length=200, help_text="Testing laboratory")
    laboratory_id = models.CharField(max_length=50, blank=True, help_text="Laboratory identifier")
    test_version = models.CharField(max_length=50, blank=True, help_text="Test version/kit version")
    
    # Sample information
    specimen_type = models.CharField(max_length=100, help_text="Type of specimen tested")
    specimen_site = models.CharField(max_length=100, blank=True, help_text="Anatomical site of specimen")
    collection_date = models.DateField(null=True, blank=True, help_text="Specimen collection date")
    
    # Test results summary
    overall_result = models.CharField(max_length=50, choices=[
        ('POSITIVE', 'Positive'),
        ('NEGATIVE', 'Negative'),
        ('INDETERMINATE', 'Indeterminate'),
        ('FAILED', 'Failed'),
    ], help_text="Overall test result")
    
    # Quality metrics
    tumor_content = models.FloatField(null=True, blank=True, help_text="Tumor content percentage")
    dna_quality = models.CharField(max_length=50, blank=True, help_text="DNA quality assessment")
    
    # Clinical relevance
    actionable_alterations_count = models.IntegerField(default=0, 
                                                      help_text="Number of actionable alterations found")
    
    # Report information
    report_date = models.DateField(null=True, blank=True, help_text="Date of report")
    report_url = models.URLField(blank=True, help_text="URL to full report")
    raw_data_available = models.BooleanField(default=False, help_text="Raw sequencing data available")
    
    class Meta:
        db_table = "molecular_test"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["test_date"]),
            models.Index(fields=["test_type"]),
            models.Index(fields=["overall_result"]),
            models.Index(fields=["trial_eligible"]),
        ]
    
    def __str__(self):
        return f"{self.test_name} for Person {self.person.person_id}"

class TreatmentLine(models.Model):
    """
    OMOP Oncology Extension for treatment line tracking
    Implements OHDSI Oncology WG principles for treatment line analysis
    Supports Artemis project methodologies for treatment line calculation
    """
    treatment_line_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='treatment_lines')
    condition_occurrence = models.ForeignKey('ConditionOccurrence', on_delete=models.CASCADE,
                                           related_name='treatment_lines', 
                                           help_text="Primary condition being treated")
    
    # Treatment line identification
    line_number = models.IntegerField(help_text="Treatment line number (1, 2, 3, etc.)")
    line_sequence = models.CharField(max_length=10, choices=TherapyLineChoices.choices,
                                   help_text="Standardized line designation")
    
    # Temporal boundaries (following OHDSI methodology)
    line_start_date = models.DateField(help_text="Start date of treatment line")
    line_end_date = models.DateField(null=True, blank=True, help_text="End date of treatment line")
    
    # Treatment characteristics
    treatment_intent = models.CharField(max_length=50, choices=TherapyIntentChoices.choices,
                                      help_text="Intent of treatment line")
    treatment_status = models.CharField(max_length=20, choices=TreatmentLineStatusChoices.choices,
                                       blank=True, help_text="Treatment status at line start")
    
    # Regimen classification
    regimen_name = models.CharField(max_length=200, blank=True, help_text="Standard regimen name")
    regimen_type = models.CharField(max_length=20, choices=RegimenTypeChoices.choices,
                                   blank=True, help_text="Type of regimen")
    drug_classifications = models.JSONField(default=list, 
                                          help_text="List of drug classifications in this line")
    
    # Treatment categorization
    platinum_based = models.BooleanField(default=False, help_text="Contains platinum-based therapy")
    immunotherapy_based = models.BooleanField(default=False, help_text="Contains immunotherapy")
    targeted_therapy_based = models.BooleanField(default=False, help_text="Contains targeted therapy")
    hormone_therapy_based = models.BooleanField(default=False, help_text="Contains hormone therapy")
    
    # Treatment outcomes
    treatment_response = models.CharField(max_length=20, choices=TreatmentResponseChoices.choices,
                                        blank=True, help_text="Best response achieved")
    progression_free_survival_days = models.IntegerField(null=True, blank=True, 
                                                        help_text="PFS duration in days")
    time_to_progression_days = models.IntegerField(null=True, blank=True,
                                                  help_text="Time to progression in days")
    treatment_outcome = models.CharField(max_length=20, choices=TreatmentOutcomeChoices.choices,
                                       blank=True, help_text="Reason treatment line ended")
    
    # Clinical trial context
    received_in_trial = models.BooleanField(default=False, help_text="Received as part of clinical trial")
    trial_identifier = models.CharField(max_length=100, blank=True, help_text="Clinical trial identifier")
    
    # OHDSI Artemis methodology fields
    line_calculation_method = models.CharField(max_length=100, blank=True,
                                             help_text="Method used to calculate treatment line")
    gap_threshold_days = models.IntegerField(default=30, 
                                           help_text="Gap threshold for line determination")
    combination_window_days = models.IntegerField(default=60,
                                                help_text="Window for combination therapy grouping")
    
    # Quality and validation
    data_source = models.CharField(max_length=100, blank=True, help_text="Source of treatment data")
    calculated_automatically = models.BooleanField(default=False, 
                                                  help_text="Calculated via automated algorithm")
    manually_reviewed = models.BooleanField(default=False, help_text="Manually reviewed by clinician")
    confidence_score = models.FloatField(null=True, blank=True, 
                                       help_text="Confidence in line assignment (0-1)")
    
    class Meta:
        db_table = "treatment_line"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["condition_occurrence"]),
            models.Index(fields=["line_number"]),
            models.Index(fields=["line_start_date"]),
            models.Index(fields=["treatment_intent"]),
            models.Index(fields=["platinum_based"]),
            models.Index(fields=["immunotherapy_based"]),
            models.Index(fields=["targeted_therapy_based"]),
            models.Index(fields=["treatment_response"]),
        ]
        unique_together = [['person', 'condition_occurrence', 'line_number']]
    
    def __str__(self):
        return f"Treatment Line {self.line_number} for Person {self.person.person_id}"

class TreatmentRegimen(models.Model):
    """
    Detailed regimen tracking within treatment lines
    Links individual drug exposures and procedures into cohesive treatment episodes
    """
    regimen_id = models.BigAutoField(primary_key=True)
    treatment_line = models.ForeignKey(TreatmentLine, on_delete=models.CASCADE, 
                                     related_name='regimens')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='treatment_regimens')
    
    # Regimen identification
    regimen_name = models.CharField(max_length=200, help_text="Standard regimen name")
    regimen_code = models.CharField(max_length=50, blank=True, help_text="Standard regimen code")
    regimen_sequence = models.IntegerField(help_text="Sequence within treatment line")
    
    # Temporal boundaries
    regimen_start_date = models.DateField(help_text="Start date of regimen")
    regimen_end_date = models.DateField(null=True, blank=True, help_text="End date of regimen")
    
    # Regimen characteristics
    regimen_type = models.CharField(max_length=20, choices=RegimenTypeChoices.choices,
                                   help_text="Type of regimen")
    number_of_cycles_planned = models.IntegerField(null=True, blank=True,
                                                  help_text="Planned number of cycles")
    number_of_cycles_completed = models.IntegerField(null=True, blank=True,
                                                    help_text="Completed number of cycles")
    
    # Drug classifications within regimen
    contains_platinum = models.BooleanField(default=False, help_text="Contains platinum agent")
    contains_immunotherapy = models.BooleanField(default=False, help_text="Contains immunotherapy")
    contains_targeted_therapy = models.BooleanField(default=False, help_text="Contains targeted therapy")
    contains_chemotherapy = models.BooleanField(default=False, help_text="Contains chemotherapy")
    contains_hormone_therapy = models.BooleanField(default=False, help_text="Contains hormone therapy")
    
    # Outcomes and response
    best_response = models.CharField(max_length=20, choices=TreatmentResponseChoices.choices,
                                   blank=True, help_text="Best response to regimen")
    toxicity_grade_max = models.IntegerField(null=True, blank=True, choices=[
        (1, 'Grade 1 - Mild'),
        (2, 'Grade 2 - Moderate'), 
        (3, 'Grade 3 - Severe'),
        (4, 'Grade 4 - Life-threatening'),
        (5, 'Grade 5 - Death'),
    ], help_text="Maximum toxicity grade")
    
    # Regimen modifications
    dose_reductions = models.IntegerField(default=0, help_text="Number of dose reductions")
    treatment_delays = models.IntegerField(default=0, help_text="Number of treatment delays")
    early_discontinuation = models.BooleanField(default=False, help_text="Discontinued early")
    discontinuation_reason = models.CharField(max_length=200, blank=True,
                                            help_text="Reason for discontinuation")
    
    # Clinical context
    performance_status_start = models.CharField(max_length=20, 
                                              choices=PerformanceStatusChoices.choices,
                                              blank=True, help_text="Performance status at start")
    comorbidity_score = models.FloatField(null=True, blank=True, help_text="Comorbidity score")
    
    class Meta:
        db_table = "treatment_regimen"
        indexes = [
            models.Index(fields=["treatment_line"]),
            models.Index(fields=["person"]),
            models.Index(fields=["regimen_start_date"]),
            models.Index(fields=["regimen_sequence"]),
            models.Index(fields=["contains_platinum"]),
            models.Index(fields=["contains_immunotherapy"]),
            models.Index(fields=["best_response"]),
        ]
        unique_together = [['treatment_line', 'regimen_sequence']]
    
    def __str__(self):
        return f"{self.regimen_name} (Sequence {self.regimen_sequence})"

class TreatmentLineComponent(models.Model):
    """
    Links individual drug exposures and procedures to treatment lines and regimens
    Enables reconstruction of complete treatment episodes for therapy analysis
    """
    component_id = models.BigAutoField(primary_key=True)
    treatment_line = models.ForeignKey(TreatmentLine, on_delete=models.CASCADE,
                                     related_name='components')
    treatment_regimen = models.ForeignKey(TreatmentRegimen, null=True, blank=True,
                                        on_delete=models.CASCADE, related_name='components')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, 
                              related_name='treatment_components')
    
    # Component identification
    component_type = models.CharField(max_length=20, choices=[
        ('DRUG', 'Drug Exposure'),
        ('PROCEDURE', 'Procedure'),
        ('RADIATION', 'Radiation Therapy'),
        ('SURGERY', 'Surgical Procedure'),
    ], help_text="Type of treatment component")
    
    # Links to OMOP domain tables
    drug_exposure = models.ForeignKey('DrugExposure', null=True, blank=True, on_delete=models.CASCADE,
                                    help_text="Related drug exposure")
    procedure_occurrence = models.ForeignKey('ProcedureOccurrence', null=True, blank=True, 
                                           on_delete=models.CASCADE,
                                           help_text="Related procedure")
    
    # Component characteristics
    component_role = models.CharField(max_length=20, choices=[
        ('PRIMARY', 'Primary Agent'),
        ('COMBINATION', 'Combination Agent'),
        ('SUPPORTIVE', 'Supportive Care'),
        ('PREMEDICATION', 'Premedication'),
    ], help_text="Role within treatment line")
    
    drug_classification = models.CharField(max_length=50, choices=DrugClassificationChoices.choices,
                                         blank=True, help_text="Drug classification")
    
    # Temporal context
    component_start_date = models.DateField(help_text="Start date of component")
    component_end_date = models.DateField(null=True, blank=True, help_text="End date of component")
    
    # Drug classification flags
    is_platinum_agent = models.BooleanField(default=False, help_text="Is platinum-based agent")
    is_immunotherapy = models.BooleanField(default=False, help_text="Is immunotherapy agent")
    is_targeted_therapy = models.BooleanField(default=False, help_text="Is targeted therapy")
    is_novel_agent = models.BooleanField(default=False, help_text="Is novel/investigational agent")
    
    # FDA approval status
    fda_approved = models.BooleanField(null=True, blank=True, help_text="FDA approved for indication")
    approval_date = models.DateField(null=True, blank=True, help_text="FDA approval date")
    off_label_use = models.BooleanField(default=False, help_text="Used off-label")
    
    # Clinical context
    indication_concept = models.ForeignKey(Concept, null=True, blank=True, on_delete=models.PROTECT,
                                         related_name='treatment_indications',
                                         help_text="Indication for treatment component")
    
    class Meta:
        db_table = "treatment_line_component"
        indexes = [
            models.Index(fields=["treatment_line"]),
            models.Index(fields=["treatment_regimen"]),
            models.Index(fields=["person"]),
            models.Index(fields=["component_type"]),
            models.Index(fields=["drug_classification"]),
            models.Index(fields=["is_platinum_agent"]),
            models.Index(fields=["is_immunotherapy"]),
            models.Index(fields=["component_start_date"]),
        ]
    
    def __str__(self):
        return f"Component {self.component_id} in Line {self.treatment_line.line_number}"

class ImagingStudy(models.Model):
    """
    OMOP Imaging Extension for comprehensive imaging study tracking
    Supports clinical trial imaging requirements and response assessments
    """
    imaging_study_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='imaging_studies')
    procedure_occurrence = models.ForeignKey(ProcedureOccurrence, null=True, blank=True, on_delete=models.SET_NULL,
                                           help_text="Related OMOP procedure occurrence")
    
    # Study identification
    study_uid = models.CharField(max_length=64, unique=True, help_text="DICOM Study Instance UID")
    accession_number = models.CharField(max_length=50, blank=True, help_text="Accession number")
    study_date = models.DateField(help_text="Date of imaging study")
    study_time = models.TimeField(null=True, blank=True, help_text="Time of imaging study")
    
    # Imaging modality and technique
    modality = models.CharField(max_length=20, choices=ImagingModalityChoices.choices,
                               help_text="Primary imaging modality")
    study_description = models.CharField(max_length=200, blank=True, help_text="Study description")
    body_part_examined = models.CharField(max_length=100, blank=True, help_text="Body part examined")
    
    # Contrast and technique details
    contrast_agent = models.CharField(max_length=20, choices=ImagingContrastChoices.choices,
                                     default='NONE', help_text="Contrast agent used")
    contrast_dose = models.FloatField(null=True, blank=True, help_text="Contrast dose in mL")
    acquisition_protocol = models.CharField(max_length=200, blank=True, help_text="Acquisition protocol")
    
    # Clinical context
    indication = models.TextField(blank=True, help_text="Clinical indication for imaging")
    referring_physician = models.CharField(max_length=200, blank=True, help_text="Referring physician")
    
    # Quality and technical parameters
    image_quality = models.CharField(max_length=50, choices=[
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('ADEQUATE', 'Adequate'),
        ('POOR', 'Poor'),
        ('NON_DIAGNOSTIC', 'Non-diagnostic'),
    ], blank=True, help_text="Overall image quality")
    
    artifacts_present = models.BooleanField(default=False, help_text="Imaging artifacts present")
    artifact_description = models.TextField(blank=True, help_text="Description of artifacts")
    
    # Data storage and access
    dicom_available = models.BooleanField(default=True, help_text="DICOM data available")
    image_count = models.IntegerField(null=True, blank=True, help_text="Number of images in study")
    data_size_mb = models.FloatField(null=True, blank=True, help_text="Data size in MB")
    storage_location = models.CharField(max_length=500, blank=True, help_text="Storage location/URL")
    
    # Clinical trial relevance
    baseline_imaging = models.BooleanField(default=False, help_text="Baseline imaging for trial")
    follow_up_imaging = models.BooleanField(default=False, help_text="Follow-up imaging for trial")
    response_assessment = models.BooleanField(default=False, help_text="Used for response assessment")
    
    class Meta:
        db_table = "imaging_study"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["study_date"]),
            models.Index(fields=["modality"]),
            models.Index(fields=["baseline_imaging"]),
            models.Index(fields=["response_assessment"]),
            models.Index(fields=["study_uid"]),
        ]
    
    def __str__(self):
        return f"{self.modality} study for Person {self.person.person_id} on {self.study_date}"

class ImagingMeasurement(models.Model):
    """
    Quantitative measurements derived from imaging studies
    Supports tumor measurements, response assessment (RECIST), and biomarker quantification
    """
    imaging_measurement_id = models.BigAutoField(primary_key=True)
    imaging_study = models.ForeignKey(ImagingStudy, on_delete=models.CASCADE, related_name='measurements')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='imaging_measurements')
    measurement_record = models.ForeignKey(Measurement, null=True, blank=True, on_delete=models.SET_NULL,
                                          help_text="Related OMOP measurement record")
    
    # Measurement identification
    measurement_concept = models.ForeignKey(Concept, on_delete=models.PROTECT,
                                          related_name='imaging_measurements',
                                          help_text="OMOP concept for measurement type")
    measurement_name = models.CharField(max_length=200, help_text="Name of measurement")
    
    # Anatomical context
    anatomic_region = models.CharField(max_length=100, blank=True, help_text="Anatomical region")
    laterality = models.CharField(max_length=20, choices=TumorLateralityChoices.choices,
                                 blank=True, help_text="Laterality if applicable")
    
    # Measurement values
    numeric_value = models.FloatField(null=True, blank=True, help_text="Numeric measurement value")
    unit = models.CharField(max_length=20, blank=True, help_text="Unit of measurement")
    categorical_value = models.CharField(max_length=100, blank=True, help_text="Categorical result")
    
    # Tumor-specific measurements
    lesion_type = models.CharField(max_length=50, choices=[
        ('TARGET', 'Target Lesion'),
        ('NON_TARGET', 'Non-target Lesion'),
        ('NEW', 'New Lesion'),
        ('UNKNOWN', 'Unknown'),
    ], blank=True, help_text="Type of lesion for RECIST")
    
    lesion_number = models.IntegerField(null=True, blank=True, help_text="Lesion identification number")
    longest_diameter = models.FloatField(null=True, blank=True, help_text="Longest diameter in mm")
    perpendicular_diameter = models.FloatField(null=True, blank=True, help_text="Perpendicular diameter in mm")
    volume = models.FloatField(null=True, blank=True, help_text="Volume in mm³")
    
    # Response assessment
    response_category = models.CharField(max_length=20, choices=TumorResponseChoices.choices,
                                       blank=True, help_text="Response assessment")
    percent_change = models.FloatField(null=True, blank=True, help_text="Percent change from baseline")
    
    # Measurement quality
    measurement_confidence = models.CharField(max_length=20, choices=[
        ('HIGH', 'High Confidence'),
        ('MODERATE', 'Moderate Confidence'),
        ('LOW', 'Low Confidence'),
    ], blank=True, help_text="Confidence in measurement")
    
    reader_name = models.CharField(max_length=200, blank=True, help_text="Name of reader/radiologist")
    measurement_date = models.DateField(help_text="Date measurement was performed")
    
    # Biomarker-derived measurements
    enhancement_pattern = models.CharField(max_length=100, blank=True, help_text="Enhancement pattern")
    signal_intensity = models.CharField(max_length=100, blank=True, help_text="Signal intensity characteristics")
    perfusion_parameters = models.JSONField(null=True, blank=True, help_text="Perfusion parameters JSON")
    
    class Meta:
        db_table = "imaging_measurement"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["imaging_study"]),
            models.Index(fields=["measurement_date"]),
            models.Index(fields=["lesion_type"]),
            models.Index(fields=["response_category"]),
            models.Index(fields=["measurement_concept"]),
        ]
    
    def __str__(self):
        return f"{self.measurement_name} for Person {self.person.person_id}"

class PatientInfo(models.Model):
    """
    Comprehensive patient information model from exactmodels.py
    Integrated with OMOP CDM Person model
    """
    # Link to OMOP Person
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='patient_info')
    
    # Language information
    languages = models.TextField(blank=True, null=True, help_text="Language codes like 'en', 'de', 'es'")
    language_skill_level = models.TextField(blank=True, null=True, help_text="'speak' or 'write'")

    # Demographics
    patient_age = models.IntegerField(help_text="What is the patient's age?", blank=True, null=True)
    gender = models.CharField(
        max_length=2,
        choices=GenderChoices.choices,
        blank=True,
        null=True,
        help_text="Patient's gender"
    )
    weight = models.FloatField(help_text="Patient's weight", blank=True, null=True)
    weight_units = models.CharField(
        max_length=2,
        choices=WeightUnits.choices,
        blank=True,
        null=True,
        default='kg',
        help_text="Units for the patient's weight"
    )
    height = models.FloatField(help_text="Patient's height", blank=True, null=True)
    height_units = models.CharField(
        max_length=2,
        choices=HeightUnits.choices,
        blank=True,
        null=True,
        default='cm',
        help_text="Units for the patient's height"
    )
    bmi = models.FloatField(editable=False, help_text="Patient's BMI (computed)", blank=True, null=True)
    ethnicity = models.TextField(blank=True, null=True)
    systolic_blood_pressure = models.IntegerField(help_text="Patient's systolic blood pressure", blank=True, null=True)
    diastolic_blood_pressure = models.IntegerField(help_text="Patient's diastolic blood pressure", blank=True, null=True)

    # Geographic location
    country = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    # Disease information
    disease = models.TextField(blank=True, null=True, default='multiple myeloma')
    stage = models.TextField(blank=True, null=True)
    karnofsky_performance_score = models.IntegerField(blank=True, null=True, default=100)
    ecog_performance_status = models.IntegerField(blank=True, null=True)
    no_other_active_malignancies = models.BooleanField(blank=False, null=False, default=True)
    no_pre_existing_conditions = models.BooleanField(blank=True, null=True)
    peripheral_neuropathy_grade = models.IntegerField(blank=True, null=True)

    # Myeloma related
    cytogenic_markers = models.TextField(blank=True, null=True)
    molecular_markers = models.TextField(blank=True, null=True)
    stem_cell_transplant_history = models.JSONField(blank=True, null=True, default=list)
    plasma_cell_leukemia = models.BooleanField(blank=True, null=True, default=True)
    progression = models.TextField(blank=True, null=True)

    # Lymphoma related
    gelf_criteria_status = models.TextField(blank=True, null=True)
    flipi_score = models.IntegerField(blank=True, null=True)
    flipi_score_options = models.TextField(blank=True, null=True)
    tumor_grade = models.IntegerField(blank=True, null=True)

    # Vital signs
    heartrate = models.IntegerField(help_text="Patient's heart rate", blank=True, null=True)
    heartrate_variability = models.IntegerField(help_text="Patient's heart rate variability", blank=True, null=True)

    # Legacy condition codes
    condition_code_icd_10 = models.TextField(blank=True, null=True)
    condition_code_snomed_ct = models.TextField(blank=True, null=True)

    # Treatment history
    prior_therapy = models.TextField(blank=True, null=True)
    first_line_therapy = models.TextField(blank=True, null=True)
    first_line_date = models.DateField(blank=True, null=True)
    first_line_outcome = models.TextField(blank=True, null=True)
    second_line_therapy = models.TextField(blank=True, null=True)
    second_line_date = models.DateField(blank=True, null=True)
    second_line_outcome = models.TextField(blank=True, null=True)
    later_therapy = models.TextField(blank=True, null=True)
    later_date = models.DateField(blank=True, null=True)
    later_outcome = models.TextField(blank=True, null=True)
    supportive_therapies = models.TextField(blank=True, null=True)
    supportive_therapy_date = models.DateField(blank=True, null=True)
    relapse_count = models.IntegerField(blank=True, null=True)
    treatment_refractory_status = models.CharField(max_length=255, blank=True, null=True)

    # Legacy therapy fields
    therapy_lines_count = models.IntegerField(blank=True, null=True)
    line_of_therapy = models.TextField(blank=True, null=True)

    # Blood work with units
    absolute_neutrophile_count = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    absolute_neutrophile_count_units = models.CharField(
        max_length=10,
        choices=PlateletCountUnits.choices,
        blank=True,
        null=True,
        default='CELLS/UL'
    )
    platelet_count = models.IntegerField(blank=True, null=True)
    platelet_count_units = models.CharField(
        max_length=10,
        choices=PlateletCountUnits.choices,
        blank=True,
        null=True,
        default='CELLS/UL'
    )
    white_blood_cell_count = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    white_blood_cell_count_units = models.CharField(
        max_length=10,
        choices=PlateletCountUnits.choices,
        blank=True,
        null=True,
        default='CELLS/L'
    )
    red_blood_cell_count = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    red_blood_cell_count_units = models.CharField(
        max_length=10,
        choices=PlateletCountUnits.choices,
        blank=True,
        null=True,
        default='CELLS/L'
    )
    serum_calcium_level = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    serum_calcium_level_units = models.CharField(
        max_length=15,
        choices=SerumCalciumUnits.choices,
        blank=True,
        null=True,
        default='MG/DL'
    )
    creatinine_clearance_rate = models.IntegerField(blank=True, null=True)
    serum_creatinine_level = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    serum_creatinine_level_units = models.CharField(
        max_length=15,
        choices=SerumCreatinineUnits.choices,
        blank=True,
        null=True,
        default='MG/DL'
    )
    hemoglobin_level = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    hemoglobin_level_units = models.CharField(
        max_length=5,
        choices=HemoglobinUnits.choices,
        blank=True,
        null=True,
        default='G/DL'
    )
    bone_lesions = models.TextField(blank=True, null=True)
    meets_crab = models.BooleanField(blank=True, null=True)

    estimated_glomerular_filtration_rate = models.IntegerField(blank=True, null=True)
    renal_adequacy_status = models.BooleanField(blank=True, null=True)
    liver_enzyme_levels_ast = models.IntegerField(blank=True, null=True)
    liver_enzyme_levels_alt = models.IntegerField(blank=True, null=True)
    liver_enzyme_levels_alp = models.IntegerField(blank=True, null=True)
    serum_bilirubin_level_total = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    serum_bilirubin_level_total_units = models.CharField(
        max_length=15,
        choices=SerumBilirubinUnits.choices,
        blank=True,
        null=True,
        default='MG/DL'
    )
    serum_bilirubin_level_direct = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    serum_bilirubin_level_direct_units = models.CharField(
        max_length=15,
        choices=SerumBilirubinUnits.choices,
        blank=True,
        null=True,
        default='MG/DL'
    )
    albumin_level = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    albumin_level_units = models.CharField(
        max_length=15,
        choices=AlbuminUnits.choices,
        blank=True,
        null=True,
        default='G/DL'
    )
    kappa_flc = models.IntegerField(blank=True, null=True)
    lambda_flc = models.IntegerField(blank=True, null=True)
    meets_slim = models.BooleanField(blank=True, null=True)

    # Legacy blood work fields
    liver_enzyme_levels = models.IntegerField(blank=True, null=True)
    serum_bilirubin_level = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    # Laboratory results
    monoclonal_protein_serum = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    monoclonal_protein_urine = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    lactate_dehydrogenase_level = models.IntegerField(blank=True, null=True)
    pulmonary_function_test_result = models.BooleanField(blank=False, null=False, default=False)
    bone_imaging_result = models.BooleanField(blank=False, null=False, default=False)
    clonal_plasma_cells = models.IntegerField(blank=True, null=True)
    ejection_fraction = models.IntegerField(blank=True, null=True)

    # Behavioral and risk factors
    consent_capability = models.BooleanField(help_text="Does the patient have cognitive ability to consent?", blank=False, null=False, default=True)
    caregiver_availability_status = models.BooleanField(help_text="Is there an available caregiver for the patient?", blank=False, null=False, default=False)
    contraceptive_use = models.BooleanField(help_text="Does the patient use contraceptives?", blank=False, null=False, default=False)
    no_pregnancy_or_lactation_status = models.BooleanField(help_text="Does the patient self assess as not pregnant or lactating?", blank=False, null=False, default=True)
    pregnancy_test_result = models.BooleanField(help_text="Does the female patient of childbearing age have a negative test result for pregnancy?", blank=False, null=False, default=False)
    no_mental_health_disorder_status = models.BooleanField(help_text="Does the patient have a mental health disorder?", blank=False, null=False, default=True)
    no_concomitant_medication_status = models.BooleanField(help_text="Does the patient have concomitant medication?", blank=False, null=False, default=True)
    concomitant_medication_details = models.CharField(max_length=255, help_text="Details about the patient's concomitant medications", blank=True, null=True)
    no_tobacco_use_status = models.BooleanField(help_text="Does the patient use tobacco?", blank=False, null=False, default=True)
    tobacco_use_details = models.CharField(max_length=255, help_text="Details about the patient's tobacco use", blank=True, null=True)
    no_substance_use_status = models.BooleanField(help_text="Does the patient use substances?", blank=False, null=False, default=True)
    substance_use_details = models.CharField(max_length=255, help_text="Details about the patient's substance use", blank=True, null=True)
    no_geographic_exposure_risk = models.BooleanField(help_text="Has the patient had geographic exposure to risk?", blank=False, null=False, default=True)
    geographic_exposure_risk_details = models.CharField(max_length=255, help_text="Details about the patient's geographic exposure risk", blank=True, null=True)

    no_hiv_status = models.BooleanField(help_text="Does the patient has had HIV?", blank=False, null=False, default=True)
    no_hepatitis_b_status = models.BooleanField(help_text="Does the patient has had Hepatitis B (HBV)?", blank=False, null=False, default=True)
    no_hepatitis_c_status = models.BooleanField(help_text="Does the patient has had Hepatitis C (HCV)?", blank=False, null=False, default=True)
    no_active_infection_status = models.BooleanField(help_text="Does the patient has any active infection?", blank=False, null=False, default=True)

    concomitant_medications = models.TextField(blank=True, null=True)
    concomitant_medication_date = models.DateField(blank=True, null=True)

    # Remission and washout periods
    remission_duration_min = models.TextField(blank=True, null=True)
    washout_period_duration = models.TextField(blank=True, null=True)

    # Viral infection status
    hiv_status = models.BooleanField(blank=True, null=True)
    hepatitis_b_status = models.BooleanField(blank=True, null=True)
    hepatitis_c_status = models.BooleanField(blank=True, null=True)

    # Treatment dates
    last_treatment = models.DateField(help_text="Date and time of the last treatment", blank=True, null=True)

    # Breast cancer specific fields
    bone_only_metastasis_status = models.BooleanField(blank=True, null=True)
    menopausal_status = models.TextField(blank=True, null=True)
    metastatic_status = models.BooleanField(blank=True, null=True)
    toxicity_grade = models.IntegerField(blank=True, null=True)
    planned_therapies = models.TextField(blank=True, null=True)

    # Biopsy results
    histologic_type = models.TextField(blank=True, null=True)
    biopsy_grade_depr = models.TextField(blank=True, null=True)
    biopsy_grade = models.IntegerField(blank=True, null=True)
    measurable_disease_by_recist_status = models.BooleanField(blank=True, null=True)
    estrogen_receptor_status = models.TextField(blank=True, null=True)
    progesterone_receptor_status = models.TextField(blank=True, null=True)
    her2_status = models.TextField(blank=True, null=True)
    tnbc_status = models.BooleanField(blank=True, null=True)
    hrd_status = models.TextField(blank=True, null=True)
    hr_status = models.TextField(blank=True, null=True)

    tumor_stage = models.TextField(blank=True, null=True)
    nodes_stage = models.TextField(blank=True, null=True)
    distant_metastasis_stage = models.TextField(blank=True, null=True)
    staging_modalities = models.TextField(blank=True, null=True)

    # Genetic mutations
    genetic_mutations = models.JSONField(blank=True, null=False, default=list)


    # PD-L1 and biomarkers
    pd_l1_tumor_cels = models.IntegerField(blank=True, null=True)
    pd_l1_assay = models.TextField(blank=True, null=True)
    pd_l1_ic_percentage = models.IntegerField(blank=True, null=True)
    pd_l1_combined_positive_score = models.IntegerField(blank=True, null=True)
    ki67_proliferation_index = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "patient_info"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["patient_age"]),
            models.Index(fields=["disease"]),
            models.Index(fields=["stage"]),
        ]

    def __str__(self):
        return f"PatientInfo for Person {self.person.person_id} (age={self.patient_age}, gender={self.gender})"
