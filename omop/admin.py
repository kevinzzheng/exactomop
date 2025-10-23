from django.contrib import admin
from .models import (
    Person, Location, ConditionOccurrence, Measurement, Observation,
    DrugExposure, ProcedureOccurrence, Episode, EpisodeEvent, Concept,
    ConceptRelationship, Vocabulary, MeasurementConcept, UnitConcept,
    Specimen, GenomicVariant, PatientInfo, ClinicalTrialParticipation,
    VisitOccurrence, OncologyConcept, MolecularTest,
    BiomarkerMeasurement, ImagingStudy, ImagingMeasurement, 
    ClinicalTrialBiomarker, ClinicalLabTest, CuratedBiomarkerVocabulary,
    TreatmentLine, TreatmentRegimen, TreatmentLineComponent,
    BehavioralVocabulary, SocialDeterminantsVocabulary, InfectiousDiseaseVocabulary,
    # OMOP Oncology Extension models
    TumorAssessment, TumorAssessmentMeasurement, CancerStagingMap,
    OncologyVocabulary, StagingMeasurementConcept, ICDOTopographyConcept,
    ICDOMorphologyConcept, Modifier, OncologyModifier, RadiationOccurrence,
    StemCellTransplant, ClinicalTrial, BiospecimenCollection, OncologyEpisodeDetail
)
# Safety Scoring Models
from .models_safety import TrialArm, AdverseEvent, TrialArmSafetyMetrics

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

@admin.register(GenomicVariant)
class GenomicVariantAdmin(admin.ModelAdmin):
    list_display = ("variant_id", "person", "gene_symbol", "variant_type", "clinical_significance", 
                   "molecular_alteration", "biomarker_status")
    search_fields = ("gene_symbol", "hgvs_notation", "clinvar_id", "cosmic_id")
    list_filter = ("variant_type", "clinical_significance", "molecular_alteration", "biomarker_status", 
                  "testing_method")

@admin.register(MolecularTest)
class MolecularTestAdmin(admin.ModelAdmin):
    list_display = ("test_id", "person", "test_name", "test_type", "test_date", "overall_result", 
                   "actionable_alterations_count")
    search_fields = ("test_name", "laboratory")
    list_filter = ("test_type", "overall_result")

@admin.register(BiomarkerMeasurement)
class BiomarkerMeasurementAdmin(admin.ModelAdmin):
    list_display = ("biomarker_id", "person", "biomarker_name", "biomarker_category", 
                   "result_interpretation", "measurement_date")
    search_fields = ("biomarker_name", "assay_name")
    list_filter = ("biomarker_category", "result_interpretation")

@admin.register(CuratedBiomarkerVocabulary)
class CuratedBiomarkerVocabularyAdmin(admin.ModelAdmin):
    list_display = ("vocabulary_id", "biomarker_name", "biomarker_category", "evidence_level")
    search_fields = ("biomarker_name", "loinc_code", "snomed_code", "hgnc_gene_symbol")
    list_filter = ("biomarker_category", "evidence_level")

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
                   "test_method")
    search_fields = ("assay_name", "drug_target")
    list_filter = ("biomarker_type", "test_method", "categorical_result")

@admin.register(ClinicalLabTest)
class ClinicalLabTestAdmin(admin.ModelAdmin):
    list_display = ("lab_test_id", "person", "test_name", "test_date", "numeric_result", 
                   "result_unit", "abnormal_flag", "ctcae_grade")
    search_fields = ("test_name", "loinc_code")
    list_filter = ("test_category", "organ_system", "abnormal_flag", "ctcae_grade")

@admin.register(TreatmentLine)
class TreatmentLineAdmin(admin.ModelAdmin):
    list_display = ("treatment_line_id", "person", "line_number", "line_start_date", "treatment_intent",
                   "platinum_based", "immunotherapy_based", "treatment_response")
    search_fields = ("regimen_name", "trial_identifier")
    list_filter = ("line_number", "treatment_intent", "platinum_based", "immunotherapy_based", 
                  "targeted_therapy_based", "treatment_response", "received_in_trial")

