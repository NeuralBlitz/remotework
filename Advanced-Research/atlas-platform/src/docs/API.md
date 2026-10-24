# ATLAS API Reference

## Core Interfaces

### PromptTemplate

The fundamental unit of prompt architecture in ATLAS.

```typescript
interface PromptTemplate {
  id: string;                      // Unique identifier
  name: string;                    // Human-readable name
  version: string;                 // Semantic version
  metaContext: MetaContext;        // Task classification
  coreDirective: string;           // Primary instruction
  conditionalAugmentation: ConditionalRule[];  // Dynamic enhancements
  constraintBoundary: string[];    // Safety guardrails
  outputSpecification: OutputSpec; // Expected output format
  performanceMetrics?: PerformanceMetrics;  // Historical performance
}
```

**Usage Example:**

```typescript
const template: PromptTemplate = {
  id: "template_001",
  name: "Research Synthesizer",
  version: "2.1",
  metaContext: {
    taskType: "research",
    complexity: 0.85,
    requiredCapabilities: {
      reasoning: 0.90,
      analysis: 0.95,
      creativity: 0.70,
      execution: 0.80,
      collaboration: 0.85
    },
    historicalSuccessRate: 0.92
  },
  coreDirective: "Conduct comprehensive research and synthesize findings",
  // ... other properties
};
```

### AgentState

Represents the current state of an agent in the system.

```typescript
interface AgentState {
  agentId: string;                 // Unique agent identifier
  agentType: AgentType;           // Agent specialization
  currentLayer: CognitiveLayer;   // Active cognitive layer
  activePrompts: PromptTemplate[]; // Currently executing prompts
  memory: MemoryEntry[];          // Agent's working memory
  status: 'idle' | 'processing' | 'waiting' | 'error';
  performance: PerformanceMetrics; // Real-time performance
}
```

**Usage Example:**

```typescript
const agentState: AgentState = {
  agentId: "agent_research_001",
  agentType: AgentType.RESEARCH,
  currentLayer: CognitiveLayer.WORKING_MEMORY,
  activePrompts: [researchPrompt],
  memory: recentMemories,
  status: 'processing',
  performance: currentMetrics
};
```

### ExecutionFeedback

Captures detailed feedback from task execution.

```typescript
interface ExecutionFeedback {
  taskId: string;                  // Task identifier
  promptTemplate: string;          // Template used
  successMetrics: PerformanceMetrics;  // Performance scores
  failurePoints: string[];         // Issues encountered
  suggestedImprovements: string[]; // Optimization recommendations
  timestamp: string;               // ISO 8601 timestamp
}
```

## Enums

### CognitiveLayer

```typescript
enum CognitiveLayer {
  PERCEPTION = 1,           // Input/output validation
  TOOL_ORCHESTRATION = 2,   // Action execution
  WORKING_MEMORY = 3,       // Context synthesis
  EXECUTIVE_PLANNER = 4,    // Task decomposition
  META_COGNITIVE = 5,       // Strategic oversight
}
```

### AgentType

```typescript
enum AgentType {
  RESEARCH = 'research',
  CODE_GENERATION = 'code_generation',
  CREATIVE_COLLABORATION = 'creative_collaboration',
  ANALYST = 'analyst',
  STRATEGIST = 'strategist',
  EXECUTOR = 'executor',
  CRITIC = 'critic',
}
```

### MemoryTier

```typescript
enum MemoryTier {
  IMMEDIATE = 1,    // Last 3 interactions
  RECENT = 2,       // Last 20 interactions
  HISTORICAL = 3,   // All prior work
  EPISODIC = 4,     // Critical decision points
}
```

## Configuration Structures

### Cognitive Layer Configuration (YAML)

```yaml
cognitive_layers:
  - id: 1
    name: "Perception & Validation"
    description: "Input/output verification"
    capabilities:
      - input_validation
      - output_verification
    prompt_templates:
      - perception_validator_v1
    resource_allocation:
      cpu_priority: high
      memory_limit: "512MB"
      timeout_seconds: 5
```

### Agent Configuration (YAML)

```yaml
agents:
  research_agent:
    id: "agent_research_001"
    name: "Autonomous Research Agent"
    type: "research"
    capabilities:
      reasoning: 0.95
      creativity: 0.70
      analysis: 0.98
      execution: 0.85
      collaboration: 0.80
    specialized_prompts:
      - source_verification_v2
      - bias_detection_v3
    tools:
      - web_search
      - document_retrieval
```

## Data Models

### Prompt Template (JSON)

```json
{
  "id": "template_001",
  "name": "Dynamic Task Analyzer",
  "version": "3.2",
  "metaContext": {
    "taskType": "analysis",
    "complexity": 0.75,
    "requiredCapabilities": {
      "reasoning": 0.85,
      "creativity": 0.60,
      "analysis": 0.95,
      "execution": 0.70,
      "collaboration": 0.65
    },
    "historicalSuccessRate": 0.89
  },
  "conditionalAugmentation": [
    {
      "condition": "complexity > 0.7",
      "injection": "Apply advanced reasoning scaffold",
      "priority": 1
    }
  ],
  "performanceMetrics": {
    "taskCompletion": 0.91,
    "efficiency": 0.87,
    "userSatisfaction": 0.93,
    "averageExecutionTime": 2.4,
    "successRate": 0.89
  }
}
```

