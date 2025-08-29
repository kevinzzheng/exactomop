from django.contrib import admin
from .models import (
    Person, Location, ConditionOccurrence, Measurement, Observation,
    DrugExposure, ProcedureOccurrence, Episode, EpisodeEvent, Concept,
    ConceptRelationship, Vocabulary, MeasurementConcept, UnitConcept,
    Specimen, GenomicVariant, PatientInfo, ClinicalTrialParticipation,
    VisitOccurrence, OncologyConcept, GenomicConcept, MolecularTest,
    BiomarkerMeasurement, ImagingStudy, ImagingMeasurement, 
    ClinicalTrialBiomarker, ClinicalLabTest, CuratedBiomarkerVocabulary,
    TreatmentLine, TreatmentRegimen, TreatmentLineComponent, TreatmentLineEligibility,
    BehavioralVocabulary, SocialDeterminantsVocabulary, InfectiousDiseaseVocabulary
)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("person_id", "gender_concept_id", "year_of_birth", "race_concept_id", "ethnicity_concept_id")
    search_fields = ("person_id",)
    list_filter = ("gender_concept_id", "year_of_birth")
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("location_id", "zip", "city", "state", "country_concept_id")
    search_fields = ("zip", "city", "state")

@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ("concept_id", "concept_name", "domain_id", "vocabulary_id", "standard_concept")
    search_fields = ("concept_name", "concept_code")
    list_filter = ("domain_id", "vocabulary_id", "standard_concept")

@admin.register(ConditionOccurrence)
class ConditionOccurrenceAdmin(admin.ModelAdmin):
    list_display = ("condition_occurrence_id", "person", "condition_concept", "condition_start_date", 
                   "tumor_laterality", "ajcc_clinical_stage", "histologic_grade")
    search_fields = ("condition_occurrence_id",)
    list_filter = ("condition_start_date", "tumor_laterality", "ajcc_clinical_stage", "histologic_grade",
                  "estrogen_receptor_status", "progesterone_receptor_status", "her2_status")

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("measurement_id", "person", "measurement_concept", "measurement_datetime", 
                   "value_as_number", "unit_concept", "biomarker_type", "clinical_interpretation")
    search_fields = ("measurement_id", "biomarker_type", "assay_method")
    list_filter = ("measurement_datetime", "measurement_source", "critical_value_flag", "biomarker_type")

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ("observation_id", "person", "observation_concept", "observation_datetime", 
                   "value_as_concept", "molecular_test_id", "clinical_significance")
    list_filter = ("observation_datetime", "observation_source", "assay_type", "clinical_significance")

@admin.register(DrugExposure)
class DrugExposureAdmin(admin.ModelAdmin):
    list_display = ("drug_exposure_id", "person", "drug_concept", "drug_exposure_start_datetime", 
                   "line_of_therapy", "treatment_line", "drug_classification", "is_platinum_agent")
    list_filter = ("drug_exposure_start_datetime", "line_of_therapy", "therapy_intent", 
                  "drug_classification", "is_platinum_agent", "is_immunotherapy", "clinical_trial_drug")

@admin.register(ProcedureOccurrence)
class ProcedureOccurrenceAdmin(admin.ModelAdmin):
    list_display = ("procedure_occurrence_id", "person", "procedure_concept", "procedure_datetime", "transplant_type")
    list_filter = ("procedure_datetime", "transplant_type", "imaging_modality")

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("episode_id", "person", "episode_concept", "episode_start_date", "episode_type", "disease_status")
    list_filter = ("episode_type", "disease_status", "response_to_treatment")

@admin.register(EpisodeEvent)
class EpisodeEventAdmin(admin.ModelAdmin):
    list_display = ("episode_event_id", "episode", "event_field_concept_id", "event_id")

@admin.register(PatientInfo)
class PatientInfoAdmin(admin.ModelAdmin):
    list_display = ("person", "patient_age", "gender", "disease", "stage")
    search_fields = ("person__person_id",)
    list_filter = ("disease", "stage", "patient_age")


