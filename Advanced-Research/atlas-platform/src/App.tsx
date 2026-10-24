import React, { useState } from ‘react’;
import { AgentType, CognitiveLayer } from ‘./types/atlas.types’;
import CognitiveStackVisualization from ‘./components/CognitiveStackVisualization’;
import AgentDashboard from ‘./components/AgentDashboard’;
import PromptEvolutionMonitor from ‘./components/PromptEvolutionMonitor’;
import TaskExecutionPanel from ‘./components/TaskExecutionPanel’;
import PerformanceMetrics from ‘./components/PerformanceMetrics’;
import ‘./App.css’;

const App: React.FC = () => {
const [activeView, setActiveView] = useState<‘overview’ | ‘agents’ | ‘prompts’ | ‘execution’ | ‘metrics’>(‘overview’);

return (
<div className="atlas-platform">
<header className="atlas-header">
<div className="header-content">
<h1 className="atlas-title">
<span className="atlas-logo">⚡</span>
ATLAS
</h1>
<p className="atlas-subtitle">Adaptive Thought-Layer Agentic System</p>
</div>
<nav className="atlas-nav">
<button
className={`nav-button ${activeView === 'overview' ? 'active' : ''}`}
onClick={() => setActiveView(‘overview’)}
>
Overview
</button>
<button
className={`nav-button ${activeView === 'agents' ? 'active' : ''}`}
onClick={() => setActiveView(‘agents’)}
>
Agents
</button>
<button
className={`nav-button ${activeView === 'prompts' ? 'active' : ''}`}
onClick={() => setActiveView(‘prompts’)}
>
Prompt Evolution
</button>
<button
className={`nav-button ${activeView === 'execution' ? 'active' : ''}`}
onClick={() => setActiveView(‘execution’)}
>
Task Execution
</button>
<button
className={`nav-button ${activeView === 'metrics' ? 'active' : ''}`}
onClick={() => setActiveView(‘metrics’)}
>
Performance
</button>
</nav>
</header>

```
  <main className="atlas-main">
    {activeView === 'overview' && (
      <div className="overview-container">
        <section className="intro-section">
          <h2>Platform Overview</h2>
          <p className="intro-text">
            ATLAS is a next-generation AI/ML platform built on a revolutionary 
            <strong> layered prompt architecture</strong> that enables truly autonomous, 
            context-aware agents capable of complex reasoning, self-improvement, and 
            collaborative task execution.
          </p>
        </section>
        
        <CognitiveStackVisualization />
        
        <section className="features-grid">
          <div className="feature-card">
            <h3>🧠 Five-Layer Cognitive Stack</h3>
            <p>Hierarchical reasoning from perception to meta-cognition</p>
          </div>
          <div className="feature-card">
            <h3>🔄 Dynamic Prompt Evolution</h3>
            <p>Self-optimizing prompts using genetic algorithms</p>
          </div>
          <div className="feature-card">
            <h3>🤝 Multi-Agent Collaboration</h3>
            <p>Specialized agents working together seamlessly</p>
          </div>
          <div className="feature-card">
            <h3>🛡️ Multi-Tier Safety</h3>
            <p>Constitutional principles to dynamic guardrails</p>
          </div>
        </section>
      </div>
    )}

    {activeView === 'agents' && <AgentDashboard />}
    {activeView === 'prompts' && <PromptEvolutionMonitor />}
    {activeView === 'execution' && <TaskExecutionPanel />}
    {activeView === 'metrics' && <PerformanceMetrics />}
  </main>

  <footer className="atlas-footer">
    <p>ATLAS Platform v1.0.0 | Cognitive Architecture for Advanced AI</p>
  </footer>
</div>
```

);
};

export default App;
