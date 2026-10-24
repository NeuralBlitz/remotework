---
name: anti-patterns
description: Common software anti-patterns, code smells, and how to avoid them
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: software-development
---

## What I do
- Identify code anti-patterns in existing code
- Suggest refactoring solutions
- Avoid common mistakes in design and implementation
- Improve code quality and maintainability
- Recognize technical debt indicators

## When to use me
When reviewing code, improving designs, or fixing maintainability issues.

## Code Anti-Patterns

### Object-Oriented
- **God Object**: Single class doing too much
- **Spaghetti Code**: Unstructured, tangled control flow
- **Magic Numbers**: Hard-coded values without constants
- **Feature Envy**: Excessive use of another class's data
- **Data Clumps**: Groups of variables passed together
- **Refused Bequest**: Not using inherited methods
- **Switch Statements**: Complex conditionals instead of polymorphism
- **Parallel Inheritance**: Duplicate class hierarchies

### Design Anti-Patterns
- **Singleton Abuse**: Overuse of singletons
- **Dependency Hell**: Complex dependency chains
- **Circular Dependencies**: A→B→C→A
- **Interface Bloat**: Overly complex interfaces
- **Leaky Abstractions**: Exposing internal details
- **Golden Hammer**: Using one solution for everything
- **Reinvention**: Not using built-in features
- **Analysis Paralysis**: Over-planning

### Database Anti-Patterns
- **Database as IPC**: Using DB for communication
- **God Table**: One table for everything
- **EAV**: Entity-Attribute-Value pattern
- **Naive Enum**: Storing enums as strings without constraints
- **Missing Indexes**: Slow queries due to full table scans
- **N+1 Queries**: Loading related data inefficiently

### Concurrency
- **Race Conditions**: Uncoordinated concurrent access
- **Deadlock**: Circular wait dependencies
- **Blocking Operations**: Synchronous calls in async code
- **Shared Mutex**: Global locks causing contention

### Testing
- **Testing the Implementation**: Instead of behavior
- **Happy Path Only**: Only testing success cases
- **Manual Testing**: No automated tests
- **Tight Coupling**: Tests depend on implementation details

## Code Smells
- Long methods
- Large classes
- Duplicate code
- Long parameter lists
- Primitive obsession
- Data classes
- Comments explaining bad code

## Refactoring Strategies
- Extract Method
- Move Method
- Replace Conditional with Polymorphism
- Introduce Parameter Object
- Replace Magic Numbers
- Extract Class
- Inline Class
- Introduce Null Object