@admin.register(TreatmentRegimen)
class TreatmentRegimenAdmin(admin.ModelAdmin):
    list_display = ("regimen_id", "person", "regimen_name", "line_number", "regimen_start_date",
                   "regimen_type", "treatment_intent", "best_response")
    search_fields = ("regimen_name", "regimen_code")
    list_filter = ("regimen_type", "treatment_intent", "best_response", "regimen_discontinued")

@admin.register(TreatmentLineComponent)
class TreatmentLineComponentAdmin(admin.ModelAdmin):
    list_display = ("component_id", "person", "treatment_line", "component_type", "drug_classification",
                   "is_platinum_agent", "is_immunotherapy", "component_role")
    search_fields = ("drug_classification",)
    list_filter = ("component_type", "component_role", "drug_classification", 
                  "is_platinum_agent", "is_immunotherapy", "is_targeted_therapy")

@admin.register(BehavioralVocabulary)
class BehavioralVocabularyAdmin(admin.ModelAdmin):
    list_display = ("vocabulary_id", "observation_type", "observation_name", "exclusion_criterion",
                   "inclusion_criterion", "risk_assessment_factor")
    search_fields = ("observation_name", "loinc_code", "snomed_code")
    list_filter = ("observation_type", "exclusion_criterion", "inclusion_criterion", 
                  "risk_assessment_factor")

@admin.register(SocialDeterminantsVocabulary)
class SocialDeterminantsVocabularyAdmin(admin.ModelAdmin):
    list_display = ("vocabulary_id", "determinant_category", "determinant_name", "health_impact_level")
    search_fields = ("determinant_name", "z_code", "snomed_code")
    list_filter = ("determinant_category", "health_impact_level")

@admin.register(InfectiousDiseaseVocabulary)
class InfectiousDiseaseVocabularyAdmin(admin.ModelAdmin):
    list_display = ("vocabulary_id", "disease_name", "pathogen_type", "exclusion_criterion",
                   "requires_monitoring", "drug_interaction_risk")
    search_fields = ("disease_name", "icd10_code", "snomed_code")
    list_filter = ("pathogen_type", "exclusion_criterion", "requires_monitoring", 
                  "drug_interaction_risk")

@admin.register(TumorAssessment)
class TumorAssessmentAdmin(admin.ModelAdmin):
    list_display = ("tumor_assessment_id", "person", "assessment_date", "assessment_method", 
                   "overall_response", "disease_status")
    search_fields = ("overall_response", "assessment_method")
    list_filter = ("assessment_method", "overall_response", "disease_status", "assessment_date")

@admin.register(CancerStagingMap)
class CancerStagingMapAdmin(admin.ModelAdmin):
    list_display = ("staging_map_id", "source_staging_system", "source_stage_value", "target_staging_system", 
                   "target_stage_value", "mapping_confidence")
    search_fields = ("source_staging_system", "source_stage_value", "target_staging_system")
    list_filter = ("source_staging_system", "target_staging_system", "mapping_confidence")

@admin.register(OncologyVocabulary)
class OncologyVocabularyAdmin(admin.ModelAdmin):
    list_display = ("oncology_vocabulary_id", "vocabulary_id", "concept_code", "concept_name", 
                   "oncology_domain", "valid_start_date")
    search_fields = ("concept_name", "concept_code", "icdo_site_code", "ajcc_chapter")
    list_filter = ("oncology_domain", "vocabulary_id")

@admin.register(StagingMeasurementConcept)
class StagingMeasurementConceptAdmin(admin.ModelAdmin):
    list_display = ("staging_concept_id", "concept", "staging_system", "staging_component", 
                   "staging_system_version", "assessment_method")
    search_fields = ("concept__concept_name", "staging_system")
    list_filter = ("staging_system", "staging_component", "assessment_method")

