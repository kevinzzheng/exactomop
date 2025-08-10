from django.contrib import admin
from .models import (
    Person, Location, ConditionOccurrence, Measurement, Observation,
    DrugExposure, ProcedureOccurrence, Episode, EpisodeEvent
)
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("person_id", "gender_concept_id", "year_of_birth", "race_concept_id", "ethnicity_concept_id")
    search_fields = ("person_id",)
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("location_id", "zip", "city")
    search_fields = ("zip", "city")
@admin.register(ConditionOccurrence)
class ConditionOccurrenceAdmin(admin.ModelAdmin):
    list_display = ("condition_occurrence_id", "person", "condition_concept_id", "condition_start_date")
    search_fields = ("condition_occurrence_id",)
    list_filter = ("condition_start_date",)
@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("measurement_id", "person", "measurement_concept_id", "measurement_date", "value_as_number", "value_as_concept_id")
    search_fields = ("measurement_id",)
    list_filter = ("measurement_date",)
@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ("observation_id", "person", "observation_concept_id", "observation_date", "value_as_concept_id")
    list_filter = ("observation_date",)
@admin.register(DrugExposure)
class DrugExposureAdmin(admin.ModelAdmin):
    list_display = ("drug_exposure_id", "person", "drug_concept_id", "drug_exposure_start_date")
    list_filter = ("drug_exposure_start_date",)
@admin.register(ProcedureOccurrence)
class ProcedureOccurrenceAdmin(admin.ModelAdmin):
    list_display = ("procedure_occurrence_id", "person", "procedure_concept_id", "procedure_date")
    list_filter = ("procedure_date",)
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("episode_id", "person", "episode_concept_id", "episode_start_date", "episode_number")
@admin.register(EpisodeEvent)
class EpisodeEventAdmin(admin.ModelAdmin):
    list_display = ("episode_event_id", "episode", "event_field_concept_id", "event_id")
