-----

## name: graph
description: >
  Graph data structures and algorithms expertise. Use this skill for implementing graph
  algorithms, designing graph data models, optimizing traversal performance, choosing graph
  databases (Neo4j, Amazon Neptune, ArangoDB), solving pathfinding problems, implementing
  social network analysis, building recommendation engines, and working with property graphs.
  Trigger for any graph data structure, algorithm, or graph database question.
license: MIT
 compatibility: opencode
 metadata:
  audience: developers
  category: data-structures

# Graph Data Structures — Complete Guide

Covers: **Graph Theory · Algorithm Implementation · Database Design · Query Optimization · Traversal Patterns · Network Analysis · Use Cases**

-----

## Graph Fundamentals

### Core Concepts

A graph G = (V, E) consists of:
- **Vertices (V)**: Nodes representing entities
- **Edges (E)**: Relationships between vertices

### Graph Types

**By directionality:**

| Type | Description | Example |
|------|-------------|---------|
| **Directed** | Edges have direction (A → B) | Twitter follows, web pages |
| **Undirected** | Edges have no direction (A — B) | Facebook friends, undirected roads |

**By structure:**

| Type | Description | Example |
|------|-------------|---------|
| **Cyclic** | Contains cycles (paths that return to start) | Social networks |
| **Acyclic** | No cycles allowed | Task dependencies (DAG) |
| **Tree** | Connected acyclic graph | File systems, org charts |
| **Forest** | Disconnected set of trees | Evolutionary trees |

**By edge weight:**

| Type | Description | Example |
|------|-------------|---------|
| **Weighted** | Edges have associated costs | Road distances, prices |
| **Unweighted** | All edges equal | Social connections |

### Graph Representations

**Adjacency Matrix:**
```
     A  B  C  D
  A  0  1  1  0
  B  1  0  0  1
  C  1  0  0  1
  D  0  1  1  0
  
Space: O(V²)
Time to enumerate neighbors: O(V)
```

**Adjacency List:**
```javascript
{
  "A": ["B", "C"],
  "B": ["A", "D"],
  "C": ["A", "D"],
  "D": ["B", "C"]
}

Space: O(V + E)
Time to enumerate neighbors: O(degree(v))
```

**Edge List:**
```javascript
[
  ["A", "B"],
  ["A", "C"],
  ["B", "D"],
  ["C", "D"]
]

Space: O(E)
```

Choose based on graph density and common operations.

-----

## Essential Graph Algorithms

### Breadth-First Search (BFS)

Explores level by level - finds shortest path in unweighted graphs:

```python
from collections import deque

def bfs(graph, start, target):
    visited = {start}
    queue = deque([(start, [start])])
    
    while queue:
        node, path = queue.popleft()
        
        if node == target:
            return path
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None  # No path found

# Example
graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"]
}

print(bfs(graph, "A", "F"))  # ['A', 'C', 'F'] or ['A', 'B', 'E', 'F']
```

**Complexity:** O(V + E) time, O(V) space

**Applications:**
- Shortest path in unweighted graphs
- Level-order tree traversal
- Finding connected components
- Social network "degrees of separation"

### Depth-First Search (DFS)

Explores as deep as possible before backtracking:

```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(f"Visited: {start}")  # Process node
    
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    
    return visited

# Iterative version with stack
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        
        if node not in visited:
            visited.add(node)
            print(f"Visited: {node}")
            
            # Add neighbors in reverse order for consistent ordering
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return visited
```

**Complexity:** O(V + E) time, O(V) space

**Applications:**
- Detecting cycles
- Topological sorting
- Finding strongly connected components
- Maze solving
- Path finding

### Dijkstra's Algorithm

Finds shortest path in weighted graphs (non-negative weights):

```python
import heapq

def dijkstra(graph, start, target):
    # Priority queue: (distance, node, path)
    pq = [(0, start, [start])]
    visited = set()
    
    while pq:
        dist, node, path = heapq.heappop(pq)
        
        if node in visited:
            continue
        
        visited.add(node)
        
        if node == target:
            return (dist, path)
        
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq, (dist + weight, neighbor, path + [neighbor]))
    
    return None  # No path found

# Example weighted graph
graph = {
    "A": [("B", 4), ("C", 2)],
    "B": [("A", 4), ("C", 1), ("D", 5)],
    "C": [("A", 2), ("B", 1), ("D", 8)],
    "D": [("B", 5), ("C", 8)]
}

result = dijkstra(graph, "A", "D")
print(f"Shortest path: {result}")  # (5, ['A', 'C', 'B', 'D'])
```

