<!--
SafetyScoreBadge Component (Vue 3)

Displays a safety score as a color-coded badge with tooltip.
Can be used in Vue applications.

Props:
- safetyScore: number (0-100)
- web: number (Weighted Event Burden)
- eair: number (Event-Adjusted Incidence Rate)
- showTooltip: boolean (default: true)
- size: 'sm' | 'md' | 'lg' (default: 'md')

Usage:
<SafetyScoreBadge 
  :safety-score="75.5" 
  :web="25.0" 
  :eair="0.35" 
/>
-->

<template>
  <div class="safety-score-badge-wrapper">
    <div
      :class="['safety-score-badge', riskCategory.category, size]"
      :style="{ backgroundColor: riskCategory.color }"
      @mouseenter="showTooltip && (tooltipVisible = true)"
      @mouseleave="showTooltip && (tooltipVisible = false)"
      :title="!showTooltip ? tooltipText : ''"
    >
      Safety: {{ safetyScore.toFixed(1) }}
    </div>
    
    <transition name="fade">
      <div v-if="showTooltip && tooltipVisible" class="safety-score-tooltip">
        <div class="tooltip-header">
          {{ riskCategory.label }}
        </div>
        <div class="tooltip-content">
          <div class="metric">
            <span class="label">Safety Score:</span>
            <strong>{{ safetyScore.toFixed(2) }}</strong>
          </div>
          <div class="metric">
            <span class="label">WEB:</span>
            <strong>{{ web.toFixed(2) }}</strong>
          </div>
          <div v-if="eair !== null && eair !== undefined" class="metric">
            <span class="label">EAIR:</span>
            <strong>{{ eair.toFixed(4) }}</strong>
          </div>
        </div>
        <div class="tooltip-footer">
          Higher scores indicate safer profiles
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  safetyScore: {
    type: Number,
    required: true,
    validator: (val) => val >= 0 && val <= 100
  },
  web: {
    type: Number,
    required: true
  },
  eair: {
    type: Number,
    default: null
  },
  showTooltip: {
    type: Boolean,
    default: true
  },
  size: {
    type: String,
    default: 'md',
    validator: (val) => ['sm', 'md', 'lg'].includes(val)
  }
});

const tooltipVisible = ref(false);

const riskCategory = computed(() => {
  const score = props.safetyScore;
  if (score >= 80) return { label: 'Low Risk', color: '#28a745', category: 'low' };
  if (score >= 60) return { label: 'Moderate Risk', color: '#ffc107', category: 'moderate' };
  if (score >= 40) return { label: 'Elevated Risk', color: '#fd7e14', category: 'elevated' };
  return { label: 'High Risk', color: '#dc3545', category: 'high' };
});

const tooltipText = computed(() => 
  `Safety Score: ${props.safetyScore.toFixed(1)} - ${riskCategory.value.label}`
);
</script>

<style scoped>
.safety-score-badge-wrapper {
  display: inline-block;
  position: relative;
}

.safety-score-badge {
  color: #fff;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
  display: inline-block;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;
}

.safety-score-badge.sm {
  padding: 4px 8px;
  font-size: 12px;
}

.safety-score-badge.lg {
  padding: 10px 16px;
  font-size: 16px;
}

.safety-score-badge:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.safety-score-badge.low {
  background-color: #28a745;
}

.safety-score-badge.moderate {
  background-color: #ffc107;
}

.safety-score-badge.elevated {
  background-color: #fd7e14;
}

.safety-score-badge.high {
  background-color: #dc3545;
}

.safety-score-tooltip {
  position: absolute;
  top: 120%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #333;
  color: #fff;
  padding: 12px;
  border-radius: 6px;
  font-size: 13px;
  white-space: nowrap;
  z-index: 1000;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.tooltip-header {
  font-weight: bold;
  margin-bottom: 6px;
}

.tooltip-content {
  font-size: 12px;
  line-height: 1.4;
}

.metric {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.metric .label {
  color: #ccc;
}

.tooltip-footer {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 11px;
  color: #ccc;
  text-align: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .safety-score-tooltip {
    font-size: 11px;
    padding: 10px;
  }
}
</style>

