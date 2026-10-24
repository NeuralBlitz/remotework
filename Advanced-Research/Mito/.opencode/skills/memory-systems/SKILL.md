-----

## name: memory-systems
description: >
  Expert memory systems assistant for computer architects and engineers. Use this skill whenever the user needs:
  help with memory hierarchy, cache design, virtual memory, or understanding memory technologies.
  Includes both theoretical foundations and practical implementation guidance.
trigger: Any computer architecture problem involving memory - from cache optimization to virtual memory management.
license: MIT
compatibility: opencode
metadata:
  audience: engineers
  category: computer-hardware

# Memory Systems — Hierarchy, Technology, and Architecture

Covers: **Cache Memory · Virtual Memory · DRAM · SRAM · Memory Controllers · Coherence · Non-Volatile Memory**

-----

## Memory Hierarchy

### Why Hierarchy?

Speed vs. cost trade-off:
- Fast: expensive, small
- Slow: cheap, large

Goal: hide latency with caching.

### Hierarchy Levels

| Level | Typical Size | Latency | Technology |
|-------|-------------|---------|------------|
| Registers | < 1 KB | < 1 ns | SRAM |
| L1 Cache | 32-64 KB | 1-2 ns | SRAM |
| L2 Cache | 256 KB-1 MB | 3-10 ns | SRAM |
| L3 Cache | 1-64 MB | 10-30 ns | eDRAM |
| Main Memory | GB | 50-100 ns | DRAM |
| Storage | TB | ms | NAND/HDD |

### Temporal Locality

Recently accessed items likely accessed again.
Implemented by keeping data in cache.

### Spatial Locality

Items near recently accessed likely accessed.
Implemented by loading cache blocks (lines).

### Cache Block (Line)

Unit of transfer between levels:
- Typical: 64 bytes
- May include spatial prefetch

### Fully Associative

Any block can go anywhere:
- Most flexible
- Expensive: CAM + comparator

### Direct-Mapped

Each address maps to exactly one location:
- Simple hardware
- May have conflicts

### Set-Associative

Hybrid: n ways:
- Block location = (block address) mod (number of sets)
- Within set, fully associative

Common: 2-way, 4-way, 8-way, 16-way.

### Cache Mapping Summary

| Type | Speed | Hardware Cost |
|------|-------|---------------|
| Direct | Fastest | Lowest |
| Set-assoc | Medium | Medium |
| Fully-assoc | Slowest | Highest |

### Write Policies

**Write-through**: Write to cache and memory.
- Simple, coherent
- Higher memory bandwidth

**Write-back**: Write to cache only.
- Write to memory on eviction.
- Better performance.

### Write Miss Policies

**Write-allocate**: Load block, then write.
**No-write-allocate**: Write directly to memory.

### Cache Performance

```
AMAT = Hit time + Miss rate × Miss penalty
```

### Miss Categories

| Type | Cause | Solution |
|------|-------|----------|
| Compulsory | First access | Prefetch |
| Capacity | Evicted due to size | Increase cache |
| Conflict | Too many to same set | Increase associativity |

### Inclusion/Exclusion

**Inclusive**: Lower level contains all in higher.
**Exclusive**: Cannot be in both.
**Victim cache**: Small fully-assoc for evicted lines.

-----

## Cache Optimizations

### Multi-Level Caches

Design L1 for hit time:
- Small, fast
- May be split I/D

Design L2 for miss rate:
- Larger, slower
- Higher associativity

### Split vs. Unified

Split: separate I and D caches.
- Allows simultaneous access
- More flexible

### Victim Cache

Small fully-associative cache:
- Holds recently evicted lines
- Reduces conflict misses

### Prefetching

Hardware: stream prefetchers.
Software: prefetch instructions.
- Effective for regular access patterns

### Non-blocking Caches

Allow hits under misses:
- Miss status holding register
- Critical word first

### Cache Compression

Reduce effective miss rate:
- Compress lines
- Decompress on hit

### Way Prediction

Predict which way to access:
- Reduce tag check time
- Recovery on mispredict

### Pseudo-associativity

Two sections, fast check first:
- Like 2-way, behaves like direct

-----

## Virtual Memory

### Why Virtual Memory?

- Simplify programming
- Provide isolation
- Enable overcommitment
- Extend address space

### Address Translation

Virtual address (VA) → Physical address (PA):
- Page table walks
- Translation lookaside buffer (TLB)

### Page Size Trade-offs

Large pages:
- Fewer entries
- More internal fragmentation

Small pages:
- Fine-grained
- More page table entries

Common: 4 KB base, 2 MB large, 1 GB huge.

