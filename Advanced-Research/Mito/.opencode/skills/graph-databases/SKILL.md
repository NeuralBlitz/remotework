---
name: graph-databases
description: Graph databases, Neo4j, Cypher queries, and graph data modeling
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: databases
---

## What I do
- Query graph databases efficiently
- Design graph schemas and models
- Traverse complex relationships
- Optimize graph queries
- Build recommendation systems

## When to use me
When working with highly connected data, social networks, fraud detection, or recommendation engines.

## Graph Concepts

### Nodes and Relationships
- **Nodes**: Entities (people, products, places)
- **Relationships**: Connections between nodes
- **Properties**: Key-value pairs on both
- **Labels**: Node types
- **Types**: Relationship types

### Property Graph Model
```cypher
CREATE (alice:Person {name: 'Alice'})-[:FRIEND {since: 2020}]->(bob:Person {name: 'Bob'})
```

## Cypher Query Language

### Basic Queries
```cypher
// Match nodes
MATCH (p:Person) WHERE p.name = 'Alice' RETURN p

// Relationships
MATCH (p1:Person)-[:FRIEND]->(p2:Person) RETURN p1, p2

// Pattern matching
MATCH (p:Person)-[:FRIEND]->(friend)-[:FRIEND]->(friendOfFriend)
WHERE p.name = 'Alice'
RETURN friendOfFriend.name
```

### Filtering
```cypher
MATCH (p:Person)
WHERE p.age > 25 AND p.name STARTS WITH 'A'
RETURN p
```

### Aggregation
```cypher
MATCH (p:Person)-[:FRIEND]->(friend)
WITH p, count(friend) AS friendCount
WHERE friendCount > 10
RETURN p
```

### Path Finding
```cypher
// Shortest path
MATCH path = shortestPath((a:Person)-[*]-(b:Person))
WHERE a.name = 'Alice' AND b.name = 'Charlie'
RETURN path
```

## Graph Modeling

### Design Principles
- Start with questions, not entities
- Use meaningful relationship types
- Model for queries
- Consider traversal depth
- Denormalize appropriately

### Common Patterns
- **Friend of Friend**: Social connections
- **Hierarchies**: Org charts, categories
- **Sequences**: User journeys, events
- **Multiple hops**: N-degree connections

## Use Cases

### Social Networks
- Friend recommendations
- Influence analysis
- Community detection

### Fraud Detection
- Unusual patterns
- Ring detection
- Connection analysis

### Recommendation Engines
- "Users who bought this also bought"
- Skill matching
- Content recommendations

### Network Analysis
- IT infrastructure
- Supply chain
- Disease spread

### Knowledge Graphs
- Semantic search
- Entity resolution
- Taxonomy

## Database Systems
- **Neo4j**: Most popular, Cypher
- **Amazon Neptune**: Multi-model (graph + RDF)
- **ArangoDB**: Multi-model (graph + document)
- **Apache Jena**: RDF triple store
- **TigerGraph**: High performance

## Performance Optimization
- Indexes on properties
- Relationship density consideration
- Avoid excessive traversal
- Use projections
- Partition large graphs
