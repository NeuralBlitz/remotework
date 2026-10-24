// ATLAS Core Type Definitions

export type ComplexityScore = number; // 0.0 - 1.0
export type ConfidenceLevel = number; // 0.0 - 1.0

export enum CognitiveLayer {
PERCEPTION = 1,
TOOL_ORCHESTRATION = 2,
WORKING_MEMORY = 3,
EXECUTIVE_PLANNER = 4,
META_COGNITIVE = 5,
}

export enum AgentType {
RESEARCH = ‘research’,
CODE_GENERATION = ‘code_generation’,
CREATIVE_COLLABORATION = ‘creative_collaboration’,
ANALYST = ‘analyst’,
STRATEGIST = ‘strategist’,
EXECUTOR = ‘executor’,
CRITIC = ‘critic’,
}

export enum MemoryTier {
IMMEDIATE = 1,
RECENT = 2,
HISTORICAL = 3,
EPISODIC = 4,
}

export interface CapabilityVector {
reasoning: number;
creativity: number;
analysis: number;
execution: number;
collaboration: number;
}

export interface TaskMetadata {
taskId: string;
taskType: string;
complexity: ComplexityScore;
requiredCapabilities: CapabilityVector;
historicalSuccessRate: number;
estimatedDuration?: number;
}

export interface PromptTemplate {
id: string;
name: string;
version: string;
metaContext: MetaContext;
coreDirective: string;
conditionalAugmentation: ConditionalRule[];
constraintBoundary: string[];
outputSpecification: OutputSpec;
performanceMetrics?: PerformanceMetrics;
}

export interface MetaContext {
taskType: string;
complexity: ComplexityScore;
requiredCapabilities: CapabilityVector;
historicalSuccessRate: number;
}

export interface ConditionalRule {
condition: string;
injection: string;
priority: number;
}

export interface OutputSpec {
format: string;
schema?: Record<string, any>;
validation?: string[];
}

export interface PerformanceMetrics {
taskCompletion: number;
efficiency: number;
userSatisfaction: number;
averageExecutionTime: number;
successRate: number;
}

export interface ExecutionFeedback {
taskId: string;
promptTemplate: string;
successMetrics: PerformanceMetrics;
failurePoints: string[];
suggestedImprovements: string[];
timestamp: string;
}

export interface MemoryEntry {
tier: MemoryTier;
content: string;
timestamp: string;
embedding?: number[];
importance: number;
}

export interface AgentState {
agentId: string;
agentType: AgentType;
currentLayer: CognitiveLayer;
activePrompts: PromptTemplate[];
memory: MemoryEntry[];
status: ‘idle’ | ‘processing’ | ‘waiting’ | ‘error’;
performance: PerformanceMetrics;
}

export interface LayerConfig {
layer: CognitiveLayer;
name: string;
description: string;
capabilities: string[];
promptTemplates: string[];
}

export interface SafetyConfig {
constitutionalPrinciples: string[];
dynamicGuardrails: string[];
outcomeSimulation: boolean;
humanOversightThreshold: number;
}

export interface PromptEvolutionMetrics {
templateId: string;
generation: number;
fitness: number;
mutations: string[];
crossoverParents?: string[];
successfulTasks: number;
failedTasks: number;
}
