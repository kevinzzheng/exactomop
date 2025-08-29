#!/usr/bin/env python
"""
Example usage of OMOP Behavioral & Social Determinants Extensions for Patient Assessment

This script demonstrates how to use the enhanced Observation model and vocabulary models
to assess patient behavioral, social, and demographic factors for comprehensive care.
"""

import os
import sys
import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omop_site.settings')
django.setup()

from omop.models import (
    Person, Observation, BehavioralVocabulary, SocialDeterminantsVocabulary,
    InfectiousDiseaseVocabulary, Concept
)

def create_example_patient():
    """Create an example patient for behavioral assessment"""
    
    patient = Person.objects.create(
        person_id=2001,
        gender_concept_id=8532,  # Female
        year_of_birth=1978,
        month_of_birth=9,
        day_of_birth=22,
        race_concept_id=8527,  # White
        ethnicity_concept_id=38003564  # Not Hispanic or Latino
    )
    
    return patient

def create_behavioral_vocabulary_entries():
    """Create example behavioral vocabulary entries"""
    
    # Create a concept for smoking status (in real implementation, use existing OMOP concepts)
    smoking_concept = Concept.objects.create(
        concept_id=1000001,
        concept_name='Smoking Status Assessment',
        domain_id='Observation',
        vocabulary_id='LOINC',
        concept_class_id='Clinical Observation',
        standard_concept='S',
        concept_code='72166-2'
    )
    
    # Create behavioral vocabulary for smoking
    smoking_vocab = BehavioralVocabulary.objects.create(
        concept=smoking_concept,
        observation_type='smoking_status',
        observation_name='Smoking History Assessment',
        loinc_code='72166-2',
        assessment_method='Clinical interview and patient history',
        clinical_cutoffs={'pack_years_threshold': 10, 'cessation_period_months': 12},
        clinical_significance='Smoking history affects treatment planning and outcomes'
    )
    
    # Create concept for pregnancy status
    pregnancy_concept = Concept.objects.create(
        concept_id=1000002,
        concept_name='Pregnancy Status',
        domain_id='Observation',
        vocabulary_id='LOINC',
        concept_class_id='Clinical Observation',
        standard_concept='S',
        concept_code='82810-3'
    )
    
    # Create behavioral vocabulary for pregnancy
    pregnancy_vocab = BehavioralVocabulary.objects.create(
        concept=pregnancy_concept,
        observation_type='pregnancy_status',
        observation_name='Pregnancy Status Assessment',
        loinc_code='82810-3',
        assessment_method='Pregnancy test and clinical assessment',
        clinical_significance='Pregnancy status critical for drug safety considerations'
    )
    
    return smoking_vocab, pregnancy_vocab

def create_social_determinants_vocabulary():
    """Create example social determinants vocabulary"""
    
    # Create concept for caregiver status
    caregiver_concept = Concept.objects.create(
        concept_id=1000003,
        concept_name='Caregiver Support Assessment',
        domain_id='Observation',
        vocabulary_id='Custom',
        concept_class_id='Social Factor',
        standard_concept='S',
        concept_code='CAREGIVER_001'
    )
    
    # Create social determinants vocabulary for caregiver support
    caregiver_vocab = SocialDeterminantsVocabulary.objects.create(
        concept=caregiver_concept,
        determinant_category='Social Support',
        determinant_name='Caregiver Availability Assessment',
        z_code='Z74.1',  # ICD-10 Z-code for need for assistance with personal care
        affects_compliance=True,
        health_impact_level='HIGH',
        assessment_method='Social work assessment and patient interview',
        screening_questions={
            'primary_question': 'Do you have someone who can help you with daily activities?',
            'followup_questions': [
                'Who is your primary caregiver?',
                'Are they available for study visits?',
                'Do they understand your medical condition?'
            ]
        }
    )
    
    return caregiver_vocab

