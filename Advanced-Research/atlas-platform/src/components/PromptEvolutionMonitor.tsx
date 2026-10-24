import React, { useState } from ‘react’;
import promptTemplatesData from ‘../data/prompt-templates.json’;

const PromptEvolutionMonitor: React.FC = () => {
const [selectedTemplate, setSelectedTemplate] = useState<any>(null);

const templates = promptTemplatesData.promptTemplates;
const evolutionMetrics = promptTemplatesData.evolutionMetrics;

const getPerformanceColor = (value: number) => {
if (value >= 0.9) return ‘#10b981’;
if (value >= 0.75) return ‘#f59e0b’;
return ‘#ef4444’;
};

return (
<div className="prompt-evolution">
<h2>Prompt Evolution Engine</h2>

```
  <div className="evolution-overview">
    <div className="overview-card">
      <h3>Total Templates</h3>
      <p className="metric-value">{templates.length}</p>
    </div>
    <div className="overview-card">
      <h3>Average Fitness</h3>
      <p className="metric-value">
        {(evolutionMetrics.reduce((acc, m) => acc + m.fitness, 0) / evolutionMetrics.length).toFixed(2)}
      </p>
    </div>
    <div className="overview-card">
      <h3>Total Generations</h3>
      <p className="metric-value">
        {Math.max(...evolutionMetrics.map(m => m.generation))}
      </p>
    </div>
  </div>

  <div className="templates-section">
    <h3>Prompt Template Library</h3>
    <div className="templates-grid">
      {templates.map(template => (
        <div 
          key={template.id}
          className={`template-card ${selectedTemplate?.id === template.id ? 'selected' : ''}`}
          onClick={() => setSelectedTemplate(template)}
        >
          <div className="template-header">
            <h4>{template.name}</h4>
            <span className="template-version">v{template.version}</span>
          </div>
          <div className="template-meta">
            <span className="meta-badge">Type: {template.metaContext.taskType}</span>
            <span className="meta-badge">
              Complexity: {(template.metaContext.complexity * 100).toFixed(0)}%
            </span>
          </div>
          <div className="template-performance">
            <div className="performance-item">
              <span>Success Rate</span>
              <span 
                className="performance-value"
                style={{ color: getPerformanceColor(template.performanceMetrics.successRate) }}
              >
                {(template.performanceMetrics.successRate * 100).toFixed(0)}%
              </span>
            </div>
            <div className="performance-item">
              <span>User Satisfaction</span>
              <span 
                className="performance-value"
                style={{ color: getPerformanceColor(template.performanceMetrics.userSatisfaction) }}
              >
                {(template.performanceMetrics.userSatisfaction * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>

  {selectedTemplate && (
    <div className="template-details">
      <h3>Template Details: {selectedTemplate.name}</h3>
      
      <div className="detail-section">
        <h4>Core Directive</h4>
        <p className="directive-text">{selectedTemplate.coreDirective}</p>
      </div>

      <div className="detail-section">
        <h4>Conditional Augmentation Rules</h4>
        <div className="augmentation-list">
          {selectedTemplate.conditionalAugmentation.map((rule: any, idx: number) => (
            <div key={idx} className="augmentation-rule">
              <div className="rule-condition">
                <strong>IF</strong> {rule.condition}
              </div>
              <div className="rule-injection">
                <strong>THEN</strong> {rule.injection}
              </div>
              <span className="rule-priority">Priority: {rule.priority}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="detail-section">
        <h4>Constraint Boundaries</h4>
        <ul className="constraints-list">
          {selectedTemplate.constraintBoundary.map((constraint: string, idx: number) => (
            <li key={idx}>{constraint}</li>
          ))}
        </ul>
      </div>

      <div className="detail-section">
        <h4>Required Capabilities</h4>
        <div className="capabilities-grid">
          {Object.entries(selectedTemplate.metaContext.requiredCapabilities).map(([key, value]) => (
            <div key={key} className="capability-box">
              <span className="capability-name">{key}</span>
              <div className="capability-meter">
                <div 
                  className="capability-meter-fill"
                  style={{ width: `${(value as number) * 100}%` }}
                />
              </div>
              <span className="capability-percent">{((value as number) * 100).toFixed(0)}%</span>
            </div>
          ))}
        </div>
      </div>

      <div className="detail-section">
        <h4>Performance Metrics</h4>
        <div className="metrics-grid">
          <div className="metric-box">
            <span className="metric-label">Task Completion</span>
            <span className="metric-number">
              {(selectedTemplate.performanceMetrics.taskCompletion * 100).toFixed(1)}%
            </span>
          </div>
          <div className="metric-box">
            <span className="metric-label">Efficiency</span>
            <span className="metric-number">
              {(selectedTemplate.performanceMetrics.efficiency * 100).toFixed(1)}%
            </span>
          </div>
          <div className="metric-box">
            <span className="metric-label">User Satisfaction</span>
            <span className="metric-number">
              {(selectedTemplate.performanceMetrics.userSatisfaction * 100).toFixed(1)}%
            </span>
          </div>
          <div className="metric-box">
            <span className="metric-label">Avg Execution Time</span>
            <span className="metric-number">
              {selectedTemplate.performanceMetrics.averageExecutionTime.toFixed(1)}s
            </span>
          </div>
        </div>
      </div>
    </div>
  )}

  <div className="evolution-section">
    <h3>Evolution Metrics</h3>
    <div className="evolution-grid">
      {evolutionMetrics.map((metric: any) => (
        <div key={metric.templateId} className="evolution-card">
          <h4>{metric.templateId}</h4>
          <div className="evolution-info">
            <div className="info-item">
              <span>Generation</span>
              <span className="info-value">{metric.generation}</span>
            </div>
            <div className="info-item">
              <span>Fitness</span>
              <span className="info-value">{(metric.fitness * 100).toFixed(0)}%</span>
            </div>
            <div className="info-item">
              <span>Success/Fail</span>
              <span className="info-value">
                {metric.successfulTasks}/{metric.failedTasks}
              </span>
            </div>
          </div>
          <div className="mutations-section">
            <strong>Mutations:</strong>
            <ul className="mutations-list">
              {metric.mutations.map((mutation: string, idx: number) => (
                <li key={idx}>{mutation}</li>
              ))}
            </ul>
          </div>
        </div>
      ))}
    </div>
  </div>
</div>
```

);
};

export default PromptEvolutionMonitor;