@admin.register(ICDOTopographyConcept)
class ICDOTopographyConceptAdmin(admin.ModelAdmin):
    list_display = ("icdo_topography_id", "concept", "icdo_site_code", "icdo_site_name", 
                   "major_site", "body_system", "laterality_applicable")
    search_fields = ("concept__concept_name", "icdo_site_code", "icdo_site_name")
    list_filter = ("major_site", "body_system", "laterality_applicable")

@admin.register(ICDOMorphologyConcept)
class ICDOMorphologyConceptAdmin(admin.ModelAdmin):
    list_display = ("icdo_morphology_id", "concept", "icdo_morphology_code", "icdo_morphology_name", 
                   "histologic_type", "behavior_code", "behavior_description")
    search_fields = ("concept__concept_name", "icdo_morphology_code", "icdo_morphology_name")
    list_filter = ("histologic_type", "behavior_code", "behavior_description")

# Additional OMOP Oncology Extension Admin Configurations

@admin.register(Modifier)
class ModifierAdmin(admin.ModelAdmin):
    list_display = ("modifier_id", "person", "modifier_concept", "modifier_of_event_id", "modifier_datetime")
    search_fields = ("modifier_concept__concept_name",)
    list_filter = ("modifier_datetime", "modifier_type_concept")

@admin.register(OncologyModifier)
class OncologyModifierAdmin(admin.ModelAdmin):
    list_display = ("oncology_modifier_id", "person", "modifier_source_concept", "modifier_datetime", "cancer_modifier_type")
    search_fields = ("modifier_source_concept__concept_name",)
    list_filter = ("cancer_modifier_type", "staging_basis", "modifier_datetime")

@admin.register(RadiationOccurrence)
class RadiationOccurrenceAdmin(admin.ModelAdmin):
    list_display = ("radiation_occurrence_id", "person", "radiation_concept", "radiation_occurrence_start_date", "treatment_intent", 
                   "total_dose", "fractions_planned")
    search_fields = ("radiation_concept__concept_name", "anatomical_site_concept__concept_name")
    list_filter = ("treatment_intent", "radiation_technique", "radiation_occurrence_start_date")

@admin.register(StemCellTransplant)
class StemCellTransplantAdmin(admin.ModelAdmin):
    list_display = ("stem_cell_transplant_id", "person", "transplant_concept", "transplant_date", "transplant_type", 
                   "stem_cell_source", "donor_type")
    search_fields = ("transplant_concept__concept_name",)
    list_filter = ("transplant_type", "donor_type", "stem_cell_source", "transplant_date")

@admin.register(TumorAssessmentMeasurement)
class TumorAssessmentMeasurementAdmin(admin.ModelAdmin):
    list_display = ("tumor_measurement_id", "tumor_assessment", "person", "lesion_id", "lesion_type", 
                   "longest_diameter", "measurement_method")
    search_fields = ("lesion_id", "anatomical_site_concept__concept_name")
    list_filter = ("lesion_type", "lesion_response", "measurement_method")

@admin.register(ClinicalTrial)
class ClinicalTrialAdmin(admin.ModelAdmin):
    list_display = ("clinical_trial_id", "nct_number", "trial_title", "trial_phase", "enrollment_date", 
                   "trial_completion_date")
    search_fields = ("nct_number", "trial_title", "trial_acronym")
    list_filter = ("trial_phase", "trial_type", "enrollment_date")

@admin.register(BiospecimenCollection)
class BiospecimenCollectionAdmin(admin.ModelAdmin):
    list_display = ("biospecimen_id", "person", "specimen_type", "collection_date", "collection_method", 
                   "storage_temperature")
    search_fields = ("biobank_id", "laboratory_id", "anatomical_site_concept__concept_name")
    list_filter = ("specimen_type", "collection_method", "collection_date", "specimen_quality")

