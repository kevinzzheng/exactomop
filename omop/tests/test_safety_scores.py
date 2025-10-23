"""
Comprehensive tests for safety score computation.

Tests cover:
- Person-years calculation
- Adverse event counting by grade
- EAIR computation
- WEB computation
- Safety score computation
- Edge cases and error handling
"""

from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
from datetime import date, timedelta

from omop.models import Person
from omop.models_safety import TrialArm, AdverseEvent, TrialArmSafetyMetrics
from omop.management.commands.compute_safety_scores import Command


class SafetyScoreCalculationTests(TestCase):
    """Test the safety score calculation logic."""

    def setUp(self):
        """Set up test data."""
        # Create test persons
        self.person1 = Person.objects.create(
            person_id=1001,
            gender_concept_id=8507,
            year_of_birth=1970,
            month_of_birth=6,
            day_of_birth=15
        )
        self.person2 = Person.objects.create(
            person_id=1002,
            gender_concept_id=8532,
            year_of_birth=1965,
            month_of_birth=3,
            day_of_birth=22
        )
        self.person3 = Person.objects.create(
            person_id=1003,
            gender_concept_id=8507,
            year_of_birth=1980,
            month_of_birth=9,
            day_of_birth=10
        )

        # Create a test trial arm
        self.trial_arm = TrialArm.objects.create(
            nct_number='NCT12345678',
            arm_name='Arm A: Experimental Drug X',
            arm_code='ARM_A',
            arm_type='EXPERIMENTAL',
            status='ACTIVE',
            enrollment_start_date=date(2023, 1, 1),
            last_data_cut=date(2024, 1, 1),
            n_patients=100,
            follow_up_months=Decimal('12.0')
        )

    def test_person_years_calculation_with_follow_up_months(self):
        """Test person-years calculation using follow_up_months."""
        # 100 patients * 12 months / 12 = 100 person-years
        command = Command()
        metrics = command.compute_metrics_for_arm(
            self.trial_arm, 
            Decimal('15.0'),
            verbosity=0
        )
        
        expected_person_years = Decimal('100') * Decimal('12.0') / Decimal('12')
        self.assertEqual(metrics['person_years'], expected_person_years)

    def test_person_years_calculation_from_dates(self):
        """Test person-years calculation when derived from enrollment dates."""
        # Create arm without follow_up_months
        arm = TrialArm.objects.create(
            nct_number='NCT87654321',
            arm_name='Arm B: Control',
            arm_code='ARM_B',
            arm_type='PLACEBO_COMPARATOR',
            status='ACTIVE',
            enrollment_start_date=date(2023, 1, 1),
            last_data_cut=date(2024, 1, 1),  # 1 year = 365 days
            n_patients=50,
            follow_up_months=None  # Force calculation from dates
        )
        
        command = Command()
        metrics = command.compute_metrics_for_arm(arm, Decimal('15.0'), verbosity=0)
        
        # Should be approximately 50 person-years
        self.assertGreater(metrics['person_years'], Decimal('49'))
        self.assertLess(metrics['person_years'], Decimal('51'))

    def test_adverse_event_counting_by_grade(self):
        """Test correct counting of adverse events by grade."""
        # Create adverse events of different grades
        # Grade 1 for person1
        AdverseEvent.objects.create(
            person=self.person1,
            trial_arm=self.trial_arm,
            event_name='Nausea',
            event_date=date(2023, 6, 1),
            grade=1
        )
        
        # Grade 2 for person2
        AdverseEvent.objects.create(
            person=self.person2,
            trial_arm=self.trial_arm,
            event_name='Fatigue',
            event_date=date(2023, 6, 15),
            grade=2
        )
        
        # Grade 3 for person3
        AdverseEvent.objects.create(
            person=self.person3,
            trial_arm=self.trial_arm,
            event_name='Neutropenia',
            event_date=date(2023, 7, 1),
            grade=3
        )
        
        # Another grade 3 for person1 (same person, should count once)
        AdverseEvent.objects.create(
            person=self.person1,
            trial_arm=self.trial_arm,
            event_name='Anemia',
            event_date=date(2023, 7, 15),
            grade=3
        )

        command = Command()
        metrics = command.compute_metrics_for_arm(
            self.trial_arm,
            Decimal('15.0'),
            verbosity=0
        )

        # Should count unique patients
        self.assertEqual(metrics['e1_2_count'], 2)  # person1 (grade 1) + person2 (grade 2)
        self.assertEqual(metrics['e3_4_count'], 2)  # person3 + person1 (both have grade 3)
        self.assertEqual(metrics['e5_count'], 0)
        self.assertEqual(metrics['patients_with_any_ae'], 3)  # 3 unique patients
        self.assertEqual(metrics['total_ae_count'], 4)  # 4 total events

    def test_eair_computation(self):
        """Test Event-Adjusted Incidence Rate (EAIR) computation."""
        # Create 10 adverse events for 10 different patients
        for i in range(10):
            person = Person.objects.create(
                person_id=2000 + i,
                gender_concept_id=8507,
                year_of_birth=1970,
                month_of_birth=1,
                day_of_birth=1
            )
            AdverseEvent.objects.create(
                person=person,
                trial_arm=self.trial_arm,
                event_name=f'Event {i}',
                event_date=date(2023, 6, 1),
                grade=2
            )

        command = Command()
        metrics = command.compute_metrics_for_arm(
            self.trial_arm,
            Decimal('15.0'),
            verbosity=0
        )

        # EAIR = 10 patients with events / 100 person-years = 0.1
        expected_eair = Decimal('10') / Decimal('100')
        self.assertEqual(metrics['eair'], expected_eair)

    def test_web_computation(self):
        """Test Weighted Event Burden (WEB) computation."""
        # Create specific grade distribution
        # 5 patients with grade 1-2
        for i in range(5):
            person = Person.objects.create(
                person_id=3000 + i,
                gender_concept_id=8507,
                year_of_birth=1970,
                month_of_birth=1,
                day_of_birth=1
            )
            AdverseEvent.objects.create(
                person=person,
                trial_arm=self.trial_arm,
                event_name=f'Mild Event {i}',
                event_date=date(2023, 6, 1),
                grade=1
            )

        # 3 patients with grade 3-4
        for i in range(3):
            person = Person.objects.create(
                person_id=3100 + i,
                gender_concept_id=8507,
                year_of_birth=1970,
                month_of_birth=1,
                day_of_birth=1
            )
            AdverseEvent.objects.create(
                person=person,
                trial_arm=self.trial_arm,
                event_name=f'Severe Event {i}',
                event_date=date(2023, 6, 1),
                grade=3
            )

        # 1 patient with grade 5
        person = Person.objects.create(
            person_id=3200,
            gender_concept_id=8507,
            year_of_birth=1970,
            month_of_birth=1,
            day_of_birth=1
        )
        AdverseEvent.objects.create(
            person=person,
            trial_arm=self.trial_arm,
            event_name='Fatal Event',
            event_date=date(2023, 6, 1),
            grade=5
        )

        command = Command()
        metrics = command.compute_metrics_for_arm(
            self.trial_arm,
            Decimal('15.0'),
            verbosity=0
        )

        # WEB = 1*5 + 10*3 + 100*1 = 5 + 30 + 100 = 135
        expected_web = Decimal('1') * 5 + Decimal('10') * 3 + Decimal('100') * 1
        self.assertEqual(metrics['web'], expected_web)

    def test_safety_score_computation(self):
        """Test overall safety score computation."""
        # Create a known WEB scenario
        # 2 grade 1-2, 1 grade 3-4, 0 grade 5
        # WEB = 1*2 + 10*1 + 100*0 = 12
        for i in range(2):
            person = Person.objects.create(
                person_id=4000 + i,
                gender_concept_id=8507,
                year_of_birth=1970,
                month_of_birth=1,
                day_of_birth=1
            )
            AdverseEvent.objects.create(
                person=person,
                trial_arm=self.trial_arm,
                event_name=f'Event {i}',
                event_date=date(2023, 6, 1),
                grade=1
            )

        person = Person.objects.create(
            person_id=4100,
            gender_concept_id=8507,
            year_of_birth=1970,
            month_of_birth=1,
            day_of_birth=1
        )
        AdverseEvent.objects.create(
            person=person,
            trial_arm=self.trial_arm,
            event_name='Severe Event',
            event_date=date(2023, 6, 1),
            grade=3
        )

        web_threshold_h = Decimal('15.0')
        command = Command()
        metrics = command.compute_metrics_for_arm(
            self.trial_arm,
            web_threshold_h,
            verbosity=0
        )

        # WEB = 12
        self.assertEqual(metrics['web'], Decimal('12'))
        
        # Safety_score = 100 / (1 + 12/15) = 100 / (1 + 0.8) = 100 / 1.8 = 55.56
        expected_safety_score = Decimal('100') / (Decimal('1') + Decimal('12') / web_threshold_h)
        self.assertAlmostEqual(
            float(metrics['safety_score']),
            float(expected_safety_score),
            places=2
        )

    def test_zero_adverse_events(self):
        """Test computation with no adverse events."""
        command = Command()
        metrics = command.compute_metrics_for_arm(
            self.trial_arm,
            Decimal('15.0'),
            verbosity=0
        )

        self.assertEqual(metrics['e1_2_count'], 0)
        self.assertEqual(metrics['e3_4_count'], 0)
        self.assertEqual(metrics['e5_count'], 0)
        self.assertEqual(metrics['web'], Decimal('0'))
        self.assertEqual(metrics['eair'], Decimal('0'))
        # Safety score should be 100 when WEB = 0
        # Safety_score = 100 / (1 + 0/15) = 100
        self.assertEqual(metrics['safety_score'], Decimal('100'))

    def test_high_adverse_event_burden(self):
        """Test computation with very high adverse event burden."""
        # Create many severe events
        for i in range(20):
            person = Person.objects.create(
                person_id=5000 + i,
                gender_concept_id=8507,
                year_of_birth=1970,
                month_of_birth=1,
                day_of_birth=1
            )
            AdverseEvent.objects.create(
                person=person,
                trial_arm=self.trial_arm,
                event_name=f'Severe Event {i}',
                event_date=date(2023, 6, 1),
                grade=4
            )

        command = Command()
        metrics = command.compute_metrics_for_arm(
            self.trial_arm,
            Decimal('15.0'),
            verbosity=0
        )

        # WEB = 10 * 20 = 200
        self.assertEqual(metrics['web'], Decimal('200'))
        
        # Safety score should be low
        # Safety_score = 100 / (1 + 200/15) ≈ 6.98
        self.assertLess(metrics['safety_score'], Decimal('10'))

    def test_patient_with_multiple_grades(self):
        """Test that a patient with multiple AE grades is counted correctly."""
        # Same patient has both grade 2 and grade 4 events
        AdverseEvent.objects.create(
            person=self.person1,
            trial_arm=self.trial_arm,
            event_name='Moderate Event',
            event_date=date(2023, 6, 1),
            grade=2
        )
        AdverseEvent.objects.create(
            person=self.person1,
            trial_arm=self.trial_arm,
            event_name='Severe Event',
            event_date=date(2023, 7, 1),
            grade=4
        )

        command = Command()
        metrics = command.compute_metrics_for_arm(
            self.trial_arm,
            Decimal('15.0'),
            verbosity=0
        )

        # Patient should be counted in both grade categories
        self.assertEqual(metrics['e1_2_count'], 1)
        self.assertEqual(metrics['e3_4_count'], 1)
        self.assertEqual(metrics['patients_with_any_ae'], 1)  # Only 1 unique patient
        self.assertEqual(metrics['total_ae_count'], 2)  # 2 total events

    def test_different_web_thresholds(self):
        """Test safety score with different WEB thresholds."""
        # Create a fixed WEB scenario
        for i in range(5):
            person = Person.objects.create(
                person_id=6000 + i,
                gender_concept_id=8507,
                year_of_birth=1970,
                month_of_birth=1,
                day_of_birth=1
            )
            AdverseEvent.objects.create(
                person=person,
                trial_arm=self.trial_arm,
                event_name=f'Event {i}',
                event_date=date(2023, 6, 1),
                grade=3
            )

        # WEB = 10 * 5 = 50
        command = Command()
        
        # Test with H = 10
        metrics_h10 = command.compute_metrics_for_arm(
            self.trial_arm,
            Decimal('10.0'),
            verbosity=0
        )
        
        # Test with H = 20
        metrics_h20 = command.compute_metrics_for_arm(
            self.trial_arm,
            Decimal('20.0'),
            verbosity=0
        )

        # Higher H should give higher safety score
        # H=10: 100 / (1 + 50/10) = 100/6 = 16.67
        # H=20: 100 / (1 + 50/20) = 100/3.5 = 28.57
        self.assertLess(metrics_h10['safety_score'], metrics_h20['safety_score'])

    def test_data_cut_date_filtering(self):
        """Test that events after data cut date are excluded."""
        # Event before data cut
        AdverseEvent.objects.create(
            person=self.person1,
            trial_arm=self.trial_arm,
            event_name='Event Before Cut',
            event_date=date(2023, 12, 1),
            grade=3
        )
        
        # Event after data cut (should be excluded)
        AdverseEvent.objects.create(
            person=self.person2,
            trial_arm=self.trial_arm,
            event_name='Event After Cut',
            event_date=date(2024, 2, 1),  # After 2024-01-01 data cut
            grade=3
        )

        command = Command()
        metrics = command.compute_metrics_for_arm(
            self.trial_arm,
            Decimal('15.0'),
            verbosity=0
        )

        # Should only count 1 event
        self.assertEqual(metrics['e3_4_count'], 1)
        self.assertEqual(metrics['total_ae_count'], 1)


