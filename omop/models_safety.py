"""
Safety Scoring Models for EXACTOMOP
This module contains models for trial arm safety analysis and adverse event tracking.
"""

from django.db import models
from .models import Person, Concept


class TrialArm(models.Model):
    """
    Clinical Trial Arm Model - represents different treatment arms within a clinical trial
    """
    trial_arm_id = models.BigAutoField(primary_key=True)
    
    # Trial reference - can link to ClinicalTrial model or external trial ID
    clinical_trial = models.ForeignKey(
        'ClinicalTrial', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='trial_arms',
        help_text="Associated clinical trial (if applicable)"
    )
    nct_number = models.CharField(
        max_length=20, 
        blank=True, 
        help_text="ClinicalTrials.gov NCT number"
    )
    
    # Arm identification
    arm_name = models.CharField(max_length=200, help_text="Treatment arm name (e.g., 'Arm A: Drug X + Standard Care')")
    arm_code = models.CharField(max_length=50, help_text="Short arm code (e.g., 'ARM_A', 'CONTROL')")
    arm_type = models.CharField(
        max_length=30,
        choices=[
            ('EXPERIMENTAL', 'Experimental'),
            ('ACTIVE_COMPARATOR', 'Active Comparator'),
            ('PLACEBO_COMPARATOR', 'Placebo Comparator'),
            ('SHAM_COMPARATOR', 'Sham Comparator'),
            ('NO_INTERVENTION', 'No Intervention'),
        ],
        help_text="Type of trial arm"
    )
    
    # Arm description
    intervention_description = models.TextField(
        blank=True,
        help_text="Detailed description of interventions in this arm"
    )
    
    # Enrollment and status
    status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'Active'),
            ('COMPLETED', 'Completed'),
            ('SUSPENDED', 'Suspended'),
            ('TERMINATED', 'Terminated'),
            ('ENDED', 'Ended'),
        ],
        default='ACTIVE',
        help_text="Current status of the trial arm"
    )
    
    enrollment_start_date = models.DateField(
        null=True, 
        blank=True,
        help_text="Date enrollment started for this arm"
    )
    enrollment_end_date = models.DateField(
        null=True, 
        blank=True,
        help_text="Date enrollment ended for this arm"
    )
    last_data_cut = models.DateField(
        null=True,
        blank=True,
        help_text="Date of last data cutoff for safety analysis"
    )
    
    # Patient counts
    n_patients = models.IntegerField(
        default=0,
        help_text="Number of patients enrolled in this arm"
    )
    
    # Follow-up information
    follow_up_months = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Average follow-up duration in months"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "trial_arm"
        indexes = [
            models.Index(fields=["nct_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["arm_code"]),
            models.Index(fields=["clinical_trial"]),
        ]
        unique_together = [['nct_number', 'arm_code']]
    
    def __str__(self):
        return f"{self.arm_name} ({self.arm_code})"


class AdverseEvent(models.Model):
    """
    Adverse Event Model - tracks adverse events for patients in clinical trials
    """
    adverse_event_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='adverse_events')
    trial_arm = models.ForeignKey(
        TrialArm,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='adverse_events',
        help_text="Trial arm patient was enrolled in when AE occurred"
    )
    
    # Event identification
    event_concept = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='adverse_events',
        help_text="OMOP concept for adverse event"
    )
    event_name = models.CharField(max_length=200, help_text="Name of adverse event")
    event_description = models.TextField(blank=True, help_text="Detailed description of event")
    
    # Timing
    event_date = models.DateField(help_text="Date adverse event occurred")
    onset_date = models.DateField(null=True, blank=True, help_text="Date of symptom onset")
    resolution_date = models.DateField(null=True, blank=True, help_text="Date event resolved")
    
    # Severity grading (CTCAE)
    grade = models.IntegerField(
        choices=[
            (1, 'Grade 1 - Mild'),
            (2, 'Grade 2 - Moderate'),
            (3, 'Grade 3 - Severe'),
            (4, 'Grade 4 - Life-threatening'),
            (5, 'Grade 5 - Death'),
        ],
        help_text="CTCAE grade (1-5)"
    )
    
    # Classification
    serious = models.BooleanField(
        default=False,
        help_text="Whether event meets criteria for Serious Adverse Event (SAE)"
    )
    expected = models.BooleanField(
        default=True,
        help_text="Whether event was expected based on known safety profile"
    )
    
    # Causality
    relationship_to_treatment = models.CharField(
        max_length=30,
        choices=[
            ('UNRELATED', 'Unrelated'),
            ('UNLIKELY', 'Unlikely Related'),
            ('POSSIBLE', 'Possibly Related'),
            ('PROBABLE', 'Probably Related'),
            ('DEFINITE', 'Definitely Related'),
        ],
        blank=True,
        help_text="Relationship to study intervention"
    )
    
    # Outcomes
    outcome = models.CharField(
        max_length=30,
        choices=[
            ('RECOVERED', 'Recovered/Resolved'),
            ('RECOVERING', 'Recovering/Resolving'),
            ('NOT_RECOVERED', 'Not Recovered'),
            ('SEQUELAE', 'Recovered with Sequelae'),
            ('FATAL', 'Fatal'),
            ('UNKNOWN', 'Unknown'),
        ],
        blank=True,
        help_text="Outcome of adverse event"
    )
    
    # Actions taken
    action_taken = models.CharField(
        max_length=50,
        choices=[
            ('NONE', 'No Action Taken'),
            ('DOSE_REDUCED', 'Dose Reduced'),
            ('DOSE_INTERRUPTED', 'Dose Interrupted'),
            ('DRUG_WITHDRAWN', 'Drug Withdrawn'),
            ('CONCOMITANT_TREATMENT', 'Concomitant Treatment Given'),
        ],
        blank=True,
        help_text="Action taken in response to event"
    )
    
    # Reporting
    reported_to_sponsor = models.BooleanField(default=False)
    reported_to_irb = models.BooleanField(default=False)
    reported_to_fda = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "adverse_event"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["trial_arm"]),
            models.Index(fields=["event_date"]),
            models.Index(fields=["grade"]),
            models.Index(fields=["serious"]),
        ]
    
    def __str__(self):
        return f"{self.event_name} (Grade {self.grade}) - Person {self.person.person_id}"


