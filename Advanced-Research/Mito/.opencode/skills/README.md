# OpenCode Agent Skills

A comprehensive collection of **580+ domain-specific skills** for AI coding agents.

## Overview

This repository contains skill definitions for OpenCode agents, covering vast domains including:

- **Biology & Medical**: genomics, proteomics, immunology, pathology, neuroscience, pharmacology, cardiology, oncology, radiology, medical-imaging, surgery, psychiatry, pediatrics, and 50+ more
- **Mathematics**: real-analysis, complex-analysis, functional-analysis, algebraic-geometry, algebraic-topology, differential-geometry, category-theory, measure-theory, stochastic-processes, partial-differential-equations, and 30+ more
- **Physics**: quantum-mechanics, quantum-field-theory, quantum-optics, quantum-information, general-relativity, solid-state-physics, high-energy-physics, astrophysics-cosmology, plasma-physics, atomic-physics, and 30+ more
- **Engineering**: electrical-engineering, mechanical-engineering, civil-engineering, aerospace-engineering, chemical-engineering, nuclear-engineering, robotics, biomedical-engineering, and 60+ more
- **Computer Science & AI/ML**: machine-learning, deep-learning, reinforcement-learning, computer-vision, nlp, transformers, causal-inference, interpretable-ml, bayesian-machine-learning, physics-informed-neural-networks, llm-agents, multi-agent-systems, agentic-ai, federated-learning, edge-ai, and 80+ more
- **Hardware & Architecture**: cpu-design, gpu-architecture, risc-v, fpga-programming, vlsi-design, memory-systems, hardware-security, and 10+ more
- **Systems & Infrastructure**: operating-systems, distributed-computing, virtualization, kubernetes, docker, networking, cybersecurity, blockchain, and 40+ more
- **Chemistry & Materials**: spectroscopy, quantum-chemistry, electrochemistry, polymer-chemistry, materials-science, and 20+ more
- **Web & Software Development**: react, vue, nextjs, python, rust, go, java, and 100+ more

## Skills Structure

Each skill is a directory containing:
- `SKILL.md` - YAML frontmatter with name, description, and metadata
- Domain-specific knowledge, patterns, and best practices

## Usage

OpenCode automatically discovers skills from:
- `.opencode/skills/<name>/SKILL.md` (project)
- `~/.config/opencode/skills/<name>/SKILL.md` (global)

Agents can load skills on-demand using the native `skill` tool.

## Stats

- **580+** skills across **50+** domains
- Covering emerging fields: quantum-computing, physics-informed-ml, agentic-ai, federated-learning, neuromorphic-computing, and more

## Contributing

Add new skills by creating a directory with `SKILL.md` following the format:

```yaml
---
name: skill-name
description: Brief description of the skill
license: MIT
compatibility: opencode
metadata:
  audience: researchers
  category: field
---

## What I do
- Key capability 1
- Key capability 2

## When to use me
When working on...

## Key Concepts
- Concept 1
- Concept 2
```

## License

MIT
