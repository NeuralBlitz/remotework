-----

## name: document
description: >
  Document data model expertise for building modern applications. Use this skill for:
  designing document schemas, implementing NoSQL patterns, optimizing query performance,
  choosing document databases (MongoDB, CouchDB, Firestore), handling nested data structures,
  managing JSON/BSON data, implementing eventual consistency, and scaling document stores.
  Trigger for any document database, schema design, or NoSQL architecture question.
license: MIT
 compatibility: opencode
 metadata:
  audience: developers
  category: databases

# Document Data Model — Comprehensive Guide

Covers: **Schema Design · Query Optimization · Database Selection · Data Modeling · Scaling Patterns · Transaction Handling · Migration Strategies**

-----

## Document Database Fundamentals

### Core Concepts

Document databases store data as JSON-like documents, offering:
- **Flexible schema**: No fixed schema required; documents can have varying structures
- **Rich data types**: Support for arrays, nested objects, dates, binary data
- **Hierarchical data**: Natural fit for tree-like and nested data structures
- **Dynamic queries**: Query any field without predefined indexes

### When to Choose Document Databases

**Ideal use cases:**
- Content management systems (CMS)
- Catalog and inventory management
- User profiles and session storage
- Real-time analytics with variable schemas
- Rapid prototyping and MVP development
- IoT data ingestion with varying sensor data

**When NOT to choose:**
- Complex relational data with many-to-many relationships requiring joins
- ACID-compliant transactional systems (banking, inventory)
- Highly normalized data with rigid schema requirements
- Complex aggregations requiring multi-document transactions

### Popular Document Databases

|Database    |Vendor/Project      |Strengths                                    |Use Cases                        |
|------------|-------------------|--------------------------------------------|---------------------------------|
|MongoDB     |MongoDB Inc.      |Mature, large ecosystem, aggregation        |Web apps, mobile backends       |
|CouchDB     |Apache             |Sync, conflict resolution, REST API         |Offline-first, distributed       |
|CouchBase   |CouchBase Inc.    |Enterprise features, N1QL                  |Enterprise, caching              |
|Firebase    |Google             |Real-time, mobile SDKs                     |Mobile apps, real-time features |
|Amazon DocDB|AWS                |MongoDB compatibility, managed              |AWS-native applications         |

-----

## Schema Design Patterns

### Flexible Schema Principles

Document databases embrace schema flexibility, but thoughtful design improves queryability:

```
# Good: Self-contained documents
{
  "orderId": "ORD-12345",
  "customer": {
    "id": "CUST-001",
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "items": [
    {"productId": "PROD-001", "qty": 2, "price": 29.99},
    {"productId": "PROD-002", "qty": 1, "price": 49.99}
  ],
  "total": 109.97,
  "createdAt": "2024-01-15T10:30:00Z"
}

# Avoid: Normalized references requiring joins
{
  "orderId": "ORD-12345",
  "customerId": "CUST-001",  // Requires separate lookup
  "itemIds": ["PROD-001", "PROD-002"]  // Requires separate lookups
}
```

### Embedding vs. Referencing

**Embedding (denormalized):**
- Use for: 1:few, 1:many where child data is always accessed with parent
- Example: User document with embedded address array
- Benefits: Single query, no joins, atomic updates
- Risks: Document size growth, duplication

**Referencing (normalized):**
- Use for: 1:many where child data is accessed independently
- Example: Blog posts with referenced comments (thousands per post)
- Benefits: Smaller documents, flexible queries
- Risks: Multiple queries or $lookup operations

### Schema Versioning

Implement versioning for schema evolution:

