import React, { useState } from ‘react’;
import { AgentType, CapabilityVector } from ‘../types/atlas.types’;

interface Agent {
id: string;
name: string;
type: AgentType;
description: string;
capabilities: CapabilityVector;
status: ‘active’ | ‘idle’ | ‘processing’;
tasksCompleted: number;
}

const mockAgents: Agent[] = [
{
id: ‘agent_research_001’,
name: ‘Research Agent’,
type: AgentType.RESEARCH,
description: ‘Conducts multi-step research with source verification’,
capabilities: { reasoning: 0.95, creativity: 0.70, analysis: 0.98, execution: 0.85, collaboration: 0.80 },
status: ‘active’,
tasksCompleted: 847
},
{
id: ‘agent_code_001’,
name: ‘Code Generation Agent’,
type: AgentType.CODE_GENERATION,
description: ‘Generates production-ready code with testing’,
capabilities: { reasoning: 0.90, creativity: 0.75, analysis: 0.88, execution: 0.95, collaboration: 0.70 },
status: ‘processing’,
tasksCompleted: 1203
},
{
id: ‘agent_creative_001’,
name: ‘Creative Agent’,
type: AgentType.CREATIVE_COLLABORATION,
description: ‘Multi-modal creative content generation’,
capabilities: { reasoning: 0.75, creativity: 0.98, analysis: 0.70, execution: 0.80, collaboration: 0.95 },
status: ‘idle’,
tasksCompleted: 634
},
{
id: ‘agent_analyst_001’,
name: ‘Analyst Agent’,
type: AgentType.ANALYST,
description: ‘Data interpretation and pattern detection’,
capabilities: { reasoning: 0.92, creativity: 0.65, analysis: 0.98, execution: 0.75, collaboration: 0.85 },
status: ‘active’,
tasksCompleted: 956
},
{
id: ‘agent_strategist_001’,
name: ‘Strategist Agent’,
type: AgentType.STRATEGIST,
description: ‘High-level strategic planning’,
capabilities: { reasoning: 0.95, creativity: 0.88, analysis: 0.90, execution: 0.70, collaboration: 0.92 },
status: ‘idle’,
tasksCompleted: 512
},
{
id: ‘agent_executor_001’,
name: ‘Executor Agent’,
type: AgentType.EXECUTOR,
description: ‘Task execution and workflow orchestration’,
capabilities: { reasoning: 0.80, creativity: 0.60, analysis: 0.75, execution: 0.98, collaboration: 0.85 },
status: ‘processing’,
tasksCompleted: 1456
},
{
id: ‘agent_critic_001’,
name: ‘Critic Agent’,
type: AgentType.CRITIC,
description: ‘Quality evaluation and improvement’,
capabilities: { reasoning: 0.93, creativity: 0.70, analysis: 0.96, execution: 0.72, collaboration: 0.88 },
status: ‘active’,
tasksCompleted: 723
}
];

const AgentDashboard: React.FC = () => {
const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

const getStatusColor = (status: string) => {
switch (status) {
case ‘active’: return ‘#10b981’;
case ‘processing’: return ‘#3b82f6’;
case ‘idle’: return ‘#6b7280’;
default: return ‘#6b7280’;
}
};

const renderCapabilityRadar = (capabilities: CapabilityVector) => {
return (
<div className="capability-chart">
<div className="capability-item">
<span className="capability-label">Reasoning</span>
<div className="capability-bar">
<div
className=“capability-fill”
style={{ width: `${capabilities.reasoning * 100}%`, backgroundColor: ‘#9333ea’ }}
/>
</div>
<span className="capability-value">{(capabilities.reasoning * 100).toFixed(0)}%</span>
</div>
<div className="capability-item">
<span className="capability-label">Creativity</span>
<div className="capability-bar">
<div
className=“capability-fill”
style={{ width: `${capabilities.creativity * 100}%`, backgroundColor: ‘#ec4899’ }}
/>
</div>
<span className="capability-value">{(capabilities.creativity * 100).toFixed(0)}%</span>
</div>
<div className="capability-item">
<span className="capability-label">Analysis</span>
<div className="capability-bar">
<div
className=“capability-fill”
style={{ width: `${capabilities.analysis * 100}%`, backgroundColor: ‘#3b82f6’ }}
/>
</div>
<span className="capability-value">{(capabilities.analysis * 100).toFixed(0)}%</span>
</div>
<div className="capability-item">
<span className="capability-label">Execution</span>
<div className="capability-bar">
<div
className=“capability-fill”
style={{ width: `${capabilities.execution * 100}%`, backgroundColor: ‘#10b981’ }}
/>
</div>
<span className="capability-value">{(capabilities.execution * 100).toFixed(0)}%</span>
</div>
<div className="capability-item">
<span className="capability-label">Collaboration</span>
<div className="capability-bar">
<div
className=“capability-fill”
style={{ width: `${capabilities.collaboration * 100}%`, backgroundColor: ‘#f59e0b’ }}
/>
</div>
<span className="capability-value">{(capabilities.collaboration * 100).toFixed(0)}%</span>
</div>
</div>
);
};

return (
<div className="agent-dashboard">
<h2>Agent Fleet Status</h2>
<div className="agents-grid">
{mockAgents.map(agent => (
<div
key={agent.id}
className={`agent-card ${selectedAgent?.id === agent.id ? 'selected' : ''}`}
onClick={() => setSelectedAgent(agent)}
>
<div className="agent-header">
<h3>{agent.name}</h3>
<div
className=“status-indicator”
style={{ backgroundColor: getStatusColor(agent.status) }}
>
{agent.status}
</div>
</div>
<p className="agent-description">{agent.description}</p>
<div className="agent-stats">
<div className="stat-item">
<span className="stat-label">Tasks Completed</span>
<span className="stat-value">{agent.tasksCompleted.toLocaleString()}</span>
</div>
<div className="stat-item">
<span className="stat-label">Type</span>
<span className="stat-value">{agent.type}</span>
</div>
</div>
</div>
))}
</div>

```
  {selectedAgent && (
    <div className="agent-details">
      <h3>Agent Capabilities: {selectedAgent.name}</h3>
      {renderCapabilityRadar(selectedAgent.capabilities)}
    </div>
  )}

  <div className="collaboration-section">
    <h3>Multi-Agent Collaboration Pipelines</h3>
    <div className="pipeline-card">
      <h4>Research → Code → Review Pipeline</h4>
      <div className="pipeline-flow">
        <div className="pipeline-step">Research Agent</div>
        <span className="pipeline-arrow">→</span>
        <div className="pipeline-step">Code Generation Agent</div>
        <span className="pipeline-arrow">→</span>
        <div className="pipeline-step">Critic Agent</div>
      </div>
    </div>
    <div className="pipeline-card">
      <h4>Strategy → Creative → Analysis Pipeline</h4>
      <div className="pipeline-flow">
        <div className="pipeline-step">Strategist Agent</div>
        <span className="pipeline-arrow">→</span>
        <div className="pipeline-step">Creative Agent</div>
        <span className="pipeline-arrow">→</span>
        <div className="pipeline-step">Analyst Agent</div>
      </div>
    </div>
  </div>
</div>
```

);
};

export default AgentDashboard;
