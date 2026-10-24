---
name: transactions
description: Database transaction management, ACID, and distributed transactions
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: databases
---

## What I do
- Manage database transactions correctly
- Handle distributed transactions across services
- Implement saga patterns for microservices
- Optimize transaction isolation levels
- Ensure data consistency

## When to use me
When building systems requiring strong data consistency, distributed systems, or microservices with multiple data sources.

## Key Concepts

### ACID Properties
- **Atomicity**: All or nothing
- **Consistency**: Valid state to valid state
- **Isolation**: Concurrent execution appears serial
- **Durability**: Committed data survives failures

### Transaction Types
- Implicit vs explicit transactions
- Auto-commit mode
- Savepoints
- Nested transactions
- Read-only transactions

### Isolation Levels
- **READ UNCOMMITTED**: Lowest isolation, may see uncommitted data
- **READ COMMITTED**: See only committed data (default in most)
- **REPEATABLE READ**: Same query returns consistent results
- **SERIALIZABLE**: Highest isolation, full isolation
- **Snapshot Isolation**: MVCC-based isolation

### Concurrency Problems
- Dirty reads
- Non-repeatable reads
- Phantom reads
- Lost updates
- Write skew

### Locking
- Shared locks (S locks)
- Exclusive locks (X locks)
- Deadlock detection and handling
- Lock escalation
- Optimistic vs pessimistic locking

### Distributed Transactions
- Two-phase commit (2PC)
- Three-phase commit (3PC)
- Saga pattern
- Eventual consistency
- Compensation actions
- Outbox pattern

### Best Practices
- Keep transactions short
- Avoid long-running operations
- Use appropriate isolation levels
- Handle deadlocks gracefully
- Test concurrency scenarios
- Monitor transaction metrics