```javascript
// Document with version tracking
{
  "_id": "prod_001",
  "_schemaVersion": 2,
  "name": "Product Name",
  "pricing": {  // v2: restructured from flat "price" field
    "amount": 29.99,
    "currency": "USD"
  },
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

### Common Anti-Patterns

- **Over-normalization**: Mimicking relational tables defeats document advantages
- **Excessive embedding**: Embedding arrays that grow unbounded
- **No indexing strategy**: Creating collections without query pattern analysis
- **Ignoring document size limits**: Most databases have 16MB document limits
- **Mixed access patterns**: Documents optimized for reads won't suit heavy writes

-----

## Query Optimization

### Indexing Strategies

**Single field indexes:**
```javascript
db.products.createIndex({ "category": 1 })
db.products.createIndex({ "price": -1 })
```

**Compound indexes:**
```javascript
// For queries like: db.products.find({ category: "electronics", price: { $lt: 500 } })
db.products.createIndex({ "category": 1, "price": -1 })
```

**Multikey indexes (arrays):**
```javascript
// Index every element in the tags array
db.products.createIndex({ "tags": 1 })
```

**Text indexes:**
```javascript
db.products.createIndex({ "description": "text", "name": "text" })
```

### Index Design Guidelines

|Query Pattern                    |Index Recommendation                 |
|---------------------------------|-------------------------------------|
|Exact match on single field     |Single field index                   |
|Range queries + equality        |Compound: equality first, range last |
|Full-text search                |Text index                           |
|Sort on specific fields         |Cover sort fields                    |
|Geo queries                     |2dsphere index                       |

### Query Analysis

Use explain plans to optimize:
```javascript
db.collection.find({ field: value }).explain("executionStats")
```

Key metrics to analyze:
- **totalDocsExamined**: Should be close to nReturned
- **indexUsed**: Verify correct index selected
- **executionTimeMillis**: Target < 100ms for user-facing queries

### Projection Optimization

Fetch only required fields:
```javascript
// Instead of fetching full documents
db.products.find({ category: "electronics" }, { name: 1, price: 1, _id: 0 })
```

-----

## Data Modeling Case Studies

### E-commerce Product Catalog

```javascript
// Products collection
{
  "_id": "prod_001",
  "sku": "ELEC-001",
  "name": "Wireless Headphones",
  "description": "Premium noise-cancelling headphones",
  "category": ["electronics", "audio", "wireless"],
  "pricing": {
    "current": 299.99,
    "original": 349.99,
    "currency": "USD"
  },
  "inventory": {
    "warehouseA": 45,
    "warehouseB": 23,
    "total": 68
  },
  "attributes": {
    "brand": "AudioTech",
    "color": "black",
    "weight": "250g",
    "batteryLife": "30 hours"
  },
  "ratings": {
    "average": 4.5,
    "count": 1247
  },
  "variants": [
    { "color": "black", "sku": "ELEC-001-BLK" },
    { "color": "white", "sku": "ELEC-001-WHT" },
    { "color": "blue", "sku": "ELEC-001-BLU" }
  ],
  "createdAt": "2023-06-15T00:00:00Z"
}
```

### User Profile with Activity

```javascript
// Users collection
{
  "_id": "user_001",
  "username": "johndoe",
  "profile": {
    "firstName": "John",
    "lastName": "Doe",
    "avatar": "https://cdn.example.com/avatars/user_001.jpg",
    "bio": "Software engineer passionate about databases"
  },
  "preferences": {
    "theme": "dark",
    "notifications": { "email": true, "push": false },
    "language": "en-US"
  },
  "stats": {
    "postsCount": 156,
    "followersCount": 2341,
    "followingCount": 189
  },
  "createdAt": "2020-03-15T00:00:00Z",
  "lastLoginAt": "2024-01-20T14:30:00Z"
}
```

### IoT Sensor Readings

```javascript
// readings collection (time-series pattern)
{
  "_id": ObjectId(),
  "deviceId": "sensor_001",
  "timestamp": ISODate("2024-01-15T10:00:00Z"),
  "readings": {
    "temperature": 22.5,
    "humidity": 65.2,
    "pressure": 1013.25
  },
  "location": {
    "type": "Point",
    "coordinates": [-122.4194, 37.7749]
  },
  "battery": 87,
  "status": "normal"
}
```

-----

## Scaling Patterns

### Horizontal Scaling (Sharding)

Sharding distributes data across clusters:
- **Shard key selection** is critical: choose high-cardinality, frequently queried fields
- Avoid: monotonically increasing keys as shard keys (hotspotting)
- Good candidates: userId, geographic region, date ranges

```javascript
// Enable sharding on database
sh.enableSharding("myapp")

