# GraNT Framework Architecture Diagram

```mermaid
graph TB
    subgraph "User Interface"
        A[Research Goal] --> B[AutoCognition Engine]
    end
    
    subgraph "Workflow Layer"
        B --> C[SEPA Engine]
        C --> D[Template Selection]
        D --> E[Solution Generation]
        E --> F[Outcome Tracking]
        F --> G[Learning Extraction]
        G --> H[Template Evolution]
        H --> C
    end
    
    subgraph "Core Mathematical Layer"
        E --> I[Granular Arithmetic]
        E --> J[Sheaf Attention]
        
        I --> K[Granule Operations]
        K --> K1["⊕ Addition"]
        K --> K2["⊗ Fusion"]
        K --> K3["↓ Projection"]
        
        J --> L[Presheaf Construction]
        L --> M[Cocycle Optimization]
        M --> N[Global Sections]
    end
    
    subgraph "Neural Network Layer"
        N --> O[SheafTransformer]
        O --> P[Embedding Layer]
        P --> Q[Sheaf Attention Layers]
        Q --> R[Output Projection]
        
        Q --> Q1[Multi-Head Cocycle Attention]
        Q1 --> Q2[Residual Connections]
        Q2 --> Q3[Layer Normalization]
    end
    
    subgraph "Output & Deployment"
        R --> S[Solution Artifact]
        S --> T[Code Generation]
        S --> U[Documentation]
        S --> V[Proof Trace]
        S --> W[Performance Metrics]
        
        T --> X[Deploy to Production]
        X --> Y[Edge Devices]
        X --> Z[Cloud Services]
    end
    
    style A fill:#e1f5ff,stroke:#0288d1
    style B fill:#fff9c4,stroke:#f57c00
    style C fill:#f3e5f5,stroke:#7b1fa2
    style I fill:#e8f5e9,stroke:#388e3c
    style J fill:#e8f5e9,stroke:#388e3c
    style O fill:#fce4ec,stroke:#c2185b
    style S fill:#fff3e0,stroke:#e65100
```

## Component Descriptions

### User Interface Layer
- **Research Goal**: Natural language task specification with constraints and metrics

### Workflow Layer
- **AutoCognition Engine**: Main orchestrator
- **SEPA Engine**: Self-Evolving Prompt Architecture for adaptive templates
- **Template Selection**: Multi-armed bandit optimization
- **Solution Generation**: Autonomous architecture design
- **Outcome Tracking**: Persistent performance logging
- **Learning Extraction**: Pattern recognition from history
- **Template Evolution**: Continuous improvement loop

### Core Mathematical Layer
- **Granular Arithmetic**: 
  - ⊕ (Addition): Type-aware combination with confidence min
  - ⊗ (Fusion): Context-preserving aggregation with confidence product
  - ↓ (Projection): Lipschitz-bounded transformation with uncertainty propagation

- **Sheaf Attention**:
  - Presheaf Construction: Hierarchical feature organization
  - Cocycle Optimization: Minimize informational tension
  - Global Sections: Consistent cross-level aggregation

### Neural Network Layer
- **SheafTransformer**: Complete transformer architecture
- **Multi-Head Cocycle Attention**: Parallel attention heads with cohomological constraints
- **Residual Connections**: Skip connections for gradient flow
- **Layer Normalization**: Stable training dynamics

### Output & Deployment
- **Solution Artifact**: Complete package ready for deployment
  - Generated code (PyTorch modules)
  - Documentation (usage guides)
  - Proof traces (mathematical derivations)
  - Performance metrics (latency, memory, accuracy)

- **Deployment Targets**:
  - Edge devices (mobile, IoT)
  - Cloud services (AWS, GCP, Azure)

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant AutoCog as AutoCognition
    participant SEPA
    participant Granule as Granular Math
    participant Sheaf as Sheaf Attention
    participant Model as Neural Network
    
    User->>AutoCog: Submit Research Goal
    AutoCog->>SEPA: Select Template
    SEPA-->>AutoCog: Best Template (ε-greedy)
    
    AutoCog->>Granule: Create Data Granules
    Granule-->>AutoCog: Granule Space with Confidence
    
    AutoCog->>Sheaf: Build Architecture
    Sheaf->>Model: Instantiate SheafTransformer
    Model-->>Sheaf: Configured Model
    
    Sheaf-->>AutoCog: Complete Solution
    AutoCog->>SEPA: Record Outcome
    SEPA->>SEPA: Update Templates (Learn)
    
    AutoCog-->>User: Solution + Documentation
```

## Mathematical Framework

```mermaid
graph LR
    subgraph "Granule Space 𝒢"
        G1["g = (x, μ, τ)"]
        G2["x ∈ X (value)"]
        G3["μ ∈ [0,1] (confidence)"]
        G4["τ ∈ T (type)"]
    end
    
    subgraph "Sheaf Theory"
        S1["F: P^op → Vect"]
        S2["ρ_VU: F(U) → F(V)"]
        S3["δ: C^0 → C^1 (coboundary)"]
        S4["α ∈ Z^1 (cocycle)"]
    end
    
    subgraph "Optimization"
        O1["E(α) = Σ α_ij D_KL(f_j||f_i)"]
        O2["+ λH(α)"]
        O3["min E(α)"]
        O4["s.t. Σ_j α_ij = 1"]
    end
    
    G1 --> S1
    S1 --> S3
    S3 --> S4
    S4 --> O1
    O1 --> O3
    O2 --> O3
    
    style G1 fill:#e8f5e9
    style S1 fill:#e1f5ff
    style O3 fill:#fff9c4
```

## Deployment Pipeline

```mermaid
graph LR
    A[Source Code] --> B[Docker Build]
    B --> C{Target Platform}
    
    C -->|Edge| D[ONNX Export]
    D --> E[Quantization]
    E --> F[Mobile/IoT Deploy]
    
    C -->|Cloud| G[Container Registry]
    G --> H[Kubernetes Cluster]
    H --> I[Auto-scaling]
    
    C -->|Research| J[Jupyter Notebook]
    J --> K[Experiment Tracking]
    K --> L[Publication]
    
    style A fill:#e8f5e9
    style F fill:#fce4ec
    style I fill:#e1f5ff
    style L fill:#fff3e0
```

---

## Key Innovations Visualized

### 1. Uncertainty Propagation

```
Input Granule: g₁ = ([1,2,3], 0.9, VECTOR)
      ↓ (Lipschitz transformation L=1.5)
Project: normalize(·)
      ↓
Output: g₂ = ([0.27,0.53,0.80], 0.87, VECTOR)
                                  ↑
                    Confidence decreased due to L
```

### 2. Cocycle Attention

```
Features: f₁, f₂, ..., fₙ
      ↓
Compute: D_KL(fⱼ || fᵢ) for all pairs
      ↓
Optimize: α* = argmin Σ α_ij D_KL + λH(α)
      ↓
Result: α_ij = softmax(-D_KL(fⱼ||fᵢ)/λ)
```

### 3. Template Evolution

```
Iteration t: Template_v1 → Execute → Metrics → Score
      ↓
Learning: Extract patterns from outcomes
      ↓
Evolution: Template_v2 = Template_v1 + Δ(patterns)
      ↓
Selection: ε-greedy choose between versions
      ↓
Iteration t+1: Best template → Execute → ...
```

---

This architecture enables:
✅ End-to-end autonomous research
✅ Mathematical rigor with practical efficiency
✅ Continuous self-improvement
✅ Production-ready deployment
