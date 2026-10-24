# NebulaWrap


A minimal, practical LLM wrapper SDK: pluggable adapters, provenance (GoldenDAG), safety hooks, memory, streaming, and a prompt test harness.

## Quickstart

1. Create a virtualenv and install:
```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
pip install openai  # if you will use OpenAIAdapter

Set OPENAI_API_KEY then run:
python examples/quickstart.py
Goals
Provider-agnostic adapters
Deterministic provenance (DecisionCapsule + GoldenDAG)
Pre/post safety hooks
Simple persistent memory (SQLite-backed)
Prompt testing harness (yaml-driven)

---

### `LICENSE` (MIT)
```text
MIT License
Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy...
(standard MIT text - paste full MIT license in your file)
