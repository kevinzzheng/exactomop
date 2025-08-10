from django.db import models

class Location(models.Model):
    location_id = models.BigAutoField(primary_key=True)
    address_1 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=20, blank=True)
    country_concept_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "location"
        indexes = [models.Index(fields=["zip"])]
    def __str__(self):
        return f"{self.address_1} {self.city} {self.zip}".strip()

class Person(models.Model):
    person_id = models.BigAutoField(primary_key=True)
    gender_concept_id = models.IntegerField()
    year_of_birth = models.IntegerField(null=True, blank=True)
    month_of_birth = models.IntegerField(null=True, blank=True)
    day_of_birth = models.IntegerField(null=True, blank=True)
    race_concept_id = models.IntegerField(null=True, blank=True)
    ethnicity_concept_id = models.IntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        db_table = "person"
        indexes = [models.Index(fields=["gender_concept_id"])]
    def __str__(self):
        return f"Person {self.person_id}"

class ConditionOccurrence(models.Model):
    condition_occurrence_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    condition_concept_id = models.IntegerField()
    condition_start_date = models.DateField()
    condition_end_date = models.DateField(null=True, blank=True)
    condition_type_concept_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "condition_occurrence"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["condition_concept_id"]),
            models.Index(fields=["condition_start_date"]),
        ]
    def __str__(self):
        return f"Condition {self.condition_occurrence_id} for Person {self.person.person_id}"

class Measurement(models.Model):
    measurement_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    measurement_concept_id = models.IntegerField()
    measurement_date = models.DateField()
    value_as_number = models.FloatField(null=True, blank=True)
    value_as_concept_id = models.IntegerField(null=True, blank=True)
    unit_concept_id = models.IntegerField(null=True, blank=True)
    modifier_of_event_id = models.BigIntegerField(null=True, blank=True)
    modifier_of_field_concept_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "measurement"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["measurement_concept_id"]),
            models.Index(fields=["measurement_date"]),
        ]
    def __str__(self):
        return f"Measurement {self.measurement_id}"

class Observation(models.Model):
    observation_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    observation_concept_id = models.IntegerField()
    observation_date = models.DateField()
    value_as_number = models.FloatField(null=True, blank=True)
    value_as_string = models.CharField(max_length=255, blank=True)
    value_as_concept_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "observation"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["observation_concept_id"]),
            models.Index(fields=["observation_date"]),
        ]
    def __str__(self):
        return f"Observation {self.observation_id}"

class DrugExposure(models.Model):
    drug_exposure_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    drug_concept_id = models.IntegerField()
    drug_exposure_start_date = models.DateField()
    drug_exposure_end_date = models.DateField(null=True, blank=True)
    route_concept_id = models.IntegerField(null=True, blank=True)
    dose = models.FloatField(null=True, blank=True)
    dose_unit_concept_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "drug_exposure"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["drug_concept_id"]),
            models.Index(fields=["drug_exposure_start_date"]),
        ]
    def __str__(self):
        return f"DrugExposure {self.drug_exposure_id}"

class ProcedureOccurrence(models.Model):
    procedure_occurrence_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    procedure_concept_id = models.IntegerField()
    procedure_date = models.DateField()
    class Meta:
        db_table = "procedure_occurrence"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["procedure_concept_id"]),
            models.Index(fields=["procedure_date"]),
        ]
    def __str__(self):
        return f"Procedure {self.procedure_occurrence_id}"

class Episode(models.Model):
    episode_id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    episode_concept_id = models.IntegerField()
    episode_start_date = models.DateField()
    episode_end_date = models.DateField(null=True, blank=True)
    episode_number = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "episode"
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["episode_concept_id"]),
            models.Index(fields=["episode_start_date"]),
        ]
    def __str__(self):
        return f"Episode {self.episode_id}"

class EpisodeEvent(models.Model):
    episode_event_id = models.BigAutoField(primary_key=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    event_field_concept_id = models.IntegerField()
    event_id = models.BigIntegerField()
    class Meta:
        db_table = "episode_event"
        indexes = [
            models.Index(fields=["episode"]),
            models.Index(fields=["event_field_concept_id"]),
        ]
    def __str__(self):
        return f"EpisodeEvent {self.episode_event_id}"
