import React, { useState } from ‘react’;

interface Task {
id: string;
title: string;
status: ‘pending’ | ‘running’ | ‘completed’ | ‘failed’;
complexity: number;
assignedAgent: string;
layer: number;
progress: number;
startTime?: string;
endTime?: string;
}

const mockTasks: Task[] = [
{
id: ‘task_001’,
title: ‘Analyze market research data for Q4 trends’,
status: ‘completed’,
complexity: 0.75,
assignedAgent: ‘Research Agent’,
layer: 4,
progress: 100,
startTime: ‘2024-12-15T14:30:00Z’,
endTime: ‘2024-12-15T14:38:27Z’
},
{
id: ‘task_002’,
title: ‘Generate Python API wrapper with tests’,
status: ‘running’,
complexity: 0.82,
assignedAgent: ‘Code Generation Agent’,
layer: 2,
progress: 65,
startTime: ‘2024-12-15T15:12:00Z’
},
{
id: ‘task_003’,
title: ‘Create marketing campaign content variations’,
status: ‘running’,
complexity: 0.68,
assignedAgent: ‘Creative Agent’,
layer: 3,
progress: 45,
startTime: ‘2024-12-15T15:45:00Z’
},
{
id: ‘task_004’,
title: ‘Optimize database query performance’,
status: ‘pending’,
complexity: 0.88,
assignedAgent: ‘Code Generation Agent’,
layer: 1,
progress: 0
},
{
id: ‘task_005’,
title: ‘Synthesize scientific literature on climate models’,
status: ‘completed’,
complexity: 0.92,
assignedAgent: ‘Research Agent’,
layer: 5,
progress: 100,
startTime: ‘2024-12-15T13:00:00Z’,
endTime: ‘2024-12-15T13:14:33Z’
}
];

