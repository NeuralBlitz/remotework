---

## name: genetic-algorithms
description: >
  Expert genetic algorithm assistant for machine learning engineers and researchers. Use this skill whenever the user needs:
  implementing evolutionary algorithms, designing genetic representations, creating fitness functions, implementing selection 
  and crossover operators, handling mutation, or any rigorous implementation of genetic algorithms. Covers single and 
  multi-objective optimization, neural architecture search, and real-world applications.
license: MIT
compatibility: opencode
metadata:
  audience: machine-learning-engineers
  category: artificial-intelligence

# Genetic Algorithms — Academic Research Assistant

Covers: **Evolutionary Computation · Selection Operators · Crossover Strategies · Mutation · Fitness Functions · Multi-Objective Optimization · Neural Architecture Search · Real-World Applications**

---

## Algorithm Fundamentals

### Genetic Algorithm Flow

```
┌──────────────┐
│   Population │◀──────────────┐
│   Generation │                │
└──────┬───────┘               │
       │                       │
       ▼                       │
┌──────────────┐    ┌─────────┐│
│   Evaluate   │    │ Select ││
│   Fitness    │───▶│ Parents││
└──────────────┘    └────┬────┘
                       │
                       ▼
                ┌─────────────┐
                │  Crossover  │
                │   + Mutate  │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   Replace   │
                │  Population │
                └──────┬──────┘
                       │
                       ▼
                ┌──────────────┐
                │   Continue?  │
                └──────────────┘
```

### Key Parameters

|Parameter| Typical Range | Effect |
|---------|---------------|--------|
|Population size|50-500|Larger = better exploration, slower|
|Mutation rate|0.01-0.3|Higher = more diversity, slower convergence|
|Crossover rate|0.6-0.95|High = keep good solutions|
|Elitism count|1-10|Preserve best solutions|
|Generations|100-1000|Depends on problem complexity|

---

## Selection Operators

### Tournament Selection

```python
class TournamentSelection:
    """Tournament selection implementation"""
    
    def __init__(self, tournament_size=3):
        self.tournament_size = tournament_size
    
    def select(self, population, fitnesses):
        """
        Select one individual via tournament
        Best fitness = higher value (maximization)
        """
        selected = []
        n = len(population)
        
        for _ in range(n):
            # Random tournament contestants
            indices = random.sample(range(n), self.tournament_size)
            tournament_fitness = [fitnesses[i] for i in indices]
            
            # Winner takes all
            winner_idx = indices[tournament_fitness.index(max(tournament_fitness))]
            selected.append(population[winner_idx].copy())
        
        return selected
    
    # Binary tournament = fast, less selection pressure
    # Larger tournament = higher selection pressure
```

### Roulette Wheel Selection

```python
class RouletteSelection:
    """Roulette (fitness proportional) selection"""
    
    def select(self, population, fitnesses):
        # Normalize fitness (handle negative values)
        min_fit = min(fitnesses)
        if min_fit < 0:
            fitnesses = [f - min_fit for f in fitnesses]
        
        total = sum(fitnesses)
        if total == 0:
            return random.choices(population, k=len(population))
        
        # Wheel selection
        selected = []
        for _ in range(len(population)):
            r = random.random() * total
            cumulative = 0
            for i, fit in enumerate(fitnesses):
                cumulative += fit
                if cumulative >= r:
                    selected.append(population[i].copy())
                    break
        
        return selected
```

### Rank-Based Selection

```python
class RankSelection:
    """Rank-based selection - more stable than roulette"""
    
    def __init__(self, selection_pressure=1.5):
        self.selection_pressure = selection_pressure  # 1-2 typical
    
    def select(self, population, fitnesses):
        # Sort by fitness
        sorted_pairs = sorted(zip(population, fitnesses), 
                            key=lambda x: x[1])
        
        n = len(population)
        ranks = list(range(1, n + 1))
        
        # Calculate selection probability based on rank
        # Linear ranking: P(i) = (2 - SP)/N + 2(i-1)(SP-1)/(N(N-1))
        probabilities = []
        for rank in ranks:
            prob = (2 - self.selection_pressure) / n + \
                   2 * (rank - 1) * (self.selection_pressure - 1) / (n * (n - 1))
            probabilities.append(prob)
        
        # Normalize
        total = sum(probabilities)
        probabilities = [p/total for p in probabilities]
        
        # Select
        selected = random.choices(population, weights=probabilities, k=n)
        return [s.copy() for s in selected]
```

---

## Crossover Operators

### Single-Point Crossover

```
Parent 1: [A B C D E F G H]
Parent 2: [1 2 3 4 5 6 7 8]

           ↓ Crossover point = 4

Child 1:  [A B C D 5 6 7 8]
Child 2:  [1 2 3 4 E F G H]
```

### Two-Point Crossover

```
Parent 1: [A B C D E F G H]
Parent 2: [1 2 3 4 5 6 7 8]

           ↓ Points = 2, 6

Child 1:  [A B 3 4 5 6 G H]
Child 2:  [1 2 C D E F 7 8]
```

