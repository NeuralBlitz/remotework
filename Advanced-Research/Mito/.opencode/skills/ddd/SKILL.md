---
name: ddd
description: Domain-Driven Design, bounded contexts, aggregates, and domain modeling
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: software-development
---

## What I do
- Design bounded contexts and their boundaries
- Create rich domain models
- Implement aggregates and aggregate roots
- Design value objects
- Define domain events
- Apply strategic and tactical DDD

## When to use me
When building complex domain logic, modeling business domains, or structuring large applications.

## Strategic Design

### Bounded Contexts
- Clear boundaries around domain models
- Each context has its own ubiquitous language
- Context mapping relationships:
  - **Customer/Supplier**: Upstream/downstream
  - **Conformist**: Downstream follows upstream
  - **Anticorruption Layer**: Translation layer
  - **Open Host Service**: Published language
  - **Separate Ways**: No relationship

### Ubiquitous Language
- Shared language between developers and domain experts
- Embedded in code (class names, methods)
- Consistent terminology

### Context Maps
- Visual representation of system boundaries
- Integration points
- Team responsibilities

## Tactical Design

### Entities
- Identity that persists over time
- Mutable state
- Unique identifier
```java
class Order {
    private OrderId id;
    private Money total;
    // Entity with unique ID
}
```

### Value Objects
- Immutable
- No identity
- Compares by value
```java
class Money {
    private final BigDecimal amount;
    private final Currency currency;
    // Value object - immutable, compared by value
}
```

### Aggregates
- Cluster of related objects
- Aggregate root controls access
- Invariants enforced within boundary
- One entity per aggregate typically
```java
class OrderAggregate {
    private OrderId id;
    private List<OrderLine> lines; // Only aggregate root can modify
    
    public void addLine(Product product, int quantity) {
        // Invariants enforced here
    }
}
```

### Domain Events
- Something significant happened
- Immutable
- Named in past tense
```java
class OrderPlacedEvent {
    private OrderId orderId;
    private Money total;
    private Instant occurredAt;
}
```

### Repositories
- Collection-like interface
- Persist aggregates
- Abstract storage details

### Domain Services
- Operations that don't belong to entities
- Cross-aggregate operations
- Stateless

### Factories
- Complex object creation
- Hide implementation details

## DDD Patterns
- CQRS with DDD
- Event sourcing
- Specification pattern
- Side effects
- Policy
- Strategy