const TaskExecutionPanel: React.FC = () => {
const [tasks] = useState<Task[]>(mockTasks);
const [selectedTask, setSelectedTask] = useState<Task | null>(null);

const getStatusColor = (status: string) => {
switch (status) {
case ‘completed’: return ‘#10b981’;
case ‘running’: return ‘#3b82f6’;
case ‘pending’: return ‘#6b7280’;
case ‘failed’: return ‘#ef4444’;
default: return ‘#6b7280’;
}
};

const getComplexityLabel = (complexity: number) => {
if (complexity >= 0.85) return ‘Very High’;
if (complexity >= 0.7) return ‘High’;
if (complexity >= 0.5) return ‘Medium’;
return ‘Low’;
};

const calculateDuration = (startTime?: string, endTime?: string) => {
if (!startTime) return ‘N/A’;
const start = new Date(startTime).getTime();
const end = endTime ? new Date(endTime).getTime() : Date.now();
const seconds = Math.floor((end - start) / 1000);
const minutes = Math.floor(seconds / 60);
const remainingSeconds = seconds % 60;
return `${minutes}m ${remainingSeconds}s`;
};

return (
<div className="task-execution">
<h2>Task Execution Monitor</h2>

```
  <div className="execution-stats">
    <div className="stat-card">
      <span className="stat-icon">✓</span>
      <div className="stat-content">
        <span className="stat-label">Completed</span>
        <span className="stat-number">
          {tasks.filter(t => t.status === 'completed').length}
        </span>
      </div>
    </div>
    <div className="stat-card">
      <span className="stat-icon">⚡</span>
      <div className="stat-content">
        <span className="stat-label">Running</span>
        <span className="stat-number">
          {tasks.filter(t => t.status === 'running').length}
        </span>
      </div>
    </div>
    <div className="stat-card">
      <span className="stat-icon">⏳</span>
      <div className="stat-content">
        <span className="stat-label">Pending</span>
        <span className="stat-number">
          {tasks.filter(t => t.status === 'pending').length}
        </span>
      </div>
    </div>
    <div className="stat-card">
      <span className="stat-icon">✗</span>
      <div className="stat-content">
        <span className="stat-label">Failed</span>
        <span className="stat-number">
          {tasks.filter(t => t.status === 'failed').length}
        </span>
      </div>
    </div>
  </div>

  <div className="tasks-list">
    <h3>Active Tasks</h3>
    {tasks.map(task => (
      <div 
        key={task.id}
        className={`task-item ${selectedTask?.id === task.id ? 'selected' : ''}`}
        onClick={() => setSelectedTask(task)}
      >
        <div className="task-header">
          <h4>{task.title}</h4>
          <span 
            className="task-status"
            style={{ backgroundColor: getStatusColor(task.status) }}
          >
            {task.status}
          </span>
        </div>
        
        <div className="task-meta">
          <span className="meta-item">
            <strong>Agent:</strong> {task.assignedAgent}
          </span>
          <span className="meta-item">
            <strong>Layer:</strong> {task.layer}
          </span>
          <span className="meta-item">
            <strong>Complexity:</strong> {getComplexityLabel(task.complexity)}
          </span>
        </div>

        {task.status === 'running' && (
          <div className="task-progress">
            <div className="progress-bar">
              <div 
                className="progress-fill"
                style={{ width: `${task.progress}%` }}
              />
            </div>
            <span className="progress-text">{task.progress}%</span>
          </div>
        )}

        <div className="task-timing">
          {task.startTime && (
            <span>Duration: {calculateDuration(task.startTime, task.endTime)}</span>
          )}
        </div>
      </div>
    ))}
  </div>

  {selectedTask && (
    <div className="task-details-panel">
      <h3>Task Execution Details</h3>
      
      <div className="detail-grid">
        <div className="detail-item">
          <span className="detail-label">Task ID</span>
          <span className="detail-value">{selectedTask.id}</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Status</span>
          <span 
            className="detail-value"
            style={{ color: getStatusColor(selectedTask.status) }}
          >
            {selectedTask.status}
          </span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Assigned Agent</span>
          <span className="detail-value">{selectedTask.assignedAgent}</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Cognitive Layer</span>
          <span className="detail-value">Layer {selectedTask.layer}</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Complexity Score</span>
          <span className="detail-value">{(selectedTask.complexity * 100).toFixed(0)}%</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Progress</span>
          <span className="detail-value">{selectedTask.progress}%</span>
        </div>
      </div>

      <div className="execution-timeline">
        <h4>Execution Flow</h4>
        <div className="timeline">
          <div className="timeline-item completed">
            <div className="timeline-marker">✓</div>
            <div className="timeline-content">
              <strong>Task Received</strong>
              <span>Layer 5: Meta-Cognitive Director</span>
            </div>
          </div>
          <div className="timeline-item completed">
            <div className="timeline-marker">✓</div>
            <div className="timeline-content">
              <strong>Planning Phase</strong>
              <span>Layer 4: Executive Planner</span>
            </div>
          </div>
          <div className={`timeline-item ${selectedTask.progress >= 50 ? 'completed' : 'active'}`}>
            <div className="timeline-marker">{selectedTask.progress >= 50 ? '✓' : '⏳'}</div>
            <div className="timeline-content">
              <strong>Context Assembly</strong>
              <span>Layer 3: Working Memory Manager</span>
            </div>
          </div>
          <div className={`timeline-item ${selectedTask.progress >= 75 ? 'completed' : selectedTask.progress >= 50 ? 'active' : 'pending'}`}>
            <div className="timeline-marker">
              {selectedTask.progress >= 75 ? '✓' : selectedTask.progress >= 50 ? '⏳' : '○'}
            </div>
            <div className="timeline-content">
              <strong>Execution Phase</strong>
              <span>Layer 2: Tool Orchestration Engine</span>
            </div>
          </div>
          <div className={`timeline-item ${selectedTask.progress === 100 ? 'completed' : selectedTask.progress >= 75 ? 'active' : 'pending'}`}>
            <div className="timeline-marker">
              {selectedTask.progress === 100 ? '✓' : selectedTask.progress >= 75 ? '⏳' : '○'}
            </div>
            <div className="timeline-content">
              <strong>Validation</strong>
              <span>Layer 1: Perception & Validation</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )}
</div>
```

);
};

export default TaskExecutionPanel;
