"""
Django REST Framework serializers for EXACTOMOP Safety Scoring
"""

from rest_framework import serializers
from .models import Person
from .models_safety import TrialArm, AdverseEvent, TrialArmSafetyMetrics


class AdverseEventSerializer(serializers.ModelSerializer):
    """Serializer for adverse events."""
    
    class Meta:
        model = AdverseEvent
        fields = [
            'adverse_event_id', 'person', 'trial_arm', 'event_name', 
            'event_description', 'event_date', 'onset_date', 'resolution_date',
            'grade', 'serious', 'expected', 'relationship_to_treatment',
            'outcome', 'action_taken', 'reported_to_sponsor', 'reported_to_irb',
            'reported_to_fda', 'created_at', 'updated_at'
        ]
        read_only_fields = ['adverse_event_id', 'created_at', 'updated_at']


class TrialArmSafetyMetricsSerializer(serializers.ModelSerializer):
    """Serializer for trial arm safety metrics."""
    
    # Add formatted/computed fields
    safety_score_display = serializers.SerializerMethodField()
    web_display = serializers.SerializerMethodField()
    eair_display = serializers.SerializerMethodField()
    safety_category = serializers.SerializerMethodField()
    
    class Meta:
        model = TrialArmSafetyMetrics
        fields = [
            'safety_metrics_id', 'trial_arm', 'computation_date', 'data_cut_date',
            'analysis_period_start', 'analysis_period_end', 'person_years', 'n_patients',
            'e1_2_count', 'e3_4_count', 'e5_count', 'total_ae_count', 'patients_with_any_ae',
            'eair', 'eair_display', 'web', 'web_display', 'safety_score', 'safety_score_display',
            'safety_category', 'web_threshold_h', 'created_at', 'updated_at'
        ]
        read_only_fields = ['safety_metrics_id', 'computation_date', 'created_at', 'updated_at']
    
    def get_safety_score_display(self, obj):
        """Format safety score for display."""
        return f"{float(obj.safety_score):.2f}"
    
    def get_web_display(self, obj):
        """Format WEB for display."""
        return f"{float(obj.web):.2f}"
    
    def get_eair_display(self, obj):
        """Format EAIR for display."""
        if obj.eair:
            return f"{float(obj.eair):.4f}"
        return "N/A"
    
    def get_safety_category(self, obj):
        """Categorize safety score into risk levels."""
        score = float(obj.safety_score)
        if score >= 80:
            return "LOW_RISK"
        elif score >= 60:
            return "MODERATE_RISK"
        elif score >= 40:
            return "ELEVATED_RISK"
        else:
            return "HIGH_RISK"


class TrialArmSerializer(serializers.ModelSerializer):
    """Serializer for trial arms with embedded safety metrics."""
    
    # Embed latest safety metrics
    latest_safety_metrics = serializers.SerializerMethodField()
    safety_score = serializers.SerializerMethodField()
    web = serializers.SerializerMethodField()
    eair = serializers.SerializerMethodField()
    safety_category = serializers.SerializerMethodField()
    
    class Meta:
        model = TrialArm
        fields = [
            'trial_arm_id', 'clinical_trial', 'nct_number', 'arm_name', 'arm_code',
            'arm_type', 'intervention_description', 'status', 'enrollment_start_date',
            'enrollment_end_date', 'last_data_cut', 'n_patients', 'follow_up_months',
            'latest_safety_metrics', 'safety_score', 'web', 'eair', 'safety_category',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['trial_arm_id', 'created_at', 'updated_at']
    
    def get_latest_safety_metrics(self, obj):
        """Get the most recent safety metrics for this trial arm."""
        latest_metrics = obj.safety_metrics.order_by('-data_cut_date').first()
        if latest_metrics:
            return TrialArmSafetyMetricsSerializer(latest_metrics).data
        return None
    
    def get_safety_score(self, obj):
        """Get safety score from latest metrics."""
        latest_metrics = obj.safety_metrics.order_by('-data_cut_date').first()
        if latest_metrics:
            return float(latest_metrics.safety_score)
        return None
    
    def get_web(self, obj):
        """Get WEB from latest metrics."""
        latest_metrics = obj.safety_metrics.order_by('-data_cut_date').first()
        if latest_metrics:
            return float(latest_metrics.web)
        return None
    
    def get_eair(self, obj):
        """Get EAIR from latest metrics."""
        latest_metrics = obj.safety_metrics.order_by('-data_cut_date').first()
        if latest_metrics and latest_metrics.eair:
            return float(latest_metrics.eair)
        return None
    
    def get_safety_category(self, obj):
        """Get safety risk category."""
        latest_metrics = obj.safety_metrics.order_by('-data_cut_date').first()
        if latest_metrics:
            score = float(latest_metrics.safety_score)
            if score >= 80:
                return "LOW_RISK"
            elif score >= 60:
                return "MODERATE_RISK"
            elif score >= 40:
                return "ELEVATED_RISK"
            else:
                return "HIGH_RISK"
        return None


class TrialMatchingResponseSerializer(serializers.Serializer):
    """Serializer for trial matching API response with safety scoring."""
    
    trial_arm = TrialArmSerializer()
    match_score = serializers.FloatField(required=False)
    match_reasons = serializers.ListField(child=serializers.CharField(), required=False)
    safety_score = serializers.FloatField(allow_null=True)
    safety_category = serializers.CharField(allow_null=True)
    web = serializers.FloatField(allow_null=True)
    eair = serializers.FloatField(allow_null=True)
    recommended = serializers.BooleanField(required=False)

