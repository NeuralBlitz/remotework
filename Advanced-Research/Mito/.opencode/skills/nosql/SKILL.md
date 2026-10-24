---
name: nosql
description: NoSQL databases, document, wide-column, graph, and key-value stores
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: databases
---

## What I do
- Choose appropriate NoSQL databases for use cases
- Design distributed data models
- Optimize for specific access patterns
- Handle eventual consistency
- Design for horizontal scalability

## When to use me
When selecting NoSQL databases, designing distributed systems, or working with non-relational data models.

## Key Concepts

### NoSQL Categories
- **Document**: MongoDB, CouchDB, Cosmos DB
- **Key-Value**: Redis, DynamoDB, etcd
- **Wide-Column**: Cassandra, HBase, Bigtable
- **Graph**: Neo4j, Amazon Neptune, ArangoDB

### Data Modeling Patterns
- Denormalization
- Embedding vs referencing
- Composite keys
- Time-series modeling
- Event sourcing patterns

### Consistency Models
- Eventual consistency
- Strong consistency
- Tunable consistency
- Read your writes consistency
- Causality and vector clocks

### Scalability
- Horizontal partitioning (sharding)
- Consistent hashing
- Data balancing
- Replication topologies
- Multi-region deployments

### Query Patterns
- Primary key access patterns
- Secondary indexes
- Full-text search
- Aggregation pipelines
- Graph traversal

### Trade-offs
- ACID vs BASE
- CAP theorem implications
- Query flexibility vs performance
- Schema flexibility vs validation

## When to Use Each Type
- **Document**: Flexible schemas, catalogs, content management
- **Key-Value**: Caching, session store, high-speed access
- **Wide-Column**: Time-series, IoT, high write throughput
- **Graph**: Social networks, recommendations, fraud detection
