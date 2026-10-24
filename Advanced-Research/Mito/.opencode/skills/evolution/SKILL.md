---

## name: evolution
description: >
  Evolution expert for understanding biological evolution, adaptation, and speciation. Use
  this skill whenever the user needs: analyzing evolutionary relationships, studying natural
  selection mechanisms, constructing phylogenetic trees, investigating molecular evolution,
  understanding population genetics, or any task involving the scientific study of biological
  evolution. This skill covers evolutionary mechanisms, phylogenetics, molecular evolution,
  population genetics, and evidence for evolution.
license: MIT
compatibility: opencode
metadata:
  audience: evolutionary biologists
  category: biology

# Evolution — Biological Change Over Time

Covers: **Natural Selection · Genetic Drift · Phylogenetics · Molecular Evolution · Population Genetics · Speciation · Adaptation · Human Evolution**

-----

## Mechanisms of Evolution

### Five Forces of Evolution

```python
# Evolution mechanisms
evolution_forces = {
    'mutation': {
        'description': 'Random changes in DNA sequence',
        'type': 'Ultimate source of genetic variation',
        'rate': 'Varies by gene and organism',
        'examples': ['Point mutations', 'Insertions', 'Deletions', 'Duplications']
    },
    'natural_selection': {
        'description': 'Differential reproductive success',
        'result': 'Adaptation to environment',
        'types': ['Directional', 'Stabilizing', 'Disruptive', 'Sexual']
    },
    'genetic_drift': {
        'description': 'Random change in allele frequencies',
        'effect': 'Stronger in small populations',
        'types': ['Founder effect', 'Bottleneck']
    },
    'gene_flow': {
        'description': 'Movement of genes between populations',
        'effect': 'Reduces genetic differentiation',
        'examples': ['Migration', 'Hybridization']
    },
    'non_random_mating': {
        'description': 'Assortative or disassortative mating',
        'effect': 'Changes genotype frequencies',
        'examples': ['Inbreeding', 'Sexual selection']
    }
}
```

### Natural Selection

```python
# Selection coefficient calculation
def selection_coefficient(w1, w2):
    """
    Calculate selection coefficient.
    w1, w2: Fitness values (0-1)
    """
    if w1 == 0:
        return 1.0
    return 1 - (w2 / w1)

def allele_frequency_change(p, q, s, t):
    """
    Calculate allele frequency change under selection.
    p: Frequency of dominant allele
    q: Frequency of recessive allele  
    s: Selection coefficient against dominant
    t: Selection coefficient against recessive
    """
    delta_p = (p * q * (p * s - q * t)) / (1 - s * p**2 - t * q**2)
    return delta_p

# Types of selection
selection_types = {
    'directional': {
        'description': 'One extreme favored over other',
        'result': 'Shift in mean phenotype',
        'example': 'Antibiotic resistance in bacteria'
    },
    'stabilizing': {
        'description': 'Intermediate phenotype favored',
        'result': 'Reduced variance',
        'example': 'Human birth weight'
    },
    'disruptive': {
        'description': 'Both extremes favored',
        'result': 'Increased variance, possible speciation',
        'example': 'African finch beak size'
    },
    'balancing': {
        'description': 'Multiple alleles maintained',
        'result': 'Polymorphism',
        'example': 'Sickle cell and malaria resistance'
    },
    'sexual': {
        'description': 'Traits affecting mating success',
        'result': 'Sexual dimorphism',
        'example': 'Peacock tail, deer antlers'
    }
}
```

### Genetic Drift

```python
# Wright-Fisher model
def wright_fisher_model(N, p, generations):
    """
    Simulate genetic drift using Wright-Fisher model.
    N: Population size (diploid)
    p: Initial allele frequency
    generations: Number of generations
    """
    p_history = [p]
    current_p = p
    
    for gen in range(generations):
        # Number of alleles
        2N = 2 * N
        
        # Binomial sampling
        n_A = np.random.binomial(2N, current_p)
        current_p = n_A / 2N
        
        p_history.append(current_p)
    
    return p_history

# Effective population size
def effective_population_size(Nm, Nf):
    """
    Calculate effective population size.
    Nm: Number of males
    Nf: Number of females
    """
    if Nm + Nf == 0:
        return 0
    return (4 * Nm * Nf) / (Nm + Nf)

# Founder effect and bottleneck
founder_bottleneck = {
    'founder_effect': {
        'description': 'New population started by small group',
        'result': 'Reduced genetic diversity',
        'examples': ['Galapagos finches', 'Hawaiian islands species']
    },
    'bottleneck': {
        'description': 'Population temporarily reduced',
        'result': 'Loss of rare alleles',
        'examples': ['Northern elephant seal', 'Cheetah']
    }
}
```