class TrialArmSafetyMetricsModelTests(TestCase):
    """Test the TrialArmSafetyMetrics model."""

    def setUp(self):
        """Set up test data."""
        self.trial_arm = TrialArm.objects.create(
            nct_number='NCT99999999',
            arm_name='Test Arm',
            arm_code='TEST_ARM',
            arm_type='EXPERIMENTAL',
            status='ACTIVE',
            enrollment_start_date=date(2023, 1, 1),
            last_data_cut=date(2024, 1, 1),
            n_patients=50,
            follow_up_months=Decimal('6.0')
        )

    def test_create_safety_metrics(self):
        """Test creating safety metrics."""
        metrics = TrialArmSafetyMetrics.objects.create(
            trial_arm=self.trial_arm,
            data_cut_date=date(2024, 1, 1),
            person_years=Decimal('25.0'),
            n_patients=50,
            e1_2_count=5,
            e3_4_count=2,
            e5_count=0,
            total_ae_count=10,
            patients_with_any_ae=7,
            eair=Decimal('0.28'),
            web=Decimal('25.0'),
            safety_score=Decimal('80.0'),
            web_threshold_h=Decimal('15.0')
        )

        self.assertIsNotNone(metrics.safety_metrics_id)
        self.assertEqual(metrics.trial_arm, self.trial_arm)
        self.assertEqual(metrics.safety_score, Decimal('80.0'))

    def test_unique_together_constraint(self):
        """Test that trial_arm + data_cut_date are unique together."""
        TrialArmSafetyMetrics.objects.create(
            trial_arm=self.trial_arm,
            data_cut_date=date(2024, 1, 1),
            person_years=Decimal('25.0'),
            n_patients=50,
            e1_2_count=5,
            e3_4_count=2,
            e5_count=0,
            eair=Decimal('0.28'),
            web=Decimal('25.0'),
            safety_score=Decimal('80.0')
        )

        # Trying to create another with same trial_arm and data_cut_date should fail
        with self.assertRaises(Exception):
            TrialArmSafetyMetrics.objects.create(
                trial_arm=self.trial_arm,
                data_cut_date=date(2024, 1, 1),  # Same date
                person_years=Decimal('30.0'),
                n_patients=50,
                e1_2_count=6,
                e3_4_count=3,
                e5_count=1,
                eair=Decimal('0.33'),
                web=Decimal('136.0'),
                safety_score=Decimal('60.0')
            )

