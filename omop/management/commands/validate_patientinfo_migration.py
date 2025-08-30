"""
Django management command to validate PatientInfo data after OMOP migration.

This command checks data quality, completeness, and consistency of migrated 
PatientInfo records.

Usage:
    python manage.py validate_patientinfo_migration
"""

from django.core.management.base import BaseCommand
from django.db.models import Count, Q, Avg, Min, Max
from omop.models import Person, PatientInfo, Measurement, Observation
from datetime import date
import json


class Command(BaseCommand):
    help = 'Validate PatientInfo data after OMOP migration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--person-ids',
            type=str,
            help='Comma-separated list of specific person IDs to validate',
        )
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed validation for each person',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("🔍 Validating PatientInfo Migration Results")
        )
        
        # Filter persons if specified
        if options['person_ids']:
            person_ids = [int(pid.strip()) for pid in options['person_ids'].split(',')]
            persons = Person.objects.filter(person_id__in=person_ids)
        else:
            persons = Person.objects.all()
        
        total_persons = persons.count()
        patientinfo_count = PatientInfo.objects.filter(person__in=persons).count()
        
        self.stdout.write(f"📊 Overview:")
        self.stdout.write(f"   Total Persons: {total_persons}")
        self.stdout.write(f"   PatientInfo Records: {patientinfo_count}")
        self.stdout.write(f"   Migration Coverage: {patientinfo_count/total_persons*100:.1f}%")
        
        # Data completeness analysis
        self.analyze_completeness(persons)
        
        # Data quality checks
        self.check_data_quality(persons)
        
        # Detailed validation if requested
        if options['detailed']:
            self.detailed_validation(persons)
    
    def analyze_completeness(self, persons):
        """Analyze data completeness across key fields"""
        
        self.stdout.write("\n📈 Data Completeness Analysis:")
        
        patient_infos = PatientInfo.objects.filter(person__in=persons)
        total = patient_infos.count()
        
        if total == 0:
            self.stdout.write("   No PatientInfo records found")
            return
        
        # Key demographic fields
        completeness_fields = [
            ('patient_age', 'Age'),
            ('gender', 'Gender'),
            ('weight', 'Weight'),
            ('height', 'Height'),
            ('bmi', 'BMI'),
            ('disease', 'Disease'),
            ('stage', 'Stage'),
        ]
        
        self.stdout.write("   Demographics:")
        for field, label in completeness_fields:
            count = patient_infos.exclude(**{field: None}).exclude(**{field: ''}).count()
            percentage = count / total * 100
            self.stdout.write(f"     {label}: {count}/{total} ({percentage:.1f}%)")
        
        # Laboratory fields
        lab_fields = [
            ('hemoglobin_level', 'Hemoglobin'),
            ('platelet_count', 'Platelet Count'),
            ('white_blood_cell_count', 'WBC Count'),
            ('serum_creatinine_level', 'Creatinine'),
        ]
        
        self.stdout.write("   Laboratory Values:")
        for field, label in lab_fields:
            count = patient_infos.exclude(**{field: None}).count()
            percentage = count / total * 100
            self.stdout.write(f"     {label}: {count}/{total} ({percentage:.1f}%)")
        
        # Treatment history
        treatment_fields = [
            ('prior_therapy', 'Prior Therapy'),
            ('therapy_lines_count', 'Therapy Lines'),
            ('first_line_therapy', 'First Line'),
        ]
        
        self.stdout.write("   Treatment History:")
        for field, label in treatment_fields:
            count = patient_infos.exclude(**{field: None}).exclude(**{field: ''}).count()
            percentage = count / total * 100
            self.stdout.write(f"     {label}: {count}/{total} ({percentage:.1f}%)")
    
    def check_data_quality(self, persons):
        """Check data quality and consistency"""
        
        self.stdout.write("\n🔬 Data Quality Checks:")
        
        patient_infos = PatientInfo.objects.filter(person__in=persons)
        issues = []
        
        # Age consistency
        age_issues = 0
        for pi in patient_infos.filter(patient_age__isnull=False):
            calculated_age = date.today().year - pi.person.year_of_birth
            if abs(pi.patient_age - calculated_age) > 1:  # Allow 1 year difference
                age_issues += 1
        
        if age_issues > 0:
            issues.append(f"Age inconsistencies: {age_issues} records")
        
        # BMI validation
        bmi_issues = patient_infos.filter(
            Q(bmi__lt=10) | Q(bmi__gt=70)  # Unrealistic BMI values
        ).count()
        
        if bmi_issues > 0:
            issues.append(f"Unrealistic BMI values: {bmi_issues} records")
        
        # Gender mapping validation
        invalid_gender = patient_infos.exclude(
            gender__in=['M', 'F', 'O', 'U', None, '']
        ).count()
        
        if invalid_gender > 0:
            issues.append(f"Invalid gender values: {invalid_gender} records")
        
        # Performance score validation
        invalid_ecog = patient_infos.filter(
            Q(ecog_performance_status__lt=0) | Q(ecog_performance_status__gt=4)
        ).count()
        
        if invalid_ecog > 0:
            issues.append(f"Invalid ECOG scores: {invalid_ecog} records")
        
        invalid_karnofsky = patient_infos.filter(
            Q(karnofsky_performance_score__lt=0) | Q(karnofsky_performance_score__gt=100)
        ).count()
        
        if invalid_karnofsky > 0:
            issues.append(f"Invalid Karnofsky scores: {invalid_karnofsky} records")
        
        # Laboratory value ranges
        lab_ranges = {
            'hemoglobin_level': (3, 20),  # g/dL
            'platelet_count': (10000, 1000000),  # cells/uL
            'serum_creatinine_level': (0.1, 15),  # mg/dL
        }
        
        for field, (min_val, max_val) in lab_ranges.items():
            out_of_range = patient_infos.filter(
                Q(**{f"{field}__lt": min_val}) | Q(**{f"{field}__gt": max_val})
            ).exclude(**{field: None}).count()
            
            if out_of_range > 0:
                issues.append(f"Out-of-range {field}: {out_of_range} records")
        
        # Report issues
        if issues:
            self.stdout.write("   ⚠️  Issues found:")
            for issue in issues:
                self.stdout.write(f"     - {issue}")
        else:
            self.stdout.write("   ✅ No data quality issues detected")
    
    def detailed_validation(self, persons):
        """Detailed validation for individual records"""
        
        self.stdout.write("\n🔎 Detailed Record Validation:")
        
        for person in persons[:5]:  # Limit to first 5 for brevity
            try:
                patient_info = PatientInfo.objects.get(person=person)
                self.stdout.write(f"\n   👤 Person {person.person_id}:")
                
                # Basic demographics
                self.stdout.write(f"     Age: {patient_info.patient_age} (birth: {person.year_of_birth})")
                self.stdout.write(f"     Gender: {patient_info.gender} (concept: {person.gender_concept_id})")
                
                # Physical measurements
                if patient_info.weight and patient_info.height:
                    self.stdout.write(f"     BMI: {patient_info.bmi} (W:{patient_info.weight}, H:{patient_info.height})")
                
                # Disease information
                if patient_info.disease:
                    stage_info = f" Stage: {patient_info.stage}" if patient_info.stage else ""
                    self.stdout.write(f"     Disease: {patient_info.disease}{stage_info}")
                
                # Treatment summary
                if patient_info.therapy_lines_count:
                    self.stdout.write(f"     Treatment lines: {patient_info.therapy_lines_count}")
                
                # Laboratory highlights
                lab_summary = []
                if patient_info.hemoglobin_level:
                    lab_summary.append(f"Hgb:{patient_info.hemoglobin_level}")
                if patient_info.platelet_count:
                    lab_summary.append(f"Plt:{patient_info.platelet_count}")
                if patient_info.serum_creatinine_level:
                    lab_summary.append(f"Cr:{patient_info.serum_creatinine_level}")
                
                if lab_summary:
                    self.stdout.write(f"     Labs: {', '.join(lab_summary)}")
                
                # Genomic data
                if patient_info.genetic_mutations:
                    mutation_count = len(patient_info.genetic_mutations)
                    genes = [m.get('gene', 'Unknown') for m in patient_info.genetic_mutations[:3]]
                    self.stdout.write(f"     Mutations: {mutation_count} total ({', '.join(genes)}...)")
                
                # Validation checks
                issues = []
                
                # Check age calculation
                if patient_info.patient_age and person.year_of_birth:
                    calculated_age = date.today().year - person.year_of_birth
                    if abs(patient_info.patient_age - calculated_age) > 1:
                        issues.append(f"Age mismatch: {patient_info.patient_age} vs calculated {calculated_age}")
                
                # Check BMI calculation
                if patient_info.weight and patient_info.height and patient_info.bmi:
                    weight_kg = patient_info.weight
                    height_m = patient_info.height / 100  # assume cm
                    calculated_bmi = weight_kg / (height_m ** 2)
                    if abs(patient_info.bmi - calculated_bmi) > 1:
                        issues.append(f"BMI mismatch: {patient_info.bmi} vs calculated {calculated_bmi:.1f}")
                
                if issues:
                    self.stdout.write(f"     ⚠️  Issues: {'; '.join(issues)}")
                else:
                    self.stdout.write("     ✅ Validation passed")
                
            except PatientInfo.DoesNotExist:
                self.stdout.write(f"   👤 Person {person.person_id}: ❌ No PatientInfo record")
        
        # Show summary statistics
        self.show_summary_statistics(persons)
    
    def show_summary_statistics(self, persons):
        """Show summary statistics for the migrated data"""
        
        self.stdout.write("\n📊 Summary Statistics:")
        
        patient_infos = PatientInfo.objects.filter(person__in=persons)
        
        # Age distribution
        age_stats = patient_infos.aggregate(
            min_age=Min('patient_age'),
            max_age=Max('patient_age'),
            avg_age=Avg('patient_age')
        )
        
        if age_stats['avg_age']:
            self.stdout.write(f"   Age: {age_stats['min_age']}-{age_stats['max_age']} (avg: {age_stats['avg_age']:.1f})")
        
        # Gender distribution
        gender_counts = patient_infos.values('gender').annotate(count=Count('gender'))
        gender_dist = {item['gender'] or 'Unknown': item['count'] for item in gender_counts}
        self.stdout.write(f"   Gender: {gender_dist}")
        
        # Disease distribution
        disease_counts = patient_infos.values('disease').annotate(count=Count('disease'))
        disease_dist = {item['disease'] or 'Unknown': item['count'] for item in disease_counts}
        self.stdout.write(f"   Diseases: {disease_dist}")
        
        # Treatment lines
        therapy_lines = patient_infos.exclude(therapy_lines_count=None)
        if therapy_lines.exists():
            line_stats = therapy_lines.aggregate(
                min_lines=Min('therapy_lines_count'),
                max_lines=Max('therapy_lines_count'),
                avg_lines=Avg('therapy_lines_count')
            )
            self.stdout.write(f"   Treatment lines: {line_stats['min_lines']}-{line_stats['max_lines']} (avg: {line_stats['avg_lines']:.1f})")
