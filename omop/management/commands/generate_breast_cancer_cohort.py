"""
Django management command to generate synthetic breast cancer patient data.

This command creates comprehensive synthetic data for breast cancer patients including:
- Demographics
- Laboratory values and biomarkers
- Genomic data
- Treatment regimens
- Clinical observations
- Social determinants

Usage:
    python manage.py generate_breast_cancer_cohort --count=100
    python manage.py generate_breast_cancer_cohort --count=50 --clean
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from omop.models import (
    Person, Measurement, Observation, ConditionOccurrence, DrugExposure,
    ProcedureOccurrence, TreatmentRegimen, GenomicVariant, TreatmentLine,
    Concept, BiomarkerMeasurement, ClinicalLabTest, Episode, EpisodeEvent
)
from datetime import date, datetime, timedelta
import random
import json


class Command(BaseCommand):
    help = 'Generate synthetic breast cancer patient data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of patients to generate (default: 100)',
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clean existing data before generating new data',
        )

    def handle(self, *args, **options):
        count = options['count']
        clean = options['clean']
        
        self.stdout.write(f"🏥 Generating {count} Breast Cancer Patients")
        
        if clean:
            self.stdout.write("🧹 Cleaning existing data...")
            self.clean_existing_data()
        
        # Create required concepts first
        self.create_required_concepts()
        
        # Generate patients
        successful = 0
        for i in range(1, count + 1):
            try:
                self.generate_patient(i)
                successful += 1
                if i % 10 == 0:
                    self.stdout.write(f"✅ Generated {successful}/{i} patients")
            except Exception as e:
                self.stdout.write(f"❌ Error generating patient {i}: {e}")
        
        self.stdout.write(
            self.style.SUCCESS(f"🎉 Successfully generated {successful}/{count} breast cancer patients!")
        )

    def clean_existing_data(self):
        """Clean existing patient data"""
        models_to_clean = [
            GenomicVariant, TreatmentLine, TreatmentRegimen, BiomarkerMeasurement,
            EpisodeEvent, Episode, DrugExposure, ProcedureOccurrence, 
            Measurement, Observation, ConditionOccurrence, Person
        ]
        
        for model in models_to_clean:
            model.objects.all().delete()

    def create_required_concepts(self):
        """Create required OMOP concepts for breast cancer data"""
        
        concepts = [
            # Gender concepts
            (8507, 'Male', 'Gender'),
            (8532, 'Female', 'Gender'),
            
            # Race concepts
            (8527, 'White', 'Race'),
            (8516, 'Black or African American', 'Race'),
            (8515, 'Asian', 'Race'),
            (8557, 'Native Hawaiian or Other Pacific Islander', 'Race'),
            (8657, 'American Indian or Alaska Native', 'Race'),
            
            # Ethnicity concepts
            (38003563, 'Hispanic or Latino', 'Ethnicity'),
            (38003564, 'Not Hispanic or Latino', 'Ethnicity'),
            
            # Condition concepts
            (4112853, 'Malignant neoplasm of breast', 'Condition'),
            (4263086, 'Invasive ductal carcinoma of breast', 'Condition'),
            (4180790, 'Invasive lobular carcinoma of breast', 'Condition'),
            (35917532, 'Breast cancer stage', 'Condition'),
            
            # Measurement concepts
            (3013682, 'Hemoglobin', 'Measurement'),
            (3010813, 'Platelet count', 'Measurement'),
            (3009744, 'White blood cell count', 'Measurement'),
            (3016723, 'Creatinine', 'Measurement'),
            (3004249, 'Alanine aminotransferase', 'Measurement'),
            (3013721, 'Aspartate aminotransferase', 'Measurement'),
            (3024128, 'Estrogen receptor', 'Measurement'),
            (3035995, 'Progesterone receptor', 'Measurement'),
            (36769180, 'HER2 receptor', 'Measurement'),
            (3007220, 'CA 15-3', 'Measurement'),
            (3009261, 'CA 27.29', 'Measurement'),
            
            # Drug concepts
            (1378382, 'Doxorubicin', 'Drug'),
            (1790868, 'Cyclophosphamide', 'Drug'),
            (1594973, 'Paclitaxel', 'Drug'),
            (1551099, 'Trastuzumab', 'Drug'),
            (1550023, 'Tamoxifen', 'Drug'),
            (40239216, 'Anastrozole', 'Drug'),
            (1539403, 'Letrozole', 'Drug'),
            (40165636, 'Pertuzumab', 'Drug'),
            
            # Procedure concepts
            (4273629, 'Mastectomy', 'Procedure'),
            (4052536, 'Lumpectomy', 'Procedure'),
            (4283893, 'Lymph node dissection', 'Procedure'),
            (4048120, 'Radiation therapy', 'Procedure'),
            
            # Observation concepts
            (4051516, 'Social history', 'Observation'),
            (4013634, 'Smoking status', 'Observation'),
            (4051865, 'Alcohol use', 'Observation'),
            (40767296, 'Employment status', 'Observation'),
            (4013395, 'Education level', 'Observation'),
            
            # Type concepts
            (32856, 'Lab result', 'Type'),
            (32817, 'EHR', 'Type'),
            (32818, 'Prescription', 'Type'),
            (32020, 'EHR diagnosis', 'Type'),
            (32531, 'Treatment episode', 'Type'),
            (1147127, 'condition_occurrence.condition_occurrence_id', 'Type'),
        ]
        
        for concept_id, concept_name, domain in concepts:
            Concept.objects.get_or_create(
                concept_id=concept_id,
                defaults={
                    'concept_name': concept_name,
                    'domain_id': domain,
                    'vocabulary_id': 'SNOMED',
                    'concept_class_id': 'Clinical Finding',
                    'concept_code': str(concept_id),
                    'valid_start_date': date(2000, 1, 1),
                    'valid_end_date': date(2099, 12, 31),
                    'invalid_reason': ''
                }
            )

    def generate_patient(self, patient_num):
        """Generate a complete breast cancer patient"""
        
        # Demographics
        person = self.create_person(patient_num)
        
        # Breast cancer diagnosis
        self.create_breast_cancer_diagnosis(person)
        
        # Laboratory values
        self.create_lab_values(person)
        
        # Biomarkers
        self.create_biomarkers(person)
        
        # Genomic data
        self.create_genomic_data(person)
        
        # Treatment regimens
        self.create_treatment_regimens(person)
        
        # Treatment lines
        self.create_treatment_lines(person)
        
        # Procedures
        self.create_procedures(person)
        
        # Social determinants
        self.create_social_determinants(person)
        
        # Episode tracking
        self.create_episodes(person)

    def create_person(self, patient_num):
        """Create a person with realistic demographics"""
        
        # Age distribution: 25-85 years, weighted toward 45-65
        age_weights = [1, 2, 3, 5, 8, 10, 8, 5, 3, 2, 1]  # Weights for each decade
        age_decade = random.choices(range(2, 9), weights=age_weights[:7])[0]  # 20s to 80s
        age = random.randint(age_decade * 10 + 5, (age_decade + 1) * 10 - 1)
        birth_year = date.today().year - age
        
        # Gender (98% female for breast cancer)
        gender_concept_id = 8532 if random.random() < 0.98 else 8507
        
        # Race distribution
        race_weights = [70, 15, 8, 4, 3]  # White, Black, Asian, Pacific Islander, Native American
        race_concepts = [8527, 8516, 8515, 8557, 8657]
        race_concept_id = random.choices(race_concepts, weights=race_weights)[0]
        
        # Ethnicity
        ethnicity_concept_id = 38003563 if random.random() < 0.18 else 38003564  # 18% Hispanic
        
        person = Person.objects.create(
            person_id=patient_num,
            gender_concept_id=gender_concept_id,
            year_of_birth=birth_year,
            month_of_birth=random.randint(1, 12),
            day_of_birth=random.randint(1, 28),
            race_concept_id=race_concept_id,
            ethnicity_concept_id=ethnicity_concept_id,
            person_source_value=f"BC_{patient_num:04d}"
        )
        
        return person

    def create_breast_cancer_diagnosis(self, person):
        """Create breast cancer diagnosis"""
        
        # Primary diagnosis
        diagnosis_concepts = [4112853, 4263086, 4180790]  # General BC, IDC, ILC
        primary_concept = random.choice(diagnosis_concepts)
        
        # Diagnosis date (within last 5 years)
        days_ago = random.randint(30, 1825)  # 30 days to 5 years ago
        diagnosis_date = date.today() - timedelta(days=days_ago)
        
        ConditionOccurrence.objects.create(
            person=person,
            condition_concept_id=primary_concept,
            condition_start_date=diagnosis_date,
            condition_type_concept_id=32020,  # EHR
            condition_source_value=f"ICD-10-CM:{random.choice(['C50.9', 'C50.1', 'C50.2'])}"
        )
        
        # Stage (separate condition)
        stages = ['Stage I', 'Stage II', 'Stage III', 'Stage IV']
        stage_weights = [25, 35, 25, 15]  # Distribution of stages
        stage = random.choices(stages, weights=stage_weights)[0]
        
        ConditionOccurrence.objects.create(
            person=person,
            condition_concept_id=35917532,  # Breast cancer stage
            condition_start_date=diagnosis_date,
            condition_type_concept_id=32020,
            condition_source_value=stage
        )

    def create_lab_values(self, person):
        """Create laboratory values"""
        
        base_date = date.today() - timedelta(days=random.randint(1, 365))
        
        # Standard lab panel
        labs = [
            (3013682, 'Hemoglobin', random.uniform(10.5, 15.5), 'g/dL'),
            (3010813, 'Platelet count', random.randint(150000, 450000), 'cells/uL'),
            (3009744, 'White blood cell count', random.uniform(3.5, 11.0), '10^3/uL'),
            (3016723, 'Creatinine', random.uniform(0.6, 1.2), 'mg/dL'),
            (3004249, 'ALT', random.randint(10, 55), 'U/L'),
            (3013721, 'AST', random.randint(10, 40), 'U/L'),
        ]
        
        for concept_id, name, value, unit in labs:
            # Create multiple measurements over time
            for i in range(random.randint(2, 8)):
                measurement_date = base_date + timedelta(days=i * random.randint(30, 90))
                
                # Add some variation to values
                varied_value = value * random.uniform(0.8, 1.2)
                if isinstance(value, int):
                    varied_value = int(varied_value)
                
                Measurement.objects.create(
                    person=person,
                    measurement_concept_id=concept_id,
                    measurement_datetime=timezone.make_aware(
                        datetime.combine(measurement_date, datetime.min.time())
                    ),
                    value_as_number=varied_value,
                    unit_source_value=unit,
                    measurement_type_concept_id=32856  # Lab result
                )

    def create_biomarkers(self, person):
        """Create breast cancer biomarkers"""
        
        diagnosis_date = date.today() - timedelta(days=random.randint(30, 1825))
        
        # Hormone receptors
        er_status = random.choices(['Positive', 'Negative'], weights=[75, 25])[0]
        pr_status = random.choices(['Positive', 'Negative'], weights=[65, 35])[0]
        
        # HER2 status
        her2_status = random.choices(['Positive', 'Negative', 'Equivocal'], weights=[20, 75, 5])[0]
        
        # Create biomarker measurements
        biomarkers = [
            (3024128, 'ER', er_status),
            (3035995, 'PR', pr_status),
            (36769180, 'HER2', her2_status),
        ]
        
        for concept_id, name, status in biomarkers:
            Measurement.objects.create(
                person=person,
                measurement_concept_id=concept_id,
                measurement_datetime=timezone.make_aware(
                    datetime.combine(diagnosis_date, datetime.min.time())
                ),
                measurement_source_value=status,
                measurement_type_concept_id=32856
            )
        
        # Tumor markers (if indicated)
        if random.random() < 0.7:  # 70% have tumor markers
            ca_15_3 = random.uniform(5, 150)  # Normal < 30
            ca_27_29 = random.uniform(5, 100)  # Normal < 38
            
            for concept_id, value, name in [(3007220, ca_15_3, 'CA 15-3'), (3009261, ca_27_29, 'CA 27.29')]:
                Measurement.objects.create(
                    person=person,
                    measurement_concept_id=concept_id,
                    measurement_datetime=timezone.make_aware(
                        datetime.combine(diagnosis_date + timedelta(days=7), datetime.min.time())
                    ),
                    value_as_number=value,
                    unit_source_value='U/mL',
                    measurement_type_concept_id=32856
                )

    def create_genomic_data(self, person):
        """Create genomic variants"""
        
        # Common breast cancer mutations
        mutations = [
            ('BRCA1', ['185delAG', '5382insC', '1675delA'], 0.05),  # 5% prevalence
            ('BRCA2', ['6174delT', '999del5', '8765delAG'], 0.05),
            ('TP53', ['R175H', 'R248Q', 'R273H'], 0.30),
            ('PIK3CA', ['E545K', 'H1047R', 'E542K'], 0.35),
            ('CDH1', ['1901C>T', '2076delA'], 0.03),
            ('PTEN', ['97C>T', '697C>T'], 0.08),
            ('ATM', ['7271T>G', '8147T>C'], 0.12),
            ('CHEK2', ['1100delC', 'I157T'], 0.15),
        ]
        
        for gene, variants, prevalence in mutations:
            if random.random() < prevalence:
                variant = random.choice(variants)
                
                # Classification
                if gene in ['BRCA1', 'BRCA2']:
                    classification = random.choices(
                        ['Pathogenic', 'Likely pathogenic', 'VUS'], 
                        weights=[70, 20, 10]
                    )[0]
                else:
                    classification = random.choices(
                        ['Pathogenic', 'Likely pathogenic', 'VUS', 'Benign'], 
                        weights=[40, 30, 20, 10]
                    )[0]
                
                GenomicVariant.objects.create(
                    person=person,
                    gene_symbol=gene,
                    hgvs_notation=variant,
                    variant_type='SNV',
                    chromosome=random.choice(['1', '2', '13', '17', '19']),
                    genomic_position=random.randint(1000000, 99999999),
                    reference_allele=random.choice(['A', 'T', 'G', 'C']),
                    alternate_allele=random.choice(['A', 'T', 'G', 'C']),
                    clinical_significance=classification,
                    test_date=date.today() - timedelta(days=random.randint(30, 365))
                )

    def create_treatment_regimens(self, person):
        """Create treatment regimens"""
        
        start_date = date.today() - timedelta(days=random.randint(30, 1460))
        
        # Common breast cancer regimens
        regimens = [
            ('AC-T', ['Doxorubicin', 'Cyclophosphamide', 'Paclitaxel']),
            ('TCH', ['Docetaxel', 'Carboplatin', 'Trastuzumab']),
            ('AC', ['Doxorubicin', 'Cyclophosphamide']),
            ('CMF', ['Cyclophosphamide', 'Methotrexate', 'Fluorouracil']),
            ('Tamoxifen', ['Tamoxifen']),
            ('Anastrozole', ['Anastrozole']),
            ('Letrozole', ['Letrozole']),
        ]
        
        # First-line treatment
        regimen_name, drugs = random.choice(regimens)
        
        regimen = TreatmentRegimen.objects.create(
            person=person,
            regimen_concept_id=1378382,  # Use a generic concept ID for treatment regimen
            regimen_name=regimen_name,
            regimen_start_date=start_date,
            regimen_end_date=start_date + timedelta(days=random.randint(90, 365)),
            line_number=1,
            regimen_type='CHEMOTHERAPY',
            cycle_length_days=random.choice([14, 21, 28]),  # Common cycle lengths
            cycles_planned=random.randint(4, 12)  # Number of planned cycles
        )
        
        # Create drug exposures
        for drug_name in drugs:
            DrugExposure.objects.create(
                person=person,
                drug_concept_id=self.get_drug_concept_id(drug_name),
                drug_exposure_start_datetime=timezone.make_aware(
                    datetime.combine(start_date, datetime.min.time())
                ),
                drug_exposure_end_datetime=timezone.make_aware(
                    datetime.combine(regimen.regimen_end_date, datetime.min.time())
                ),
                drug_type_concept_id=32818,  # Prescription
                drug_source_value=drug_name
            )

    def create_treatment_lines(self, person):
        """Create treatment line tracking"""
        
        # Get the primary breast cancer diagnosis
        primary_condition = ConditionOccurrence.objects.filter(
            person=person,
            condition_concept_id__in=[4112853, 4263086, 4180790]  # Breast cancer concepts
        ).first()
        
        if not primary_condition:
            # If no condition found, return without creating treatment lines
            return
        
        # First line
        start_date = date.today() - timedelta(days=random.randint(30, 1460))
        
        TreatmentLine.objects.create(
            person=person,
            condition_occurrence_id=primary_condition.condition_occurrence_id,
            line_number=1,
            line_start_date=start_date,
            line_end_date=start_date + timedelta(days=random.randint(120, 365)),
            treatment_response='Complete Response' if random.random() < 0.3 else 'Partial Response',
            time_to_progression_days=random.randint(180, 300) if random.random() < 0.3 else None,
            treatment_status='Completed'
        )
        
        # Second line (if progression)
        if random.random() < 0.4:  # 40% need second line
            second_start = start_date + timedelta(days=random.randint(200, 400))
            TreatmentLine.objects.create(
                person=person,
                condition_occurrence_id=primary_condition.condition_occurrence_id,
                line_number=2,
                line_start_date=second_start,
                line_end_date=second_start + timedelta(days=random.randint(90, 270)),
                treatment_response=random.choice(['Partial Response', 'Stable Disease', 'Progressive Disease']),
                time_to_progression_days=random.randint(60, 180),
                treatment_status=random.choice(['Completed', 'Ongoing', 'Discontinued'])
            )

    def create_procedures(self, person):
        """Create surgical and radiation procedures"""
        
        diagnosis_date = date.today() - timedelta(days=random.randint(30, 1825))
        
        # Surgery (90% have surgery)
        if random.random() < 0.9:
            surgery_type = random.choices(
                [4052536, 4273629],  # Lumpectomy, Mastectomy
                weights=[60, 40]
            )[0]
            
            surgery_date = diagnosis_date + timedelta(days=random.randint(7, 60))
            
            ProcedureOccurrence.objects.create(
                person=person,
                procedure_concept_id=surgery_type,
                procedure_datetime=surgery_date,
                procedure_type_concept_id=32818
            )
            
            # Lymph node dissection (70% of surgery patients)
            if random.random() < 0.7:
                ProcedureOccurrence.objects.create(
                    person=person,
                    procedure_concept_id=4283893,  # Lymph node dissection
                    procedure_datetime=surgery_date,
                    procedure_type_concept_id=32818
                )
        
        # Radiation therapy (75% receive radiation)
        if random.random() < 0.75:
            radiation_start = diagnosis_date + timedelta(days=random.randint(30, 120))
            
            ProcedureOccurrence.objects.create(
                person=person,
                procedure_concept_id=4048120,  # Radiation therapy
                procedure_datetime=radiation_start,
                procedure_type_concept_id=32818
            )

    def create_social_determinants(self, person):
        """Create social determinant observations"""
        
        assessment_date = date.today() - timedelta(days=random.randint(1, 365))
        
        # Smoking status
        smoking_statuses = ['Never smoker', 'Former smoker', 'Current smoker']
        smoking_weights = [60, 25, 15]
        smoking_status = random.choices(smoking_statuses, weights=smoking_weights)[0]
        
        Observation.objects.create(
            person=person,
            observation_concept_id=4013634,
            observation_datetime=timezone.make_aware(
                datetime.combine(assessment_date, datetime.min.time())
            ),
            observation_source_value=smoking_status,
            observation_type_concept_id=32817
        )
        
        # Alcohol use
        alcohol_statuses = ['Never', 'Occasional', 'Moderate', 'Heavy']
        alcohol_weights = [20, 40, 30, 10]
        alcohol_status = random.choices(alcohol_statuses, weights=alcohol_weights)[0]
        
        Observation.objects.create(
            person=person,
            observation_concept_id=4051865,
            observation_datetime=timezone.make_aware(
                datetime.combine(assessment_date, datetime.min.time())
            ),
            observation_source_value=alcohol_status,
            observation_type_concept_id=32817
        )
        
        # Employment status
        employment_statuses = ['Employed full-time', 'Employed part-time', 'Unemployed', 'Retired', 'Disabled']
        employment_weights = [45, 15, 10, 20, 10]
        employment_status = random.choices(employment_statuses, weights=employment_weights)[0]
        
        Observation.objects.create(
            person=person,
            observation_concept_id=40767296,
            observation_datetime=timezone.make_aware(
                datetime.combine(assessment_date, datetime.min.time())
            ),
            observation_source_value=employment_status,
            observation_type_concept_id=32817
        )

    def create_episodes(self, person):
        """Create episode tracking for treatment phases"""
        
        diagnosis_date = date.today() - timedelta(days=random.randint(30, 1825))
        
        # Primary treatment episode
        episode = Episode.objects.create(
            person=person,
            episode_concept_id=32531,  # Treatment episode
            episode_start_date=diagnosis_date,
            episode_end_date=diagnosis_date + timedelta(days=random.randint(180, 730)),
            parent_episode=None,
            episode_number=1,
            episode_type='primary_diagnosis'
        )
        
        # Link major events to episode
        conditions = ConditionOccurrence.objects.filter(person=person)
        for condition in conditions:
            EpisodeEvent.objects.create(
                episode=episode,
                event_id=condition.condition_occurrence_id,
                event_field_concept_id=1147127  # condition_occurrence.condition_occurrence_id
            )

    def get_drug_concept_id(self, drug_name):
        """Get concept ID for drug name"""
        drug_mapping = {
            'Doxorubicin': 1378382,
            'Cyclophosphamide': 1790868,
            'Paclitaxel': 1594973,
            'Trastuzumab': 1551099,
            'Tamoxifen': 1550023,
            'Anastrozole': 40239216,
            'Letrozole': 1539403,
            'Pertuzumab': 40165636,
            'Docetaxel': 1000560,
            'Carboplatin': 1378382,
            'Methotrexate': 1305058,
            'Fluorouracil': 1790021,
        }
        return drug_mapping.get(drug_name, 1378382)  # Default to doxorubicin
