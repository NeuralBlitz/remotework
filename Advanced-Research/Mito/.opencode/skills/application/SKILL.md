---
name: application
description: Application architecture, design patterns, and structural patterns
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: software-development
---

## What I do
- Design application architecture from requirements
- Choose appropriate architectural patterns
- Structure code into modules and layers
- Handle dependencies and dependencies injection
- Define component boundaries and responsibilities

## When to use me
When building applications from scratch, refactoring existing code, or choosing architectural approaches.

## Architectural Patterns

### Layered Architecture
- Presentation layer
- Business logic layer
- Data access layer
- Separation of concerns
- Pros: Simple, well-understood
- Cons: Can lead to tight coupling

### Clean/Hexagonal Architecture
- Domain layer (core)
- Application layer (use cases)
- Infrastructure layer (adapters)
- Ports and adapters
- Pros: Testable, flexible
- Cons: More complex initial setup

### CQRS (Command Query Responsibility Segregation)
- Separate read and write models
- Different representations for queries vs commands
- Event sourcing support
- Pros: Optimized reads/writes
- Cons: Complexity, eventual consistency

### Event-Driven Architecture
- Event producers and consumers
- Message queues/brokers
- Event sourcing
- Pros: Loose coupling, scalability
- Cons: Complexity, debugging

### Microservices
- Service decomposition
- API gateways
- Service mesh
- Distributed data
- Pros: Independent deployment, scaling
- Cons: Distributed system complexity

## Design Patterns

### Creational
- Factory Method
- Abstract Factory
- Builder
- Prototype
- Singleton

### Structural
- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Flyweight
- Proxy

### Behavioral
- Chain of Responsibility
- Command
- Iterator
- Mediator
- Memento
- Observer
- State
- Strategy
- Template Method
- Visitor

## Dependency Management
- Dependency Injection
- Inversion of Control
- Service Locator
- Constructor Injection
- Property Injection
- Interface-based design
- Dependency graphs

## Module Design
- High cohesion, low coupling
- Single Responsibility Principle
- Common Closure Principle
- Acyclic Dependencies Principle
- Stable Dependencies Principle
- Stable Abstractions Principle
