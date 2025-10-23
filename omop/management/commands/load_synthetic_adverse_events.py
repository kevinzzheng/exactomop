"""
Django management command to load synthetic adverse event data for safety scoring testing
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
import os


class Command(BaseCommand):
    help = 'Load synthetic adverse event data with trial arms and comprehensive AE records for testing safety scoring'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing trial arms and adverse events before loading new data',
        )
        parser.add_argument(
            '--compute-scores',
            action='store_true',
            help='Automatically compute safety scores after loading data',
        )

    def handle(self, *args, **options):
        fixture_path = 'omop/fixtures/synthetic_adverse_events.json'
        
        if not os.path.exists(fixture_path):
            self.stdout.write(
                self.style.ERROR(f'Fixture file not found: {fixture_path}')
            )
            return

        if options['clear']:
            self.stdout.write('Clearing existing adverse event data...')
            from omop.models_safety import AdverseEvent, TrialArm, TrialArmSafetyMetrics
            from omop.models import Concept
            
            # Clear in dependency order
            TrialArmSafetyMetrics.objects.all().delete()
            AdverseEvent.objects.all().delete()
            TrialArm.objects.all().delete()
            
            # Clear AE-related concepts
            ae_concept_ids = [4103703, 437663, 4223659, 4165112, 315286, 
                            4230254, 4141062, 4084139, 4229881, 437082]
            Concept.objects.filter(concept_id__in=ae_concept_ids).delete()
            
            self.stdout.write(self.style.SUCCESS('Data cleared successfully'))

        self.stdout.write(f'Loading synthetic adverse event data from {fixture_path}...')
        
        try:
            with transaction.atomic():
                call_command('loaddata', fixture_path, verbosity=1)
            
            self.stdout.write(
                self.style.SUCCESS('Successfully loaded synthetic adverse event data')
            )
            
            # Print summary
            from omop.models_safety import TrialArm, AdverseEvent
            from omop.models import Concept
            
            trial_arm_count = TrialArm.objects.count()
            adverse_event_count = AdverseEvent.objects.count()
            concept_count = Concept.objects.filter(
                concept_id__in=[4103703, 437663, 4223659, 4165112, 315286, 
                              4230254, 4141062, 4084139, 4229881, 437082]
            ).count()
            
            self.stdout.write(f'\n{self.style.SUCCESS("="*60)}')
            self.stdout.write(f'{self.style.SUCCESS("Data Summary:")}')
            self.stdout.write(f'  Trial Arms: {trial_arm_count}')
            self.stdout.write(f'  Adverse Events: {adverse_event_count}')
            self.stdout.write(f'  AE Concepts: {concept_count}')
            
            # Show trial arm summary
            self.stdout.write(f'\n{self.style.SUCCESS("Trial Arms:")}')
            for arm in TrialArm.objects.all():
                ae_count = arm.adverse_events.count()
                self.stdout.write(
                    f'  {arm.nct_number} - {arm.arm_name}: '
                    f'{arm.n_patients} patients, {ae_count} AEs, '
                    f'Status: {arm.status}'
                )
            
            # Show AE breakdown by grade
            self.stdout.write(f'\n{self.style.SUCCESS("Adverse Events by Grade:")}')
            for grade in range(1, 6):
                count = AdverseEvent.objects.filter(grade=grade).count()
                grade_label = {
                    1: 'Grade 1 (Mild)',
                    2: 'Grade 2 (Moderate)', 
                    3: 'Grade 3 (Severe)',
                    4: 'Grade 4 (Life-threatening)',
                    5: 'Grade 5 (Death)'
                }[grade]
                self.stdout.write(f'  {grade_label}: {count}')
            
            # Show serious AE count
            serious_count = AdverseEvent.objects.filter(serious=True).count()
            self.stdout.write(f'\n  Serious Adverse Events (SAEs): {serious_count}')
            
            # Show sample adverse events
            self.stdout.write(f'\n{self.style.SUCCESS("Sample Adverse Events:")}')
            for ae in AdverseEvent.objects.select_related('person', 'trial_arm')[:5]:
                self.stdout.write(
                    f'  Patient {ae.person.person_source_value}: '
                    f'{ae.event_name} (Grade {ae.grade}) - '
                    f'{ae.outcome}, {ae.relationship_to_treatment}'
                )
            
            self.stdout.write(f'{self.style.SUCCESS("="*60)}')
            
            # Compute safety scores if requested
            if options['compute_scores']:
                self.stdout.write(f'\n{self.style.WARNING("Computing safety scores...")}')
                try:
                    call_command('compute_safety_scores', verbosity=2)
                    self.stdout.write(
                        self.style.SUCCESS('Safety scores computed successfully')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error computing safety scores: {str(e)}')
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading data: {str(e)}')
            )
            import traceback
            self.stdout.write(traceback.format_exc())