### Page Tables

Map VPN → PPN + attributes:
- Valid, dirty, accessed
- Can be large for 64-bit

### Hierarchical Page Tables

Multi-level:
- Page directory
- Page table
- Offset

x86-64: 4-level, IA-32e.

### TLB (Translation Lookaside Buffer)

Cache recent translations:
- Fully-associative or set-assoc
- Small: 32-512 entries

### TLB Performance

TLB hit → single cycle.
TLB miss → page table walk (expensive).

### TLB Improvements

- Larger TLB
- Substantial page sizes
- ASID (Address Space ID)
- TLB prefetching

### Page Faults

Page not in memory:
- OS loads from disk
- May involve eviction
- Can be 10⁶ cycles

### Demand Paging

Load pages on first access.
Working set: pages actively used.

### Replacement Policies

- LRU: Least Recently Used
- Clock: approximated LRU
- FIFO: First In, First Out
- Random: random eviction

### Working Set Model

Set of pages process needs:
- Monitored by OS
- Thrashing when exceeds memory

### Inverted Page Table

Hash table: physical → virtual:
- Smaller
- Slower access

### Page Table Entry (PTE)

Contains:
- Physical frame number
- Valid bit
- Protection bits
- Dirty bit
- Reference bit

### Protection

- Read, write, execute
- User vs. kernel
- NX (no execute)

-----

## DRAM Technology

### DRAM Basics

Capacitor stores charge:
- 1T1C cell
- Refresh required

### DRAM Organization

Bank → Row → Column:
- Open row: faster access
- Precharge to close

### DRAM Timing

Parameters:
- t_RCD: RAS to CAS delay
- t_CAS: CAS latency
- t_RP: precharge time
- t_RAS: row active time

### DDR SDRAM

Double data rate:
- Transfer on rising and falling
- DDR4: 2133-3200 MT/s

### DDR Generations

| Standard | Data Rate | Voltage |
|----------|-----------|---------|
| DDR | 200-400 MT/s | 2.5 V |
| DDR2 | 400-800 MT/s | 1.8 V |
| DDR3 | 800-2133 MT/s | 1.5 V |
| DDR4 | 2133-3200 MT/s | 1.2 V |
| DDR5 | 4800-8400 MT/s | 1.1 V |

### DRAM Channels

Multiple channels:
- Increase bandwidth
- Independent access

### Memory Controller

Manages DRAM:
- Address mapping
- Timing
- Refresh
- Error correction

### ECC (Error-Correcting Code)

Detect and correct errors:
- SECDED: single error correct, double detect
- Multi-bit detection with stronger codes

### Row Hammer

Repeated access causes bit flips:
- Counter: targeted refresh
- Error correction helps

### Low Power DRAM

LPDDR:
- Mobile devices
- Lower power, lower performance

### High Bandwidth Memory (HBM)

Stacked DRAM:
- 3D integration
- Very high bandwidth

### HBM2

Stacks:
- 4-8 dies
- Through-silicon vias
- Wide interfaces

-----

## SRAM Technology

### SRAM Basics

Cross-coupled inverters:
- 6T cell
- No refresh needed
- Stable when powered

### SRAM Characteristics

- Fast access (~ns)
- High power
- Low density
- Expensive per bit

### Cache Implementation

SRAM for L1-L3 caches:
- Trade-off speed vs. density

### SRAM Scaling

Challenges:
- Leakage current
- Variability
- Process variation

### Register Files

Specialized SRAM:
- Multiple ports
- High speed critical

-----

## Memory Controllers

### Controller Functions

- Command scheduling
- Refresh
- Error detection/correction
- Power management

### Address Mapping

Interleaving across banks/channels:
- Reduce latency
- Increase bandwidth

### Command Scheduling

Reorder commands:
- Hide latency
- Maximize parallelism

### Open/Closed Page Policy

Open: keep row open.
- Better for sequential
- Worse for random

Closed: precharge after access.
- Better for random
- Predictable

### Adaptive Policies

Learn access patterns:
- Switch between open/closed

### Refresh Management

Self-refresh:
- Low power mode
- Important for mobile

### Memory Scheduling

First-ready, first-come-first-served (FR-FCFS):
- Prioritize critical requests

### Page Policy Migration

Change policy per page:
- Hardware learning

-----

## Cache Coherence

### The Coherence Problem

Multiple caches may have different data.
Need consistent view.

### Write Invalidate vs. Write Update

Invalidate: mark other copies stale.
Update: push new value to others.

### MESI Protocol

States:
- Modified: exclusive, dirty
- Exclusive: exclusive, clean
- Shared: shared, clean
- Invalid: not present

