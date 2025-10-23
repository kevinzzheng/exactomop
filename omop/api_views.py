"""
API Views for EXACTOMOP Safety Scoring
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Prefetch
from django.utils import timezone

from .models_safety import TrialArm, AdverseEvent, TrialArmSafetyMetrics
from .serializers import (
    TrialArmSerializer, AdverseEventSerializer, 
    TrialArmSafetyMetricsSerializer, TrialMatchingResponseSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for API results."""
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class TrialArmViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trial Arms with safety metrics.
    
    Endpoints:
    - GET /api/trial-arms/ - List all trial arms
    - GET /api/trial-arms/{id}/ - Get specific trial arm
    - GET /api/trial-arms/{id}/safety-metrics/ - Get all safety metrics for an arm
    - GET /api/trial-arms/{id}/adverse-events/ - Get all adverse events for an arm
    """
    queryset = TrialArm.objects.all().prefetch_related('safety_metrics')
    serializer_class = TrialArmSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Filter trial arms by query parameters."""
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by NCT number
        nct_number = self.request.query_params.get('nct_number', None)
        if nct_number:
            queryset = queryset.filter(nct_number=nct_number)
        
        # Filter by minimum safety score
        min_safety_score = self.request.query_params.get('min_safety_score', None)
        if min_safety_score:
            # Get trial arms with latest safety score >= threshold
            trial_arm_ids = []
            for arm in queryset:
                latest = arm.safety_metrics.order_by('-data_cut_date').first()
                if latest and float(latest.safety_score) >= float(min_safety_score):
                    trial_arm_ids.append(arm.trial_arm_id)
            queryset = queryset.filter(trial_arm_id__in=trial_arm_ids)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def safety_metrics(self, request, pk=None):
        """Get all safety metrics for a trial arm."""
        trial_arm = self.get_object()
        metrics = trial_arm.safety_metrics.all().order_by('-data_cut_date')
        serializer = TrialArmSafetyMetricsSerializer(metrics, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def adverse_events(self, request, pk=None):
        """Get all adverse events for a trial arm."""
        trial_arm = self.get_object()
        events = AdverseEvent.objects.filter(trial_arm=trial_arm).order_by('-event_date')
        serializer = AdverseEventSerializer(events, many=True)
        return Response(serializer.data)


class AdverseEventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Adverse Events.
    
    Endpoints:
    - GET /api/adverse-events/ - List all adverse events
    - POST /api/adverse-events/ - Create new adverse event
    - GET /api/adverse-events/{id}/ - Get specific adverse event
    - PUT /api/adverse-events/{id}/ - Update adverse event
    - DELETE /api/adverse-events/{id}/ - Delete adverse event
    """
    queryset = AdverseEvent.objects.all().select_related('person', 'trial_arm')
    serializer_class = AdverseEventSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Filter adverse events by query parameters."""
        queryset = super().get_queryset()
        
        # Filter by grade
        grade = self.request.query_params.get('grade', None)
        if grade:
            queryset = queryset.filter(grade=int(grade))
        
        # Filter by serious
        serious = self.request.query_params.get('serious', None)
        if serious is not None:
            queryset = queryset.filter(serious=(serious.lower() == 'true'))
        
        # Filter by trial arm
        trial_arm_id = self.request.query_params.get('trial_arm_id', None)
        if trial_arm_id:
            queryset = queryset.filter(trial_arm_id=int(trial_arm_id))
        
        # Filter by person
        person_id = self.request.query_params.get('person_id', None)
        if person_id:
            queryset = queryset.filter(person_id=int(person_id))
        
        return queryset


class TrialArmSafetyMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Trial Arm Safety Metrics (read-only).
    
    Metrics are computed via the compute_safety_scores management command.
    
    Endpoints:
    - GET /api/safety-metrics/ - List all safety metrics
    - GET /api/safety-metrics/{id}/ - Get specific safety metric
    """
    queryset = TrialArmSafetyMetrics.objects.all().select_related('trial_arm')
    serializer_class = TrialArmSafetyMetricsSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Filter safety metrics by query parameters."""
        queryset = super().get_queryset()
        
        # Filter by trial arm
        trial_arm_id = self.request.query_params.get('trial_arm_id', None)
        if trial_arm_id:
            queryset = queryset.filter(trial_arm_id=int(trial_arm_id))
        
        # Filter by minimum safety score
        min_safety_score = self.request.query_params.get('min_safety_score', None)
        if min_safety_score:
            queryset = queryset.filter(safety_score__gte=float(min_safety_score))
        
        # Filter by data cut date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(data_cut_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(data_cut_date__lte=end_date)
        
        return queryset


@api_view(['POST', 'GET'])
def trial_matching(request):
    """
    Trial matching endpoint with safety scoring integration.
    
    POST /api/trial-matching/ - Find matching trials for a patient
    GET /api/trial-matching/ - Get available trials with safety scores
    
    Query Parameters:
    - status: Filter by trial arm status (ACTIVE, COMPLETED, etc.)
    - min_safety_score: Minimum safety score threshold
    - max_results: Maximum number of results to return
    - include_safety_details: Include detailed safety metrics (default: true)
    
    POST Body (for patient matching):
    {
        "person_id": 123,
        "diagnosis": "Breast Cancer",
        "stage": "III",
        "biomarkers": {...},
        "prior_therapies": [...]
    }
    
    Response:
    [
        {
            "trial_arm": {...},
            "match_score": 0.85,
            "match_reasons": ["Biomarker match", "Stage appropriate"],
            "safety_score": 75.5,
            "safety_category": "MODERATE_RISK",
            "web": 25.0,
            "eair": 0.35,
            "recommended": true
        }
    ]
    """
    if request.method == 'POST':
        # Patient-specific matching
        person_id = request.data.get('person_id')
        diagnosis = request.data.get('diagnosis')
        min_safety_score = request.data.get('min_safety_score', 0)
        
        # Query active trial arms
        trial_arms = TrialArm.objects.filter(
            status__in=['ACTIVE', 'ENDED']
        ).prefetch_related('safety_metrics')
        
        # Filter by minimum safety score if specified
        if min_safety_score > 0:
            trial_arm_ids = []
            for arm in trial_arms:
                latest = arm.safety_metrics.order_by('-data_cut_date').first()
                if latest and float(latest.safety_score) >= min_safety_score:
                    trial_arm_ids.append(arm.trial_arm_id)
            trial_arms = trial_arms.filter(trial_arm_id__in=trial_arm_ids)
        
        # Build response with safety scoring
        results = []
        for arm in trial_arms:
            latest_metrics = arm.safety_metrics.order_by('-data_cut_date').first()
            
            # Calculate match score (simplified - extend with real matching logic)
            match_score = 0.8  # Placeholder
            match_reasons = ["Active trial", "Safety profile available"]
            
            result = {
                'trial_arm': TrialArmSerializer(arm).data,
                'match_score': match_score,
                'match_reasons': match_reasons,
                'safety_score': float(latest_metrics.safety_score) if latest_metrics else None,
                'safety_category': _get_safety_category(latest_metrics) if latest_metrics else None,
                'web': float(latest_metrics.web) if latest_metrics else None,
                'eair': float(latest_metrics.eair) if latest_metrics and latest_metrics.eair else None,
                'recommended': (
                    latest_metrics and 
                    float(latest_metrics.safety_score) >= 60 and 
                    match_score >= 0.7
                )
            }
            results.append(result)
        
        # Sort by match score and safety score
        results.sort(
            key=lambda x: (x['match_score'] if x['match_score'] else 0, 
                          x['safety_score'] if x['safety_score'] else 0),
            reverse=True
        )
        
        # Limit results
        max_results = int(request.data.get('max_results', 10))
        results = results[:max_results]
        
        return Response(results)
    
    else:
        # GET - List all trials with safety scores
        status_filter = request.query_params.get('status', 'ACTIVE')
        min_safety_score = float(request.query_params.get('min_safety_score', 0))
        max_results = int(request.query_params.get('max_results', 25))
        
        trial_arms = TrialArm.objects.filter(
            status=status_filter
        ).prefetch_related('safety_metrics')
        
        results = []
        for arm in trial_arms:
            latest_metrics = arm.safety_metrics.order_by('-data_cut_date').first()
            
            # Skip if no safety metrics or below threshold
            if not latest_metrics:
                continue
            if float(latest_metrics.safety_score) < min_safety_score:
                continue
            
            result = {
                'trial_arm': TrialArmSerializer(arm).data,
                'safety_score': float(latest_metrics.safety_score),
                'safety_category': _get_safety_category(latest_metrics),
                'web': float(latest_metrics.web),
                'eair': float(latest_metrics.eair) if latest_metrics.eair else None,
            }
            results.append(result)
        
        # Sort by safety score
        results.sort(key=lambda x: x['safety_score'], reverse=True)
        results = results[:max_results]
        
        return Response(results)


def _get_safety_category(metrics):
    """Helper function to categorize safety score."""
    if not metrics:
        return None
    score = float(metrics.safety_score)
    if score >= 80:
        return "LOW_RISK"
    elif score >= 60:
        return "MODERATE_RISK"
    elif score >= 40:
        return "ELEVATED_RISK"
    else:
        return "HIGH_RISK"

