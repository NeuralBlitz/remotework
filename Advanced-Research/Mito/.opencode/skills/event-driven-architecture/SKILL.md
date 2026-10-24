---
name: event-driven-architecture
description: Event-driven architecture, message queues, event sourcing, and CQRS
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: architecture
---

## What I do
- Design event-driven systems
- Implement message queues and brokers
- Use event sourcing patterns
- Handle asynchronous messaging
- Build event processing pipelines
- Ensure event ordering and delivery

## When to use me
When building loosely coupled, scalable systems, microservices, or real-time processing applications.

## Core Concepts

### Event-Driven Architecture
- Producers emit events
- Consumers react to events
- Decoupled communication
- Temporal coupling eliminated

### Event Types
- **Domain Events**: Business meaningful
- **Integration Events**: Cross-service communication
- **Change Data Capture**: Database changes
- **System Events**: Infrastructure events

### Message Patterns

#### Point-to-Point
- One producer → One consumer
- Queue-based
- Guaranteed processing

#### Pub/Sub
- One producer → Multiple consumers
- Topic-based
- Event notification

## Message Brokers

### Apache Kafka
- Distributed event streaming
- High throughput
- Persistence
- Exactly-once semantics
- Use cases: Log aggregation, CDC, Event streaming

### RabbitMQ
- Traditional message broker
- Complex routing
- Multiple protocols (AMQP, MQTT, STOMP)
- Use cases: Task queues, RPC

### AWS SQS
- Managed queue service
- FIFO queues
- Dead letter queues
- Use cases: Microservices, Batch jobs

### NATS
- Lightweight
- Pub/sub, request/reply
- JetStream for persistence

## Event Sourcing

### Concept
- Store events, not state
- Rebuild state by replaying events
- Complete audit trail
- Time travel debugging

### Implementation
```csharp
// Command
public class PlaceOrderCommand {
    public Guid OrderId;
    public List<OrderItem> Items;
}

// Event
public class OrderPlacedEvent {
    public Guid OrderId;
    public List<OrderItem> Items;
    public DateTime PlacedAt;
}

// Aggregate
public class Order {
    private List<OrderPlacedEvent> _events = new();
    
    public void PlaceOrder(PlaceOrderCommand cmd) {
        // Validate
        // Create event
        var evt = new OrderPlacedEvent(cmd.OrderId, cmd.Items, DateTime.UtcNow);
        _events.Add(evt);
    }
}
```

### Benefits
- Complete history
- Temporal queries
- Event replay
- Audit trail
- Performance

### Challenges
- Event schema evolution
- Eventual consistency
- Performance with many events
- CQRS required

## CQRS (Command Query Responsibility Segregation)

### Pattern
- Separate read and write models
- Different data structures
- Synchronization via events

### Implementation
- Commands: Intent to change
- Queries: Read data
- Read models updated via events

### Benefits
- Optimized read/write
- Scalability
- Flexibility

## Best Practices
- Idempotent consumers
- Handle duplicates
- Order events appropriately
- Use correlation IDs
- Document event schemas (Avro, Protobuf)
- Version events
- Dead letter handling
