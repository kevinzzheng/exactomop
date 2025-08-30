from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q, Max
from omop.models import (
    Person, PatientInfo, ConditionOccurrence, Measurement, 
    DrugExposure, ProcedureOccurrence, Observation, Episode,
    TreatmentLine, TreatmentRegimen, BiomarkerMeasurement, ClinicalTrialBiomarker,
    GenomicVariant, MolecularTest, ClinicalLabTest, TumorAssessment,
    RadiationOccurrence, StemCellTransplant, ClinicalTrial, BiospecimenCollection,
    OncologyEpisodeDetail
)
from datetime import date, datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update PatientInfo records with latest data from OMOP CDM tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--person-id',
            type=int,
            help='Update specific person ID only',
        )
        parser.add_argument(
            '--updated-since',
            type=str,
            help='Update records modified since date (YYYY-MM-DD)',
        )
        parser.add_argument(
            '--force-update',
            action='store_true',
            help='Force update even if PatientInfo is newer',
        )
        parser.add_argument(
            '--incremental',
            action='store_true',
            help='Only update fields with new data',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of records to process in each batch',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        person_id = options.get('person_id')
        updated_since = options.get('updated_since')
        force_update = options.get('force_update')
        incremental = options.get('incremental')
        batch_size = options.get('batch_size')
        dry_run = options.get('dry_run')
        
        # Parse updated_since date
        since_date = None
        if updated_since:
            try:
                since_date = datetime.strptime(updated_since, '%Y-%m-%d').date()
            except ValueError:
                self.stderr.write('Invalid date format. Use YYYY-MM-DD')
                return
        
        self.stdout.write(f'Starting PatientInfo update ({"DRY RUN" if dry_run else "LIVE RUN"})')
        
        # Build query for persons to update
        person_query = self.build_person_query(person_id, since_date, force_update)
        
        total_persons = person_query.count()
        self.stdout.write(f'Found {total_persons} persons to process')
        
        if total_persons == 0:
            self.stdout.write('No persons found matching criteria.')
            return
        
        update_stats = {
            'processed': 0,
            'updated': 0,
            'created': 0,
            'skipped': 0,
            'errors': 0
        }
        
        # Process in batches
        for i in range(0, total_persons, batch_size):
            batch_persons = person_query[i:i + batch_size]
            
            for person in batch_persons:
                try:
                    result = self.update_patient_info(
                        person, incremental, force_update, dry_run
                    )
                    
                    update_stats['processed'] += 1
                    update_stats[result] += 1
                    
                    if update_stats['processed'] % 50 == 0:
                        self.stdout.write(
                            f'Processed {update_stats["processed"]}/{total_persons} persons...'
                        )
                        
                except Exception as e:
                    update_stats['errors'] += 1
                    self.stderr.write(f'Error updating person {person.person_id}: {str(e)}')
                    logger.error(f'Error updating person {person.person_id}: {str(e)}')
        
        self.print_update_summary(update_stats, dry_run)

    def build_person_query(self, person_id, since_date, force_update):
        """Build query for persons to update"""
        
        if person_id:
            return Person.objects.filter(person_id=person_id)
        
        # Start with all persons
        query = Person.objects.all()
        
        if since_date and not force_update:
            # Find persons with OMOP data modified since the date
            modified_conditions = ConditionOccurrence.objects.filter(
                Q(condition_start_date__gte=since_date) |
                Q(condition_end_date__gte=since_date)
            ).values_list('person_id', flat=True)
            
            modified_measurements = Measurement.objects.filter(
                measurement_date__gte=since_date
            ).values_list('person_id', flat=True)
            
            modified_drugs = DrugExposure.objects.filter(
                drug_exposure_start_date__gte=since_date
            ).values_list('person_id', flat=True)
            
            modified_procedures = ProcedureOccurrence.objects.filter(
                procedure_date__gte=since_date
            ).values_list('person_id', flat=True)
            
            # Combine all modified person IDs
            modified_person_ids = set()
            modified_person_ids.update(modified_conditions)
            modified_person_ids.update(modified_measurements)
            modified_person_ids.update(modified_drugs)
            modified_person_ids.update(modified_procedures)
            
            if modified_person_ids:
                query = query.filter(person_id__in=modified_person_ids)
            else:
                # No modifications found
                query = Person.objects.none()
        
        return query.order_by('person_id')

    def update_patient_info(self, person, incremental, force_update, dry_run):
        """Update PatientInfo for a single person"""
        
        try:
            patient_info = PatientInfo.objects.get(person=person)
            is_new = False
        except PatientInfo.DoesNotExist:
            patient_info = PatientInfo(person=person)
            is_new = True
        
        # Check if update is needed
        if not is_new and not force_update:
            if self.should_skip_update(patient_info, person):
                return 'skipped'
        
        # Store original values for comparison
        original_data = self.get_patient_info_snapshot(patient_info) if not is_new else {}
        
        # Update demographics
        self.update_demographics(patient_info, person, incremental)
        
        # Update cancer condition information
        self.update_cancer_condition(patient_info, person, incremental)
        
        # Update staging information
        self.update_staging(patient_info, person, incremental)
        
        # Update laboratory values
        self.update_lab_values(patient_info, person, incremental)
        
        # Update biomarker data
        self.update_biomarkers(patient_info, person, incremental)
        
        # Update treatment information
        self.update_treatments(patient_info, person, incremental)
        
        # Update genomic data
        self.update_genomics(patient_info, person, incremental)
        
        # Update comprehensive OMOP data
        self.update_comprehensive_data(patient_info, person, incremental)
        
        # Check if any changes were made
        current_data = self.get_patient_info_snapshot(patient_info)
        has_changes = original_data != current_data or is_new
        
        if dry_run:
            if has_changes:
                self.stdout.write(f'DRY RUN: Would {"create" if is_new else "update"} PatientInfo for person {person.person_id}')
            return 'updated' if has_changes else 'skipped'
        
        if has_changes:
            patient_info.updated_at = datetime.now()
            patient_info.save()
            return 'created' if is_new else 'updated'
        else:
            return 'skipped'

    def should_skip_update(self, patient_info, person):
        """Determine if update should be skipped"""
        
        # Get latest modification dates from OMOP data
        latest_condition = ConditionOccurrence.objects.filter(person=person).aggregate(
            max_date=Max('condition_start_date')
        )['max_date']
        
        latest_measurement = Measurement.objects.filter(person=person).aggregate(
            max_date=Max('measurement_date')
        )['max_date']
        
        latest_drug = DrugExposure.objects.filter(person=person).aggregate(
            max_date=Max('drug_exposure_start_date')
        )['max_date']
        
        latest_procedure = ProcedureOccurrence.objects.filter(person=person).aggregate(
            max_date=Max('procedure_date')
        )['max_date']
        
        # Find the most recent OMOP modification
        omop_dates = [d for d in [latest_condition, latest_measurement, latest_drug, latest_procedure] if d]
        
        if not omop_dates:
            return True  # No OMOP data, skip update
        
        latest_omop_date = max(omop_dates)
        
        # Compare with PatientInfo update date
        if patient_info.updated_at and patient_info.updated_at.date() >= latest_omop_date:
            return True  # PatientInfo is newer or same age
        
        return False

    def get_patient_info_snapshot(self, patient_info):
        """Get a snapshot of PatientInfo data for comparison"""
        
        return {
            'patient_age': patient_info.patient_age,
            'gender': patient_info.gender,
            'disease': patient_info.disease,
            'diagnosis_date': patient_info.diagnosis_date,
            'hemoglobin': patient_info.hemoglobin,
            'hematocrit': patient_info.hematocrit,
            'platelet_count': patient_info.platelet_count,
            'wbc_count': patient_info.wbc_count,
            'creatinine': patient_info.creatinine,
            'bilirubin': patient_info.bilirubin,
            'albumin': patient_info.albumin,
            'prior_lines_therapy': patient_info.prior_lines_therapy,
            'current_line_therapy': patient_info.current_line_therapy,
            'prior_platinum_therapy': patient_info.prior_platinum_therapy,
            'prior_immunotherapy': patient_info.prior_immunotherapy,
            'prior_targeted_therapy': patient_info.prior_targeted_therapy,
            'pdl1_cps_score': patient_info.pdl1_cps_score,
            'pdl1_tps_score': patient_info.pdl1_tps_score,
            'biomarker_results': patient_info.biomarker_results,
            'genetic_test_results': patient_info.genetic_test_results,
            'omop_data_json': patient_info.omop_data_json,
        }

    def update_demographics(self, patient_info, person, incremental):
        """Update demographic information"""
        
        # Calculate age
        if person.year_of_birth:
            calculated_age = date.today().year - person.year_of_birth
            if not incremental or not patient_info.patient_age:
                patient_info.patient_age = calculated_age
        
        # Update gender
        gender_map = {8507: 'M', 8532: 'F', 8551: 'O', 8570: 'U'}
        calculated_gender = gender_map.get(person.gender_concept_id, 'U')
        if not incremental or not patient_info.gender:
            patient_info.gender = calculated_gender

    def update_cancer_condition(self, patient_info, person, incremental):
        """Update cancer condition information"""
        
        # Get primary cancer condition
        cancer_condition = self.get_primary_cancer_condition(person)
        
        if cancer_condition:
            # Update disease name
            if not incremental or not patient_info.disease:
                if cancer_condition.condition_concept:
                    patient_info.disease = cancer_condition.condition_concept.concept_name
            
            # Update diagnosis date
            if not incremental or not patient_info.diagnosis_date:
                patient_info.diagnosis_date = cancer_condition.condition_start_date
            
            # Update tumor laterality
            if hasattr(cancer_condition, 'tumor_laterality'):
                if not incremental or not patient_info.tumor_laterality:
                    patient_info.tumor_laterality = cancer_condition.tumor_laterality

    def update_staging(self, patient_info, person, incremental):
        """Update staging information"""
        
        cancer_condition = self.get_primary_cancer_condition(person)
        
        if cancer_condition:
            staging_fields = [
                'ajcc_clinical_t', 'ajcc_clinical_n', 'ajcc_clinical_m',
                'ajcc_pathologic_t', 'ajcc_pathologic_n', 'ajcc_pathologic_m',
                'ajcc_clinical_stage', 'ajcc_pathologic_stage'
            ]
            
            for field in staging_fields:
                if hasattr(cancer_condition, field):
                    omop_value = getattr(cancer_condition, field)
                    if omop_value and (not incremental or not getattr(patient_info, field, None)):
                        setattr(patient_info, field, omop_value)

    def update_lab_values(self, patient_info, person, incremental):
        """Update laboratory values with latest results"""
        
        # Get latest measurements
        latest_measurements = Measurement.objects.filter(
            person=person
        ).order_by('measurement_concept_id', '-measurement_datetime').distinct('measurement_concept_id')
        
        lab_mappings = {
            'hemoglobin': ['hemoglobin', 'hgb'],
            'hematocrit': ['hematocrit', 'hct'],
            'platelet_count': ['platelet', 'plt'],
            'wbc_count': ['white blood cell', 'wbc', 'leukocyte'],
            'creatinine': ['creatinine'],
            'bilirubin': ['bilirubin'],
            'albumin': ['albumin']
        }
        
        for pi_field, keywords in lab_mappings.items():
            if incremental and getattr(patient_info, pi_field):
                continue  # Skip if value exists and incremental update
            
            for measurement in latest_measurements:
                if measurement.measurement_concept and measurement.value_as_number:
                    concept_name = measurement.measurement_concept.concept_name.lower()
                    if any(keyword in concept_name for keyword in keywords):
                        setattr(patient_info, pi_field, measurement.value_as_number)
                        break

    def update_biomarkers(self, patient_info, person, incremental):
        """Update biomarker information"""
        
        # Update PD-L1 scores
        pdl1_measurements = Measurement.objects.filter(
            person=person,
            measurement_concept__concept_name__icontains='pd-l1'
        ).order_by('-measurement_datetime')
        
        for measurement in pdl1_measurements:
            concept_name = measurement.measurement_concept.concept_name.lower()
            if 'cps' in concept_name and (not incremental or not patient_info.pdl1_cps_score):
                patient_info.pdl1_cps_score = measurement.value_as_number
            elif 'tps' in concept_name and (not incremental or not patient_info.pdl1_tps_score):
                patient_info.pdl1_tps_score = measurement.value_as_number
        
        # Update biomarker results JSON
        if not incremental or not patient_info.biomarker_results:
            biomarker_data = self.collect_biomarker_data(person)
            if biomarker_data:
                patient_info.biomarker_results = json.dumps(biomarker_data)

    def update_treatments(self, patient_info, person, incremental):
        """Update treatment information"""
        
        treatment_lines = TreatmentLine.objects.filter(person=person)
        
        if treatment_lines.exists():
            # Update prior lines
            if not incremental or not patient_info.prior_lines_therapy:
                patient_info.prior_lines_therapy = treatment_lines.count()
            
            # Update current line
            if not incremental or not patient_info.current_line_therapy:
                max_line = treatment_lines.aggregate(max_line=Max('line_number'))['max_line']
                patient_info.current_line_therapy = max_line
            
            # Update therapy flags
            if not incremental or not patient_info.prior_platinum_therapy:
                patient_info.prior_platinum_therapy = treatment_lines.filter(
                    platinum_based=True
                ).exists()
            
            if not incremental or not patient_info.prior_immunotherapy:
                patient_info.prior_immunotherapy = treatment_lines.filter(
                    immunotherapy_based=True
                ).exists()
            
            if not incremental or not patient_info.prior_targeted_therapy:
                patient_info.prior_targeted_therapy = treatment_lines.filter(
                    targeted_therapy_based=True
                ).exists()

    def update_genomics(self, patient_info, person, incremental):
        """Update genomic data"""
        
        if not incremental or not patient_info.genetic_test_results:
            genomic_data = self.collect_genomic_data(person)
            if genomic_data:
                patient_info.genetic_test_results = json.dumps(genomic_data)

    def update_comprehensive_data(self, patient_info, person, incremental):
        """Update comprehensive OMOP data JSON"""
        
        if not incremental or not patient_info.omop_data_json:
            comprehensive_data = self.collect_comprehensive_data(person)
            if comprehensive_data:
                patient_info.omop_data_json = json.dumps(comprehensive_data)

    def collect_biomarker_data(self, person):
        """Collect biomarker data from various sources"""
        biomarker_data = {}
        
        # Get biomarker measurements
        biomarkers = BiomarkerMeasurement.objects.filter(person=person)
        for biomarker in biomarkers:
            biomarker_data[biomarker.biomarker_name] = {
                'result': biomarker.result_value,
                'date': biomarker.measurement_date.isoformat() if biomarker.measurement_date else None,
                'method': biomarker.test_method
            }
        
        return biomarker_data

    def collect_genomic_data(self, person):
        """Collect genomic data"""
        genomic_data = {}
        
        # Get genomic variants
        variants = GenomicVariant.objects.filter(person=person)
        genomic_data['variants'] = []
        
        for variant in variants:
            genomic_data['variants'].append({
                'gene': variant.gene_name,
                'variant': variant.variant_name,
                'type': variant.variant_type,
                'significance': variant.clinical_significance
            })
        
        return genomic_data

    def collect_comprehensive_data(self, person):
        """Collect comprehensive OMOP data"""
        data = {}
        
        # Radiation therapy
        radiation = RadiationOccurrence.objects.filter(person=person)
        if radiation.exists():
            data['radiation'] = [
                {
                    'date': r.radiation_start_date.isoformat() if r.radiation_start_date else None,
                    'technique': r.radiation_technique,
                    'dose': r.total_dose,
                    'intent': r.treatment_intent
                }
                for r in radiation
            ]
        
        # Clinical trials
        trials = ClinicalTrial.objects.filter(person=person)
        if trials.exists():
            data['trials'] = [
                {
                    'identifier': t.trial_identifier,
                    'phase': t.trial_phase,
                    'start_date': t.enrollment_date.isoformat() if t.enrollment_date else None
                }
                for t in trials
            ]
        
        return data

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

    def print_update_summary(self, stats, dry_run):
        """Print update summary"""
        
        self.stdout.write(self.style.SUCCESS('\n=== UPDATE SUMMARY ==='))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No actual changes made'))
        
        self.stdout.write(f'Total persons processed: {stats["processed"]}')
        self.stdout.write(f'Records {"would be " if dry_run else ""}created: {stats["created"]}')
        self.stdout.write(f'Records {"would be " if dry_run else ""}updated: {stats["updated"]}')
        self.stdout.write(f'Records skipped: {stats["skipped"]}')
        self.stdout.write(f'Errors encountered: {stats["errors"]}')
        
        success_rate = ((stats["created"] + stats["updated"]) / stats["processed"]) * 100 if stats["processed"] > 0 else 0
        self.stdout.write(f'Success rate: {success_rate:.2f}%')
        
        if dry_run and (stats["created"] + stats["updated"]) > 0:
            self.stdout.write(
                self.style.WARNING(
                    '\nTo perform actual updates, run this command again without --dry-run'
                )
            )