def create_infectious_disease_vocabulary():
    """Create example infectious disease vocabulary"""
    
    # Create concept for HIV status
    hiv_concept = Concept.objects.create(
        concept_id=1000004,
        concept_name='HIV Status',
        domain_id='Observation',
        vocabulary_id='SNOMED',
        concept_class_id='Clinical Finding',
        standard_concept='S',
        concept_code='165816005'
    )
    
    # Create infectious disease vocabulary for HIV
    hiv_vocab = InfectiousDiseaseVocabulary.objects.create(
        concept=hiv_concept,
        disease_name='Human Immunodeficiency Virus',
        pathogen_type='VIRUS',
        icd10_code='Z21',
        requires_monitoring=True,
        drug_interaction_risk=True,
        standard_tests={
            'screening_tests': ['HIV-1/2 antibody', 'HIV-1/2 antigen/antibody'],
            'confirmatory_tests': ['HIV-1 Western blot', 'HIV-1 RNA PCR'],
            'monitoring_tests': ['CD4 count', 'HIV viral load']
        },
        treatment_considerations='HIV-positive patients may require dose modifications'
    )
    
    return hiv_vocab

def create_patient_behavioral_assessments(patient):
    """Create comprehensive behavioral assessments for a patient"""
    
    assessments = []
    
    # Smoking status assessment
    smoking_obs = Observation.objects.create(
        person=patient,
        observation_datetime=date.today(),
        behavioral_category='smoking_status',
        smoking_status='former_smoker',
        tobacco_product_type='cigarettes',
        pack_years=8.5,  # Moderate smoking history
        smoking_cessation_date=date(2020, 3, 15),  # Quit 4+ years ago
        observation_source_value='Clinical interview'
    )
    assessments.append(smoking_obs)
    
    # Pregnancy status assessment
    pregnancy_obs = Observation.objects.create(
        person=patient,
        observation_datetime=date.today(),
        behavioral_category='pregnancy_status',
        pregnancy_status='not_pregnant',
        pregnancy_test_date=date.today() - timedelta(days=7),
        contraceptive_method='hormonal_oral',
        menopausal_status='premenopausal'
    )
    assessments.append(pregnancy_obs)
    
    # Substance use assessment
    substance_obs = Observation.objects.create(
        person=patient,
        observation_datetime=date.today(),
        behavioral_category='substance_use',
        substance_use_category='alcohol',
        alcohol_use_level='light',  # 1-7 drinks/week
        drinks_per_week=4,
        substance_use_details='Social drinking only, no history of alcohol abuse'
    )
    assessments.append(substance_obs)
    
    # Infectious disease screening
    hiv_obs = Observation.objects.create(
        person=patient,
        observation_datetime=date.today(),
        behavioral_category='infectious_disease',
        infectious_disease_type='Human Immunodeficiency Virus',
        infectious_disease_status='negative',
        infection_test_date=date.today() - timedelta(days=30),
        infection_test_result='HIV-1/2 antibody: Negative'
    )
    assessments.append(hiv_obs)
    
    # Hepatitis B screening
    hbv_obs = Observation.objects.create(
        person=patient,
        observation_datetime=date.today(),
        behavioral_category='infectious_disease',
        infectious_disease_type='Hepatitis B',
        infectious_disease_status='immune',
        infection_test_date=date.today() - timedelta(days=30),
        infection_test_result='HBsAg: Negative, Anti-HBs: Positive (vaccinated)',
        vaccination_status='Completed HBV vaccine series'
    )
    assessments.append(hbv_obs)
    
    # Caregiver support assessment
    caregiver_obs = Observation.objects.create(
        person=patient,
        observation_datetime=date.today(),
        behavioral_category='caregiver_status',
        caregiver_status='available_family',
        caregiver_relationship='Spouse',
        social_support_score=8,  # Scale 1-10, 8 indicates good support
        lives_alone=False,
        transportation_access=True
    )
    assessments.append(caregiver_obs)
    
    # Mental health and consent capability
    mental_health_obs = Observation.objects.create(
        person=patient,
        observation_datetime=date.today(),
        behavioral_category='mental_health',
        mental_health_status='no_disorder',
        consent_capability='capable',
        cognitive_assessment_score=28,  # MMSE score (normal: 24-30)
        depression_screening_score=3,   # PHQ-9 score (normal: 0-4)
        anxiety_screening_score=2      # GAD-7 score (normal: 0-4)
    )
    assessments.append(mental_health_obs)
    
    # Mark assessments as complete
    for obs in assessments:
        obs.behavioral_data_complete = True
        obs.social_data_complete = True
        obs.risk_assessment_date = date.today()
        obs.assessment_provider = 'Dr. Smith, Clinical Research Team'
        obs.save()
    
    return assessments

