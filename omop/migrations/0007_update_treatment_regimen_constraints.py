# Generated manually on 2025-08-30

from django.db import migrations, models
import omop.models


class Migration(migrations.Migration):

    dependencies = [
        ('omop', '0006_add_behavioral_social_determinants'),
    ]

    operations = [
        # Remove nullable constraints from TreatmentRegimen fields
        migrations.AlterField(
            model_name='treatmentregimen',
            name='regimen_code',
            field=models.CharField(max_length=50, help_text="Standard regimen code"),
        ),
        migrations.AlterField(
            model_name='treatmentregimen',
            name='treatment_setting',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('INPATIENT', 'Inpatient'),
                    ('OUTPATIENT', 'Outpatient'),
                    ('AMBULATORY', 'Ambulatory'),
                ],
                help_text="Treatment setting"
            ),
        ),
        migrations.AlterField(
            model_name='treatmentregimen',
            name='best_response',
            field=models.CharField(
                max_length=20,
                choices=omop.models.TumorResponseChoices.choices,
                help_text="Best overall response to regimen"
            ),
        ),
    ]
