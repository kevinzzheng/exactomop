/**
 * SafetyScoreBadge Component
 * 
 * Displays a safety score as a color-coded badge with tooltip.
 * Can be used in React applications.
 * 
 * Props:
 * - safetyScore: number (0-100)
 * - web: number (Weighted Event Burden)
 * - eair: number (Event-Adjusted Incidence Rate)
 * - showTooltip: boolean (default: true)
 * - size: 'sm' | 'md' | 'lg' (default: 'md')
 */

import React, { useState } from 'react';
import './SafetyScoreBadge.css';

const SafetyScoreBadge = ({ 
  safetyScore, 
  web, 
  eair, 
  showTooltip = true,
  size = 'md'
}) => {
  const [tooltipVisible, setTooltipVisible] = useState(false);

  // Determine risk category and color
  const getRiskCategory = (score) => {
    if (score >= 80) return { label: 'Low Risk', color: '#28a745', category: 'low' };
    if (score >= 60) return { label: 'Moderate Risk', color: '#ffc107', category: 'moderate' };
    if (score >= 40) return { label: 'Elevated Risk', color: '#fd7e14', category: 'elevated' };
    return { label: 'High Risk', color: '#dc3545', category: 'high' };
  };

  const risk = getRiskCategory(safetyScore);

  const badgeStyle = {
    backgroundColor: risk.color,
    color: '#fff',
    padding: size === 'sm' ? '4px 8px' : size === 'lg' ? '10px 16px' : '6px 12px',
    borderRadius: '4px',
    fontSize: size === 'sm' ? '12px' : size === 'lg' ? '16px' : '14px',
    fontWeight: 'bold',
    display: 'inline-block',
    cursor: showTooltip ? 'pointer' : 'default',
    position: 'relative',
    userSelect: 'none',
  };

  const tooltipStyle = {
    position: 'absolute',
    top: '120%',
    left: '50%',
    transform: 'translateX(-50%)',
    backgroundColor: '#333',
    color: '#fff',
    padding: '12px',
    borderRadius: '6px',
    fontSize: '13px',
    whiteSpace: 'nowrap',
    zIndex: 1000,
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    opacity: tooltipVisible ? 1 : 0,
    pointerEvents: 'none',
    transition: 'opacity 0.2s',
  };

  return (
    <div style={{ display: 'inline-block', position: 'relative' }}>
      <div
        className={`safety-score-badge ${risk.category}`}
        style={badgeStyle}
        onMouseEnter={() => showTooltip && setTooltipVisible(true)}
        onMouseLeave={() => showTooltip && setTooltipVisible(false)}
        title={!showTooltip ? `Safety Score: ${safetyScore.toFixed(1)} - ${risk.label}` : ''}
      >
        Safety: {safetyScore.toFixed(1)}
      </div>
      
      {showTooltip && tooltipVisible && (
        <div style={tooltipStyle} className="safety-score-tooltip">
          <div style={{ fontWeight: 'bold', marginBottom: '6px' }}>
            {risk.label}
          </div>
          <div style={{ fontSize: '12px', lineHeight: '1.4' }}>
            <div>Safety Score: <strong>{safetyScore.toFixed(2)}</strong></div>
            <div>WEB: <strong>{web.toFixed(2)}</strong></div>
            {eair !== null && eair !== undefined && (
              <div>EAIR: <strong>{eair.toFixed(4)}</strong></div>
            )}
          </div>
          <div style={{ 
            marginTop: '8px', 
            paddingTop: '8px', 
            borderTop: '1px solid rgba(255,255,255,0.2)',
            fontSize: '11px',
            color: '#ccc'
          }}>
            Higher scores indicate safer profiles
          </div>
        </div>
      )}
    </div>
  );
};

export default SafetyScoreBadge;