def demonstrate_patient_assessment(patient):
    """Demonstrate patient behavioral and social assessment queries"""
    
    print("\n=== Patient Behavioral & Social Assessment ===")
    print(f"Patient: {patient.person_id}")
    
    # Assessment 1: Smoking history review
    smoking_obs = Observation.objects.filter(
        person=patient,
        behavioral_category='smoking_status'
    ).first()
    
    if smoking_obs:
        print(f"📋 SMOKING HISTORY: {smoking_obs.smoking_status.replace('_', ' ').title()}")
        if smoking_obs.pack_years:
            print(f"   Pack-years: {smoking_obs.pack_years}")
        if smoking_obs.smoking_cessation_date:
            print(f"   Quit date: {smoking_obs.smoking_cessation_date}")
    
    # Assessment 2: Reproductive health status
    pregnancy_obs = Observation.objects.filter(
        person=patient,
        behavioral_category='pregnancy_status'
    ).first()
    
    if pregnancy_obs:
        print(f"📋 REPRODUCTIVE HEALTH:")
        print(f"   Pregnancy status: {pregnancy_obs.pregnancy_status.replace('_', ' ').title()}")
        if pregnancy_obs.contraceptive_method:
            print(f"   Contraceptive method: {pregnancy_obs.contraceptive_method.replace('_', ' ').title()}")
        if pregnancy_obs.menopausal_status:
            print(f"   Menopausal status: {pregnancy_obs.menopausal_status.replace('_', ' ').title()}")
    
    # Assessment 3: Infectious disease screening results
    infectious_obs = Observation.objects.filter(
        person=patient,
        behavioral_category='infectious_disease'
    )
    
    print(f"📋 INFECTIOUS DISEASE SCREENING:")
    for obs in infectious_obs:
        status = obs.infectious_disease_status.replace('_', ' ').title()
        print(f"   {obs.infectious_disease_type}: {status}")
        if obs.infection_test_date:
            print(f"     Test date: {obs.infection_test_date}")
    
    # Assessment 4: Social support evaluation
    caregiver_obs = Observation.objects.filter(
        person=patient,
        behavioral_category='caregiver_status'
    ).first()
    
    if caregiver_obs:
        print(f"📋 SOCIAL SUPPORT:")
        print(f"   Caregiver status: {caregiver_obs.caregiver_status.replace('_', ' ').title()}")
        if caregiver_obs.caregiver_relationship:
            print(f"   Relationship: {caregiver_obs.caregiver_relationship}")
        if caregiver_obs.social_support_score:
            print(f"   Support score: {caregiver_obs.social_support_score}/10")
        print(f"   Transportation access: {'Yes' if caregiver_obs.transportation_access else 'No'}")
    
    # Assessment 5: Mental health and cognition
    mental_obs = Observation.objects.filter(
        person=patient,
        behavioral_category='mental_health'
    ).first()
    
    if mental_obs:
        print(f"📋 MENTAL HEALTH & COGNITION:")
        print(f"   Mental health status: {mental_obs.mental_health_status.replace('_', ' ').title()}")
        print(f"   Consent capability: {mental_obs.consent_capability.title()}")
        if mental_obs.cognitive_assessment_score:
            print(f"   Cognitive score (MMSE): {mental_obs.cognitive_assessment_score}/30")
        if mental_obs.depression_screening_score is not None:
            print(f"   Depression score (PHQ-9): {mental_obs.depression_screening_score}")
        if mental_obs.anxiety_screening_score is not None:
            print(f"   Anxiety score (GAD-7): {mental_obs.anxiety_screening_score}")
    
    # Assessment 6: Substance use review
    substance_obs = Observation.objects.filter(
        person=patient,
        behavioral_category='substance_use'
    ).first()
    
    if substance_obs:
        print(f"📋 SUBSTANCE USE:")
        print(f"   Category: {substance_obs.substance_use_category.title()}")
        if substance_obs.alcohol_use_level:
            print(f"   Alcohol use level: {substance_obs.alcohol_use_level.title()}")
        if substance_obs.drinks_per_week:
            print(f"   Drinks per week: {substance_obs.drinks_per_week}")
    
    print(f"\n=== ASSESSMENT SUMMARY ===")
    print("Comprehensive behavioral and social determinants assessment completed.")
    print("All key areas evaluated for optimal patient care planning.")

