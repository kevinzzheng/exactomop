from django.urls import path
from . import views
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("patients/", views.PersonListView.as_view(), name="person-list"),
    path("person/<int:pk>/", views.PersonDetailView.as_view(), name="person-detail"),
    path("<str:slug>/", lambda r, slug: views.GenericListView.as_view(model=views.MODEL_MAP[slug])(r), name="generic-list"),
    path("<str:slug>/<int:pk>/", lambda r, slug, pk: views.GenericDetailView.as_view(model=views.MODEL_MAP[slug])(r, pk=pk), name="generic-detail"),
]
