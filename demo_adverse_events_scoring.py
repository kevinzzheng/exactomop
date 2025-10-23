#!/usr/bin/env python3
"""
Comprehensive Demo Script for Adverse Events Safety Scoring Feature
================================================================

This script demonstrates the complete adverse events safety scoring functionality
using the synthetic dataset. It shows data loading, safety score computation,
analysis, and API usage.

Usage:
    python3 demo_adverse_events_scoring.py

Requirements:
    - Django project setup with migrations applied
    - Synthetic data fixtures available
    - Dependencies installed (requirements.txt)
"""

import os
import sys
import django
from django.core.management import call_command
from django.core.management.base import CommandError
import requests
import json
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omop_site.settings')
django.setup()

from omop.models_safety import TrialArm, AdverseEvent, TrialArmSafetyMetrics
from omop.models import Person


class AdverseEventsScoringDemo:
    """Comprehensive demo of the adverse events safety scoring feature."""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.server_process = None
        
    def print_header(self, title):
        """Print a formatted header."""
        print("\n" + "=" * 80)
        print(f"🎯 {title}")
        print("=" * 80)
        
    def print_section(self, title):
        """Print a formatted section header."""
        print(f"\n📊 {title}")
        print("-" * 60)
        
    def step_1_setup_data(self):
        """Step 1: Load synthetic data and compute safety scores."""
        self.print_header("STEP 1: DATA SETUP AND SAFETY SCORE COMPUTATION")
        
        try:
            print("Loading synthetic breast cancer patients...")
            call_command('load_synthetic_breast_cancer_data')
            print("✅ Breast cancer patients loaded successfully")
            
            print("\nLoading synthetic adverse events and computing safety scores...")
            call_command('load_synthetic_adverse_events', '--clear', '--compute-scores')
            print("✅ Adverse events loaded and safety scores computed successfully")
            
        except CommandError as e:
            print(f"❌ Error loading data: {e}")
            return False
            
        return True
    
    def step_2_verify_data(self):
        """Step 2: Verify data loading and show summary."""
        self.print_header("STEP 2: DATA VERIFICATION AND SUMMARY")
        
        # Count data
        trial_arms = TrialArm.objects.count()
        adverse_events = AdverseEvent.objects.count()
        safety_metrics = TrialArmSafetyMetrics.objects.count()
        
        print(f"📈 Data Summary:")
        print(f"   Trial Arms: {trial_arms}")
        print(f"   Adverse Events: {adverse_events}")
        print(f"   Safety Metrics: {safety_metrics}")
        
        # Show trial arms
        self.print_section("Trial Arms Overview")
        for arm in TrialArm.objects.all().order_by('trial_arm_id'):
            try:
                metrics = arm.safety_metrics.latest('computation_date')
                print(f"{arm.trial_arm_id}: {arm.arm_name}")
                print(f"   NCT: {arm.nct_number} | Patients: {arm.n_patients} | Status: {arm.status}")
                print(f"   Safety Score: {metrics.safety_score:.2f} | WEB: {metrics.web} | EAIR: {metrics.eair:.4f}")
                print(f"   Grade Distribution: G1-2: {metrics.e1_2_count}, G3-4: {metrics.e3_4_count}, G5: {metrics.e5_count}")
                print()
            except TrialArmSafetyMetrics.DoesNotExist:
                print(f"{arm.trial_arm_id}: {arm.arm_name} - No safety metrics computed")
                print()
    
    def step_3_analyze_safety_scores(self):
        """Step 3: Analyze safety scores and risk categories."""
        self.print_header("STEP 3: SAFETY SCORE ANALYSIS")
        
        # Get all safety metrics
        metrics = TrialArmSafetyMetrics.objects.all().order_by('safety_score')
        
        self.print_section("Safety Score Ranking (Lowest = Highest Risk)")
        for i, metric in enumerate(metrics, 1):
            arm = metric.trial_arm
            print(f"{i}. {arm.arm_name}")
            print(f"   Safety Score: {metric.safety_score:.2f} ({metric.safety_category})")
            print(f"   WEB: {metric.web} | EAIR: {metric.eair:.4f}")
            print(f"   Patients with AEs: {metric.patients_with_any_ae}/{metric.n_patients}")
            print()
        
        # Risk category distribution
        self.print_section("Risk Category Distribution")
        categories = {}
        for metric in metrics:
            category = metric.safety_category
            categories[category] = categories.get(category, 0) + 1
        
        for category, count in categories.items():
            print(f"   {category}: {count} trial arms")
    
    def step_4_adverse_events_analysis(self):
        """Step 4: Analyze adverse events patterns."""
        self.print_header("STEP 4: ADVERSE EVENTS ANALYSIS")
        
        # Grade distribution
        self.print_section("Grade Distribution")
        for grade in range(1, 6):
            count = AdverseEvent.objects.filter(grade=grade).count()
            if count > 0:
                print(f"   Grade {grade}: {count} events")
        
        # Serious adverse events
        sae_count = AdverseEvent.objects.filter(serious=True).count()
        print(f"\n   Serious Adverse Events (SAEs): {sae_count}")
        
        # Events by trial arm
        self.print_section("Adverse Events by Trial Arm")
        for arm in TrialArm.objects.all().order_by('trial_arm_id'):
            ae_count = AdverseEvent.objects.filter(trial_arm=arm).count()
            if ae_count > 0:
                print(f"{arm.arm_name}: {ae_count} adverse events")
                # Show sample events
                sample_events = AdverseEvent.objects.filter(trial_arm=arm)[:3]
                for ae in sample_events:
                    print(f"  - {ae.event_name} (Grade {ae.grade}) - {ae.outcome}")
            else:
                print(f"{arm.arm_name}: No adverse events")
            print()
    
    def step_5_api_demonstration(self):
        """Step 5: Demonstrate API endpoints."""
        self.print_header("STEP 5: API ENDPOINT DEMONSTRATION")
        
        try:
            # Test if server is running
            response = requests.get(f"{self.base_url}/api/trial-arms/", timeout=5)
            if response.status_code != 200:
                print("❌ API server not accessible. Please start with: python manage.py runserver")
                return False
                
        except requests.exceptions.RequestException:
            print("❌ API server not accessible. Please start with: python manage.py runserver")
            return False
        
        # API queries
        self.print_section("API Query Examples")
        
        # 1. Get all trial arms
        print("1. All Trial Arms:")
        response = requests.get(f"{self.base_url}/api/trial-arms/")
        data = response.json()
        for arm in data['results']:
            print(f"   {arm['arm_name']}: Score {arm['safety_score']:.2f} ({arm['safety_category']})")
        
        # 2. High-risk trial arms
        print("\n2. High-Risk Trial Arms (Score < 50):")
        response = requests.get(f"{self.base_url}/api/trial-arms/?max_safety_score=50")
        data = response.json()
        for arm in data['results']:
            print(f"   {arm['arm_name']}: Score {arm['safety_score']:.2f}")
        
        # 3. Adverse events
        print("\n3. Sample Adverse Events:")
        response = requests.get(f"{self.base_url}/api/adverse-events/")
        data = response.json()
        print(f"   Total AEs: {data['count']}")
        for ae in data['results'][:5]:
            print(f"   - {ae['event_name']} (Grade {ae['grade']}) - {ae['outcome']}")
        
        return True
    
    def step_6_safety_scoring_methodology(self):
        """Step 6: Explain safety scoring methodology."""
        self.print_header("STEP 6: SAFETY SCORING METHODOLOGY")
        
        print("""
The safety scoring system uses three key metrics:

1. WEB (Weighted Event Burden):
   - WEB = 1 × (Grade 1-2 events) + 10 × (Grade 3-4 events) + 100 × (Grade 5 events)
   - Higher WEB = Higher risk

2. EAIR (Event-Adjusted Incidence Rate):
   - EAIR = (Patients with events) / (Person-years of follow-up)
   - Higher EAIR = Higher event frequency

3. Safety Score:
   - Safety Score = 100 / (1 + WEB/H)
   - Where H = WEB threshold (default: 15.0)
   - Higher score = Safer (0-100 scale)

Risk Categories:
- LOW_RISK: Score ≥ 70
- ELEVATED_RISK: Score 50-69
- HIGH_RISK: Score < 50
        """)
        
        # Show calculation example
        self.print_section("Calculation Example")
        arm = TrialArm.objects.get(trial_arm_id=1001)  # AC-T Chemotherapy
        metrics = arm.safety_metrics.latest('computation_date')
        
        print(f"Trial Arm: {arm.arm_name}")
        print(f"Patients: {metrics.n_patients}")
        print(f"Person-years: {metrics.person_years}")
        print(f"Grade 1-2 events: {metrics.e1_2_count}")
        print(f"Grade 3-4 events: {metrics.e3_4_count}")
        print(f"Grade 5 events: {metrics.e5_count}")
        print()
        print("Calculations:")
        print(f"WEB = 1×{metrics.e1_2_count} + 10×{metrics.e3_4_count} + 100×{metrics.e5_count} = {metrics.web}")
        print(f"EAIR = {metrics.patients_with_any_ae} / {metrics.person_years} = {metrics.eair:.4f}")
        print(f"Safety Score = 100 / (1 + {metrics.web}/15) = {metrics.safety_score:.2f}")
    
    def step_7_frontend_components(self):
        """Step 7: Show frontend component usage."""
        self.print_header("STEP 7: FRONTEND COMPONENT INTEGRATION")
        
        print("""
The system includes React and Vue components for displaying safety scores:

React Components:
- SafetyScoreBadge: Displays safety score with color coding
- TrialArmSafetyCard: Full safety information card

Vue Components:
- SafetyScoreBadge.vue: Vue version of safety badge

Example Usage:
```jsx
// React
import { SafetyScoreBadge, TrialArmSafetyCard } from './components';

<SafetyScoreBadge 
  safetyScore={trialArm.safety_score}
  web={trialArm.web}
  eair={trialArm.eair}
/>

<TrialArmSafetyCard trialArm={trialArm} />
```

```vue
<!-- Vue -->
<SafetyScoreBadge 
  :safety-score="trialArm.safety_score"
  :web="trialArm.web"
  :eair="trialArm.eair"
/>
```
        """)
    
    def run_complete_demo(self):
        """Run the complete demonstration."""
        print("🚀 ADVERSE EVENTS SAFETY SCORING DEMO")
        print("=" * 80)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all steps
        steps = [
            self.step_1_setup_data,
            self.step_2_verify_data,
            self.step_3_analyze_safety_scores,
            self.step_4_adverse_events_analysis,
            self.step_5_api_demonstration,
            self.step_6_safety_scoring_methodology,
            self.step_7_frontend_components,
        ]
        
        for i, step in enumerate(steps, 1):
            try:
                result = step()
                if result is False:
                    print(f"\n❌ Step {i} failed. Stopping demo.")
                    return False
            except Exception as e:
                print(f"\n❌ Step {i} failed with error: {e}")
                return False
        
        self.print_header("DEMO COMPLETED SUCCESSFULLY")
        print("✅ All steps completed successfully!")
        print("\nNext steps:")
        print("1. Explore the Django admin interface: http://localhost:8000/admin/")
        print("2. Test API endpoints: http://localhost:8000/api/")
        print("3. Integrate frontend components in your application")
        print("4. Customize safety scoring parameters in settings.py")
        
        return True


def main():
    """Main function to run the demo."""
    demo = AdverseEventsScoringDemo()
    
    try:
        success = demo.run_complete_demo()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
