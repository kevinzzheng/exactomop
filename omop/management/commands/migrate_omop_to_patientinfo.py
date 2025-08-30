"""
Django management command to migrate OMOP CDM data to PatientInfo table.

This command extracts data from OMOP Person, Measurement, Observation, ConditionOccurrence,
TreatmentRegimen, and other tables to populate the consolidated PatientInfo model.

Usage:
    python manage.py migrate_omop_to_patientinfo
    python manage.py migrate_omop_to_patientinfo --clean
    python manage.py migrate_omop_to_patientinfo --person-ids 1,2,3
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import datetime, date
import json

from omop.models import (
    Person, PatientInfo, Measurement, Observation, ConditionOccurrence, 
    TreatmentRegimen, TreatmentLine, GenomicVariant, Concept
)


class Command(BaseCommand):
    help = 'Migrate OMOP CDM data to PatientInfo table'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clean existing PatientInfo records before migration',
        )
        parser.add_argument(
            '--person-ids',
            type=str,
            help='Comma-separated list of Person IDs to migrate (if not specified, migrates all)',
        )

    def handle(self, *args, **options):
        self.stdout.write("🔄 Starting OMOP to PatientInfo migration...")
        
        if options['clean']:
            self.stdout.write("🧹 Cleaning existing PatientInfo records...")
            PatientInfo.objects.all().delete()
            self.stdout.write("✅ Cleaned existing PatientInfo records")

        # Determine which persons to migrate
        if options['person_ids']:
            person_ids = [int(id.strip()) for id in options['person_ids'].split(',')]
            persons = Person.objects.filter(person_id__in=person_ids)
        else:
            persons = Person.objects.all()

        total_persons = persons.count()
        self.stdout.write(f"📊 Found {total_persons} persons to migrate")

        migrated_count = 0
        failed_count = 0

        for person in persons:
            try:
                with transaction.atomic():
                    patient_info = self.migrate_person_to_patient_info(person)
                    if patient_info:
                        migrated_count += 1
                        if migrated_count % 10 == 0:
                            self.stdout.write(f"✅ Migrated {migrated_count}/{total_persons} patients")
                    else:
                        failed_count += 1
                        self.stdout.write(f"⚠️  Skipped Person {person.person_id} (no data to migrate)")
                        
            except Exception as e:
                failed_count += 1
                self.stdout.write(f"❌ Error migrating Person {person.person_id}: {str(e)}")

        self.stdout.write(f"\n🎉 Migration complete!")
        self.stdout.write(f"✅ Successfully migrated: {migrated_count}")
        self.stdout.write(f"❌ Failed/Skipped: {failed_count}")
        self.stdout.write(f"📊 Total processed: {total_persons}")

    def migrate_person_to_patient_info(self, person):
        """Migrate a single Person and related OMOP data to PatientInfo"""
        
        # Check if PatientInfo already exists
        patient_info, created = PatientInfo.objects.get_or_create(
            person=person,
            defaults={}
        )
        
        if not created:
            self.stdout.write(f"📝 Updating existing PatientInfo for Person {person.person_id}")

        # Extract demographics from Person
        self.extract_demographics(person, patient_info)
        
        # Extract disease information from ConditionOccurrence
        self.extract_disease_info(person, patient_info)
        
        # Extract lab values and biomarkers from Measurement
        self.extract_lab_values(person, patient_info)
        
        # Extract clinical observations
        self.extract_observations(person, patient_info)
        
        # Extract treatment information
        self.extract_treatment_info(person, patient_info)
        
        # Extract genomic information
        self.extract_genomic_info(person, patient_info)
        
        # Calculate derived fields
        self.calculate_derived_fields(patient_info)
        
        patient_info.save()
        return patient_info

    def extract_demographics(self, person, patient_info):
        """Extract demographic information from Person"""
        
        # Basic demographics
        if person.birth_datetime:
            today = date.today()
            birth_date = person.birth_datetime.date() if hasattr(person.birth_datetime, 'date') else person.birth_datetime
            patient_info.patient_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Gender mapping from OMOP concept to PatientInfo choices
        if person.gender_concept_id:
            gender_mapping = {
                8507: 'M',   # Male
                8532: 'F',   # Female
                8551: 'U',   # Unknown
                8570: 'O',   # Other (though not in PatientInfo choices, will default to None)
            }
            patient_info.gender = gender_mapping.get(person.gender_concept_id)
        
        # Race and ethnicity
        if person.race_concept_id:
            try:
                race_concept = Concept.objects.get(concept_id=person.race_concept_id)
                patient_info.ethnicity = race_concept.concept_name
            except Concept.DoesNotExist:
                pass
        
        # Location information
        if person.location_id:
            # In a real implementation, you'd extract from Location table
            # For now, we'll set some defaults
            patient_info.country = "United States"

    def extract_disease_info(self, person, patient_info):
        """Extract disease information from ConditionOccurrence"""
        
        # Get primary condition (assuming breast cancer for our dataset)
        primary_condition = ConditionOccurrence.objects.filter(
            person=person,
            condition_concept_id__in=[4112853, 4263086, 4180790]  # Breast cancer concepts
        ).first()
        
        if primary_condition:
            patient_info.disease = "breast cancer"
            
            # Extract staging information from related Observations
            staging_obs = Observation.objects.filter(
                person=person,
                observation_concept_id__in=[
                    1635579,  # TNM T stage
                    1634371,  # TNM N stage  
                    1634444,  # TNM M stage
                    1635919,  # Overall stage
                ]
            )
            
            stage_components = []
            for obs in staging_obs:
                if obs.value_as_string:
                    stage_components.append(obs.value_as_string)
                elif obs.value_as_concept:
                    try:
                        concept = Concept.objects.get(concept_id=obs.value_as_concept.concept_id)
                        stage_components.append(concept.concept_name)
                    except Concept.DoesNotExist:
                        pass
            
            if stage_components:
                patient_info.stage = " ".join(stage_components)
                patient_info.tumor_stage = stage_components[0] if len(stage_components) > 0 else None
                patient_info.nodes_stage = stage_components[1] if len(stage_components) > 1 else None
                patient_info.distant_metastasis_stage = stage_components[2] if len(stage_components) > 2 else None

    def extract_lab_values(self, person, patient_info):
        """Extract laboratory values and biomarkers from Measurement"""
        
        # Hormone receptor status (ER, PR, HER2)
        hormone_measurements = Measurement.objects.filter(
            person=person,
            measurement_concept_id__in=[
                4268518,  # ER status
                4069297,  # PR status  
                4058187,  # HER2 status
            ]
        )
        
        for measurement in hormone_measurements:
            if measurement.measurement_concept_id == 4268518:  # ER
                patient_info.estrogen_receptor_status = measurement.measurement_source_value or measurement.value_as_string
            elif measurement.measurement_concept_id == 4069297:  # PR
                patient_info.progesterone_receptor_status = measurement.measurement_source_value or measurement.value_as_string
            elif measurement.measurement_concept_id == 4058187:  # HER2
                patient_info.her2_status = measurement.measurement_source_value or measurement.value_as_string

        # Blood work values
        blood_measurements = Measurement.objects.filter(
            person=person,
            measurement_concept_id__in=[
                3000963,  # Hemoglobin
                3013682,  # White blood cell count
                3012888,  # Platelet count
                3016723,  # Creatinine
                3006906,  # Albumin
            ]
        )
        
        for measurement in blood_measurements:
            value = measurement.value_as_number
            if value is None:
                continue
                
            if measurement.measurement_concept_id == 3000963:  # Hemoglobin
                patient_info.hemoglobin_level = value
                patient_info.hemoglobin_level_units = 'G/DL'
            elif measurement.measurement_concept_id == 3013682:  # WBC
                patient_info.white_blood_cell_count = value
                patient_info.white_blood_cell_count_units = 'CELLS/L'
            elif measurement.measurement_concept_id == 3012888:  # Platelets
                patient_info.platelet_count = int(value) if value else None
                patient_info.platelet_count_units = 'CELLS/UL'
            elif measurement.measurement_concept_id == 3016723:  # Creatinine
                patient_info.serum_creatinine_level = value
                patient_info.serum_creatinine_level_units = 'MG/DL'
            elif measurement.measurement_concept_id == 3006906:  # Albumin
                patient_info.albumin_level = value
                patient_info.albumin_level_units = 'G/DL'

        # Tumor markers
        tumor_markers = Measurement.objects.filter(
            person=person,
            measurement_concept_id__in=[
                3007220,  # CA 15-3
                3009261,  # CA 27.29
            ]
        )
        
        # For now, we'll store these in a text field since PatientInfo doesn't have specific fields
        marker_values = []
        for marker in tumor_markers:
            if marker.value_as_number:
                concept_name = "Unknown"
                try:
                    concept = Concept.objects.get(concept_id=marker.measurement_concept_id)
                    concept_name = concept.concept_name
                except Concept.DoesNotExist:
                    pass
                marker_values.append(f"{concept_name}: {marker.value_as_number}")
        
        if marker_values:
            # Store in a generic text field for now
            if hasattr(patient_info, 'molecular_markers'):
                patient_info.molecular_markers = "; ".join(marker_values)

    def extract_observations(self, person, patient_info):
        """Extract clinical observations and social determinants"""
        
        # Performance status
        performance_obs = Observation.objects.filter(
            person=person,
            observation_concept_id__in=[
                4161279,  # ECOG performance status
                4174715,  # Karnofsky performance status
            ]
        ).first()
        
        if performance_obs:
            if performance_obs.value_as_number is not None:
                if performance_obs.observation_concept_id == 4161279:  # ECOG
                    patient_info.ecog_performance_status = int(performance_obs.value_as_number)
                elif performance_obs.observation_concept_id == 4174715:  # Karnofsky
                    patient_info.karnofsky_performance_score = int(performance_obs.value_as_number)

        # Smoking status
        smoking_obs = Observation.objects.filter(
            person=person,
            observation_concept_id=4013634  # Smoking status
        ).first()
        
        if smoking_obs and smoking_obs.observation_source_value:
            patient_info.no_tobacco_use_status = smoking_obs.observation_source_value.lower() == 'never'
            if smoking_obs.observation_source_value.lower() != 'never':
                patient_info.tobacco_use_details = smoking_obs.observation_source_value

        # Alcohol use
        alcohol_obs = Observation.objects.filter(
            person=person,
            observation_concept_id=4267213  # Alcohol use
        ).first()
        
        if alcohol_obs and alcohol_obs.observation_source_value:
            # Store alcohol use details if not 'Never'
            if alcohol_obs.observation_source_value.lower() != 'never':
                patient_info.substance_use_details = f"Alcohol: {alcohol_obs.observation_source_value}"

    def extract_treatment_info(self, person, patient_info):
        """Extract treatment information from TreatmentRegimen and TreatmentLine"""
        
        # Get treatment lines
        treatment_lines = TreatmentLine.objects.filter(person=person).order_by('line_number')
        
        if treatment_lines.exists():
            patient_info.therapy_lines_count = treatment_lines.count()
            
            # First line therapy
            first_line = treatment_lines.filter(line_number=1).first()
            if first_line:
                patient_info.first_line_date = first_line.line_start_date
                patient_info.first_line_outcome = first_line.treatment_response
                
                # Get associated treatment regimen
                regimen = TreatmentRegimen.objects.filter(
                    person=person,
                    regimen_start_date__lte=first_line.line_start_date,
                    regimen_end_date__gte=first_line.line_start_date
                ).first()
                
                if regimen:
                    patient_info.first_line_therapy = regimen.regimen_name or "Systemic therapy"

            # Second line therapy
            second_line = treatment_lines.filter(line_number=2).first()
            if second_line:
                patient_info.second_line_date = second_line.line_start_date
                patient_info.second_line_outcome = second_line.treatment_response
                
                regimen = TreatmentRegimen.objects.filter(
                    person=person,
                    regimen_start_date__lte=second_line.line_start_date,
                    regimen_end_date__gte=second_line.line_start_date
                ).first()
                
                if regimen:
                    patient_info.second_line_therapy = regimen.regimen_name or "Systemic therapy"

        # Get last treatment date from most recent regimen
        last_regimen = TreatmentRegimen.objects.filter(person=person).order_by('-regimen_end_date').first()
        if last_regimen and last_regimen.regimen_end_date:
            patient_info.last_treatment = last_regimen.regimen_end_date

    def extract_genomic_info(self, person, patient_info):
        """Extract genomic information from GenomicVariant"""
        
        variants = GenomicVariant.objects.filter(person=person)
        
        if variants.exists():
            genetic_mutations = []
            for variant in variants:
                mutation_info = {
                    'gene': variant.gene_symbol,
                    'variant': variant.hgvs_notation or variant.protein_change or 'Unknown',
                    'type': variant.variant_type,
                    'clinical_significance': variant.clinical_significance,
                }
                if variant.variant_allele_frequency:
                    mutation_info['allele_frequency'] = float(variant.variant_allele_frequency)
                
                genetic_mutations.append(mutation_info)
            
            patient_info.genetic_mutations = genetic_mutations
            
            # Extract specific mutations for breast cancer
            brca_variants = variants.filter(gene_symbol__in=['BRCA1', 'BRCA2'])
            if brca_variants.exists():
                brca_info = []
                for variant in brca_variants:
                    variant_desc = variant.hgvs_notation or variant.protein_change or 'mutation detected'
                    brca_info.append(f"{variant.gene_symbol}: {variant_desc}")
                patient_info.molecular_markers = "; ".join(brca_info)

    def calculate_derived_fields(self, patient_info):
        """Calculate derived fields like BMI"""
        
        if patient_info.height and patient_info.weight:
            # Convert height to meters if in cm
            height_m = patient_info.height
            if patient_info.height_units == 'cm':
                height_m = patient_info.height / 100
            elif patient_info.height_units == 'in':
                height_m = patient_info.height * 0.0254
            
            # Convert weight to kg if needed
            weight_kg = patient_info.weight
            if patient_info.weight_units == 'lb':
                weight_kg = patient_info.weight * 0.453592
            
            if height_m > 0:
                patient_info.bmi = round(weight_kg / (height_m ** 2), 2)

        # Set breast cancer specific defaults
        if patient_info.disease == "breast cancer":
            # Default values for breast cancer patients
            if patient_info.no_other_active_malignancies is None:
                patient_info.no_other_active_malignancies = True
            if patient_info.consent_capability is None:
                patient_info.consent_capability = True