def demonstrate_vocabulary_usage():
    """Demonstrate how to use vocabulary models for standardization"""
    
    print("\n=== Vocabulary Standardization Examples ===")
    
    # Find behavioral vocabulary entries
    smoking_vocab = BehavioralVocabulary.objects.filter(
        observation_type='smoking_status'
    ).first()
    
    if smoking_vocab:
        print(f"Smoking Assessment Vocabulary:")
        print(f"  Name: {smoking_vocab.observation_name}")
        print(f"  LOINC Code: {smoking_vocab.loinc_code}")
        print(f"  Clinical Cutoffs: {smoking_vocab.clinical_cutoffs}")
    
    # Find social determinants vocabulary
    caregiver_vocab = SocialDeterminantsVocabulary.objects.filter(
        determinant_category='Social Support'
    ).first()
    
    if caregiver_vocab:
        print(f"\nSocial Support Vocabulary:")
        print(f"  Name: {caregiver_vocab.determinant_name}")
        print(f"  Z-Code: {caregiver_vocab.z_code}")
        print(f"  Health Impact: {caregiver_vocab.health_impact_level}")
        print(f"  Affects Compliance: {caregiver_vocab.affects_compliance}")
    
    # Find infectious disease vocabulary
    hiv_vocab = InfectiousDiseaseVocabulary.objects.filter(
        disease_name='Human Immunodeficiency Virus'
    ).first()
    
    if hiv_vocab:
        print(f"\nHIV Screening Vocabulary:")
        print(f"  Disease: {hiv_vocab.disease_name}")
        print(f"  ICD-10 Code: {hiv_vocab.icd10_code}")
        print(f"  Requires Monitoring: {hiv_vocab.requires_monitoring}")
        print(f"  Standard Tests: {hiv_vocab.standard_tests}")

def main():
    """Main demonstration function"""
    
    print("=== OMOP Behavioral & Social Determinants Demonstration ===")
    
    # Create example data
    print("\n1. Creating example patient...")
    patient = create_example_patient()
    print(f"   Created patient {patient.person_id}")
    
    print("\n2. Setting up vocabulary entries...")
    smoking_vocab, pregnancy_vocab = create_behavioral_vocabulary_entries()
    caregiver_vocab = create_social_determinants_vocabulary()
    hiv_vocab = create_infectious_disease_vocabulary()
    print("   Created behavioral, social determinants, and infectious disease vocabularies")
    
    print("\n3. Creating comprehensive behavioral assessments...")
    assessments = create_patient_behavioral_assessments(patient)
    print(f"   Created {len(assessments)} behavioral and social assessments")
    
    # Demonstrate patient assessment
    demonstrate_patient_assessment(patient)
    
    # Demonstrate vocabulary usage
    demonstrate_vocabulary_usage()
    
    print("\n=== Demonstration Complete ===")
    print("\nThis example shows how the enhanced OMOP Observation model")
    print("and new vocabulary models enable comprehensive assessment of")
    print("behavioral, social determinants, and demographic factors")
    print("for optimal patient care and treatment planning.")

if __name__ == "__main__":
    main()