-----

## Population Genetics

### Hardy-Weinberg Equilibrium

```python
# Hardy-Weinberg proportions
def hardy_weinberg_proportions(p, q=None):
    """
    Calculate genotype frequencies under HWE.
    p: Frequency of dominant allele
    q: Frequency of recessive allele (computed if not given)
    """
    if q is None:
        q = 1 - p
    
    return {
        'AA': p**2,      # Homozygous dominant
        'Aa': 2 * p * q, # Heterozygous
        'aa': q**2       # Homozygous recessive
    }

def test_hardy_weinberg(observed_AA, observed_Aa, observed_aa, N):
    """
    Test for Hardy-Weinberg equilibrium using chi-square test.
    """
    # Total number of alleles
    total_alleles = 2 * N
    
    # Observed allele frequencies
    p = (2 * observed_AA + observed_Aa) / total_alleles
    q = 1 - p
    
    # Expected under HWE
    expected_AA = p**2 * N
    expected_Aa = 2 * p * q * N
    expected_aa = q**2 * N
    
    # Chi-square test
    chi_square = ((observed_AA - expected_AA)**2 / expected_AA +
                  (observed_Aa - expected_Aa)**2 / expected_Aa +
                  (observed_aa - expected_aa)**2 / expected_aa)
    
    # Degrees of freedom = 1 (one allele frequency estimated)
    # Critical value at p=0.05 with df=1 is 3.84
    return chi_square, chi_square < 3.84

# Fixation index (Fst)
def calculate_fst(populations):
    """
    Calculate Wright's Fst to measure population differentiation.
    """
    # Heterozygosity within populations (Hs)
    # Total heterozygosity (Ht)
    # Fst = (Ht - Hs) / Ht
    pass
```

### Molecular Population Genetics

```python
# Tajima's D
def tajima_d(seq1, seq2, theta_estimates):
    """
    Calculate Tajima's D test statistic.
    Tests for selection using frequency spectrum.
    """
    # Based on differences between theta estimates
    # Positive D: balancing selection or bottleneck
    # Negative D: directional selection or population expansion
    pass

# McDonald-Kreitman test
def mckreitman_test(aligned_sequences):
    """
    Test for positive selection using MK test.
    Compare substitution rates in:
    - Fixed differences between species (divergence)
    - Polymorphism within species
    """
    # Count fixed substitutions
    # Count polymorphic sites
    # Use G-test for independence
    pass
```

-----

## Phylogenetics

### Phylogenetic Methods

```python
# Distance-based methods
distance_methods = {
    'UPGMA': {
        'name': 'Unweighted Pair Group Method with Arithmetic Mean',
        'assumptions': 'Molecular clock',
        'strength': 'Simple, fast',
        'weakness': 'Assumes clock-like evolution'
    },
    'neighbor_joining': {
        'name': 'Neighbor-Joining',
        'assumptions': 'None (correct tree for additive distances)',
        'strength': 'Does not assume clock',
        'weakness': 'Can produce negative branch lengths'
    }
}

# Character-based methods
character_methods = {
    'maximum_parsimony': {
        'description': 'Find tree requiring fewest changes',
        'strength': 'Fast, simple',
        'weakness': 'May not find most likely tree'
    },
    'maximum_likelihood': {
        'description': 'Find tree maximizing likelihood given model',
        'strength': 'Uses explicit evolutionary model',
        'weakness': 'Computationally intensive'
    },
    'bayesian': {
        'description': 'Sample from posterior distribution of trees',
        'strength': 'Provides uncertainty estimates',
        'weakness': 'Computationally intensive'
    }
}
```

### Tree Building