@admin.register(MeasurementConcept)
class MeasurementConceptAdmin(admin.ModelAdmin):
    list_display = ("concept", "patient_info_field", "measurement_category", "preferred_unit_concept")
    search_fields = ("patient_info_field", "concept__concept_name")
    list_filter = ("measurement_category",)

@admin.register(OncologyConcept)
class OncologyConceptAdmin(admin.ModelAdmin):
    list_display = ("concept", "oncology_category", "cancer_type", "staging_system", "biomarker_type")
    search_fields = ("concept__concept_name", "cancer_type")
    list_filter = ("oncology_category", "staging_system", "biomarker_type")

@admin.register(GenomicConcept)
class GenomicConceptAdmin(admin.ModelAdmin):
    list_display = ("concept", "genomic_category", "gene_symbol", "clinical_actionability")
    search_fields = ("concept__concept_name", "gene_symbol")
    list_filter = ("genomic_category", "clinical_actionability")

@admin.register(GenomicVariant)
class GenomicVariantAdmin(admin.ModelAdmin):
    list_display = ("variant_id", "person", "gene_symbol", "variant_type", "clinical_significance", 
                   "molecular_alteration", "biomarker_status", "eligibility_relevant")
    search_fields = ("gene_symbol", "hgvs_notation", "clinvar_id", "cosmic_id")
    list_filter = ("variant_type", "clinical_significance", "molecular_alteration", "biomarker_status", 
                  "eligibility_relevant", "testing_method")

@admin.register(MolecularTest)
class MolecularTestAdmin(admin.ModelAdmin):
    list_display = ("test_id", "person", "test_name", "test_type", "test_date", "overall_result", 
                   "actionable_alterations_count", "trial_eligible")
    search_fields = ("test_name", "laboratory")
    list_filter = ("test_type", "overall_result", "trial_eligible")

@admin.register(BiomarkerMeasurement)
class BiomarkerMeasurementAdmin(admin.ModelAdmin):
    list_display = ("biomarker_id", "person", "biomarker_name", "biomarker_category", 
                   "result_interpretation", "trial_eligibility_criterion", "actionable_biomarker")
    search_fields = ("biomarker_name", "assay_name")
    list_filter = ("biomarker_category", "result_interpretation", "trial_eligibility_criterion", 
                  "actionable_biomarker")

@admin.register(CuratedBiomarkerVocabulary)
class CuratedBiomarkerVocabularyAdmin(admin.ModelAdmin):
    list_display = ("vocabulary_id", "biomarker_name", "biomarker_category", "evidence_level",
                   "common_eligibility_criterion", "companion_diagnostic")
    search_fields = ("biomarker_name", "loinc_code", "snomed_code", "hgnc_gene_symbol")
    list_filter = ("biomarker_category", "evidence_level", "common_eligibility_criterion", 
                  "companion_diagnostic", "stratification_factor")

@admin.register(ImagingStudy)
class ImagingStudyAdmin(admin.ModelAdmin):
    list_display = ("imaging_study_id", "person", "modality", "study_date", "body_part_examined",
                   "baseline_imaging", "response_assessment", "image_quality")
    search_fields = ("study_uid", "accession_number", "study_description")
    list_filter = ("modality", "contrast_agent", "baseline_imaging", "response_assessment", "image_quality")

@admin.register(ImagingMeasurement)
class ImagingMeasurementAdmin(admin.ModelAdmin):
    list_display = ("imaging_measurement_id", "person", "measurement_name", "lesion_type", 
                   "longest_diameter", "response_category", "measurement_date")
    search_fields = ("measurement_name", "anatomic_region")
    list_filter = ("lesion_type", "response_category", "measurement_confidence")

@admin.register(ClinicalTrialBiomarker)
class ClinicalTrialBiomarkerAdmin(admin.ModelAdmin):
    list_display = ("biomarker_id", "person", "biomarker_type", "test_date", "categorical_result",
                   "threshold_met", "companion_diagnostic")
    search_fields = ("assay_name", "drug_target")
    list_filter = ("biomarker_type", "test_method", "categorical_result", "threshold_met", 
                  "companion_diagnostic", "trial_eligibility_biomarker")

