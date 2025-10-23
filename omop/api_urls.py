"""
API URL Configuration for EXACTOMOP Safety Scoring
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    TrialArmViewSet,
    AdverseEventViewSet,
    TrialArmSafetyMetricsViewSet,
    trial_matching
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'trial-arms', TrialArmViewSet, basename='trial-arm')
router.register(r'adverse-events', AdverseEventViewSet, basename='adverse-event')
router.register(r'safety-metrics', TrialArmSafetyMetricsViewSet, basename='safety-metrics')

urlpatterns = [
    # Trial matching endpoint
    path('trial-matching/', trial_matching, name='trial-matching'),
    
    # Include router URLs
    path('', include(router.urls)),
]

