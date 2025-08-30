from django.core.management.base import BaseCommand
from django.db import transaction
from omop.models import (
    Person, PatientInfo, ConditionOccurrence, Measurement, 
    DrugExposure, ProcedureOccurrence, Observation, Episode,
    TreatmentLine, TreatmentRegimen, BiomarkerMeasurement, ClinicalTrialBiomarker,
    GenomicVariant, MolecularTest, ClinicalLabTest, TumorAssessment,
    RadiationOccurrence, StemCellTransplant, ClinicalTrial, BiospecimenCollection,
    OncologyEpisodeDetail, CancerStagingMap, OncologyVocabulary
)
from datetime import date, timedelta
import logging
import json

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populate PatientInfo table from OMOP CDM tables with comprehensive oncology extensions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--person-id',
            type=int,
            help='Process specific person ID only',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Batch size for processing',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without making changes',
        )
        parser.add_argument(
            '--force-update',
            action='store_true',
            help='Force update existing PatientInfo records',
        )

    def handle(self, *args, **options):
        person_id = options.get('person_id')
        batch_size = options.get('batch_size')
        dry_run = options.get('dry_run')
        force_update = options.get('force_update')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        if person_id:
            persons = Person.objects.filter(person_id=person_id)
            self.stdout.write(f'Processing single person: {person_id}')
        else:
            persons = Person.objects.all()
            self.stdout.write(f'Processing all persons in batches of {batch_size}')
        
        total_processed = 0
        total_created = 0
        total_updated = 0
        
        for i in range(0, persons.count(), batch_size):
            batch = persons[i:i + batch_size]
            
            for person in batch:
                try:
                    created, updated = self.process_person(person, dry_run, force_update)
                    if created:
                        total_created += 1
                    if updated:
                        total_updated += 1
                    total_processed += 1
                    
                    if total_processed % 50 == 0:
                        self.stdout.write(f'Processed {total_processed} persons...')
                        
                except Exception as e:
                    self.stderr.write(f'Error processing person {person.person_id}: {str(e)}')
                    logger.error(f'Error processing person {person.person_id}: {str(e)}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Processing complete. Processed: {total_processed}, '
                f'Created: {total_created}, Updated: {total_updated}'
            )
        )

    @transaction.atomic
    def process_person(self, person, dry_run=False, force_update=False):
        """Process a single person and create/update PatientInfo"""
        
        # Check if PatientInfo already exists
        patient_info, created = PatientInfo.objects.get_or_create(person=person)
        
        if not created and not force_update:
            return False, False
        
        # Collect all data for this person
        patient_data = self.collect_patient_data(person)
        
        if dry_run:
            self.stdout.write(f'DRY RUN: Would process person {person.person_id}')
            return False, False
        
        # Update PatientInfo with collected data
        updated = self.update_patient_info(patient_info, patient_data)
        
        return created, updated

    def collect_patient_data(self, person):
        """Collect comprehensive patient data from all OMOP tables"""
        data = {
            'demographics': self.get_demographics(person),
            'conditions': self.get_cancer_conditions(person),
            'measurements': self.get_measurements(person),
            'biomarkers': self.get_biomarkers(person),
            'genomics': self.get_genomics(person),
            'treatments': self.get_treatments(person),
            'procedures': self.get_procedures(person),
            'observations': self.get_observations(person),
            'staging': self.get_staging_info(person),
            'episodes': self.get_episode_data(person),
            'trials': self.get_trial_participation(person),
            'radiation': self.get_radiation_therapy(person),
            'transplants': self.get_transplants(person),
            'biospecimens': self.get_biospecimens(person),
        }
        return data

    def get_demographics(self, person):
        """Extract demographic information"""
        today = date.today()
        birth_year = person.year_of_birth or today.year - 65  # Default age if missing
        age = today.year - birth_year
        
        # Get gender from concept mapping
        gender_map = {
            8507: 'M',     # Male
            8532: 'F',     # Female
            8551: 'O',     # Other
            8570: 'U',     # Unknown
        }
        
        return {
            'age': age,
            'gender': gender_map.get(person.gender_concept_id, 'U'),
            'race_concept_id': person.race_concept_id,
            'ethnicity_concept_id': person.ethnicity_concept_id,
        }

    def get_cancer_conditions(self, person):
        """Get primary cancer condition with enhanced staging"""
        conditions = ConditionOccurrence.objects.filter(
            person=person
        ).order_by('condition_start_date')
        
        primary_condition = None
        for condition in conditions:
            # Check if this is a cancer condition
            if self.is_cancer_condition(condition):
                primary_condition = condition
                break
        
        if not primary_condition:
            return {}
        
        return {
            'primary_condition': primary_condition,
            'disease': self.get_disease_name(primary_condition),
            'stage': self.get_comprehensive_stage(primary_condition),
            'diagnosis_date': primary_condition.condition_start_date,
            'laterality': getattr(primary_condition, 'tumor_laterality', None),
            'histology': getattr(primary_condition, 'histology_concept_id', None),
            'morphology': getattr(primary_condition, 'morphology_concept_id', None),
            'topography': getattr(primary_condition, 'topography_concept_id', None),
            'staging_system': getattr(primary_condition, 'staging_system', None),
            'ajcc_clinical_stage': getattr(primary_condition, 'ajcc_clinical_stage', None),
            'ajcc_pathologic_stage': getattr(primary_condition, 'ajcc_pathologic_stage', None),
            'grade': getattr(primary_condition, 'histologic_grade', None),
        }

    def get_measurements(self, person):
        """Get enhanced measurement data with oncology biomarkers"""
        measurements = Measurement.objects.filter(person=person).order_by('-measurement_datetime')
        
        measurement_data = {}
        
        # Standard lab values
        for measurement in measurements:
            concept_name = getattr(measurement.measurement_concept, 'concept_name', '').lower()
            
            # Map common lab values
            if 'hemoglobin' in concept_name:
                measurement_data['hemoglobin'] = measurement.value_as_number
                measurement_data['hemoglobin_unit'] = self.get_unit_name(measurement.unit_concept)
            elif 'hematocrit' in concept_name:
                measurement_data['hematocrit'] = measurement.value_as_number
            elif 'platelet' in concept_name:
                measurement_data['platelet_count'] = measurement.value_as_number
            elif 'white blood cell' in concept_name or 'wbc' in concept_name:
                measurement_data['wbc_count'] = measurement.value_as_number
            elif 'creatinine' in concept_name:
                measurement_data['creatinine'] = measurement.value_as_number
            elif 'bilirubin' in concept_name:
                measurement_data['bilirubin'] = measurement.value_as_number
            elif 'albumin' in concept_name:
                measurement_data['albumin'] = measurement.value_as_number
        
        # Add oncology-specific biomarker measurements
        biomarker_summary = self.get_biomarker_summary(person)
        measurement_data.update(biomarker_summary)
        
        return measurement_data

    def get_biomarkers(self, person):
        """Get comprehensive biomarker data from multiple sources"""
        biomarker_data = {}
        
        # From enhanced Measurement table with oncology extensions
        measurements = Measurement.objects.filter(person=person)
        for measurement in measurements:
            if hasattr(measurement, 'expression_level') and measurement.expression_level:
                biomarker_data['expression_levels'] = biomarker_data.get('expression_levels', [])
                biomarker_data['expression_levels'].append({
                    'biomarker': getattr(measurement.measurement_concept, 'concept_name', ''),
                    'level': measurement.expression_level,
                    'ihc_score': measurement.ihc_score,
                    'percent_positive': measurement.percent_positive_cells,
                    'h_score': measurement.h_score,
                })
            
            # Genomic biomarkers
            if hasattr(measurement, 'mutation_status') and measurement.mutation_status:
                biomarker_data['genomic_markers'] = biomarker_data.get('genomic_markers', [])
                biomarker_data['genomic_markers'].append({
                    'biomarker': getattr(measurement.measurement_concept, 'concept_name', ''),
                    'mutation_status': measurement.mutation_status,
                    'tmb_score': measurement.tmb_score,
                    'tmb_status': measurement.tmb_status,
                    'msi_status': measurement.msi_status,
                    'hrd_status': measurement.hrd_status,
                })
            
            # PD-L1 scoring
            if hasattr(measurement, 'pdl1_combined_positive_score') and measurement.pdl1_combined_positive_score:
                biomarker_data['pdl1_cps'] = measurement.pdl1_combined_positive_score
                biomarker_data['pdl1_tps'] = measurement.pdl1_tumor_proportion_score
                biomarker_data['pdl1_ics'] = measurement.pdl1_immune_cell_score
        
        # From BiomarkerMeasurement table
        biomarker_measurements = BiomarkerMeasurement.objects.filter(person=person)
        for bm in biomarker_measurements:
            biomarker_data['specialized_biomarkers'] = biomarker_data.get('specialized_biomarkers', [])
            biomarker_data['specialized_biomarkers'].append({
                'name': bm.biomarker_name,
                'category': bm.biomarker_category,
                'result': bm.result_interpretation,
                'numeric_value': bm.numeric_value,
                'date': bm.measurement_date,
                'assay': bm.assay_name,
            })
        
        # From ClinicalTrialBiomarker table
        trial_biomarkers = ClinicalTrialBiomarker.objects.filter(person=person)
        for tb in trial_biomarkers:
            biomarker_data['trial_biomarkers'] = biomarker_data.get('trial_biomarkers', [])
            biomarker_data['trial_biomarkers'].append({
                'type': tb.biomarker_type,
                'method': tb.test_method,
                'result': tb.categorical_result,
                'numeric_value': tb.numeric_value,
                'threshold': tb.threshold_value,
                'date': tb.test_date,
            })
        
        return biomarker_data

    def get_genomics(self, person):
        """Get genomic variant and molecular test data"""
        genomic_data = {}
        
        # Genomic variants
        variants = GenomicVariant.objects.filter(person=person)
        variant_list = []
        for variant in variants:
            variant_list.append({
                'gene': variant.gene_symbol,
                'variant_type': variant.variant_type,
                'significance': variant.clinical_significance,
                'alteration': variant.molecular_alteration,
                'biomarker_status': variant.biomarker_status,
                'hgvs': variant.hgvs_notation,
                'testing_method': variant.testing_method,
            })
        
        genomic_data['variants'] = variant_list
        
        # Molecular tests
        mol_tests = MolecularTest.objects.filter(person=person)
        test_list = []
        for test in mol_tests:
            test_list.append({
                'name': test.test_name,
                'type': test.test_type,
                'date': test.test_date,
                'result': test.overall_result,
                'actionable_count': test.actionable_alterations_count,
                'laboratory': test.laboratory,
            })
        
        genomic_data['molecular_tests'] = test_list
        
        return genomic_data

    def get_treatments(self, person):
        """Get comprehensive treatment data with oncology extensions"""
        treatment_data = {}
        
        # Treatment lines
        treatment_lines = TreatmentLine.objects.filter(person=person).order_by('line_number')
        lines_data = []
        
        for line in treatment_lines:
            line_data = {
                'line_number': line.line_number,
                'start_date': line.line_start_date,
                'end_date': line.line_end_date,
                'intent': line.treatment_intent,
                'regimen_name': line.regimen_name,
                'platinum_based': line.platinum_based,
                'immunotherapy_based': line.immunotherapy_based,
                'targeted_therapy_based': line.targeted_therapy_based,
                'response': line.treatment_response,
                'pfs_days': line.progression_free_survival_days,
                'outcome': line.treatment_outcome,
                'trial_context': line.received_in_trial,
            }
            lines_data.append(line_data)
        
        treatment_data['treatment_lines'] = lines_data
        
        # Treatment regimens
        regimens = TreatmentRegimen.objects.filter(person=person).order_by('regimen_start_date')
        regimen_data = []
        
        for regimen in regimens:
            regimen_data.append({
                'name': regimen.regimen_name,
                'line_number': regimen.line_number,
                'type': regimen.regimen_type,
                'intent': regimen.treatment_intent,
                'start_date': regimen.regimen_start_date,
                'end_date': regimen.regimen_end_date,
                'cycles_planned': regimen.cycles_planned,
                'cycles_completed': regimen.cycles_completed,
                'best_response': regimen.best_response,
                'discontinued': regimen.regimen_discontinued,
                'discontinuation_reason': regimen.discontinuation_reason,
            })
        
        treatment_data['regimens'] = regimen_data
        
        # Drug exposures with enhanced tracking
        drugs = DrugExposure.objects.filter(person=person).order_by('-drug_exposure_start_datetime')
        drug_data = []
        
        for drug in drugs:
            drug_data.append({
                'drug_name': getattr(drug.drug_concept, 'concept_name', ''),
                'start_date': drug.drug_exposure_start_datetime,
                'end_date': drug.drug_exposure_end_datetime,
                'line_of_therapy': drug.line_of_therapy,
                'classification': drug.drug_classification,
                'is_platinum': drug.is_platinum_agent,
                'is_immunotherapy': drug.is_immunotherapy,
                'is_targeted': drug.is_targeted_therapy,
                'regimen_role': drug.regimen_role,
                'trial_drug': drug.clinical_trial_drug,
                'cycle_number': drug.cycle_number,
            })
        
        treatment_data['drugs'] = drug_data
        
        return treatment_data

    def get_procedures(self, person):
        """Get procedure data with surgical oncology extensions"""
        procedures = ProcedureOccurrence.objects.filter(person=person).order_by('-procedure_datetime')
        
        procedure_data = []
        for proc in procedures:
            proc_info = {
                'procedure_name': getattr(proc.procedure_concept, 'concept_name', ''),
                'date': proc.procedure_datetime,
                'outcome': proc.procedure_outcome,
                'location': proc.procedure_location,
                'laterality': proc.procedure_laterality,
            }
            
            # Add surgical oncology extensions if available
            if hasattr(proc, 'surgical_approach') and proc.surgical_approach:
                proc_info.update({
                    'surgical_approach': proc.surgical_approach,
                    'resection_type': proc.resection_type,
                    'margin_status': proc.margin_status,
                    'lymph_nodes_examined': proc.lymph_nodes_examined,
                    'lymph_nodes_positive': proc.lymph_nodes_positive,
                    'surgical_intent': proc.surgical_intent,
                    'tumor_size_pathologic': proc.tumor_size_pathologic,
                    'operative_time_minutes': proc.operative_time_minutes,
                    'reconstruction_performed': proc.reconstruction_performed,
                })
            
            procedure_data.append(proc_info)
        
        return procedure_data

    def get_observations(self, person):
        """Get comprehensive observation data including behavioral and social determinants"""
        observations = Observation.objects.filter(person=person)
        
        obs_data = {
            'performance_status': [],
            'behavioral_factors': {},
            'social_determinants': {},
            'genetic_findings': [],
        }
        
        for obs in observations:
            # Performance status
            if hasattr(obs, 'performance_score_type') and obs.performance_score_type:
                obs_data['performance_status'].append({
                    'type': obs.performance_score_type,
                    'score': obs.value_as_number,
                    'date': obs.observation_datetime,
                })
            
            # Smoking and substance use
            if hasattr(obs, 'smoking_status') and obs.smoking_status:
                obs_data['behavioral_factors']['smoking_status'] = obs.smoking_status
                obs_data['behavioral_factors']['pack_years'] = obs.pack_years
                obs_data['behavioral_factors']['tobacco_product'] = obs.tobacco_product_type
            
            if hasattr(obs, 'alcohol_use_level') and obs.alcohol_use_level:
                obs_data['behavioral_factors']['alcohol_use'] = obs.alcohol_use_level
                obs_data['behavioral_factors']['drinks_per_week'] = obs.drinks_per_week
            
            # Reproductive health
            if hasattr(obs, 'pregnancy_status') and obs.pregnancy_status:
                obs_data['behavioral_factors']['pregnancy_status'] = obs.pregnancy_status
                obs_data['behavioral_factors']['menopausal_status'] = obs.menopausal_status
                obs_data['behavioral_factors']['contraceptive_method'] = obs.contraceptive_method
            
            # Social support
            if hasattr(obs, 'caregiver_status') and obs.caregiver_status:
                obs_data['social_determinants']['caregiver_status'] = obs.caregiver_status
                obs_data['social_determinants']['lives_alone'] = obs.lives_alone
                obs_data['social_determinants']['transportation_access'] = obs.transportation_access
            
            # Mental health
            if hasattr(obs, 'mental_health_status') and obs.mental_health_status:
                obs_data['behavioral_factors']['mental_health'] = obs.mental_health_status
                obs_data['behavioral_factors']['depression_score'] = obs.depression_screening_score
                obs_data['behavioral_factors']['anxiety_score'] = obs.anxiety_screening_score
        
        return obs_data

    def get_staging_info(self, person):
        """Get comprehensive staging information"""
        staging_data = {}
        
        # From ConditionOccurrence with enhanced staging
        conditions = ConditionOccurrence.objects.filter(person=person)
        for condition in conditions:
            if self.is_cancer_condition(condition):
                staging_data.update({
                    'clinical_t': getattr(condition, 'ajcc_clinical_t', None),
                    'clinical_n': getattr(condition, 'ajcc_clinical_n', None),
                    'clinical_m': getattr(condition, 'ajcc_clinical_m', None),
                    'pathologic_t': getattr(condition, 'ajcc_pathologic_t', None),
                    'pathologic_n': getattr(condition, 'ajcc_pathologic_n', None),
                    'pathologic_m': getattr(condition, 'ajcc_pathologic_m', None),
                    'clinical_stage_group': getattr(condition, 'ajcc_clinical_stage', None),
                    'pathologic_stage_group': getattr(condition, 'ajcc_pathologic_stage', None),
                    'staging_system': getattr(condition, 'staging_system', None),
                    'staging_system_version': getattr(condition, 'staging_system_version', None),
                })
                break
        
        # From TumorAssessment
        assessments = TumorAssessment.objects.filter(person=person).order_by('-assessment_date')
        if assessments.exists():
            latest_assessment = assessments.first()
            staging_data.update({
                'latest_assessment_date': latest_assessment.assessment_date,
                'assessment_method': latest_assessment.assessment_method,
                'overall_response': latest_assessment.overall_response,
                'disease_status': latest_assessment.disease_status,
                'sum_target_lesions': latest_assessment.sum_target_lesions,
                'new_lesions_present': latest_assessment.new_lesions_present,
            })
        
        return staging_data

    def get_episode_data(self, person):
        """Get episode and disease progression data"""
        episodes = Episode.objects.filter(person=person).order_by('episode_start_date')
        
        episode_data = []
        for episode in episodes:
            ep_data = {
                'episode_type': episode.episode_type,
                'start_date': episode.episode_start_date,
                'end_date': episode.episode_end_date,
                'disease_status': episode.disease_status,
                'response_to_treatment': episode.response_to_treatment,
            }
            
            # Get oncology episode details
            details = OncologyEpisodeDetail.objects.filter(episode=episode)
            if details.exists():
                detail = details.first()
                ep_data.update({
                    'days_from_diagnosis': detail.days_from_diagnosis,
                    'disease_status_detail': detail.disease_status,
                    'progression_type': detail.progression_type,
                    'ecog_ps': detail.ecog_performance_status,
                    'metastatic_sites': detail.total_metastatic_sites,
                })
            
            episode_data.append(ep_data)
        
        return episode_data

    def get_trial_participation(self, person):
        """Get clinical trial participation data"""
        trials = ClinicalTrial.objects.filter(person=person)
        
        trial_data = []
        for trial in trials:
            trial_data.append({
                'nct_number': trial.nct_number,
                'title': trial.trial_title,
                'phase': trial.trial_phase,
                'type': trial.trial_type,
                'enrollment_date': trial.enrollment_date,
                'completion_date': trial.trial_completion_date,
                'treatment_arm': trial.treatment_arm,
                'randomized': trial.randomized,
                'blinded': trial.blinded,
            })
        
        return trial_data

    def get_radiation_therapy(self, person):
        """Get radiation therapy data"""
        radiation = RadiationOccurrence.objects.filter(person=person)
        
        radiation_data = []
        for rad in radiation:
            radiation_data.append({
                'radiation_type': getattr(rad.radiation_concept, 'concept_name', ''),
                'start_date': rad.radiation_occurrence_start_date,
                'end_date': rad.radiation_occurrence_end_date,
                'technique': rad.radiation_technique,
                'intent': rad.treatment_intent,
                'total_dose': rad.total_dose,
                'fractions_planned': rad.fractions_planned,
                'fractions_delivered': rad.fractions_delivered,
            })
        
        return radiation_data

    def get_transplants(self, person):
        """Get stem cell transplant data"""
        transplants = StemCellTransplant.objects.filter(person=person)
        
        transplant_data = []
        for tx in transplants:
            transplant_data.append({
                'transplant_type': tx.transplant_type,
                'date': tx.transplant_date,
                'stem_cell_source': tx.stem_cell_source,
                'donor_type': tx.donor_type,
                'hla_match': getattr(tx, 'hla_match_grade', None),
            })
        
        return transplant_data

    def get_biospecimens(self, person):
        """Get biospecimen collection data"""
        biospecimens = BiospecimenCollection.objects.filter(person=person)
        
        biospecimen_data = []
        for bio in biospecimens:
            biospecimen_data.append({
                'specimen_type': bio.specimen_type,
                'collection_date': bio.collection_date,
                'collection_method': bio.collection_method,
                'tumor_content': bio.tumor_content,
                'quality': bio.specimen_quality,
                'genomic_testing': bio.genomic_testing,
                'biobank_id': bio.biobank_id,
            })
        
        return biospecimen_data

    def update_patient_info(self, patient_info, data):
        """Update PatientInfo with collected data"""
        demographics = data['demographics']
        conditions = data['conditions']
        measurements = data['measurements']
        staging = data['staging']
        treatments = data['treatments']
        
        # Update basic demographics
        patient_info.patient_age = demographics['age']
        patient_info.gender = demographics['gender']
        
        # Update cancer condition information
        if conditions:
            patient_info.disease = conditions.get('disease', '')
            patient_info.stage = conditions.get('stage', '')
            patient_info.diagnosis_date = conditions.get('diagnosis_date')
            patient_info.tumor_laterality = conditions.get('laterality', '')
        
        # Update staging information
        if staging:
            patient_info.ajcc_clinical_t = staging.get('clinical_t', '')
            patient_info.ajcc_clinical_n = staging.get('clinical_n', '')
            patient_info.ajcc_clinical_m = staging.get('clinical_m', '')
            patient_info.ajcc_pathologic_t = staging.get('pathologic_t', '')
            patient_info.ajcc_pathologic_n = staging.get('pathologic_n', '')
            patient_info.ajcc_pathologic_m = staging.get('pathologic_m', '')
            patient_info.ajcc_clinical_stage = staging.get('clinical_stage_group', '')
            patient_info.ajcc_pathologic_stage = staging.get('pathologic_stage_group', '')
        
        # Update lab values
        if measurements:
            patient_info.hemoglobin = measurements.get('hemoglobin')
            patient_info.hemoglobin_unit = measurements.get('hemoglobin_unit', 'g/dL')
            patient_info.hematocrit = measurements.get('hematocrit')
            patient_info.platelet_count = measurements.get('platelet_count')
            patient_info.wbc_count = measurements.get('wbc_count')
            patient_info.creatinine = measurements.get('creatinine')
            patient_info.bilirubin = measurements.get('bilirubin')
            patient_info.albumin = measurements.get('albumin')
        
        # Update biomarker information
        biomarkers = data['biomarkers']
        if biomarkers:
            # Store biomarker data as JSON
            patient_info.biomarker_results = json.dumps(biomarkers)
            
            # Extract key biomarkers for direct fields
            if 'pdl1_cps' in biomarkers:
                patient_info.pdl1_cps_score = biomarkers['pdl1_cps']
            if 'pdl1_tps' in biomarkers:
                patient_info.pdl1_tps_score = biomarkers['pdl1_tps']
        
        # Update genomic information
        genomics = data['genomics']
        if genomics and genomics.get('variants'):
            patient_info.genetic_test_results = json.dumps(genomics)
        
        # Update treatment information
        if treatments:
            if treatments.get('treatment_lines'):
                lines = treatments['treatment_lines']
                patient_info.prior_lines_therapy = len(lines)
                
                # Get current line information
                current_line = max(lines, key=lambda x: x['line_number']) if lines else None
                if current_line:
                    patient_info.current_line_therapy = current_line['line_number']
                    patient_info.treatment_intent = current_line.get('intent', '')
            
            # Treatment flags
            has_platinum = any(line.get('platinum_based', False) for line in treatments.get('treatment_lines', []))
            has_immunotherapy = any(line.get('immunotherapy_based', False) for line in treatments.get('treatment_lines', []))
            has_targeted = any(line.get('targeted_therapy_based', False) for line in treatments.get('treatment_lines', []))
            
            patient_info.prior_platinum_therapy = has_platinum
            patient_info.prior_immunotherapy = has_immunotherapy
            patient_info.prior_targeted_therapy = has_targeted
        
        # Store comprehensive data as JSON
        patient_info.omop_data_json = json.dumps(data, default=str)
        
        # Update timestamps
        patient_info.last_updated = date.today()
        
        patient_info.save()
        return True

    def get_biomarker_summary(self, person):
        """Get biomarker summary for key oncology markers"""
        summary = {}
        
        # Get key biomarkers from Measurement table
        measurements = Measurement.objects.filter(person=person)
        
        for measurement in measurements:
            concept_name = getattr(measurement.measurement_concept, 'concept_name', '').lower()
            
            # HER2 status
            if 'her2' in concept_name:
                if hasattr(measurement, 'ihc_score') and measurement.ihc_score:
                    summary['her2_ihc'] = measurement.ihc_score
                if hasattr(measurement, 'fish_interpretation') and measurement.fish_interpretation:
                    summary['her2_fish'] = measurement.fish_interpretation
            
            # ER/PR status
            elif 'estrogen receptor' in concept_name or 'er status' in concept_name:
                if hasattr(measurement, 'expression_level') and measurement.expression_level:
                    summary['er_status'] = measurement.expression_level
                if hasattr(measurement, 'percent_positive_cells'):
                    summary['er_percent'] = measurement.percent_positive_cells
            
            elif 'progesterone receptor' in concept_name or 'pr status' in concept_name:
                if hasattr(measurement, 'expression_level') and measurement.expression_level:
                    summary['pr_status'] = measurement.expression_level
                if hasattr(measurement, 'percent_positive_cells'):
                    summary['pr_percent'] = measurement.percent_positive_cells
            
            # TMB and MSI
            elif 'tumor mutational burden' in concept_name or 'tmb' in concept_name:
                if hasattr(measurement, 'tmb_status') and measurement.tmb_status:
                    summary['tmb_status'] = measurement.tmb_status
                if hasattr(measurement, 'tmb_score'):
                    summary['tmb_score'] = measurement.tmb_score
            
            elif 'microsatellite' in concept_name or 'msi' in concept_name:
                if hasattr(measurement, 'msi_status') and measurement.msi_status:
                    summary['msi_status'] = measurement.msi_status
        
        return summary

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

    def get_disease_name(self, condition):
        """Extract disease name from condition"""
        if condition.condition_concept:
            return condition.condition_concept.concept_name
        return 'Unknown Cancer'

    def get_comprehensive_stage(self, condition):
        """Get comprehensive staging information"""
        # Try different staging fields
        stage_fields = [
            'ajcc_clinical_stage', 'ajcc_pathologic_stage', 
            'overall_stage', 'condition_status_concept_id'
        ]
        
        for field in stage_fields:
            stage = getattr(condition, field, None)
            if stage:
                return str(stage)
        
        return 'Unknown'

    def get_unit_name(self, unit_concept):
        """Get unit name from concept"""
        if unit_concept:
            return unit_concept.concept_name
        return ''