### MOESI

Add Owned state:
- Owned: dirty, sharable

### Directory-Based

Track sharing:
- Point-to-point messages
- Scales to many cores

### Snooping

Broadcast all transactions:
- All caches listen
- Scales poorly

### False Sharing

Different variables, same cache line:
- Causes coherence traffic
- Padding can fix

### Coherence Traffic

Increases with cores:
- Limits scalability
- Optimize layout

### Cache Affinity

Keep data near using core:
- Reduces coherence
- Improves performance

-----

## Memory Consistency

### Sequential Consistency

All loads and stores appear in order.
- Intuitive but slow

### Total Store Order (TSO)

Store buffer:
- Reads can bypass writes
- x86 model

### Relaxed Consistency

Weaker guarantees:
- Release consistency
- Weak ordering

### fences

Force ordering:
- mfence (all)
- sfence (store)
- lfence (load)

### Atomics

Atomic read-modify-write:
- lock prefix on x86
- ldrex/strex on ARM

### Performance vs. Correctness

Weaker models faster:
- Allow hardware optimizations
- Programmer must use fences

-----

## Non-Volatile Memory

### NVM Technologies

- Flash (NAND, NOR)
- MRAM
- ReRAM (Resistive)
- PCM (Phase Change)
- 3D XPoint

### Flash Memory

Floating gate transistor:
- Charge trapped
- Retains without power

### NAND Flash

High density:
- Page-based read/write
- Block-based erase

### Flash Limitations

- Limited writes per block
- Erase before write
- Wear leveling needed

### NOR Flash

Executable:
- Random access
- Lower density

### MRAM

Magnetic tunnel junction:
- Fast, durable
- Expensive

### ReRAM

Resistance change:
- Bipolar
- Multi-level possible

### PCM

Phase change:
- Amorphous/crystalline
- Good endurance

### 3D XPoint

Intel Optane:
- Non-volatile
- Between DRAM and NAND

### NVM Use Cases

- Storage-class memory
- Fast boot
- Persistent memory

### Memory Persistence

Ensure durability:
- Cache flush
- Write barriers

-----

## Memory System Design

### Bandwidth Analysis

Calculate needed:
- Peak bandwidth
- Sustained bandwidth

### Latency Budget

Where time goes:
- Critical path
- Queueing delays

### Capacity Planning

Working set:
- Profile application
- Size caches

### Memory-Centric Computing

Processing in memory:
- Reduce data movement
- Novel architectures

### Processing-in-Memory

Near memory logic:
- Reduce energy
- Increase bandwidth

### Near-Memory Computing

Stacked memory with logic:
- High bandwidth
- Limited compute

### Computational Storage

Drive-integrated compute:
- Filters at storage

### Optical Memory

Future technology:
- Low latency interconnect

### Emerging Technologies

- DNA storage
- Racetrack memory
- Spin transfer torque MRAM

-----

## Performance Optimization

### Memory Profiling

Identify hot spots:
- Cache misses
- Memory bandwidth

### Cache Blocking

Algorithm restructure:
- Fit in cache
- Reduce misses

### Loop Tiling

Block loops:
- Better cache use
- Balance computation/I/O

### Array of Structures vs. Structure of Arrays

SoA often better:
- SIMD friendly
- Better spatial locality

### Padding and Alignment

Avoid false sharing:
- Cache line align critical data

### Prefetching

Hardware or software:
- Hide latency
- Intelligent algorithms

### NUMA Awareness

Multi-socket systems:
- Local vs. remote access
- Data placement

### Memory DAX

Direct access:
- Bypass page cache
- Persistent memory

### Huge Pages

Reduce TLB misses:
- 2 MB or 1 GB pages
- Kernel support

### Memory Compression

Reduce memory pressure:
- Compress cold pages
- Transparent

### Memory Error Handling

Detect and correct:
- ECC
- Retry on error

-----

## Common Errors to Avoid

- Confusing cache size with capacity
- Ignoring write-through vs. write-back trade-offs
- Not considering associativity effects
- Using wrong replacement policy for workload
- Ignoring memory latency in performance models
- Confusing virtual memory with physical
- Not understanding TLB miss cost
- Overlooking coherence overhead
- Ignoring NUMA effects
- Using incorrect memory ordering
- Forgetting about memory bandwidth
- Not considering memory power

-----

## Key References

- **Computer Organization and Design** by Patterson & Hennessy
- **Memory Systems** by Jacob, Ng, Wang
- **Computer Architecture: A Quantitative Approach**
- **Modern Processor Design** by Shen and Lipasti