@admin.register(ClinicalLabTest)
class ClinicalLabTestAdmin(admin.ModelAdmin):
    list_display = ("lab_test_id", "person", "test_name", "test_date", "numeric_result", 
                   "result_unit", "abnormal_flag", "ctcae_grade")
    search_fields = ("test_name", "loinc_code")
    list_filter = ("test_category", "organ_system", "abnormal_flag", "ctcae_grade", 
                  "eligibility_test", "safety_monitoring", "baseline_test")

@admin.register(TreatmentLine)
class TreatmentLineAdmin(admin.ModelAdmin):
    list_display = ("treatment_line_id", "person", "line_number", "line_start_date", "treatment_intent",
                   "platinum_based", "immunotherapy_based", "treatment_response")
    search_fields = ("regimen_name", "trial_identifier")
    list_filter = ("line_number", "treatment_intent", "platinum_based", "immunotherapy_based", 
                  "targeted_therapy_based", "treatment_response", "received_in_trial")

@admin.register(TreatmentRegimen)
class TreatmentRegimenAdmin(admin.ModelAdmin):
    list_display = ("regimen_id", "person", "regimen_name", "regimen_sequence", "regimen_start_date",
                   "contains_platinum", "contains_immunotherapy", "best_response")
    search_fields = ("regimen_name", "regimen_code")
    list_filter = ("regimen_type", "contains_platinum", "contains_immunotherapy", 
                  "contains_targeted_therapy", "best_response", "early_discontinuation")

@admin.register(TreatmentLineComponent)
class TreatmentLineComponentAdmin(admin.ModelAdmin):
    list_display = ("component_id", "person", "treatment_line", "component_type", "drug_classification",
                   "is_platinum_agent", "is_immunotherapy", "component_role")
    search_fields = ("drug_classification",)
    list_filter = ("component_type", "component_role", "drug_classification", 
                  "is_platinum_agent", "is_immunotherapy", "is_targeted_therapy")

@admin.register(TreatmentLineEligibility)
class TreatmentLineEligibilityAdmin(admin.ModelAdmin):
    list_display = ("eligibility_id", "person", "assessment_date", "total_lines_received",
                   "meets_one_prior_platinum", "meets_immunotherapy_naive", "current_treatment_status")
    search_fields = ("calculation_algorithm",)
    list_filter = ("meets_one_prior_line", "meets_two_prior_lines", "meets_one_prior_platinum", 
                  "meets_platinum_refractory", "meets_immunotherapy_naive", "current_treatment_status",
                  "needs_manual_review")

@admin.register(BehavioralVocabulary)
class BehavioralVocabularyAdmin(admin.ModelAdmin):
    list_display = ("vocabulary_id", "observation_type", "observation_name", "exclusion_criterion",
                   "inclusion_criterion", "risk_assessment_factor")
    search_fields = ("observation_name", "loinc_code", "snomed_code")
    list_filter = ("observation_type", "exclusion_criterion", "inclusion_criterion", 
                  "risk_assessment_factor")

@admin.register(SocialDeterminantsVocabulary)
class SocialDeterminantsVocabularyAdmin(admin.ModelAdmin):
    list_display = ("vocabulary_id", "determinant_category", "determinant_name", "health_impact_level",
                   "affects_eligibility", "affects_compliance", "affects_outcomes")
    search_fields = ("determinant_name", "z_code", "snomed_code")
    list_filter = ("determinant_category", "health_impact_level", "affects_eligibility", 
                  "affects_compliance", "affects_outcomes")

@admin.register(InfectiousDiseaseVocabulary)
class InfectiousDiseaseVocabularyAdmin(admin.ModelAdmin):
    list_display = ("vocabulary_id", "disease_name", "pathogen_type", "exclusion_criterion",
                   "requires_monitoring", "drug_interaction_risk")
    search_fields = ("disease_name", "icd10_code", "snomed_code")
    list_filter = ("pathogen_type", "exclusion_criterion", "requires_monitoring", 
                  "drug_interaction_risk")
