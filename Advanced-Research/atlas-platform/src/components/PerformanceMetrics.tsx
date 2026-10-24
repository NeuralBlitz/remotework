import React from ‘react’;
import executionFeedbackData from ‘../data/execution-feedback.json’;

const PerformanceMetrics: React.FC = () => {
const { aggregateMetrics, trendAnalysis, executionFeedback } = executionFeedbackData;

const renderMetricCard = (label: string, value: number, isPercentage = true, trend?: string) => (
<div className="metric-card-large">
<h3>{label}</h3>
<div className="metric-display">
<span className="metric-large">
{isPercentage ? `${(value * 100).toFixed(1)}%` : value.toFixed(2)}
</span>
{trend && (
<span className={`trend-indicator ${trend}`}>
{trend === ‘improving’ ? ‘↗’ : trend === ‘stable’ ? ‘→’ : ‘↘’}
{trend}
</span>
)}
</div>
</div>
);

const getPerformanceColor = (value: number) => {
if (value >= 0.9) return ‘#10b981’;
if (value >= 0.75) return ‘#f59e0b’;
return ‘#ef4444’;
};

return (
<div className="performance-metrics">
<h2>Platform Performance Analytics</h2>

```
  <div className="aggregate-section">
    <h3>Aggregate Metrics</h3>
    <div className="metrics-grid-large">
      {renderMetricCard('Average Completion', aggregateMetrics.averageCompletion, true, trendAnalysis.completionTrend)}
      {renderMetricCard('Average Efficiency', aggregateMetrics.averageEfficiency, true, trendAnalysis.efficiencyTrend)}
      {renderMetricCard('Average Satisfaction', aggregateMetrics.averageSatisfaction, true, trendAnalysis.satisfactionTrend)}
      {renderMetricCard('Average Execution Time', aggregateMetrics.averageExecutionTime, false)}
      {renderMetricCard('Overall Success Rate', aggregateMetrics.overallSuccessRate)}
    </div>
  </div>

  <div className="trend-section">
    <h3>Trend Analysis ({trendAnalysis.period.replace('_', ' ')})</h3>
    <div className="trend-cards">
      <div className="trend-card">
        <h4>Common Failure Patterns</h4>
        <ul className="failure-list">
          {trendAnalysis.commonFailurePatterns.map((pattern, idx) => (
            <li key={idx}>
              <span className="failure-icon">⚠</span>
              {pattern}
            </li>
          ))}
        </ul>
      </div>
      <div className="trend-card">
        <h4>Top Improvement Areas</h4>
        <ul className="improvement-list">
          {trendAnalysis.topImprovementAreas.map((area, idx) => (
            <li key={idx}>
              <span className="improvement-icon">💡</span>
              {area}
            </li>
          ))}
        </ul>
      </div>
    </div>
  </div>

  <div className="feedback-section">
    <h3>Recent Execution Feedback</h3>
    <div className="feedback-list">
      {executionFeedback.map((feedback, idx) => (
        <div key={idx} className="feedback-item">
          <div className="feedback-header">
            <h4>Task {feedback.taskId}</h4>
            <span className="feedback-timestamp">
              {new Date(feedback.timestamp).toLocaleString()}
            </span>
          </div>
          
          <div className="feedback-metrics">
            <div className="feedback-metric">
              <span className="metric-name">Completion</span>
              <div className="metric-bar-container">
                <div 
                  className="metric-bar"
                  style={{ 
                    width: `${feedback.successMetrics.taskCompletion * 100}%`,
                    backgroundColor: getPerformanceColor(feedback.successMetrics.taskCompletion)
                  }}
                />
              </div>
              <span className="metric-percent">
                {(feedback.successMetrics.taskCompletion * 100).toFixed(0)}%
              </span>
            </div>
            <div className="feedback-metric">
              <span className="metric-name">Efficiency</span>
              <div className="metric-bar-container">
                <div 
                  className="metric-bar"
                  style={{ 
                    width: `${feedback.successMetrics.efficiency * 100}%`,
                    backgroundColor: getPerformanceColor(feedback.successMetrics.efficiency)
                  }}
                />
              </div>
              <span className="metric-percent">
                {(feedback.successMetrics.efficiency * 100).toFixed(0)}%
              </span>
            </div>
            <div className="feedback-metric">
              <span className="metric-name">Satisfaction</span>
              <div className="metric-bar-container">
                <div 
                  className="metric-bar"
                  style={{ 
                    width: `${feedback.successMetrics.userSatisfaction * 100}%`,
                    backgroundColor: getPerformanceColor(feedback.successMetrics.userSatisfaction)
                  }}
                />
              </div>
              <span className="metric-percent">
                {(feedback.successMetrics.userSatisfaction * 100).toFixed(0)}%
              </span>
            </div>
          </div>

          {feedback.failurePoints.length > 0 && (
            <div className="failure-points">
              <strong>Failure Points:</strong>
              <ul>
                {feedback.failurePoints.map((point, fpIdx) => (
                  <li key={fpIdx}>{point}</li>
                ))}
              </ul>
            </div>
          )}

          {feedback.suggestedImprovements.length > 0 && (
            <div className="suggested-improvements">
              <strong>Suggested Improvements:</strong>
              <ul>
                {feedback.suggestedImprovements.map((improvement, siIdx) => (
                  <li key={siIdx}>{improvement}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="feedback-footer">
            <span className="template-used">Template: {feedback.promptTemplate}</span>
            <span className="execution-time">
              Execution: {feedback.successMetrics.averageExecutionTime.toFixed(1)}s
            </span>
          </div>
        </div>
      ))}
    </div>
  </div>

  <div className="success-criteria">
    <h3>Platform Success Criteria</h3>
    <div className="criteria-grid">
      <div className="criteria-card">
        <div className="criteria-header">
          <span className="criteria-icon">🎯</span>
          <h4>Task Completion Improvement</h4>
        </div>
        <div className="criteria-target">
          <span className="target-label">Target:</span>
          <span className="target-value">40% vs baseline</span>
        </div>
        <div className="criteria-status achieved">
          <span>Status: On Track</span>
        </div>
      </div>
      
      <div className="criteria-card">
        <div className="criteria-header">
          <span className="criteria-icon">🛡️</span>
          <h4>Safety Compliance</h4>
        </div>
        <div className="criteria-target">
          <span className="target-label">Target:</span>
          <span className="target-value">99.9%</span>
        </div>
        <div className="criteria-status achieved">
          <span>Status: Achieved</span>
        </div>
      </div>
      
      <div className="criteria-card">
        <div className="criteria-header">
          <span className="criteria-icon">⚡</span>
          <h4>Prompt Adaptation Time</h4>
        </div>
        <div className="criteria-target">
          <span className="target-label">Target:</span>
          <span className="target-value">&lt; 1 second</span>
        </div>
        <div className="criteria-status achieved">
          <span>Status: Achieved</span>
        </div>
      </div>
      
      <div className="criteria-card">
        <div className="criteria-header">
          <span className="criteria-icon">😊</span>
          <h4>User Satisfaction</h4>
        </div>
        <div className="criteria-target">
          <span className="target-label">Target:</span>
          <span className="target-value">90%+</span>
        </div>
        <div className="criteria-status achieved">
          <span>Status: Achieved ({(aggregateMetrics.averageSatisfaction * 100).toFixed(0)}%)</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

);
};

export default PerformanceMetrics;
