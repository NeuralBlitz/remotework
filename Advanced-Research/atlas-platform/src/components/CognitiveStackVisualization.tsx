import React from ‘react’;
import { CognitiveLayer } from ‘../types/atlas.types’;

interface LayerData {
id: number;
name: string;
description: string;
color: string;
icon: string;
}

const layers: LayerData[] = [
{
id: CognitiveLayer.META_COGNITIVE,
name: ‘Meta-Cognitive Director’,
description: ‘Strategic oversight’,
color: ‘#9333ea’,
icon: ‘🎯’
},
{
id: CognitiveLayer.EXECUTIVE_PLANNER,
name: ‘Executive Planner’,
description: ‘Task decomposition’,
color: ‘#3b82f6’,
icon: ‘📋’
},
{
id: CognitiveLayer.WORKING_MEMORY,
name: ‘Working Memory Manager’,
description: ‘Context synthesis’,
color: ‘#06b6d4’,
icon: ‘🧩’
},
{
id: CognitiveLayer.TOOL_ORCHESTRATION,
name: ‘Tool Orchestration Engine’,
description: ‘Action execution’,
color: ‘#10b981’,
icon: ‘⚙️’
},
{
id: CognitiveLayer.PERCEPTION,
name: ‘Perception & Validation’,
description: ‘Input/output verification’,
color: ‘#f59e0b’,
icon: ‘👁️’
}
];

const CognitiveStackVisualization: React.FC = () => {
return (
<div className="cognitive-stack">
<h2>Five-Layer Cognitive Architecture</h2>
<div className="stack-container">
{layers.map((layer, index) => (
<div
key={layer.id}
className=“stack-layer”
style={{
backgroundColor: layer.color,
animationDelay: `${index * 0.1}s`
}}
>
<div className="layer-header">
<span className="layer-icon">{layer.icon}</span>
<div className="layer-info">
<h3 className="layer-name">Layer {layer.id}: {layer.name}</h3>
<p className="layer-description">{layer.description}</p>
</div>
</div>
<div className="layer-badge">Level {layer.id}</div>
</div>
))}
</div>
<div className="stack-flow">
<div className="flow-arrow">↓</div>
<p className="flow-text">Information flows bidirectionally through all layers</p>
</div>
</div>
);
};

export default CognitiveStackVisualization;
