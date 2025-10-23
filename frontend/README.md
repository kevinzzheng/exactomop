# EXACTOMOP Safety Scoring - Frontend Components

This directory contains React and Vue.js components for displaying safety scores in the EXACTOMOP system.

## Components

### SafetyScoreBadge (React & Vue)

A compact badge component that displays a safety score with color-coded risk levels.

**Features:**
- Color-coded based on risk level (Low/Moderate/Elevated/High)
- Interactive tooltip showing detailed metrics
- Configurable size (sm, md, lg)
- Accessible and responsive

**Usage (React):**
```jsx
import SafetyScoreBadge from './components/SafetyScoreBadge';

<SafetyScoreBadge 
  safetyScore={75.5} 
  web={25.0} 
  eair={0.35} 
  showTooltip={true}
  size="md"
/>
```

**Usage (Vue):**
```vue
<template>
  <SafetyScoreBadge 
    :safety-score="75.5" 
    :web="25.0" 
    :eair="0.35" 
    show-tooltip
    size="md"
  />
</template>

<script setup>
import SafetyScoreBadge from './components/SafetyScoreBadge.vue';
</script>
```

### TrialArmSafetyCard (React)

A comprehensive card component that displays all safety information for a trial arm.

**Features:**
- Displays trial arm information
- Shows safety score badge
- Visualizes adverse event breakdown by grade
- Shows enrollment and follow-up metrics
- Interactive and clickable

**Usage:**
```jsx
import TrialArmSafetyCard from './components/TrialArmSafetyCard';

<TrialArmSafetyCard 
  trialArm={trialArmData} 
  onSelect={(arm) => console.log('Selected:', arm)}
/>
```

## Risk Level Color Scheme

- **Low Risk** (Score ≥ 80): Green (#28a745)
- **Moderate Risk** (Score 60-79): Yellow (#ffc107)
- **Elevated Risk** (Score 40-59): Orange (#fd7e14)
- **High Risk** (Score < 40): Red (#dc3545)

## Installation

### For React Projects:

1. Copy the React components to your project
2. Install dependencies (if not already installed):
```bash
npm install react react-dom
```

3. Import and use the components

### For Vue Projects:

1. Copy the Vue components to your project
2. Install dependencies (if not already installed):
```bash
npm install vue@3
```

3. Import and use the components

## API Integration

These components work seamlessly with the EXACTOMOP REST API:

```javascript
// Fetch trial arms with safety metrics
fetch('/api/trial-arms/?status=ACTIVE')
  .then(res => res.json())
  .then(data => {
    // data contains trial arms with latest_safety_metrics
    // Pass to TrialArmSafetyCard or use SafetyScoreBadge
  });
```

## Customization

All components can be customized via CSS variables or by modifying the component styles directly.

### CSS Variables (recommended):

```css
:root {
  --safety-low-risk-color: #28a745;
  --safety-moderate-risk-color: #ffc107;
  --safety-elevated-risk-color: #fd7e14;
  --safety-high-risk-color: #dc3545;
}
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Accessibility

All components follow WCAG 2.1 Level AA guidelines:
- Proper color contrast ratios
- Keyboard navigation support
- Screen reader compatible
- ARIA labels where appropriate

## License

Apache 2.0 (same as EXACTOMOP project)