```python
# Simple neighbor-joining implementation
def neighbor_joining(distance_matrix, labels):
    """
    Build phylogenetic tree using NJ algorithm.
    """
    n = len(distance_matrix)
    active = set(range(n))
    tree = {}
    
    while len(active) > 2:
        # Calculate Q matrix
        Q = np.zeros((n, n))
        for i in active:
            for j in active:
                if i != j:
                    r_i = sum(distance_matrix[i, k] for k in active if k != i)
                    r_j = sum(distance_matrix[j, k] for k in active if k != j)
                    Q[i, j] = (n - 2) * distance_matrix[i, j] - r_i - r_j
        
        # Find minimum Q
        min_q = float('inf')
        min_pair = None
        for i in active:
            for j in active:
                if i < j and Q[i, j] < min_q:
                    min_q = Q[i, j]
                    min_pair = (i, j)
        
        i, j = min_pair
        
        # Calculate branch lengths
        r_i = sum(distance_matrix[i, k] for k in active if k != i)
        r_j = sum(distance_matrix[j, k] for k in active if k != j)
        
        dist_ij = distance_matrix[i, j]
        branch_i = (dist_ij + (r_i - r_j) / (n - 2)) / 2
        branch_j = dist_ij - branch_i
        
        # Record in tree
        # ... (implementation details)
        
        # Update distance matrix
        # ... (implementation details)
    
    # Connect final two nodes
    # Return tree
```

### Molecular Clock

```python
# Molecular clock hypothesis
molecular_clock = {
    'hypothesis': 'Mutations accumulate at constant rate',
    'neutral_theory': 'Most mutations are neutral',
    'applications': [
        'Dating divergence events',
        'Estimating species ages',
        'Molecular phylogenetics'
    ],
    'caveats': [
        'Rates vary across lineages',
        'Rate heterogeneity possible',
        'Generation time effects'
    ]
}

def calculate_divergence_time(distance, rate):
    """
    Calculate divergence time from genetic distance.
    """
    return distance / (2 * rate)

# Calibration points
calibration_types = {
    'paleontological': 'Fossil ages',
    'geological': 'Vicariance events',
    'biological': 'Known hybridization/crossing',
    'historical': 'Documented events'
}
```

-----

## Molecular Evolution

### dN/dS Ratio

```python
# dN/dS (Ka/Ks) analysis
def calculate_ka_ks(sequence1, sequence2, genetic_code='standard'):
    """
    Calculate synonymous (dS) and nonsynonymous (dN) substitutions.
    """
    # Identify synonymous and nonsynonymous sites
    # Count substitutions in each category
    # Apply appropriate substitution model
    pass

def interpret_ka_ks(ratio):
    """
    Interpret dN/dS ratio.
    """
    if ratio < 1:
        return 'Purifying (negative) selection'
    elif ratio == 1:
        return 'Neutral evolution'
    else:
        return 'Positive selection'

# Example interpretation
ka_ks_interpretation = {
    'ratio_less_1': {
        'interpretation': 'Purifying selection',
        'meaning': 'Deleterious mutations removed'
    },
    'ratio_1': {
        'interpretation': 'Neutral',
        'meaning': 'No selective pressure'
    },
    'ratio_greater_1': {
        'interpretation': 'Positive selection',
        'meaning': 'Adaptive evolution at site'
    }
}
```

### Positive Selection

```python
# Detecting positive selection
selection_detection = {
    'site_models': {
        'M1a': 'Nearly neutral (two categories)',
        'M2a': 'Adds positive selection category',
        'M7': 'Beta distribution (10 categories)',
        'M8': 'Beta + ω > 1 category'
    },
    'branch_models': {
        'one_ratio': 'Single ω for all branches',
        'foreground': 'Different ω for foreground branch'
    },
    'branch_site_models': {
        'A': 'Allow ω > 1 on foreground branches at some sites',
        'null': 'ω ≤ 1 everywhere'
    }
}
```

-----

## Speciation

### Modes of Speciation

```python
speciation_modes = {
    'allopatric': {
        'description': 'Geographic isolation',
        'barriers': ['Mountains', 'Rivers', 'Oceans', 'Distance'],
        'prevalence': 'Most common in animals'
    },
    'parapatric': {
        'description': 'Adjacent ranges with some overlap',
        'mechanism': 'Differential selection across gradient',
        'example': 'Ring species'
    },
    'sympatric': {
        'description': 'Reproductive isolation without geography',
        'mechanism': 'Ecological differentiation, sexual selection',
        'prevalence': 'Common in plants, some insects'
    },
    'peripatric': {
        'description': 'Small population at edge of range',
        'mechanism': 'Founder effect + selection'
    }
}

# Reproductive isolation
reproductive_isolation = {
    'prezygotic': {
        'habitat': 'Different habitats',
        'temporal': 'Different timing',
        'behavioral': 'Sexual isolation',
        'mechanical': 'Incompatible genitalia',
        'gametic': 'Gamete incompatibility'
    },
    'postzygotic': {
        'hybrid_inviability': 'Hybrid dies',
        'hybrid_sterility': 'Hybrid sterile',
        'hybrid_breakdown': 'F2 hybrids have problems'
    }
}
```