class TrialArmSafetyMetrics(models.Model):
    """
    Trial Arm Safety Metrics Model - stores computed safety scores for trial arms
    """
    safety_metrics_id = models.BigAutoField(primary_key=True)
    trial_arm = models.ForeignKey(
        TrialArm,
        on_delete=models.CASCADE,
        related_name='safety_metrics',
        help_text="Trial arm these metrics apply to"
    )
    
    # Computation period
    computation_date = models.DateField(
        auto_now=True,
        help_text="Date when metrics were computed"
    )
    data_cut_date = models.DateField(
        help_text="Date of data cutoff for this computation"
    )
    analysis_period_start = models.DateField(
        null=True,
        blank=True,
        help_text="Start date of analysis period"
    )
    analysis_period_end = models.DateField(
        null=True,
        blank=True,
        help_text="End date of analysis period"
    )
    
    # Person-time metrics
    person_years = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Total person-years of follow-up"
    )
    n_patients = models.IntegerField(
        help_text="Number of patients in analysis"
    )
    
    # Adverse event counts by grade
    e1_2_count = models.IntegerField(
        default=0,
        help_text="Count of patients with Grade 1-2 adverse events"
    )
    e3_4_count = models.IntegerField(
        default=0,
        help_text="Count of patients with Grade 3-4 adverse events"
    )
    e5_count = models.IntegerField(
        default=0,
        help_text="Count of patients with Grade 5 (death) adverse events"
    )
    
    # Total AE counts
    total_ae_count = models.IntegerField(
        default=0,
        help_text="Total number of adverse events (all grades)"
    )
    patients_with_any_ae = models.IntegerField(
        default=0,
        help_text="Number of patients with at least one AE"
    )
    
    # Computed safety metrics
    eair = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Event-Adjusted Incidence Rate (patients with events / person-years)"
    )
    
    web = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Weighted Event Burden (WEB = 1*e1_2 + 10*e3_4 + 100*e5)"
    )
    
    safety_score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Overall safety score (0-100, higher is safer)"
    )
    
    # Configuration used
    web_threshold_h = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=15.0,
        help_text="WEB threshold (H) used in safety score calculation"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "trial_arm_safety_metrics"
        indexes = [
            models.Index(fields=["trial_arm"]),
            models.Index(fields=["computation_date"]),
            models.Index(fields=["safety_score"]),
            models.Index(fields=["data_cut_date"]),
        ]
        unique_together = [['trial_arm', 'data_cut_date']]
    
    def __str__(self):
        return f"Safety Metrics for {self.trial_arm.arm_name} - Score: {self.safety_score}"

