from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("omop.api_urls")),
    path("", include("omop.urls")),
]
