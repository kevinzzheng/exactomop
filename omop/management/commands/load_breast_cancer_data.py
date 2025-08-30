from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from omop.models import *
import json
import os

class Command(BaseCommand):
    help = 'Load synthetic breast cancer patient data for testing PatientInfo population scripts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-concepts',
            action='store_true',
            help='Create basic OMOP concepts needed for the fixtures',
        )

    def handle(self, *args, **options):
        create_concepts = options.get('create_concepts')
        
        self.stdout.write('Loading synthetic breast cancer patient data...')
        
        if create_concepts:
            self.create_basic_concepts()
        
        # Load the fixtures
        fixture_path = os.path.join('omop', 'fixtures', 'breast_cancer_patients.json')
        
        try:
            with transaction.atomic():
                call_command('loaddata', fixture_path)
                self.stdout.write(
                    self.style.SUCCESS('Successfully loaded breast cancer patient fixtures')
                )
                
                # Create additional supporting data
                self.create_additional_data()
                
        except Exception as e:
            self.stderr.write(f'Error loading fixtures: {str(e)}')
            raise
        
        # Print summary
        self.print_data_summary()

    def create_basic_concepts(self):
        """Create basic OMOP concepts needed for the fixtures"""
        
        self.stdout.write('Creating basic OMOP concepts...')
        
        concepts = [
            # Gender concepts
            {'concept_id': 8532, 'concept_name': 'FEMALE', 'domain_id': 'Gender', 'vocabulary_id': 'Gender', 'concept_class_id': 'Gender', 'concept_code': 'F'},
            {'concept_id': 8507, 'concept_name': 'MALE', 'domain_id': 'Gender', 'vocabulary_id': 'Gender', 'concept_class_id': 'Gender', 'concept_code': 'M'},
            
            # Race concepts
            {'concept_id': 8527, 'concept_name': 'White', 'domain_id': 'Race', 'vocabulary_id': 'Race', 'concept_class_id': 'Race', 'concept_code': '5'},
            {'concept_id': 8516, 'concept_name': 'Black or African American', 'domain_id': 'Race', 'vocabulary_id': 'Race', 'concept_class_id': 'Race', 'concept_code': '3'},
            {'concept_id': 8515, 'concept_name': 'Asian', 'domain_id': 'Race', 'vocabulary_id': 'Race', 'concept_class_id': 'Race', 'concept_code': '2'},
            
            # Ethnicity concepts
            {'concept_id': 38003564, 'concept_name': 'Not Hispanic or Latino', 'domain_id': 'Ethnicity', 'vocabulary_id': 'Ethnicity', 'concept_class_id': 'Ethnicity', 'concept_code': 'Not Hispanic'},
            {'concept_id': 38003563, 'concept_name': 'Hispanic or Latino', 'domain_id': 'Ethnicity', 'vocabulary_id': 'Ethnicity', 'concept_class_id': 'Ethnicity', 'concept_code': 'Hispanic'},
            
            # Condition concepts
            {'concept_id': 4112853, 'concept_name': 'Malignant neoplasm of breast', 'domain_id': 'Condition', 'vocabulary_id': 'SNOMED', 'concept_class_id': 'Clinical Finding', 'concept_code': '254837009'},
            
            # Measurement concepts
            {'concept_id': 3000963, 'concept_name': 'Hemoglobin', 'domain_id': 'Measurement', 'vocabulary_id': 'LOINC', 'concept_class_id': 'Lab Test', 'concept_code': '718-7'},
            {'concept_id': 3013682, 'concept_name': 'Platelet count', 'domain_id': 'Measurement', 'vocabulary_id': 'LOINC', 'concept_class_id': 'Lab Test', 'concept_code': '777-3'},
            {'concept_id': 3020564, 'concept_name': 'Estrogen receptor', 'domain_id': 'Measurement', 'vocabulary_id': 'LOINC', 'concept_class_id': 'Lab Test', 'concept_code': '16112-5'},
            {'concept_id': 3025315, 'concept_name': 'Progesterone receptor', 'domain_id': 'Measurement', 'vocabulary_id': 'LOINC', 'concept_class_id': 'Lab Test', 'concept_code': '16113-3'},
            {'concept_id': 3006256, 'concept_name': 'HER2/neu', 'domain_id': 'Measurement', 'vocabulary_id': 'LOINC', 'concept_class_id': 'Lab Test', 'concept_code': '48676-1'},
            
            # Drug concepts
            {'concept_id': 1367268, 'concept_name': 'Trastuzumab', 'domain_id': 'Drug', 'vocabulary_id': 'RxNorm', 'concept_class_id': 'Ingredient', 'concept_code': '224905'},
            {'concept_id': 1378382, 'concept_name': 'Carboplatin', 'domain_id': 'Drug', 'vocabulary_id': 'RxNorm', 'concept_class_id': 'Ingredient', 'concept_code': '2555'},
            {'concept_id': 1313200, 'concept_name': 'Doxorubicin', 'domain_id': 'Drug', 'vocabulary_id': 'RxNorm', 'concept_class_id': 'Ingredient', 'concept_code': '3639'},
            {'concept_id': 1314924, 'concept_name': 'Cyclophosphamide', 'domain_id': 'Drug', 'vocabulary_id': 'RxNorm', 'concept_class_id': 'Ingredient', 'concept_code': '3002'},
            
            # Unit concepts
            {'concept_id': 8713, 'concept_name': 'gram per deciliter', 'domain_id': 'Unit', 'vocabulary_id': 'UCUM', 'concept_class_id': 'Unit', 'concept_code': 'g/dL'},
            {'concept_id': 8961, 'concept_name': 'per microliter', 'domain_id': 'Unit', 'vocabulary_id': 'UCUM', 'concept_class_id': 'Unit', 'concept_code': '/uL'},
            
            # Type concepts
            {'concept_id': 32020, 'concept_name': 'EHR Chief Complaint', 'domain_id': 'Type Concept', 'vocabulary_id': 'Type Concept', 'concept_class_id': 'Type Concept', 'concept_code': 'OMOP4822000'},
            {'concept_id': 44818702, 'concept_name': 'Lab result', 'domain_id': 'Type Concept', 'vocabulary_id': 'Type Concept', 'concept_class_id': 'Type Concept', 'concept_code': 'OMOP4822001'},
            {'concept_id': 38000177, 'concept_name': 'Inpatient administration', 'domain_id': 'Type Concept', 'vocabulary_id': 'Type Concept', 'concept_class_id': 'Type Concept', 'concept_code': 'OMOP4822002'},
            {'concept_id': 4171047, 'concept_name': 'Intravenous route', 'domain_id': 'Route', 'vocabulary_id': 'SNOMED', 'concept_class_id': 'Qualifier Value', 'concept_code': '47625008'},
            
            # Value concepts
            {'concept_id': 4181412, 'concept_name': 'Positive', 'domain_id': 'Meas Value', 'vocabulary_id': 'SNOMED', 'concept_class_id': 'Qualifier Value', 'concept_code': '10828004'},
            {'concept_id': 9189, 'concept_name': 'Negative', 'domain_id': 'Meas Value', 'vocabulary_id': 'SNOMED', 'concept_class_id': 'Qualifier Value', 'concept_code': '260385009'},
            
            # Episode concepts
            {'concept_id': 32531, 'concept_name': 'Disease episode', 'domain_id': 'Episode', 'vocabulary_id': 'Episode', 'concept_class_id': 'Episode', 'concept_code': 'Disease'},
            {'concept_id': 32545, 'concept_name': 'Episode derived from EHR record', 'domain_id': 'Type Concept', 'vocabulary_id': 'Type Concept', 'concept_class_id': 'Type Concept', 'concept_code': 'OMOP4822003'},
            
            # Observation concepts for behavioral data
            {'concept_id': 4275495, 'concept_name': 'Tobacco smoking status', 'domain_id': 'Observation', 'vocabulary_id': 'SNOMED', 'concept_class_id': 'Observable Entity', 'concept_code': '229819007'},
            {'concept_id': 44814721, 'concept_name': 'Patient reported', 'domain_id': 'Type Concept', 'vocabulary_id': 'Type Concept', 'concept_class_id': 'Type Concept', 'concept_code': 'OMOP4822004'},
            {'concept_id': 4222695, 'concept_name': 'Never smoker', 'domain_id': 'Observation', 'vocabulary_id': 'SNOMED', 'concept_class_id': 'Qualifier Value', 'concept_code': '266919005'},
            {'concept_id': 4053609, 'concept_name': 'Insurance status', 'domain_id': 'Observation', 'vocabulary_id': 'SNOMED', 'concept_class_id': 'Observable Entity', 'concept_code': '408864009'},
        ]
        
        for concept_data in concepts:
            concept, created = Concept.objects.get_or_create(
                concept_id=concept_data['concept_id'],
                defaults={
                    'concept_name': concept_data['concept_name'],
                    'domain_id': concept_data['domain_id'],
                    'vocabulary_id': concept_data['vocabulary_id'],
                    'concept_class_id': concept_data['concept_class_id'],
                    'standard_concept': 'S',
                    'concept_code': concept_data['concept_code'],
                    'valid_start_date': '1970-01-01',
                    'valid_end_date': '2099-12-31',
                    'invalid_reason': ''
                }
            )
            if created:
                self.stdout.write(f'Created concept: {concept.concept_name}')

    def create_additional_data(self):
        """Create additional supporting data"""
        
        self.stdout.write('Creating additional supporting data...')
        
        # Create treatment line components
        self.create_treatment_line_components()
        
        # Create additional biomarker measurements
        self.create_additional_biomarkers()
        
        # Create imaging studies
        self.create_imaging_studies()
        
        # Create observations for behavioral data
        self.create_behavioral_observations()

    def create_treatment_line_components(self):
        """Create treatment line components linking drugs to treatment lines"""
        
        components = [
            # TCH regimen components for patient 1001
            {
                'treatment_line_id': 6001,
                'person_id': 1001,
                'component_type': 'DRUG',
                'drug_exposure_id': 5001,
                'component_role': 'PRIMARY',
                'drug_classification': 'TARGETED_THERAPY',
                'component_start_date': '2023-02-15',
                'component_end_date': '2023-05-15',
                'is_targeted_therapy': True,
            },
            {
                'treatment_line_id': 6001,
                'person_id': 1001,
                'component_type': 'DRUG',
                'drug_exposure_id': 5002,
                'component_role': 'COMBINATION',
                'drug_classification': 'PLATINUM_AGENT',
                'component_start_date': '2023-02-15',
                'component_end_date': '2023-05-15',
                'is_platinum_agent': True,
            },
            # AC regimen components for patient 1002
            {
                'treatment_line_id': 6002,
                'person_id': 1002,
                'component_type': 'DRUG',
                'drug_exposure_id': 5003,
                'component_role': 'PRIMARY',
                'drug_classification': 'ANTHRACYCLINE',
                'component_start_date': '2023-07-01',
                'component_end_date': '2023-12-01',
                'is_platinum_agent': False,
            },
            {
                'treatment_line_id': 6002,
                'person_id': 1002,
                'component_type': 'DRUG',
                'drug_exposure_id': 5004,
                'component_role': 'COMBINATION',
                'drug_classification': 'ALKYLATING_AGENT',
                'component_start_date': '2023-07-01',
                'component_end_date': '2023-12-01',
                'is_platinum_agent': False,
            },
        ]
        
        for comp_data in components:
            component, created = TreatmentLineComponent.objects.get_or_create(
                treatment_line_id=comp_data['treatment_line_id'],
                drug_exposure_id=comp_data.get('drug_exposure_id'),
                defaults=comp_data
            )
            if created:
                self.stdout.write(f'Created treatment line component: {component.component_id}')

    def create_additional_biomarkers(self):
        """Create additional biomarker measurements"""
        
        # Ki-67 for patient 1001
        biomarker = BiomarkerMeasurement.objects.create(
            person_id=1001,
            biomarker_name='Ki-67',
            biomarker_category='PROLIFERATION',
            result_value='25',
            result_unit='percent',
            interpretation='MODERATE',
            measurement_date='2023-02-01',
            test_method='IMMUNOHISTOCHEMISTRY',
            laboratory='Johns Hopkins Pathology',
            specimen_type='TISSUE',
            clinical_significance='Proliferation index',
            reference_range='<20% low, 20-30% moderate, >30% high',
            quality_score=0.94
        )
        self.stdout.write(f'Created Ki-67 biomarker for patient 1001')
        
        # PD-L1 for patient 1002 (triple negative)
        biomarker = BiomarkerMeasurement.objects.create(
            person_id=1002,
            biomarker_name='PD-L1',
            biomarker_category='IMMUNE_CHECKPOINT',
            result_value='45',
            result_unit='CPS',
            interpretation='POSITIVE',
            measurement_date='2023-06-15',
            test_method='IMMUNOHISTOCHEMISTRY',
            laboratory='Johns Hopkins Pathology',
            specimen_type='TISSUE',
            clinical_significance='Predicts response to immunotherapy',
            reference_range='CPS ≥1 positive',
            quality_score=0.97
        )
        self.stdout.write(f'Created PD-L1 biomarker for patient 1002')

    def create_imaging_studies(self):
        """Create imaging studies for staging and follow-up"""
        
        # Baseline imaging for patient 1001
        imaging = ImagingStudy.objects.create(
            person_id=1001,
            study_uid='1.2.3.4.5.6.7.8.9.1001.1',
            accession_number='IMG001-2023',
            study_date='2023-01-18',
            modality='CT',
            study_description='CT Chest/Abdomen/Pelvis',
            body_part_examined='Chest, Abdomen, Pelvis',
            contrast_agent='IV_CONTRAST',
            indication='Initial staging for breast cancer',
            image_quality='EXCELLENT',
            baseline_imaging=True,
            response_assessment=False
        )
        self.stdout.write(f'Created baseline CT imaging for patient 1001')
        
        # Follow-up imaging for patient 1001
        imaging = ImagingStudy.objects.create(
            person_id=1001,
            study_uid='1.2.3.4.5.6.7.8.9.1001.2',
            accession_number='IMG002-2023',
            study_date='2023-08-15',
            modality='CT',
            study_description='CT Chest/Abdomen/Pelvis',
            body_part_examined='Chest, Abdomen, Pelvis',
            contrast_agent='IV_CONTRAST',
            indication='Post-treatment surveillance',
            image_quality='EXCELLENT',
            baseline_imaging=False,
            response_assessment=True
        )
        self.stdout.write(f'Created follow-up CT imaging for patient 1001')

    def create_behavioral_observations(self):
        """Create behavioral and social determinant observations"""
        
        # Smoking status for patient 1001
        observation = Observation.objects.create(
            person_id=1001,
            observation_concept_id=4275495,  # Tobacco smoking status
            observation_date='2023-01-15',
            observation_datetime='2023-01-15T09:30:00Z',
            observation_type_concept_id=44814721,  # Patient reported
            value_as_concept_id=4222695,  # Never smoker
            observation_source_value='Never smoker',
            behavioral_category='TOBACCO_USE',
            social_determinant_category='BEHAVIORAL_RISK',
            assessment_method='Patient interview',
            clinical_significance='No tobacco-related contraindications'
        )
        self.stdout.write(f'Created smoking status observation for patient 1001')
        
        # Insurance status for patient 1002
        observation = Observation.objects.create(
            person_id=1002,
            observation_concept_id=4053609,  # Insurance status
            observation_date='2023-06-10',
            observation_datetime='2023-06-10T11:15:00Z',
            observation_type_concept_id=44814721,  # Patient reported
            value_as_string='Private insurance',
            observation_source_value='Private insurance',
            behavioral_category='SOCIOECONOMIC',
            social_determinant_category='FINANCIAL_RESOURCE',
            assessment_method='Registration form',
            clinical_significance='Good insurance coverage for treatment'
        )
        self.stdout.write(f'Created insurance status observation for patient 1002')

    def print_data_summary(self):
        """Print summary of loaded data"""
        
        self.stdout.write(self.style.SUCCESS('\n=== DATA SUMMARY ==='))
        
        # Count records by model
        counts = {
            'Persons': Person.objects.count(),
            'Condition Occurrences': ConditionOccurrence.objects.count(),
            'Measurements': Measurement.objects.count(),
            'Drug Exposures': DrugExposure.objects.count(),
            'Episodes': Episode.objects.count(),
            'Treatment Lines': TreatmentLine.objects.count(),
            'Treatment Regimens': TreatmentRegimen.objects.count(),
            'Treatment Line Components': TreatmentLineComponent.objects.count(),
            'Genomic Variants': GenomicVariant.objects.count(),
            'Molecular Tests': MolecularTest.objects.count(),
            'Biomarker Measurements': BiomarkerMeasurement.objects.count(),
            'Radiation Occurrences': RadiationOccurrence.objects.count(),
            'Tumor Assessments': TumorAssessment.objects.count(),
            'Clinical Trials': ClinicalTrial.objects.count(),
            'Biospecimen Collections': BiospecimenCollection.objects.count(),
            'Oncology Episode Details': OncologyEpisodeDetail.objects.count(),
            'Imaging Studies': ImagingStudy.objects.count(),
            'Observations': Observation.objects.count(),
        }
        
        for model_name, count in counts.items():
            self.stdout.write(f'{model_name}: {count}')
        
        self.stdout.write('\n=== PATIENT SCENARIOS ===')
        
        # Patient summaries
        patients = [
            {
                'id': 1001,
                'age': 48,
                'scenario': 'HER2+ breast cancer, Stage IIB, treated with TCH regimen + radiation, excellent response',
                'biomarkers': 'ER+/PR+/HER2+',
                'mutations': 'BRCA1 pathogenic variant'
            },
            {
                'id': 1002,
                'age': 41,
                'scenario': 'Triple-negative breast cancer, Stage IA, treated with AC regimen, partial response',
                'biomarkers': 'ER-/PR-/HER2-, PD-L1 positive (CPS 45)',
                'mutations': 'None detected'
            },
            {
                'id': 1003,
                'age': 55,
                'scenario': 'Metastatic HER2+ breast cancer, Stage IV, clinical trial participation',
                'biomarkers': 'ER+/PR+/HER2+',
                'mutations': 'PIK3CA H1047R mutation'
            }
        ]
        
        for patient in patients:
            self.stdout.write(f"\nPatient {patient['id']} (Age {patient['age']}):")
            self.stdout.write(f"  Scenario: {patient['scenario']}")
            self.stdout.write(f"  Biomarkers: {patient['biomarkers']}")
            self.stdout.write(f"  Mutations: {patient['mutations']}")
        
        self.stdout.write(self.style.SUCCESS('\n✓ Synthetic breast cancer data loaded successfully!'))
        self.stdout.write('You can now test the PatientInfo population scripts with this data.')
        self.stdout.write('\nTry running:')
        self.stdout.write('  python manage.py populate_patient_info --dry-run')
        self.stdout.write('  python manage.py validate_patient_info --detailed-report')