@admin.register(OncologyEpisodeDetail)
class OncologyEpisodeDetailAdmin(admin.ModelAdmin):
    list_display = ("episode_detail_id", "episode", "person", "detail_date", "disease_status", 
                   "days_from_diagnosis", "ecog_performance_status")
    search_fields = ("disease_status", "progression_type")
    list_filter = ("disease_status", "progression_type", "detail_date", "ecog_performance_status")

# Safety Scoring Models Admin

@admin.register(TrialArm)
class TrialArmAdmin(admin.ModelAdmin):
    list_display = ("trial_arm_id", "nct_number", "arm_name", "arm_code", "arm_type", "status", 
                   "n_patients", "enrollment_start_date", "last_data_cut")
    search_fields = ("nct_number", "arm_name", "arm_code")
    list_filter = ("status", "arm_type", "enrollment_start_date")
    readonly_fields = ("created_at", "updated_at")

@admin.register(AdverseEvent)
class AdverseEventAdmin(admin.ModelAdmin):
    list_display = ("adverse_event_id", "person", "trial_arm", "event_name", "grade", 
                   "event_date", "serious", "relationship_to_treatment", "outcome")
    search_fields = ("event_name", "person__person_id")
    list_filter = ("grade", "serious", "relationship_to_treatment", "outcome", "event_date")
    readonly_fields = ("created_at", "updated_at")
    
    fieldsets = (
        ("Event Identification", {
            "fields": ("person", "trial_arm", "event_concept", "event_name", "event_description")
        }),
        ("Timing", {
            "fields": ("event_date", "onset_date", "resolution_date")
        }),
        ("Severity & Classification", {
            "fields": ("grade", "serious", "expected")
        }),
        ("Causality & Outcomes", {
            "fields": ("relationship_to_treatment", "outcome", "action_taken")
        }),
        ("Reporting", {
            "fields": ("reported_to_sponsor", "reported_to_irb", "reported_to_fda")
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

@admin.register(TrialArmSafetyMetrics)
class TrialArmSafetyMetricsAdmin(admin.ModelAdmin):
    list_display = ("safety_metrics_id", "trial_arm", "data_cut_date", "safety_score", 
                   "person_years", "n_patients", "e1_2_count", "e3_4_count", "e5_count", 
                   "web", "eair")
    search_fields = ("trial_arm__arm_name", "trial_arm__arm_code", "trial_arm__nct_number")
    list_filter = ("data_cut_date", "computation_date")
    readonly_fields = ("computation_date", "created_at", "updated_at")
    
    fieldsets = (
        ("Trial Arm & Period", {
            "fields": ("trial_arm", "data_cut_date", "analysis_period_start", "analysis_period_end")
        }),
        ("Patient Metrics", {
            "fields": ("n_patients", "person_years")
        }),
        ("Adverse Event Counts", {
            "fields": ("e1_2_count", "e3_4_count", "e5_count", "total_ae_count", "patients_with_any_ae")
        }),
        ("Computed Safety Metrics", {
            "fields": ("eair", "web", "safety_score", "web_threshold_h")
        }),
        ("Metadata", {
            "fields": ("computation_date", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    # Add custom actions for recomputing safety scores
    actions = ['recompute_safety_scores']
    
    def recompute_safety_scores(self, request, queryset):
        """Admin action to recompute safety scores for selected metrics."""
        from django.core.management import call_command
        from io import StringIO
        
        trial_arm_ids = list(queryset.values_list('trial_arm_id', flat=True).distinct())
        
        for trial_arm_id in trial_arm_ids:
            out = StringIO()
            call_command('compute_safety_scores', trial_arm_id=trial_arm_id, force=True, 
                        stdout=out, verbosity=1)
        
        self.message_user(request, f"Recomputed safety scores for {len(trial_arm_ids)} trial arm(s).")
    
    recompute_safety_scores.short_description = "Recompute safety scores for selected trial arms"
