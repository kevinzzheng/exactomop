"""
Django management command to compute safety scores for trial arms.

Usage:
    python manage.py compute_safety_scores [--force] [--verbosity=2]
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from collections import defaultdict

from omop.models_safety import TrialArm, AdverseEvent, TrialArmSafetyMetrics


class Command(BaseCommand):
    help = 'Compute safety scores for trial arms based on adverse event data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recomputation even if already computed this month',
        )
        parser.add_argument(
            '--trial-arm-id',
            type=int,
            help='Compute for a specific trial arm only',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be computed without saving',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        trial_arm_id = options.get('trial_arm_id')
        dry_run = options.get('dry_run', False)
        verbosity = options.get('verbosity', 1)

        # Get the WEB threshold from settings
        web_threshold_h = Decimal(str(getattr(settings, 'SAFETY_WEB_THRESHOLD', 15.0)))

        if verbosity >= 1:
            self.stdout.write(self.style.SUCCESS(
                f"Starting safety score computation with WEB threshold H={web_threshold_h}"
            ))

        # Get current month's first day for checking if already computed
        today = timezone.now().date()
        current_month_start = today.replace(day=1)

        # Query trial arms
        trial_arms_query = TrialArm.objects.filter(
            status__in=['ACTIVE', 'ENDED', 'COMPLETED']
        )

        if trial_arm_id:
            trial_arms_query = trial_arms_query.filter(trial_arm_id=trial_arm_id)

        # Filter out arms already computed this month unless --force
        if not force:
            already_computed = TrialArmSafetyMetrics.objects.filter(
                computation_date__gte=current_month_start
            ).values_list('trial_arm_id', flat=True)
            
            trial_arms_query = trial_arms_query.exclude(
                trial_arm_id__in=already_computed
            )

        trial_arms = list(trial_arms_query)

        if verbosity >= 1:
            self.stdout.write(
                f"Found {len(trial_arms)} trial arm(s) to process"
            )

        if not trial_arms:
            self.stdout.write(self.style.WARNING("No trial arms to process"))
            return

        computed_count = 0
        error_count = 0

        for trial_arm in trial_arms:
            try:
                metrics = self.compute_metrics_for_arm(
                    trial_arm, web_threshold_h, verbosity
                )
                
                if verbosity >= 2:
                    self.stdout.write(
                        f"\n{trial_arm.arm_name} ({trial_arm.arm_code}):"
                    )
                    self.stdout.write(f"  Person-years: {metrics['person_years']}")
                    self.stdout.write(f"  Grade 1-2 count: {metrics['e1_2_count']}")
                    self.stdout.write(f"  Grade 3-4 count: {metrics['e3_4_count']}")
                    self.stdout.write(f"  Grade 5 count: {metrics['e5_count']}")
                    self.stdout.write(f"  EAIR: {metrics['eair']}")
                    self.stdout.write(f"  WEB: {metrics['web']}")
                    self.stdout.write(
                        self.style.SUCCESS(f"  Safety Score: {metrics['safety_score']}")
                    )

                if not dry_run:
                    with transaction.atomic():
                        # Update or create safety metrics
                        safety_metrics, created = TrialArmSafetyMetrics.objects.update_or_create(
                            trial_arm=trial_arm,
                            data_cut_date=metrics['data_cut_date'],
                            defaults=metrics
                        )
                        
                        action = "Created" if created else "Updated"
                        if verbosity >= 1:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"{action} safety metrics for {trial_arm.arm_code} "
                                    f"(Score: {safety_metrics.safety_score})"
                                )
                            )
                
                computed_count += 1

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"Error computing metrics for {trial_arm.arm_code}: {str(e)}"
                    )
                )
                if verbosity >= 2:
                    import traceback
                    self.stdout.write(traceback.format_exc())

        # Summary
        if verbosity >= 1:
            self.stdout.write("\n" + "=" * 60)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully computed: {computed_count}"
                )
            )
            if error_count:
                self.stdout.write(
                    self.style.ERROR(f"Errors: {error_count}")
                )
            if dry_run:
                self.stdout.write(
                    self.style.WARNING("DRY RUN - No data was saved")
                )

    def compute_metrics_for_arm(self, trial_arm, web_threshold_h, verbosity):
        """
        Compute safety metrics for a single trial arm.
        """
        # Determine data cut date
        data_cut_date = trial_arm.last_data_cut or timezone.now().date()
        
        # Compute person-years
        if trial_arm.follow_up_months and trial_arm.n_patients:
            person_years = Decimal(str(trial_arm.n_patients)) * (
                Decimal(str(trial_arm.follow_up_months)) / Decimal('12')
            )
        elif trial_arm.enrollment_start_date and data_cut_date:
            # Fallback: derive from enrollment date to last data cut
            days_followup = (data_cut_date - trial_arm.enrollment_start_date).days
            months_followup = Decimal(str(days_followup)) / Decimal('30.44')  # Average days per month
            person_years = Decimal(str(trial_arm.n_patients)) * (months_followup / Decimal('12'))
        else:
            raise ValueError(
                f"Cannot compute person-years for {trial_arm.arm_code}: "
                "missing follow_up_months or enrollment dates"
            )

        if person_years <= 0:
            raise ValueError(
                f"Invalid person-years ({person_years}) for {trial_arm.arm_code}"
            )

        # Get adverse events for this trial arm
        adverse_events = AdverseEvent.objects.filter(
            trial_arm=trial_arm,
            event_date__lte=data_cut_date
        ).select_related('person')

        # Count patients with events by grade
        # A patient can have multiple AEs, we count unique patients
        patients_with_grade_1_2 = set()
        patients_with_grade_3_4 = set()
        patients_with_grade_5 = set()
        patients_with_any_ae = set()
        total_ae_count = 0

        for ae in adverse_events:
            patient_id = ae.person.person_id
            patients_with_any_ae.add(patient_id)
            total_ae_count += 1
            
            if ae.grade in [1, 2]:
                patients_with_grade_1_2.add(patient_id)
            elif ae.grade in [3, 4]:
                patients_with_grade_3_4.add(patient_id)
            elif ae.grade == 5:
                patients_with_grade_5.add(patient_id)

        e1_2_count = len(patients_with_grade_1_2)
        e3_4_count = len(patients_with_grade_3_4)
        e5_count = len(patients_with_grade_5)

        # Compute EAIR (Event-Adjusted Incidence Rate)
        # EAIR = number of patients with events / person-years
        num_patients_with_event = len(patients_with_any_ae)
        eair = Decimal(str(num_patients_with_event)) / person_years if person_years > 0 else Decimal('0')

        # Compute WEB (Weighted Event Burden)
        # WEB = 1 * e1_2_count + 10 * e3_4_count + 100 * e5_count
        web = (
            Decimal('1') * Decimal(str(e1_2_count)) +
            Decimal('10') * Decimal(str(e3_4_count)) +
            Decimal('100') * Decimal(str(e5_count))
        )

        # Compute Safety Score
        # Safety_score = 100 / (1 + WEB/H)
        safety_score = Decimal('100') / (Decimal('1') + (web / web_threshold_h))

        # Determine analysis period
        if trial_arm.enrollment_start_date:
            analysis_period_start = trial_arm.enrollment_start_date
        else:
            analysis_period_start = None

        analysis_period_end = data_cut_date

        return {
            'trial_arm': trial_arm,
            'data_cut_date': data_cut_date,
            'analysis_period_start': analysis_period_start,
            'analysis_period_end': analysis_period_end,
            'person_years': person_years,
            'n_patients': trial_arm.n_patients,
            'e1_2_count': e1_2_count,
            'e3_4_count': e3_4_count,
            'e5_count': e5_count,
            'total_ae_count': total_ae_count,
            'patients_with_any_ae': num_patients_with_event,
            'eair': eair,
            'web': web,
            'safety_score': safety_score,
            'web_threshold_h': web_threshold_h,
        }

