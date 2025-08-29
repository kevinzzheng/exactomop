#!/usr/bin/env python
"""
Example usage of OMOP Treatment Line Tracking for Clinical Trial Eligibility

This script demonstrates how to use the treatment line models to assess
clinical trial eligibility criteria such as "≥1 prior line of platinum therapy"
"""

import os
import sys
import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omop_site.settings')
django.setup()

from omop.models import (
    Person, ConditionOccurrence, DrugExposure, TreatmentLine, 
    TreatmentRegimen, TreatmentLineComponent, TreatmentLineEligibility,
    Concept
)

def create_example_patient():
    """Create an example patient with breast cancer treatment history"""
    
    # Create patient
    patient = Person.objects.create(
        person_id=1001,
        gender_concept_id=8532,  # Female
        year_of_birth=1965,
        month_of_birth=3,
        day_of_birth=15,
        race_concept_id=8527,  # White
        ethnicity_concept_id=38003564  # Not Hispanic or Latino
    )
    
    # Create breast cancer condition
    breast_cancer = ConditionOccurrence.objects.create(
        person=patient,
        condition_concept_id=4112853,  # Malignant neoplasm of breast
        condition_start_date=date(2022, 6, 1),
        condition_type_concept_id=32020  # EHR problem list entry
    )
    
    return patient, breast_cancer

def create_first_line_treatment(patient, condition):
    """Create first-line AC treatment (Adriamycin + Cyclophosphamide)"""
    
    # Create treatment line
    line1 = TreatmentLine.objects.create(
        person=patient,
        condition_occurrence=condition,
        line_number=1,
        line_start_date=date(2022, 7, 1),
        line_end_date=date(2022, 10, 15),
        treatment_intent='curative',
        treatment_setting='adjuvant',
        line_status='completed',
        gap_threshold_days=120,
        combination_window_days=30,
        line_calculation_method='OHDSI_Oncology_WG'
    )
    
    # Create regimen within the line
    regimen1 = TreatmentRegimen.objects.create(
        treatment_line=line1,
        person=patient,
        regimen_sequence=1,
        regimen_name='AC',
        regimen_start_date=date(2022, 7, 1),
        regimen_end_date=date(2022, 10, 15),
        regimen_type='standard_combination',
        planned_cycles=4,
        completed_cycles=4
    )
    
    # Create Adriamycin (Doxorubicin) exposure
    doxorubicin = DrugExposure.objects.create(
        person=patient,
        drug_concept_id=1790868,  # Doxorubicin
        drug_exposure_start_date=date(2022, 7, 1),
        drug_exposure_end_date=date(2022, 10, 15),
        drug_type_concept_id=38000177,  # Prescription written
        treatment_line=line1,
        treatment_regimen=regimen1,
        drug_classification='cytotoxic_chemotherapy',
        regimen_role='backbone',
        cycle_number=4,
        total_cycles_planned=4
    )
    
    # Create Cyclophosphamide exposure
    cyclophosphamide = DrugExposure.objects.create(
        person=patient,
        drug_concept_id=1378382,  # Cyclophosphamide
        drug_exposure_start_date=date(2022, 7, 1),
        drug_exposure_end_date=date(2022, 10, 15),
        drug_type_concept_id=38000177,  # Prescription written
        treatment_line=line1,
        treatment_regimen=regimen1,
        drug_classification='cytotoxic_chemotherapy',
        regimen_role='combination',
        cycle_number=4,
        total_cycles_planned=4
    )
    
    # Create treatment line components
    TreatmentLineComponent.objects.create(
        treatment_line=line1,
        treatment_regimen=regimen1,
        person=patient,
        component_type='drug_exposure',
        drug_exposure=doxorubicin,
        component_start_date=date(2022, 7, 1),
        component_end_date=date(2022, 10, 15),
        drug_classification='cytotoxic_chemotherapy'
    )
    
    TreatmentLineComponent.objects.create(
        treatment_line=line1,
        treatment_regimen=regimen1,
        person=patient,
        component_type='drug_exposure',
        drug_exposure=cyclophosphamide,
        component_start_date=date(2022, 7, 1),
        component_end_date=date(2022, 10, 15),
        drug_classification='cytotoxic_chemotherapy'
    )
    
    return line1, regimen1

