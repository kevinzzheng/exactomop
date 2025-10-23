/**
 * TrialArmSafetyCard Component
 * 
 * Displays comprehensive safety information for a trial arm.
 * Shows safety metrics, adverse event breakdown, and visualizations.
 * 
 * Props:
 * - trialArm: object (trial arm data with safety metrics)
 * - onSelect: function (callback when card is clicked)
 */

import React from 'react';
import SafetyScoreBadge from './SafetyScoreBadge';
import './TrialArmSafetyCard.css';

const TrialArmSafetyCard = ({ trialArm, onSelect }) => {
  const safetyMetrics = trialArm.latest_safety_metrics;
  
  if (!safetyMetrics) {
    return (
      <div className="trial-arm-safety-card no-data">
        <div className="card-header">
          <h3>{trialArm.arm_name}</h3>
          <span className="arm-code">{trialArm.arm_code}</span>
        </div>
        <div className="no-safety-data">
          <p>Safety data not yet available</p>
        </div>
      </div>
    );
  }

  const handleCardClick = () => {
    if (onSelect) {
      onSelect(trialArm);
    }
  };

  // Calculate percentages for adverse event visualization
  const totalPatients = safetyMetrics.n_patients;
  const ae1_2Percent = ((safetyMetrics.e1_2_count / totalPatients) * 100).toFixed(1);
  const ae3_4Percent = ((safetyMetrics.e3_4_count / totalPatients) * 100).toFixed(1);
  const ae5Percent = ((safetyMetrics.e5_count / totalPatients) * 100).toFixed(1);

  return (
    <div className="trial-arm-safety-card" onClick={handleCardClick}>
      <div className="card-header">
        <div>
          <h3>{trialArm.arm_name}</h3>
          <div className="arm-meta">
            <span className="arm-code">{trialArm.arm_code}</span>
            {trialArm.nct_number && (
              <span className="nct-number">{trialArm.nct_number}</span>
            )}
            <span className={`status-badge ${trialArm.status.toLowerCase()}`}>
              {trialArm.status}
            </span>
          </div>
        </div>
        <SafetyScoreBadge
          safetyScore={parseFloat(safetyMetrics.safety_score)}
          web={parseFloat(safetyMetrics.web)}
          eair={safetyMetrics.eair ? parseFloat(safetyMetrics.eair) : null}
          size="lg"
        />
      </div>

      <div className="card-body">
        <div className="metrics-grid">
          <div className="metric-item">
            <div className="metric-label">Patients Enrolled</div>
            <div className="metric-value">{safetyMetrics.n_patients}</div>
          </div>
          <div className="metric-item">
            <div className="metric-label">Person-Years</div>
            <div className="metric-value">{parseFloat(safetyMetrics.person_years).toFixed(1)}</div>
          </div>
          <div className="metric-item">
            <div className="metric-label">Data Cut Date</div>
            <div className="metric-value">{safetyMetrics.data_cut_date}</div>
          </div>
        </div>

        <div className="adverse-events-section">
          <h4>Adverse Events Profile</h4>
          <div className="ae-breakdown">
            <div className="ae-item grade-1-2">
              <div className="ae-header">
                <span className="ae-label">Grade 1-2 (Mild-Moderate)</span>
                <span className="ae-count">{safetyMetrics.e1_2_count} pts ({ae1_2Percent}%)</span>
              </div>
              <div className="ae-bar" style={{ width: `${ae1_2Percent}%` }}></div>
            </div>
            <div className="ae-item grade-3-4">
              <div className="ae-header">
                <span className="ae-label">Grade 3-4 (Severe)</span>
                <span className="ae-count">{safetyMetrics.e3_4_count} pts ({ae3_4Percent}%)</span>
              </div>
              <div className="ae-bar" style={{ width: `${ae3_4Percent}%` }}></div>
            </div>
            <div className="ae-item grade-5">
              <div className="ae-header">
                <span className="ae-label">Grade 5 (Fatal)</span>
                <span className="ae-count">{safetyMetrics.e5_count} pts ({ae5Percent}%)</span>
              </div>
              <div className="ae-bar" style={{ width: `${ae5Percent > 0 ? Math.max(ae5Percent, 5) : 0}%` }}></div>
            </div>
          </div>
        </div>

        <div className="safety-summary">
          <div className="summary-item">
            <span className="summary-label">Total AEs:</span>
            <span className="summary-value">{safetyMetrics.total_ae_count}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Patients with any AE:</span>
            <span className="summary-value">
              {safetyMetrics.patients_with_any_ae} 
              ({((safetyMetrics.patients_with_any_ae / totalPatients) * 100).toFixed(1)}%)
            </span>
          </div>
          <div className="summary-item">
            <span className="summary-label">WEB Score:</span>
            <span className="summary-value">{parseFloat(safetyMetrics.web).toFixed(2)}</span>
          </div>
        </div>
      </div>

      <div className="card-footer">
        <small>Last computed: {safetyMetrics.computation_date}</small>
      </div>
    </div>
  );
};

export default TrialArmSafetyCard;