**Complexity:** O((V + E) log V) with binary heap

**Variants:**
- **A* Algorithm**: Heuristic-guided Dijkstra for faster pathfinding
- **Bellman-Ford**: Handles negative edge weights
- **Floyd-Warshall**: All-pairs shortest paths

### Topological Sort

Ordering vertices in a DAG such that all edges point forward:

```python
def topological_sort(graph):
    # Calculate in-degrees
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
    
    # Start with nodes that have no incoming edges
    queue = [node for node, degree in in_degree.items() if degree == 0]
    result = []
    
    while queue:
        node = queue.pop(0)
        result.append(node)
        
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(result) != len(graph):
        raise ValueError("Graph has a cycle - topological sort not possible")
    
    return result

# Example: Build system dependencies
dependencies = {
    "make": [],
    "gcc": [],
    "linker": ["gcc"],
    "parser": [],
    "compiler": ["parser", "gcc"],
    "assembler": ["parser", "gcc"],
    "executable": ["linker", "compiler", "assembler"]
}

print(topological_sort(dependencies))
# Potential order: ['make', 'gcc', 'parser', 'assembler', 'compiler', 'linker', 'executable']
```

-----

## Graph Data Modeling

### Property Graph Model

Property graphs allow vertices and edges to have attributes:

```cypher
// Neo4j/Cypher example

// Create vertices
CREATE (alice:Person {name: 'Alice', age: 30})
CREATE (bob:Person {name: 'Bob', age: 25})
CREATE (carol:Person {name: 'Carol', age: 28})

// Create edges with properties
CREATE (alice)-[:FRIEND_OF {since: 2020, type: 'close'}]->(bob)
CREATE (alice)-[:FRIEND_OF {since: 2021, type: 'work'}]->(carol)
CREATE (bob)-[:FRIEND_OF {since: 2019}]->(carol)

// Query relationships
MATCH (a:Person {name: 'Alice'})-[r:FRIEND_OF]->(b)
RETURN b.name, r.since, r.type
```

### Common Graph Patterns

**Hierarchical patterns (trees):**
```javascript
// Organization chart
{
  "type": "person",
  "id": "emp_001",
  "name": "CEO Name",
  "reports_to": "emp_000"  // Parent reference
}
```

**Network patterns (social):**
```javascript
{
  "type": "user",
  "id": "user_001",
  "follows": ["user_002", "user_003", "user_004"],
  "followed_by": ["user_005", "user_006"]
}
```

**Flow patterns (processes):**
```javascript
{
  "type": "workflow_node",
  "id": "approve",
  "next": ["notify", "archive"],
  "previous": ["submit", "review"]
}
```

-----

## Graph Database Operations

### Cypher Query Examples (Neo4j)

**Find friends of friends:**
```cypher
MATCH (person:Person {name: 'Alice'})-[:FRIEND_OF]->(friend)-[:FRIEND_OF]->(fof)
WHERE NOT (person)-[:FRIEND_OF]->(fof)
RETURN DISTINCT fof.name
LIMIT 10
```

**Shortest weighted path:**
```cypher
MATCH (start:Location {name: 'A'}), (end:Location {name: 'Z'})
CALL algo.shortestPath(start, end, 'distance')
YIELD path, length
RETURN path, length
```

**Community detection:**
```cypher
CALL algo.labelPropagation('Person', 'FRIEND_OF', {direction: 'BOTH'})
YIELD nodes, iterations, loadMillis, computeMillis, writeMillis
```

### Graph Database Comparison

|Database    |Query Language |Strengths                          |Best For                      |
|------------|--------------|-----------------------------------|------------------------------|
|Neo4j       |Cypher       |Mature, large ecosystem           |Social networks, fraud       |
|Amazon Neptune|Gremlin/SPARQL|Managed, multi-model            |Knowledge graphs              |
|ArangoDB    |AQL          |Multi-model (doc + graph)         |General purpose               |
|JanusGraph  |Gremlin       |Distributed, scalable             |Large graphs                  |
|Orleans     | -            |Virtual actors                    |Distributed systems          |