// Shard collection by region
sh.shardCollection("myapp.users", { "region": 1, "userId": 1 })
```

### Read Replicas

Configure replica sets for:
- **Read scaling**: Distribute read load
- **High availability**: Automatic failover
- **Geographic distribution**: Local reads for users

```
Primary → Secondary (sync)
    ↓
Secondary (async)
    ↓
Secondary (async)
```

### Write Concern Levels

|wlevel    |Description                           |Use Case                    |
|----------|--------------------------------------|----------------------------|
|0         |Don't wait for acknowledgment        |Analytics, logging          |
|1         |Wait for primary acknowledgment       |Default                     |
|majority  |Wait for majority replicas           |Critical data               |
|{w: "all"}|Wait for all replicas                |Maximum consistency         |

-----

## Transaction Handling

### Single Document Atomicity

Document databases provide atomic operations on single documents:
```javascript
// Atomic update - either all succeed or none
db.orders.updateOne(
  { _id: "order_001" },
  {
    $set: { status: "processing" },
    $push: { items: { productId: "prod_001", qty: 1 } }
  }
)
```

### Multi-Document Transactions (MongoDB 4.0+)

For ACID operations across documents:
```javascript
const session = db.getMongo().startSession();

session.startTransaction({
  readConcern: { level: "snapshot" },
  writeConcern: { level: "majority" }
});

try {
  session.withTransaction(() => {
    const db1 = session.getDatabase("orders");
    const db2 = session.getDatabase("inventory");

    db1.orders.insertOne({ _id: "order_001", total: 99.99 });
    db2.inventory.updateOne(
      { productId: "prod_001", qty: { $gte: 1 } },
      { $inc: { qty: -1 } }
    );
  });
} finally {
  session.endSession();
}
```

### Optimistic Concurrency

Implement version-based concurrency control:
```javascript
// Only update if version matches (no concurrent modification)
db.documents.updateOne(
  { _id: "doc_001", version: 5 },
  {
    $set: { data: newData, version: 6 },
    $set: { updatedAt: new Date() }
  }
)
```

-----

## Migration Strategies

### Schema Migration Patterns

**Phase 1: Add new field, maintain old**
```javascript
// Migration script
db.products.find({ price: { $exists: true } }).forEach(doc => {
  db.products.updateOne(
    { _id: doc._id },
    {
      $set: {
        pricing: {
          current: doc.price,
          currency: "USD"
        }
      }
    }
  );
});
```

**Phase 2: Update application code to use new field**

**Phase 3: Remove old field**
```javascript
db.products.updateMany(
  {},
  { $unset: { price: "" } }
)
```

### Data Migration Best Practices

- **Backup first**: Always backup before migration
- **Test on staging**: Validate migration logic before production
- **Batch processing**: Process in chunks to avoid memory issues
- **Add progress tracking**: Log migration progress for recovery
- **Verify post-migration**: Run validation queries

-----

## Common Errors to Avoid

- **No schema thinking**: Even flexible schemas need design discipline
- **Ignoring indexing costs**: Indexes consume memory and slow writes
- **Over-embedding**: Unbounded arrays cause document bloat
- **Missing data validation**: Documents can contain invalid data
- **Inefficient queries**: N+1 patterns in application code
- **Ignoring eventual consistency**: Reads may return stale data
- **No connection pooling**: Creating new connections per request
- **Storing large files in documents**: Use GridFS or object storage for files > 16MB
