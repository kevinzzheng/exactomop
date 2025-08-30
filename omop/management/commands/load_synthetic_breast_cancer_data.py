"""
Django management command to load synthetic breast cancer patient data
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Load synthetic breast cancer patient data with comprehensive TreatmentRegimen entries'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading new data',
        )

    def handle(self, *args, **options):
        fixture_path = 'omop/fixtures/synthetic_breast_cancer_patients.json'
        
        if not os.path.exists(fixture_path):
            self.stdout.write(
                self.style.ERROR(f'Fixture file not found: {fixture_path}')
            )
            return

        if options['clear']:
            self.stdout.write('Clearing existing data...')
            # Clear data in reverse dependency order
            from omop.models import (
                TreatmentRegimen, TreatmentLine, Measurement, 
                ConditionOccurrence, Person, Concept
            )
            
            TreatmentRegimen.objects.all().delete()
            TreatmentLine.objects.all().delete()
            Measurement.objects.all().delete()
            ConditionOccurrence.objects.all().delete()
            Person.objects.all().delete()
            # Don't delete all concepts, just the ones we know we're adding
            concept_ids = [4112853, 35807188, 35807075, 35807189, 35807076, 35807077, 35807078,
                          8532, 8527, 8516, 8515, 38003564, 38003563, 32020, 44818702,
                          4181412, 9189, 3000963, 3006256, 3013682]
            Concept.objects.filter(concept_id__in=concept_ids).delete()
            
            self.stdout.write(self.style.SUCCESS('Data cleared successfully'))

        self.stdout.write(f'Loading synthetic data from {fixture_path}...')
        
        try:
            call_command('loaddata', fixture_path, verbosity=1)
            self.stdout.write(
                self.style.SUCCESS('Successfully loaded synthetic breast cancer data')
            )
            
            # Print summary
            from omop.models import Person, TreatmentRegimen, TreatmentLine, Measurement
            
            person_count = Person.objects.count()
            regimen_count = TreatmentRegimen.objects.count()
            line_count = TreatmentLine.objects.count()
            measurement_count = Measurement.objects.count()
            
            self.stdout.write(f'\nData Summary:')
            self.stdout.write(f'  Patients: {person_count}')
            self.stdout.write(f'  Treatment Regimens: {regimen_count}')
            self.stdout.write(f'  Treatment Lines: {line_count}')
            self.stdout.write(f'  Measurements: {measurement_count}')
            
            # Show some sample regimens
            self.stdout.write(f'\nSample Treatment Regimens:')
            for regimen in TreatmentRegimen.objects.select_related('person')[:5]:
                self.stdout.write(f'  Patient {regimen.person.person_source_value}: '
                                f'{regimen.regimen_name} (Line {regimen.line_number}) - '
                                f'{regimen.best_response} response')
                                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading data: {str(e)}')
            )