### Adaptive Radiation

```python
adaptive_radiation = {
    'definition': 'Rapid diversification of single lineage',
    'requirements': [
        'Ecological opportunity',
        'Available niches',
        'Key innovation',
        'Few competitors'
    ],
    'classic_examples': [
        'Darwin\'s finches (Galapagos)',
        'Hawaiian honeycreepers',
        'Cichlid fish (African lakes)',
        'Marsupials (Australia)'
    ],
    'stages': [
        '1. Colonization of new area',
        '2. Ecological release',
        '3. Divergence and adaptation',
        '4. Coexistence through niche partitioning'
    ]
}
```

-----

## Human Evolution

### Hominin Evolution

```python
hominin_lineage = {
    'sahelanthropus_tchadensis': {
        'date': '7-6 million years ago',
        'location': 'Chad',
        'features': ['Bipedal', 'Small brain']
    },
    'ardipithecus_ramidus': {
        'date': '4.4 million years ago',
        'location': 'Ethiopia',
        'features': ['Arborial', 'Bipedal']
    },
    'australopithecus_afarensis': {
        'date': '3.9-2.9 million years ago',
        'location': 'East Africa',
        'features': ['Lucy', 'Fully bipedal', 'Small brain']
    },
    'homo_habilis': {
        'date': '2.4-1.4 million years ago',
        'location': 'Africa',
        'features': ['Stone tools', 'Larger brain']
    },
    'homo_erectus': {
        'date': '1.9-0.1 million years ago',
        'location': 'Africa, Asia',
        'features': ['Fire', 'Acheulean tools', 'Out of Africa'
    },
    'homo_neanderthalensis': {
        'date': '400,000-40,000 years ago',
        'location': 'Europe, Asia',
        'features': ['Complex tools', 'Burial', 'Large brain']
    },
    'homo_sapiens': {
        'date': '300,000 years ago to present',
        'location': 'Worldwide',
        'features': ['Modern behavior', 'Language', 'Art']
    }
}
```

### Evidence for Human Evolution

```python
human_evolution_evidence = {
    'fossil_record': [
        'Skull shape changes',
        'Pelvic structure',
        'Dental changes',
        'Bipedal adaptations'
    ],
    'molecular': [
        'DNA similarity to great apes',
        'Mitochondrial Eve',
        'Y-chromosome Adam',
        'Neanderthal admixture'
    ],
    'comparative': [
        'Embryonic development',
        'Vestigial structures',
        'Atavisms',
        'Molecular homology'
    ],
    'behavioral': [
        'Tool use',
        'Art and symbolism',
        'Language',
        'Social organization'
    ]
}
```

-----

## Evidence for Evolution

### Types of Evidence

| Evidence Type | Description | Examples |
|---------------|-------------|----------|
| **Fossil** | Remains in rock layers | Transitional forms |
| **Comparative Anatomy** | Homologous structures | Forelimbs of mammals |
| **Molecular** | DNA/protein similarities | Cytochrome c |
| **Biogeography** | Geographic distribution | Island species |
| **Direct Observation** | Real-time change | Antibiotic resistance |

```python
# Molecular clock evidence
molecular_evidence = {
    'cytochrome_c': {
        'organisms_compared': 'Humans and chimpanzees',
        'differences': '0 differences',
        'interpretation': 'Recent common ancestor'
    },
    'hemoglobin': {
        'similarity': 'Humans and mice have ~85% similarity',
        'interpretation': 'Shared ancestry'
    },
    'endogenous_retroviruses': {
        'description': 'Viral DNA integrated into genome',
        'evidence': 'Same ERV loci in related species',
        'interpretation': 'Common ancestry'
    }
}
```

-----

## Common Errors to Avoid

- **Confusing evolution with progress**: Evolution has no direction
- **Thinking evolution is random**: Selection is not random, mutation is
- **Ignoring genetic drift**: Especially important in small populations
- **Conflating correlation with causation**: Environment influences traits
- **Misunderstanding "survival of the fittest"**: Not about strongest
- **Ignoring the role of chance**: Genetic drift, founder effects
- **Assuming humans are "more evolved"**: All lineages evolve equally
- **Confusing species concepts**: Biological, phylogenetic, morphological
- **Not understanding "junk DNA"**: Much has regulatory functions
- **Ignoring gene regulation**: Most evolution is regulatory changes