### Execution Feedback (JSON)

```json
{
  "taskId": "task_2024_001_3847",
  "promptTemplate": "template_001_v3.2",
  "successMetrics": {
    "taskCompletion": 0.95,
    "efficiency": 0.87,
    "userSatisfaction": 0.92,
    "averageExecutionTime": 2.3,
    "successRate": 0.95
  },
  "failurePoints": [],
  "suggestedImprovements": [
    "Consider parallel execution for sub-tasks",
    "Optimize dependency resolution"
  ],
  "timestamp": "2024-12-15T14:32:17Z"
}
```

## Utility Types

### CapabilityVector

Represents agent capabilities across five dimensions.

```typescript
interface CapabilityVector {
  reasoning: number;      // 0.0 - 1.0
  creativity: number;     // 0.0 - 1.0
  analysis: number;       // 0.0 - 1.0
  execution: number;      // 0.0 - 1.0
  collaboration: number;  // 0.0 - 1.0
}
```

### PerformanceMetrics

Tracks execution quality and efficiency.

```typescript
interface PerformanceMetrics {
  taskCompletion: number;        // 0.0 - 1.0
  efficiency: number;            // 0.0 - 1.0
  userSatisfaction: number;      // 0.0 - 1.0
  averageExecutionTime: number;  // seconds
  successRate: number;           // 0.0 - 1.0
}
```

### ConditionalRule

Defines conditional prompt augmentation.

```typescript
interface ConditionalRule {
  condition: string;    // Boolean expression
  injection: string;    // Additional prompt content
  priority: number;     // Execution order
}
```

### OutputSpec

Specifies expected output format.

```typescript
interface OutputSpec {
  format: string;                  // 'json' | 'markdown' | 'text'
  schema?: Record<string, any>;    // JSON schema (optional)
  validation?: string[];           // Validation rules (optional)
}
```

## Component Props

### CognitiveStackVisualization

```typescript
// No props required - uses internal layer data
<CognitiveStackVisualization />
```

### AgentDashboard

```typescript
// No props required - manages internal state
<AgentDashboard />
```

### PromptEvolutionMonitor

```typescript
// No props required - loads data from JSON
<PromptEvolutionMonitor />
```

### TaskExecutionPanel

```typescript
// No props required - manages task state internally
<TaskExecutionPanel />
```

### PerformanceMetrics

```typescript
// No props required - loads feedback data
<PerformanceMetrics />
```

## Constants

### Complexity Thresholds

```typescript
const COMPLEXITY_THRESHOLDS = {
  LOW: 0.5,
  MEDIUM: 0.7,
  HIGH: 0.85,
  VERY_HIGH: 0.9
};
```

### Performance Targets

```typescript
const PERFORMANCE_TARGETS = {
  MIN_SUCCESS_RATE: 0.75,
  MIN_EFFICIENCY: 0.70,
  MIN_SATISFACTION: 0.80,
  MAX_EXECUTION_TIME: 10.0  // seconds
};
```

### Safety Constants

```typescript
const SAFETY_CONFIG = {
  HUMAN_OVERSIGHT_THRESHOLD: 0.5,  // Confidence level
  MAX_RETRY_ATTEMPTS: 3,
  ESCALATION_TIMEOUT: 30  // seconds
};
```

## Error Codes

```typescript
enum AtlasErrorCode {
  PROMPT_COMPILATION_FAILED = 'PROMPT_001',
  AGENT_UNAVAILABLE = 'AGENT_001',
  LAYER_TRANSITION_FAILED = 'LAYER_001',
  MEMORY_OVERFLOW = 'MEMORY_001',
  VALIDATION_FAILED = 'VALID_001',
  SAFETY_VIOLATION = 'SAFETY_001',
  TIMEOUT_EXCEEDED = 'TIME_001',
}
```

## Best Practices

### Prompt Template Design

1. **Keep core directives clear and concise**
1. **Use conditional augmentation for complexity**
1. **Define explicit constraints**
1. **Specify output format precisely**
1. **Track performance metrics**

### Agent Configuration

1. **Specialize agents for specific domains**
1. **Balance capability scores realistically**
1. **Provide domain-specific tools**
1. **Define clear safety constraints**
1. **Enable collaboration where beneficial**

### Performance Optimization

1. **Cache frequently used prompts**
1. **Batch similar tasks**
1. **Use appropriate cognitive layers**
1. **Monitor and adjust thresholds**
1. **Implement graceful degradation**

-----

This API reference provides the foundation for working with the ATLAS platform’s core components and data structures.
