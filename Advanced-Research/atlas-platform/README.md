# Agentic Prompt Orchestration Architecture


[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A flexible, extensible framework for orchestrating multiple AI agents to solve complex tasks through coordinated prompt chaining and intelligent workflow management.

## 🚀 Features

- **Multi-Agent Coordination**: Specialized agents (Planner, Executor, Validator, Router, Synthesizer)
- **4 Execution Strategies**: Sequential, Parallel, Conditional, and DAG (Directed Acyclic Graph)
- **Dynamic Task Generation**: Agents can create follow-up tasks based on outputs
- **Template-Based Prompts**: Flexible prompt templates with variable substitution
- **Agent Memory System**: Short-term, long-term, and working memory for each agent
- **Validation Framework**: Custom validation rules for quality assurance
- **Dependency Resolution**: Automatic task ordering based on dependencies
- **Fully Typed**: Complete TypeScript implementation with comprehensive types

## 📋 Prerequisites

- Node.js 18.x or 20.x
- npm 9.x or higher
- TypeScript 5.x

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/NeuralBlitz/agentic-prompt-orchestration.git
cd agentic-prompt-orchestration

# Install dependencies
npm install

# Build the project
npm run build
```

## 🏃 Quick Start

```typescript
import { createOrchestrationSystem } from './index';

// Initialize the system
const { templateEngine, orchestrator, agents } = createOrchestrationSystem();

// Load workflow configurations
const workflowConfig = require('./workflows.json');
templateEngine.loadFromJSON(workflowConfig);

// Create and register agents
const planner = agents.createPlanner({
  id: 'planner-agent',
  role: 'planner',
  name: 'Task Planner',
  description: 'Plans and organizes tasks',
  capabilities: ['planning']
});

orchestrator.registerAgent(planner);

// Execute a workflow
const context = {
  conversationId: 'session-001',
  variables: { topic: 'AI Research' },
  history: [],
  state: {}
};

const results = await orchestrator.executeWorkflow('research-workflow', context);
console.log(results);
```

## 📖 Documentation

- [Complete Guide](README.mdx) - Comprehensive documentation with examples
- [Usage Guide](USAGE_GUIDE.mdx) - Practical patterns and best practices
- [Architecture](ARCHITECTURE.md) - System design and component interactions

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## 🔧 Development

```bash
# Run in development mode
npm run dev

# Run linter
npm run lint

# Format code
npm run format

# Build for production
npm run build
```

## 📁 Project Structure

```
├── types.ts                    # Type definitions
├── PromptTemplateEngine.ts     # Template rendering engine
├── agents.ts                   # Agent implementations
├── orchestrator.ts             # Workflow orchestration
├── index.ts                    # Main entry point
├── example.ts                  # Example application
├── workflows.json              # Workflow configurations
├── advanced-workflow.json      # Advanced workflow example
├── __tests__/                  # Test files
│   └── PromptTemplateEngine.test.ts
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD
└── README.md                   # This file
```

## 🔄 CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

- **Build**: Compiles TypeScript and creates distribution files
- **Test**: Runs unit tests with coverage reporting
- **Lint**: Checks code quality with ESLint and Prettier
- **Multi-Node**: Tests against Node.js 18.x and 20.x

## 🤝 Contributing

1. Fork the repository
1. Create a feature branch (`git checkout -b feature/amazing-feature`)
1. Commit your changes (`git commit -m 'Add amazing feature'`)
1. Push to the branch (`git push origin feature/amazing-feature`)
1. Open a Pull Request

## 📝 Example Workflows

### Research Pipeline

```typescript
const researchWorkflow = {
  id: 'research-pipeline',
  strategy: { type: 'dag', config: {} },
  tasks: [
    { id: 'plan', agentId: 'planner' },
    { id: 'research', agentId: 'researcher', dependencies: ['plan'] },
    { id: 'validate', agentId: 'validator', dependencies: ['research'] },
    { id: 'synthesize', agentId: 'synthesizer', dependencies: ['validate'] }
  ]
};
```

### Content Creation

```typescript
const contentWorkflow = {
  id: 'content-creation',
  strategy: { type: 'parallel', config: { maxConcurrency: 3 } },
  tasks: [
    { id: 'intro', agentId: 'writer-1' },
    { id: 'body', agentId: 'writer-2' },
    { id: 'conclusion', agentId: 'writer-3' },
    { id: 'edit', agentId: 'editor', dependencies: ['intro', 'body', 'conclusion'] }
  ]
};
```

## 🐛 Troubleshooting

### Common Issues

**Issue: “Dependencies lock file is not found”**

- Solution: Run `npm install` to generate `package-lock.json`

**Issue: “Agent not found”**

- Solution: Ensure agents are registered before executing workflows

**Issue: “Circular dependency detected”**

- Solution: Review task dependencies to ensure they form a DAG

## 📜 License

This project is licensed under the MIT License - see the <LICENSE> file for details.

## 🙏 Acknowledgments

- Built with TypeScript for type safety
- Inspired by multi-agent AI systems research
- Designed for extensibility and real-world use cases

## 📧 Contact

- GitHub: [@NeuralBlitz](https://github.com/NeuralBlitz)
- Issues: [GitHub Issues](https://github.com/NeuralBlitz/agentic-prompt-orchestration/issues)

-----

**Built with ❤️ for the AI agent community**
