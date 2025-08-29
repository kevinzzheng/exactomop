from django.views.generic import ListView, DetailView, TemplateView
from .models import (
    Person, Location, ConditionOccurrence, Measurement, Observation,
    DrugExposure, ProcedureOccurrence, Episode, EpisodeEvent
)

class HomeView(TemplateView):
    template_name = "omop/home.html"

class PersonListView(ListView):
    model = Person
    paginate_by = 25
class PersonDetailView(DetailView):
    model = Person
class GenericListView(ListView):
    paginate_by = 25
class GenericDetailView(DetailView):
    pass
MODEL_MAP = {
    "person": Person,
    "location": Location,
    "condition": ConditionOccurrence,
    "measurement": Measurement,
    "observation": Observation,
    "drug": DrugExposure,
    "procedure": ProcedureOccurrence,
    "episode": Episode,
    "episodeevent": EpisodeEvent,
}