-----

## Traversal Optimization

### Index-Free Adjacency

Graph databases use index-free adjacency for O(1) neighbor lookups:
- Each vertex stores direct pointers to neighbors
- No index lookups needed during traversal
- Trade-off: Write-heavy workloads may have overhead

### Traversal Strategies

**Depth-first (deep traversal):**
- Use when: Target is far from start, or exploring specific paths
- Memory: O(depth) - more memory efficient
- Risk: May get lost in deep branches

**Breadth-first (wide traversal):**
- Use when: Finding nearest neighbors, shortest path
- Memory: O(width) - can be expensive
- Guarantee: Finds shortest path in unweighted graphs

**Bidirectional search:**
- Use when: Searching between two known nodes
- Complexity: O(b^(d/2)) vs O(b^d) for BFS

### Caching Strategies

```python
# LRU cache for path results
from functools import lru_cache

@lru_cache(maxsize=10000)
def cached_path(graph, start, end):
    return find_path(graph, start, end)
```

-----

## Network Analysis Metrics

### Centrality Measures

**Degree Centrality:**
```python
def degree_centrality(graph):
    return {node: len(neighbors) for node, neighbors in graph.items()}

# For directed graphs, calculate in-degree and out-degree separately
```

**Betweenness Centrality:**
- Measures how often a node lies on shortest paths
- Important for: identifying bridges, bottlenecks

**Closeness Centrality:**
- Average distance to all other nodes
- Important for: identifying accessible nodes

**PageRank:**
- Recursive importance based on incoming links
- Originally developed for web page ranking

### Community Detection

**Girvan-Newman:** Removes edges with highest betweenness
**Louvain:** Optimizes modularity (most common)
**Label Propagation:** Fast, near-linear time

```python
# Simple label propagation
def label_propagation(graph, max_iterations=100):
    labels = {node: node for node in graph}
    
    for _ in range(max_iterations):
        changed = False
        for node in graph:
            neighbor_labels = [labels[neighbor] for neighbor in graph[node]]
            if neighbor_labels:
                most_common = max(set(neighbor_labels), key=neighbor_labels.count)
                if labels[node] != most_common:
                    labels[node] = most_common
                    changed = True
        
        if not changed:
            break
    
    return labels
```

-----

## Practical Applications

### Recommendation Engines

```cypher
// Find friends who bought items that user didn't buy yet
MATCH (user:User {id: 'user_001'})-[:FRIEND_OF]->(friend)-[:BOUGHT]->(item)
WHERE NOT (user)-[:BOUGHT]->(item)
RETURN item.name, COUNT(*) AS score
ORDER BY score DESC
LIMIT 10
```

### Fraud Detection

```cypher
// Find suspicious patterns: shared identifiers between accounts
MATCH (a:Account)-[:HAS_PHONE]->(phone)<-[:HAS_PHONE]-(b:Account)
WHERE a.id <> b.id
WITH a, b, phone
MATCH (a)-[:HAS_EMAIL]->(email)<-[:HAS_EMAIL]-(b)
RETURN a.id, b.id, phone, email
LIMIT 100
```

### Knowledge Graphs

```cypher
// Query entity relationships
MATCH (entity {name: 'Albert Einstein'})-[:WORKED_AT]->(institution)
MATCH (entity)-[:BORN_IN]->(birthplace)
RETURN entity.name, institution.name, birthplace.name
```

-----

## Common Errors to Avoid

- **Confusing directed vs. undirected graphs** in implementation
- **Stack overflow** with recursive DFS on large graphs - use iterative
- **Forgetting visited set** - leads to infinite loops in cycles
- **Using wrong algorithm** - Dijkstra for negative weights (use Bellman-Ford)
- **Memory issues** with adjacency matrix for large sparse graphs
- **Ignoring graph density** when choosing representation
- **Missing handling of disconnected components**
- **Not considering time complexity** - O(V²) can be unacceptable for large graphs