def create_second_line_treatment(patient, condition):
    """Create second-line carboplatin + paclitaxel treatment"""
    
    # Create treatment line
    line2 = TreatmentLine.objects.create(
        person=patient,
        condition_occurrence=condition,
        line_number=2,
        line_start_date=date(2023, 3, 1),
        line_end_date=date(2023, 8, 15),
        treatment_intent='palliative',
        treatment_setting='metastatic',
        line_status='completed',
        platinum_based=True,  # Contains carboplatin
        gap_threshold_days=120,
        combination_window_days=30,
        line_calculation_method='OHDSI_Oncology_WG'
    )
    
    # Create regimen within the line
    regimen2 = TreatmentRegimen.objects.create(
        treatment_line=line2,
        person=patient,
        regimen_sequence=1,
        regimen_name='Carboplatin + Paclitaxel',
        regimen_start_date=date(2023, 3, 1),
        regimen_end_date=date(2023, 8, 15),
        regimen_type='standard_combination',
        contains_platinum=True,
        planned_cycles=6,
        completed_cycles=6,
        best_response='partial_response'
    )
    
    # Create Carboplatin exposure
    carboplatin = DrugExposure.objects.create(
        person=patient,
        drug_concept_id=1378382,  # Carboplatin concept ID would be different
        drug_exposure_start_date=date(2023, 3, 1),
        drug_exposure_end_date=date(2023, 8, 15),
        drug_type_concept_id=38000177,  # Prescription written
        treatment_line=line2,
        treatment_regimen=regimen2,
        drug_classification='platinum_agent',
        regimen_role='backbone',
        is_platinum_agent=True,
        cycle_number=6,
        total_cycles_planned=6
    )
    
    # Create Paclitaxel exposure
    paclitaxel = DrugExposure.objects.create(
        person=patient,
        drug_concept_id=1378382,  # Paclitaxel concept ID would be different
        drug_exposure_start_date=date(2023, 3, 1),
        drug_exposure_end_date=date(2023, 8, 15),
        drug_type_concept_id=38000177,  # Prescription written
        treatment_line=line2,
        treatment_regimen=regimen2,
        drug_classification='taxane',
        regimen_role='combination',
        cycle_number=6,
        total_cycles_planned=6
    )
    
    return line2, regimen2

def create_eligibility_assessment(patient, condition):
    """Create eligibility assessment for clinical trial screening"""
    
    eligibility = TreatmentLineEligibility.objects.create(
        person=patient,
        condition_occurrence=condition,
        assessment_date=date.today(),
        total_lines_received=2,
        total_platinum_lines=1,
        total_immunotherapy_lines=0,
        total_targeted_therapy_lines=0,
        meets_one_prior_line=True,
        meets_one_prior_platinum=True,
        meets_platinum_refractory=False,
        meets_immunotherapy_naive=True,
        current_treatment_status='off_treatment',
        days_since_last_treatment=30,
        assessment_method='automated'
    )
    
    return eligibility

def demonstrate_eligibility_queries(patient, condition):
    """Demonstrate common clinical trial eligibility queries"""
    
    print("\n=== Clinical Trial Eligibility Assessment ===")
    
    # Query 1: Check if patient has prior platinum therapy
    eligibility = TreatmentLineEligibility.objects.filter(
        person=patient,
        condition_occurrence=condition,
        meets_one_prior_platinum=True
    ).first()
    
    if eligibility:
        print(f"✓ Patient meets '≥1 prior line of platinum therapy' criteria")
        print(f"  - Total treatment lines: {eligibility.total_lines_received}")
        print(f"  - Total platinum lines: {eligibility.total_platinum_lines}")
    else:
        print("✗ Patient does not meet platinum therapy requirements")
    
    # Query 2: Check immunotherapy-naive status
    immuno_naive = TreatmentLineEligibility.objects.filter(
        person=patient,
        condition_occurrence=condition,
        meets_immunotherapy_naive=True
    ).first()
    
    if immuno_naive:
        print(f"✓ Patient is immunotherapy-naive")
        print(f"  - Total immunotherapy lines: {immuno_naive.total_immunotherapy_lines}")
    else:
        print("✗ Patient has received prior immunotherapy")
    
    # Query 3: Treatment line summary
    treatment_lines = TreatmentLine.objects.filter(
        person=patient,
        condition_occurrence=condition
    ).order_by('line_number')
    
    print(f"\n--- Treatment History Summary ---")
    for line in treatment_lines:
        print(f"Line {line.line_number}: {line.line_start_date} to {line.line_end_date}")
        print(f"  Intent: {line.treatment_intent}, Setting: {line.treatment_setting}")
        print(f"  Platinum-based: {line.platinum_based}")
        print(f"  Immunotherapy-based: {line.immunotherapy_based}")
        
        # Show regimens within the line
        regimens = TreatmentRegimen.objects.filter(treatment_line=line)
        for regimen in regimens:
            print(f"  Regimen: {regimen.regimen_name} ({regimen.completed_cycles}/{regimen.planned_cycles} cycles)")
            if regimen.best_response:
                print(f"    Best response: {regimen.best_response}")

def main():
    """Main function to demonstrate treatment line tracking"""
    
    print("=== OMOP Treatment Line Tracking Demonstration ===")
    
    # Create example patient and condition
    print("\n1. Creating example patient with breast cancer...")
    patient, condition = create_example_patient()
    print(f"   Created patient {patient.person_id} with breast cancer")
    
    # Create treatment history
    print("\n2. Creating first-line adjuvant AC treatment...")
    line1, regimen1 = create_first_line_treatment(patient, condition)
    print(f"   Created Line 1: {regimen1.regimen_name}")
    
    print("\n3. Creating second-line metastatic carboplatin + paclitaxel...")
    line2, regimen2 = create_second_line_treatment(patient, condition)
    print(f"   Created Line 2: {regimen2.regimen_name}")
    
    # Create eligibility assessment
    print("\n4. Creating eligibility assessment...")
    eligibility = create_eligibility_assessment(patient, condition)
    print(f"   Assessment completed on {eligibility.assessment_date}")
    
    # Demonstrate eligibility queries
    demonstrate_eligibility_queries(patient, condition)
    
    print("\n=== Demonstration Complete ===")
    print("\nThis example shows how the OMOP treatment line tracking")
    print("enables sophisticated clinical trial eligibility assessment")
    print("following OHDSI Oncology Working Group methodologies.")

if __name__ == "__main__":
    main()
