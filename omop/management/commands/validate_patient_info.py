from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from omop.models import (
    Person, PatientInfo, ConditionOccurrence, Measurement, 
    DrugExposure, ProcedureOccurrence, Observation, Episode,
    TreatmentLine, TreatmentRegimen, BiomarkerMeasurement, ClinicalTrialBiomarker,
    GenomicVariant, MolecularTest, ClinicalLabTest, TumorAssessment,
    RadiationOccurrence, StemCellTransplant, ClinicalTrial, BiospecimenCollection,
    OncologyEpisodeDetail
)
from datetime import date, datetime
import logging
import json

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Validate PatientInfo data against OMOP CDM sources with comprehensive oncology validation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--person-id',
            type=int,
            help='Validate specific person ID only',
        )
        parser.add_argument(
            '--fix-errors',
            action='store_true',
            help='Attempt to fix validation errors',
        )
        parser.add_argument(
            '--detailed-report',
            action='store_true',
            help='Generate detailed validation report',
        )

    def handle(self, *args, **options):
        person_id = options.get('person_id')
        fix_errors = options.get('fix_errors')
        detailed_report = options.get('detailed_report')
        
        if person_id:
            patient_infos = PatientInfo.objects.filter(person__person_id=person_id)
            self.stdout.write(f'Validating single person: {person_id}')
        else:
            patient_infos = PatientInfo.objects.all()
            self.stdout.write(f'Validating all {patient_infos.count()} PatientInfo records')
        
        validation_results = {
            'total_validated': 0,
            'errors_found': 0,
            'warnings_found': 0,
            'errors_fixed': 0,
            'validation_details': []
        }
        
        for patient_info in patient_infos:
            try:
                result = self.validate_patient_info(patient_info, fix_errors, detailed_report)
                validation_results['total_validated'] += 1
                validation_results['errors_found'] += len(result['errors'])
                validation_results['warnings_found'] += len(result['warnings'])
                
                if fix_errors:
                    validation_results['errors_fixed'] += result['fixed_count']
                
                if detailed_report:
                    validation_results['validation_details'].append(result)
                
                if result['errors'] or result['warnings']:
                    self.stdout.write(
                        f'Person {patient_info.person.person_id}: '
                        f'{len(result["errors"])} errors, {len(result["warnings"])} warnings'
                    )
                    
            except Exception as e:
                self.stderr.write(f'Error validating person {patient_info.person.person_id}: {str(e)}')
                logger.error(f'Error validating person {patient_info.person.person_id}: {str(e)}')
        
        # Print summary
        self.print_validation_summary(validation_results, detailed_report)

    def validate_patient_info(self, patient_info, fix_errors=False, detailed_report=False):
        """Validate a single PatientInfo record"""
        
        result = {
            'person_id': patient_info.person.person_id,
            'errors': [],
            'warnings': [],
            'fixed_count': 0,
            'validation_timestamp': datetime.now()
        }
        
        # Validate demographics
        demo_validation = self.validate_demographics(patient_info)
        result['errors'].extend(demo_validation['errors'])
        result['warnings'].extend(demo_validation['warnings'])
        
        # Validate cancer condition data
        condition_validation = self.validate_cancer_condition(patient_info)
        result['errors'].extend(condition_validation['errors'])
        result['warnings'].extend(condition_validation['warnings'])
        
        # Validate staging information
        staging_validation = self.validate_staging(patient_info)
        result['errors'].extend(staging_validation['errors'])
        result['warnings'].extend(staging_validation['warnings'])
        
        # Validate laboratory values
        lab_validation = self.validate_lab_values(patient_info)
        result['errors'].extend(lab_validation['errors'])
        result['warnings'].extend(lab_validation['warnings'])
        
        # Validate biomarker data
        biomarker_validation = self.validate_biomarkers(patient_info)
        result['errors'].extend(biomarker_validation['errors'])
        result['warnings'].extend(biomarker_validation['warnings'])
        
        # Validate treatment data
        treatment_validation = self.validate_treatments(patient_info)
        result['errors'].extend(treatment_validation['errors'])
        result['warnings'].extend(treatment_validation['warnings'])
        
        # Validate genomic data
        genomic_validation = self.validate_genomics(patient_info)
        result['errors'].extend(genomic_validation['errors'])
        result['warnings'].extend(genomic_validation['warnings'])
        
        # Validate oncology extensions
        oncology_validation = self.validate_oncology_extensions(patient_info)
        result['errors'].extend(oncology_validation['errors'])
        result['warnings'].extend(oncology_validation['warnings'])
        
        # Attempt to fix errors if requested
        if fix_errors and result['errors']:
            result['fixed_count'] = self.fix_validation_errors(patient_info, result['errors'])
        
        return result

    def validate_demographics(self, patient_info):
        """Validate demographic data consistency"""
        errors = []
        warnings = []
        
        person = patient_info.person
        
        # Age validation
        if patient_info.patient_age:
            calculated_age = date.today().year - (person.year_of_birth or 1950)
            if abs(patient_info.patient_age - calculated_age) > 2:
                errors.append(f'Age mismatch: PatientInfo has {patient_info.patient_age}, calculated {calculated_age}')
        
        # Gender validation
        gender_map = {8507: 'M', 8532: 'F', 8551: 'O', 8570: 'U'}
        expected_gender = gender_map.get(person.gender_concept_id, 'U')
        if patient_info.gender != expected_gender:
            errors.append(f'Gender mismatch: PatientInfo has {patient_info.gender}, OMOP has {expected_gender}')
        
        # Check for missing demographics
        if not patient_info.patient_age:
            warnings.append('Missing patient age')
        if not patient_info.gender:
            warnings.append('Missing gender information')
        
        return {'errors': errors, 'warnings': warnings}

    def validate_cancer_condition(self, patient_info):
        """Validate cancer condition information"""
        errors = []
        warnings = []
        
        person = patient_info.person
        
        # Get primary cancer condition from OMOP
        cancer_conditions = ConditionOccurrence.objects.filter(person=person)
        primary_condition = None
        
        for condition in cancer_conditions:
            if self.is_cancer_condition(condition):
                primary_condition = condition
                break
        
        if not primary_condition and patient_info.disease:
            warnings.append('PatientInfo has disease but no cancer condition found in OMOP')
        elif primary_condition and not patient_info.disease:
            warnings.append('Cancer condition exists in OMOP but not in PatientInfo')
        
        # Validate diagnosis date
        if primary_condition and patient_info.diagnosis_date:
            if primary_condition.condition_start_date != patient_info.diagnosis_date:
                errors.append(
                    f'Diagnosis date mismatch: PatientInfo has {patient_info.diagnosis_date}, '
                    f'OMOP has {primary_condition.condition_start_date}'
                )
        
        # Validate tumor laterality
        if (primary_condition and 
            hasattr(primary_condition, 'tumor_laterality') and 
            primary_condition.tumor_laterality != patient_info.tumor_laterality):
            warnings.append(f'Tumor laterality mismatch')
        
        return {'errors': errors, 'warnings': warnings}

    def validate_staging(self, patient_info):
        """Validate staging information consistency"""
        errors = []
        warnings = []
        
        person = patient_info.person
        
        # Get staging from ConditionOccurrence
        cancer_condition = self.get_primary_cancer_condition(person)
        
        if cancer_condition:
            # Validate AJCC staging components
            staging_fields = [
                ('ajcc_clinical_t', 'ajcc_clinical_t'),
                ('ajcc_clinical_n', 'ajcc_clinical_n'),
                ('ajcc_clinical_m', 'ajcc_clinical_m'),
                ('ajcc_pathologic_t', 'ajcc_pathologic_t'),
                ('ajcc_pathologic_n', 'ajcc_pathologic_n'),
                ('ajcc_pathologic_m', 'ajcc_pathologic_m'),
                ('ajcc_clinical_stage', 'ajcc_clinical_stage'),
                ('ajcc_pathologic_stage', 'ajcc_pathologic_stage'),
            ]
            
            for pi_field, omop_field in staging_fields:
                pi_value = getattr(patient_info, pi_field, None)
                omop_value = getattr(cancer_condition, omop_field, None)
                
                if pi_value != omop_value:
                    if pi_value and omop_value:
                        errors.append(f'Staging mismatch in {pi_field}: {pi_value} vs {omop_value}')
                    elif omop_value and not pi_value:
                        warnings.append(f'Missing {pi_field} in PatientInfo')
        
        # Validate tumor assessments
        tumor_assessments = TumorAssessment.objects.filter(person=person)
        if tumor_assessments.exists() and not patient_info.omop_data_json:
            warnings.append('Tumor assessments exist but not captured in PatientInfo')
        
        return {'errors': errors, 'warnings': warnings}

    def validate_lab_values(self, patient_info):
        """Validate laboratory values"""
        errors = []
        warnings = []
        
        person = patient_info.person
        
        # Get latest lab values from OMOP
        lab_measurements = Measurement.objects.filter(person=person).order_by('-measurement_datetime')
        lab_tests = ClinicalLabTest.objects.filter(person=person).order_by('-test_date')
        
        # Check common lab values
        lab_fields = [
            ('hemoglobin', 'hemoglobin'),
            ('hematocrit', 'hematocrit'),
            ('platelet_count', 'platelet'),
            ('wbc_count', 'white blood cell'),
            ('creatinine', 'creatinine'),
            ('bilirubin', 'bilirubin'),
            ('albumin', 'albumin')
        ]
        
        for pi_field, concept_keyword in lab_fields:
            pi_value = getattr(patient_info, pi_field, None)
            
            # Find corresponding measurement in OMOP
            omop_value = None
            for measurement in lab_measurements:
                if measurement.measurement_concept:
                    concept_name = measurement.measurement_concept.concept_name.lower()
                    if concept_keyword in concept_name:
                        omop_value = measurement.value_as_number
                        break
            
            # Validate ranges for key lab values
            if pi_value is not None:
                validation_result = self.validate_lab_range(pi_field, pi_value)
                if validation_result:
                    warnings.append(validation_result)
        
        return {'errors': errors, 'warnings': warnings}

    def validate_biomarkers(self, patient_info):
        """Validate biomarker data consistency"""
        errors = []
        warnings = []
        
        person = patient_info.person
        
        # Check biomarker measurements
        biomarker_measurements = BiomarkerMeasurement.objects.filter(person=person)
        trial_biomarkers = ClinicalTrialBiomarker.objects.filter(person=person)
        
        # Validate PD-L1 scores
        if patient_info.pdl1_cps_score or patient_info.pdl1_tps_score:
            # Check if corresponding measurements exist
            pdl1_measurements = Measurement.objects.filter(
                person=person,
                measurement_concept__concept_name__icontains='pd-l1'
            )
            
            if not pdl1_measurements.exists() and not trial_biomarkers.filter(biomarker_type='PD_L1').exists():
                warnings.append('PD-L1 scores in PatientInfo but no PD-L1 measurements found')
        
        # Validate biomarker JSON data
        if patient_info.biomarker_results:
            try:
                biomarker_data = json.loads(patient_info.biomarker_results)
                # Validate structure
                if not isinstance(biomarker_data, dict):
                    errors.append('Biomarker results JSON is not a valid dictionary')
            except json.JSONDecodeError:
                errors.append('Invalid JSON in biomarker_results field')
        
        # Check for missing key biomarkers
        key_biomarkers = ['HER2', 'ER', 'PR', 'TMB', 'MSI']
        missing_biomarkers = []
        
        for biomarker in key_biomarkers:
            has_measurement = biomarker_measurements.filter(
                biomarker_name__icontains=biomarker
            ).exists()
            has_trial_biomarker = trial_biomarkers.filter(
                biomarker_type__icontains=biomarker
            ).exists()
            
            if not has_measurement and not has_trial_biomarker:
                missing_biomarkers.append(biomarker)
        
        if missing_biomarkers:
            warnings.append(f'Missing key biomarkers: {", ".join(missing_biomarkers)}')
        
        return {'errors': errors, 'warnings': warnings}

    def validate_treatments(self, patient_info):
        """Validate treatment data consistency"""
        errors = []
        warnings = []
        
        person = patient_info.person
        
        # Get treatment data from OMOP
        treatment_lines = TreatmentLine.objects.filter(person=person)
        treatment_regimens = TreatmentRegimen.objects.filter(person=person)
        drug_exposures = DrugExposure.objects.filter(person=person)
        
        # Validate treatment line counts
        if patient_info.prior_lines_therapy:
            actual_lines = treatment_lines.count()
            if patient_info.prior_lines_therapy != actual_lines:
                errors.append(
                    f'Treatment lines mismatch: PatientInfo has {patient_info.prior_lines_therapy}, '
                    f'OMOP has {actual_lines}'
                )
        
        # Validate current line
        if patient_info.current_line_therapy:
            max_line = treatment_lines.aggregate(max_line=models.Max('line_number'))['max_line']
            if max_line and patient_info.current_line_therapy != max_line:
                warnings.append(
                    f'Current line mismatch: PatientInfo has {patient_info.current_line_therapy}, '
                    f'OMOP max is {max_line}'
                )
        
        # Validate therapy flags
        therapy_flags = [
            ('prior_platinum_therapy', 'platinum_based'),
            ('prior_immunotherapy', 'immunotherapy_based'),
            ('prior_targeted_therapy', 'targeted_therapy_based')
        ]
        
        for pi_field, line_field in therapy_flags:
            pi_value = getattr(patient_info, pi_field, False)
            omop_value = treatment_lines.filter(**{line_field: True}).exists()
            
            if pi_value != omop_value:
                errors.append(f'Treatment flag mismatch: {pi_field}')
        
        return {'errors': errors, 'warnings': warnings}

    def validate_genomics(self, patient_info):
        """Validate genomic data"""
        errors = []
        warnings = []
        
        person = patient_info.person
        
        # Check genomic variants
        genomic_variants = GenomicVariant.objects.filter(person=person)
        molecular_tests = MolecularTest.objects.filter(person=person)
        
        # Validate genetic test results JSON
        if patient_info.genetic_test_results:
            try:
                genetic_data = json.loads(patient_info.genetic_test_results)
                if not isinstance(genetic_data, dict):
                    errors.append('Genetic test results JSON is not a valid dictionary')
            except json.JSONDecodeError:
                errors.append('Invalid JSON in genetic_test_results field')
        
        # Check for genomic data consistency
        if genomic_variants.exists() and not patient_info.genetic_test_results:
            warnings.append('Genomic variants exist but not captured in PatientInfo')
        
        if molecular_tests.exists() and not patient_info.genetic_test_results:
            warnings.append('Molecular tests exist but not captured in PatientInfo')
        
        return {'errors': errors, 'warnings': warnings}

    def validate_oncology_extensions(self, patient_info):
        """Validate OMOP Oncology Extension data"""
        errors = []
        warnings = []
        
        person = patient_info.person
        
        # Check radiation therapy
        radiation_occurrences = RadiationOccurrence.objects.filter(person=person)
        if radiation_occurrences.exists():
            if not patient_info.omop_data_json:
                warnings.append('Radiation therapy exists but not captured in comprehensive data')
            else:
                try:
                    omop_data = json.loads(patient_info.omop_data_json)
                    if 'radiation' not in omop_data or not omop_data['radiation']:
                        warnings.append('Radiation therapy data missing from comprehensive JSON')
                except json.JSONDecodeError:
                    errors.append('Invalid JSON in omop_data_json field')
        
        # Check stem cell transplants
        transplants = StemCellTransplant.objects.filter(person=person)
        if transplants.exists():
            if not patient_info.omop_data_json:
                warnings.append('Stem cell transplants exist but not captured')
        
        # Check clinical trials
        clinical_trials = ClinicalTrial.objects.filter(person=person)
        if clinical_trials.exists():
            if not patient_info.omop_data_json:
                warnings.append('Clinical trial participation exists but not captured')
        
        # Check biospecimen collections
        biospecimens = BiospecimenCollection.objects.filter(person=person)
        if biospecimens.exists():
            if not patient_info.omop_data_json:
                warnings.append('Biospecimen collections exist but not captured')
        
        return {'errors': errors, 'warnings': warnings}

    def validate_lab_range(self, field_name, value):
        """Validate laboratory value ranges"""
        ranges = {
            'hemoglobin': (8.0, 18.0, 'g/dL'),
            'hematocrit': (24.0, 54.0, '%'),
            'platelet_count': (150, 450, 'K/μL'),
            'wbc_count': (4.0, 11.0, 'K/μL'),
            'creatinine': (0.5, 2.0, 'mg/dL'),
            'bilirubin': (0.1, 1.2, 'mg/dL'),
            'albumin': (3.5, 5.0, 'g/dL'),
        }
        
        if field_name in ranges:
            min_val, max_val, unit = ranges[field_name]
            if value < min_val or value > max_val:
                return f'{field_name} value {value} outside normal range ({min_val}-{max_val} {unit})'
        
        return None

    def fix_validation_errors(self, patient_info, errors):
        """Attempt to fix validation errors"""
        fixed_count = 0
        
        # This is a placeholder for error fixing logic
        # In practice, you would implement specific fixes for each error type
        
        for error in errors:
            if 'Age mismatch' in error:
                # Recalculate age from birth year
                birth_year = patient_info.person.year_of_birth
                if birth_year:
                    patient_info.patient_age = date.today().year - birth_year
                    fixed_count += 1
            
            elif 'Gender mismatch' in error:
                # Update gender from OMOP concept
                gender_map = {8507: 'M', 8532: 'F', 8551: 'O', 8570: 'U'}
                patient_info.gender = gender_map.get(patient_info.person.gender_concept_id, 'U')
                fixed_count += 1
        
        if fixed_count > 0:
            patient_info.save()
        
        return fixed_count

    def get_primary_cancer_condition(self, person):
        """Get primary cancer condition for a person"""
        conditions = ConditionOccurrence.objects.filter(person=person)
        
        for condition in conditions:
            if self.is_cancer_condition(condition):
                return condition
        
        return None

    def is_cancer_condition(self, condition):
        """Check if condition is a cancer diagnosis"""
        if not condition.condition_concept:
            return False
        
        concept_name = condition.condition_concept.concept_name.lower()
        cancer_keywords = [
            'cancer', 'carcinoma', 'adenocarcinoma', 'sarcoma', 'lymphoma', 
            'leukemia', 'melanoma', 'tumor', 'neoplasm', 'malignant'
        ]
        
        return any(keyword in concept_name for keyword in cancer_keywords)

    def print_validation_summary(self, results, detailed_report):
        """Print validation summary"""
        self.stdout.write(self.style.SUCCESS('\n=== VALIDATION SUMMARY ==='))
        self.stdout.write(f'Total records validated: {results["total_validated"]}')
        self.stdout.write(f'Total errors found: {results["errors_found"]}')
        self.stdout.write(f'Total warnings found: {results["warnings_found"]}')
        
        if results.get('errors_fixed'):
            self.stdout.write(f'Errors fixed: {results["errors_fixed"]}')
        
        error_rate = (results["errors_found"] / results["total_validated"]) * 100 if results["total_validated"] > 0 else 0
        warning_rate = (results["warnings_found"] / results["total_validated"]) * 100 if results["total_validated"] > 0 else 0
        
        self.stdout.write(f'Error rate: {error_rate:.2f}%')
        self.stdout.write(f'Warning rate: {warning_rate:.2f}%')
        
        if detailed_report and results['validation_details']:
            self.stdout.write('\n=== DETAILED VALIDATION REPORT ===')
            for detail in results['validation_details']:
                if detail['errors'] or detail['warnings']:
                    self.stdout.write(f'\nPerson {detail["person_id"]}:')
                    for error in detail['errors']:
                        self.stdout.write(f'  ERROR: {error}')
                    for warning in detail['warnings']:
                        self.stdout.write(f'  WARNING: {warning}')
