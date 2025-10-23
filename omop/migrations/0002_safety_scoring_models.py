# Generated migration for Safety Scoring models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('omop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrialArm',
            fields=[
                ('trial_arm_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nct_number', models.CharField(blank=True, help_text='ClinicalTrials.gov NCT number', max_length=20)),
                ('arm_name', models.CharField(help_text="Treatment arm name (e.g., 'Arm A: Drug X + Standard Care')", max_length=200)),
                ('arm_code', models.CharField(help_text="Short arm code (e.g., 'ARM_A', 'CONTROL')", max_length=50)),
                ('arm_type', models.CharField(choices=[('EXPERIMENTAL', 'Experimental'), ('ACTIVE_COMPARATOR', 'Active Comparator'), ('PLACEBO_COMPARATOR', 'Placebo Comparator'), ('SHAM_COMPARATOR', 'Sham Comparator'), ('NO_INTERVENTION', 'No Intervention')], help_text='Type of trial arm', max_length=30)),
                ('intervention_description', models.TextField(blank=True, help_text='Detailed description of interventions in this arm')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('COMPLETED', 'Completed'), ('SUSPENDED', 'Suspended'), ('TERMINATED', 'Terminated'), ('ENDED', 'Ended')], default='ACTIVE', help_text='Current status of the trial arm', max_length=20)),
                ('enrollment_start_date', models.DateField(blank=True, help_text='Date enrollment started for this arm', null=True)),
                ('enrollment_end_date', models.DateField(blank=True, help_text='Date enrollment ended for this arm', null=True)),
                ('last_data_cut', models.DateField(blank=True, help_text='Date of last data cutoff for safety analysis', null=True)),
                ('n_patients', models.IntegerField(default=0, help_text='Number of patients enrolled in this arm')),
                ('follow_up_months', models.DecimalField(blank=True, decimal_places=2, help_text='Average follow-up duration in months', max_digits=8, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('clinical_trial', models.ForeignKey(blank=True, help_text='Associated clinical trial (if applicable)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trial_arms', to='omop.clinicaltrial')),
            ],
            options={
                'db_table': 'trial_arm',
                'indexes': [
                    models.Index(fields=['nct_number'], name='trial_arm_nct_number_idx'),
                    models.Index(fields=['status'], name='trial_arm_status_idx'),
                    models.Index(fields=['arm_code'], name='trial_arm_arm_code_idx'),
                    models.Index(fields=['clinical_trial'], name='trial_arm_clinical_trial_idx'),
                ],
                'unique_together': {('nct_number', 'arm_code')},
            },
        ),
        migrations.CreateModel(
            name='AdverseEvent',
            fields=[
                ('adverse_event_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('event_name', models.CharField(help_text='Name of adverse event', max_length=200)),
                ('event_description', models.TextField(blank=True, help_text='Detailed description of event')),
                ('event_date', models.DateField(help_text='Date adverse event occurred')),
                ('onset_date', models.DateField(blank=True, help_text='Date of symptom onset', null=True)),
                ('resolution_date', models.DateField(blank=True, help_text='Date event resolved', null=True)),
                ('grade', models.IntegerField(choices=[(1, 'Grade 1 - Mild'), (2, 'Grade 2 - Moderate'), (3, 'Grade 3 - Severe'), (4, 'Grade 4 - Life-threatening'), (5, 'Grade 5 - Death')], help_text='CTCAE grade (1-5)')),
                ('serious', models.BooleanField(default=False, help_text='Whether event meets criteria for Serious Adverse Event (SAE)')),
                ('expected', models.BooleanField(default=True, help_text='Whether event was expected based on known safety profile')),
                ('relationship_to_treatment', models.CharField(blank=True, choices=[('UNRELATED', 'Unrelated'), ('UNLIKELY', 'Unlikely Related'), ('POSSIBLE', 'Possibly Related'), ('PROBABLE', 'Probably Related'), ('DEFINITE', 'Definitely Related')], help_text='Relationship to study intervention', max_length=30)),
                ('outcome', models.CharField(blank=True, choices=[('RECOVERED', 'Recovered/Resolved'), ('RECOVERING', 'Recovering/Resolving'), ('NOT_RECOVERED', 'Not Recovered'), ('SEQUELAE', 'Recovered with Sequelae'), ('FATAL', 'Fatal'), ('UNKNOWN', 'Unknown')], help_text='Outcome of adverse event', max_length=30)),
                ('action_taken', models.CharField(blank=True, choices=[('NONE', 'No Action Taken'), ('DOSE_REDUCED', 'Dose Reduced'), ('DOSE_INTERRUPTED', 'Dose Interrupted'), ('DRUG_WITHDRAWN', 'Drug Withdrawn'), ('CONCOMITANT_TREATMENT', 'Concomitant Treatment Given')], help_text='Action taken in response to event', max_length=50)),
                ('reported_to_sponsor', models.BooleanField(default=False)),
                ('reported_to_irb', models.BooleanField(default=False)),
                ('reported_to_fda', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event_concept', models.ForeignKey(blank=True, help_text='OMOP concept for adverse event', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='adverse_events', to='omop.concept')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adverse_events', to='omop.person')),
                ('trial_arm', models.ForeignKey(blank=True, help_text='Trial arm patient was enrolled in when AE occurred', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='adverse_events', to='omop.trialarm')),
            ],
            options={
                'db_table': 'adverse_event',
                'indexes': [
                    models.Index(fields=['person'], name='adverse_event_person_idx'),
                    models.Index(fields=['trial_arm'], name='adverse_event_trial_arm_idx'),
                    models.Index(fields=['event_date'], name='adverse_event_event_date_idx'),
                    models.Index(fields=['grade'], name='adverse_event_grade_idx'),
                    models.Index(fields=['serious'], name='adverse_event_serious_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='TrialArmSafetyMetrics',
            fields=[
                ('safety_metrics_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('computation_date', models.DateField(auto_now=True, help_text='Date when metrics were computed')),
                ('data_cut_date', models.DateField(help_text='Date of data cutoff for this computation')),
                ('analysis_period_start', models.DateField(blank=True, help_text='Start date of analysis period', null=True)),
                ('analysis_period_end', models.DateField(blank=True, help_text='End date of analysis period', null=True)),
                ('person_years', models.DecimalField(decimal_places=2, help_text='Total person-years of follow-up', max_digits=12)),
                ('n_patients', models.IntegerField(help_text='Number of patients in analysis')),
                ('e1_2_count', models.IntegerField(default=0, help_text='Count of patients with Grade 1-2 adverse events')),
                ('e3_4_count', models.IntegerField(default=0, help_text='Count of patients with Grade 3-4 adverse events')),
                ('e5_count', models.IntegerField(default=0, help_text='Count of patients with Grade 5 (death) adverse events')),
                ('total_ae_count', models.IntegerField(default=0, help_text='Total number of adverse events (all grades)')),
                ('patients_with_any_ae', models.IntegerField(default=0, help_text='Number of patients with at least one AE')),
                ('eair', models.DecimalField(blank=True, decimal_places=4, help_text='Event-Adjusted Incidence Rate (patients with events / person-years)', max_digits=10, null=True)),
                ('web', models.DecimalField(decimal_places=2, help_text='Weighted Event Burden (WEB = 1*e1_2 + 10*e3_4 + 100*e5)', max_digits=12)),
                ('safety_score', models.DecimalField(decimal_places=2, help_text='Overall safety score (0-100, higher is safer)', max_digits=6)),
                ('web_threshold_h', models.DecimalField(decimal_places=2, default=15.0, help_text='WEB threshold (H) used in safety score calculation', max_digits=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('trial_arm', models.ForeignKey(help_text='Trial arm these metrics apply to', on_delete=django.db.models.deletion.CASCADE, related_name='safety_metrics', to='omop.trialarm')),
            ],
            options={
                'db_table': 'trial_arm_safety_metrics',
                'indexes': [
                    models.Index(fields=['trial_arm'], name='trial_arm_safety_metrics_trial_arm_idx'),
                    models.Index(fields=['computation_date'], name='trial_arm_safety_metrics_computation_date_idx'),
                    models.Index(fields=['safety_score'], name='trial_arm_safety_metrics_safety_score_idx'),
                    models.Index(fields=['data_cut_date'], name='trial_arm_safety_metrics_data_cut_date_idx'),
                ],
                'unique_together': {('trial_arm', 'data_cut_date')},
            },
        ),
    ]