### Uniform Crossover

```
Parent 1: [A B C D E F G H]
Parent 2: [1 2 3 4 5 6 7 8]

Random mask: [1 0 1 0 0 1 0 1]

Child 1:  [A 2 C D 5 F G H]
Child 2:  [1 B 3 4 E 6 7 8]
```

### Arithmetic Crossover (Real-Valued)

```python
class CrossoverOperators:
    """Collection of crossover operators"""
    
    @staticmethod
    def single_point(parent1, parent2):
        """Single-point crossover for lists"""
        if len(parent1) != len(parent2):
            raise ValueError("Parents must have same length")
        
        if random.random() > 0.8:  # Crossover rate
            return parent1.copy(), parent2.copy()
        
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        
        return child1, child2
    
    @staticmethod
    def uniform(parent1, parent2, swap_prob=0.5):
        """Uniform crossover"""
        child1, child2 = [], []
        for g1, g2 in zip(parent1, parent2):
            if random.random() < swap_prob:
                child1.append(g2)
                child2.append(g1)
            else:
                child1.append(g1)
                child2.append(g2)
        
        return child1, child2
    
    @staticmethod
    def arithmetic(parent1, parent2, alpha=0.5):
        """Linear arithmetic crossover for real values"""
        child = []
        for g1, g2 in zip(parent1, parent2):
            child.append(alpha * g1 + (1 - alpha) * g2)
        
        return child
    
    @staticmethod
    def simulated_binary(SBX, parent1, parent2, eta=15):
        """
        Simulated Binary Crossover (SBX)
        Similar to single-point for real-valued GA
        eta: distribution index (higher = children close to parents)
        """
        child1, child2 = [], []
        
        for x1, x2 in zip(parent1, parent2):
            if random.random() < 0.5:
                if abs(x1 - x2) > 1e-14:
                    if random.random() < 0.5:
                        beta = random.betavariate(eta + 1, eta + 1)
                    else:
                        beta = 1 + (2 * (x1 - x2) / abs(x1 - x2))
                    
                    beta **= 1.0 / (eta + 1)
                    child1.append(0.5 * ((1 + beta) * x1 + (1 - beta) * x2))
                    child2.append(0.5 * ((1 - beta) * x1 + (1 + beta) * x2))
                else:
                    child1.append(x1)
                    child2.append(x2)
            else:
                child1.append(x1)
                child2.append(x2)
        
        return child1, child2
```

---

## Mutation Operators

### Bit Flip Mutation

```
Before: [1 0 1 1 0 0 1 0]
After:  [1 0 0 1 0 0 1 0]  (bit 3 flipped)
```

### Gaussian Mutation

```python
class MutationOperators:
    """Collection of mutation operators"""
    
    @staticmethod
    def gaussian(individual, mutation_strength=0.1, probability=0.1):
        """Gaussian mutation for real-valued genes"""
        mutated = []
        
        for gene in individual:
            if random.random() < probability:
                # Add Gaussian noise
                gene += random.gauss(0, mutation_strength)
            
            mutated.append(gene)
        
        return mutated
    
    @staticmethod
    def polynomial(individual, eta=20, probability=0.1):
        """
        Polynomial mutation for real-valued GA
        eta: distribution index
        """
        mutated = []
        
        for gene in individual:
            if random.random() < probability:
                delta_l = gene - 0  # Lower bound
                delta_u = 1 - gene   # Upper bound (assuming [0,1])
                
                if random.random() < 0.5:
                    delta_q = (2 * random.random()) ** (1.0 / (eta + 1)) - 1
                    gene += delta_q * delta_l
                else:
                    delta_q = 1 - (2 * (1 - random.random())) ** (1.0 / (eta + 1))
                    gene += delta_q * delta_u
            
            mutated.append(gene)
        
        return mutated
    
    @staticmethod
    def swap(individual):
        """Swap mutation - swap two positions"""
        if len(individual) < 2:
            return individual
        
        idx1, idx2 = random.sample(range(len(individual)), 2)
        mutated = individual.copy()
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
        
        return mutated
    
    @staticmethod
    def scramble(individual):
        """Scramble mutation - shuffle subset"""
        if len(individual) < 2:
            return individual
        
        start, end = sorted(random.sample(range(len(individual)), 2))
        subset = individual[start:end+1]
        random.shuffle(subset)
        
        return individual[:start] + subset + individual[end+1:]
```

---

## Multi-Objective Optimization

### Non-Dominated Sorting (NSGA-II)

