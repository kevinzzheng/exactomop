#!/usr/bin/env python
"""
Test script for OMOP to PatientInfo migration

This script demonstrates how to use the migrate_omop_to_patientinfo management command
and validates the data migration results.

Usage:
    python test_migration.py
"""

import os
import sys
import django
from django.core.management import call_command

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omop_site.settings')
django.setup()

from omop.models import Person, PatientInfo, Measurement, Observation


def test_migration():
    """Test the OMOP to PatientInfo migration"""
    
    print("🧪 Testing OMOP to PatientInfo Migration")
    print("=" * 50)
    
    # Check if we have OMOP data
    person_count = Person.objects.count()
    measurement_count = Measurement.objects.count()
    observation_count = Observation.objects.count()
    
    print(f"📊 OMOP Data Summary:")
    print(f"   - Persons: {person_count}")
    print(f"   - Measurements: {measurement_count}")
    print(f"   - Observations: {observation_count}")
    
    if person_count == 0:
        print("❌ No Person records found. Please load OMOP data first:")
        print("   python manage.py load_synthetic_breast_cancer_data")
        return False
    
    # Test dry run first
    print("\n🔍 Running dry-run migration...")
    try:
        call_command('migrate_omop_to_patientinfo', '--dry-run')
        print("✅ Dry run completed successfully")
    except Exception as e:
        print(f"❌ Dry run failed: {e}")
        return False
    
    # Test migration of first 3 persons
    print("\n📋 Running actual migration for first 3 persons...")
    first_persons = Person.objects.all()[:3]
    person_ids = [str(p.person_id) for p in first_persons]
    
    try:
        call_command(
            'migrate_omop_to_patientinfo', 
            '--person-ids', ','.join(person_ids),
            verbosity=2
        )
        print("✅ Migration completed successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    # Validate results
    print("\n🔬 Validating migration results...")
    validate_migration_results(person_ids)
    
    return True


def validate_migration_results(person_ids):
    """Validate the migration results"""
    
    for person_id in person_ids:
        try:
            person = Person.objects.get(person_id=person_id)
            patient_info = PatientInfo.objects.get(person=person)
            
            print(f"\n👤 Person {person_id} -> PatientInfo:")
            print(f"   - Age: {patient_info.patient_age}")
            print(f"   - Gender: {patient_info.gender}")
            print(f"   - Disease: {patient_info.disease}")
            print(f"   - BMI: {patient_info.bmi}")
            print(f"   - Language: {patient_info.languages}")
            
            # Check lab values
            lab_values = []
            if patient_info.hemoglobin_level:
                lab_values.append(f"Hgb: {patient_info.hemoglobin_level}")
            if patient_info.platelet_count:
                lab_values.append(f"Plt: {patient_info.platelet_count}")
            if patient_info.serum_creatinine_level:
                lab_values.append(f"Cr: {patient_info.serum_creatinine_level}")
            
            if lab_values:
                print(f"   - Labs: {', '.join(lab_values)}")
            
            # Check treatment history
            if patient_info.prior_therapy:
                print(f"   - Prior therapy: {patient_info.prior_therapy}")
            if patient_info.therapy_lines_count:
                print(f"   - Therapy lines: {patient_info.therapy_lines_count}")
            
            # Check genomic data
            if patient_info.genetic_mutations:
                mutation_count = len(patient_info.genetic_mutations)
                print(f"   - Genetic mutations: {mutation_count} variants")
            
            print("   ✅ PatientInfo record validated")
            
        except PatientInfo.DoesNotExist:
            print(f"   ❌ No PatientInfo found for Person {person_id}")
        except Person.DoesNotExist:
            print(f"   ❌ Person {person_id} not found")
        except Exception as e:
            print(f"   ❌ Validation error: {e}")


def show_usage_examples():
    """Show usage examples for the migration command"""
    
    print("\n📖 Usage Examples:")
    print("=" * 50)
    
    examples = [
        {
            "description": "Migrate all persons",
            "command": "python manage.py migrate_omop_to_patientinfo"
        },
        {
            "description": "Clear existing data and migrate all",
            "command": "python manage.py migrate_omop_to_patientinfo --clear"
        },
        {
            "description": "Migrate specific persons",
            "command": "python manage.py migrate_omop_to_patientinfo --person-ids 1001,1002,1003"
        },
        {
            "description": "Dry run (no changes)",
            "command": "python manage.py migrate_omop_to_patientinfo --dry-run"
        },
        {
            "description": "Verbose output",
            "command": "python manage.py migrate_omop_to_patientinfo --verbosity=2"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['description']}:")
        print(f"   {example['command']}")
        print()


def main():
    """Main test function"""
    
    print("🚀 OMOP to PatientInfo Migration Test Suite")
    print("=" * 60)
    
    # Show usage examples
    show_usage_examples()
    
    # Run tests
    success = test_migration()
    
    if success:
        print("\n🎉 Migration test completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Review the migrated PatientInfo records in Django admin")
        print("   2. Run the full migration: python manage.py migrate_omop_to_patientinfo")
        print("   3. Validate data quality and completeness")
    else:
        print("\n❌ Migration test failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