```python
class MultiObjectiveGA:
    """Multi-objective genetic algorithm (NSGA-II inspired)"""
    
    def dominates(self, fitness1, fitness2):
        """Check if solution1 dominates solution2"""
        better_in_any = False
        
        for f1, f2 in zip(fitness1, fitness2):
            if f1 > f2:  # Maximization
                return False
            if f1 < f2:
                better_in_any = True
        
        return better_in_any
    
    def fast_non_dominated_sort(self, population, fitness_matrix):
        """Sort population into Pareto fronts"""
        n = len(population)
        domination_count = [0] * n
        dominated_sets = [[] for _ in range(n)]
        fronts = [[]]
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    if self.dominates(fitness_matrix[i], fitness_matrix[j]):
                        dominated_sets[i].append(j)
                    elif self.dominates(fitness_matrix[j], fitness_matrix[i]):
                        domination_count[i] += 1
            
            if domination_count[i] == 0:
                fronts[0].append(i)
        
        current_front = 0
        while fronts[current_front]:
            next_front = []
            for i in fronts[current_front]:
                for j in dominated_sets[i]:
                    domination_count[j] -= 1
                    if domination_count[j] == 0:
                        next_front.append(j)
            
            current_front += 1
            if next_front:
                fronts.append(next_front)
        
        return fronts[:-1] if not fronts[-1] else fronts
    
    def crowding_distance(self, fitness_matrix, front):
        """Calculate crowding distance for diversity preservation"""
        n = len(front)
        if n <= 2:
            return {i: float('inf') for i in front}
        
        distances = {i: 0 for i in front}
        
        for obj in range(len(fitness_matrix[0])):
            # Sort by objective
            sorted_front = sorted(front, key=lambda x: fitness_matrix[x][obj])
            
            # Boundary points get infinite distance
            distances[sorted_front[0]] = float('inf')
            distances[sorted_front[-1]] = float('inf')
            
            # Calculate range
            obj_range = fitness_matrix[sorted_front[-1]][obj] - \
                       fitness_matrix[sorted_front[0]][obj]
            
            if obj_range == 0:
                continue
            
            # Interior points
            for i in range(1, n - 1):
                distances[sorted_front[i]] += \
                    (fitness_matrix[sorted_front[i+1]][obj] - 
                     fitness_matrix[sorted_front[i-1]][obj]) / obj_range
        
        return distances
```

---

## Neural Architecture Search

### Evolutionary Architecture Search

```python
class NeuroEvolution:
    """Neural network architecture evolution"""
    
    def __init__(self, max_layers=10, max_neurons=512):
        self.max_layers = max_layers
        self.max_neurons = max_neurons
    
    def create_random_architecture(self):
        """Generate random network architecture"""
        n_layers = random.randint(1, self.max_layers)
        architecture = []
        
        for i in range(n_layers):
            n_neurons = random.choice([16, 32, 64, 128, 256, 512])
            activation = random.choice(['relu', 'tanh', 'sigmoid'])
            
            layer = {
                'neurons': n_neurons,
                'activation': activation,
                'dropout': random.uniform(0, 0.5)
            }
            
            # Can add skip connections, attention, etc.
            if i > 0 and random.random() < 0.2:
                layer['skip_to'] = random.randint(0, i - 1)
            
            architecture.append(layer)
        
        return architecture
    
    def mutate_architecture(self, architecture):
        """Mutate an architecture"""
        mutation = random.choice(['add_layer', 'remove_layer', 
                                'change_neurons', 'change_activation',
                                'change_dropout', 'add_skip'])
        
        mutated = [layer.copy() for layer in architecture]
        
        if mutation == 'add_layer' and len(mutated) < self.max_layers:
            new_layer = {
                'neurons': random.choice([16, 32, 64, 128]),
                'activation': random.choice(['relu', 'tanh']),
                'dropout': random.uniform(0, 0.3)
            }
            idx = random.randint(0, len(mutated))
            mutated.insert(idx, new_layer)
        
        elif mutation == 'remove_layer' and len(mutated) > 1:
            idx = random.randint(0, len(mutated) - 1)
            mutated.pop(idx)
        
        elif mutation == 'change_neurons':
            layer = random.choice(mutated)
            layer['neurons'] = random.choice([16, 32, 64, 128, 256, 512])
        
        # ... other mutations
        
        return mutated
    
    def crossover_architectures(self, arch1, arch2):
        """Crossover two architectures"""
        if len(arch1) != len(arch2):
            # Different lengths - random choice
            return random.choice([arch1, arch2]).copy()
        
        # Same length - crossover
        child = []
        for layer1, layer2 in zip(arch1, arch2):
            if random.random() < 0.5:
                child.append(layer1.copy())
            else:
                child.append(layer2.copy())
        
        return child
```

---

## Common Errors to Avoid

1. **Poor fitness function design** — Fitness must capture true optimization goals
2. **Premature convergence** — Too high selection pressure, too low mutation
3. **Ignoring parameter tuning** — GA performance highly parameter-dependent
4. **No diversity preservation** — Use niching or crowding
5. **Inappropriate representation** — Binary vs. real-valued affects everything
6. **Not using elitism** — Risk losing best solutions
7. **Overcomplicating operators** — Simple often works better
8. **Insufficient generations** — Too early stopping misses optimal
9. **Ignoring constraint handling** — Must handle infeasible solutions
10. **Not comparing to baselines** — GA not always best choice

