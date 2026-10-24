---

## name: multi-agent-systems
description: >
  Multi-agent systems expert for distributed AI, agent-based modeling, and emergent
  behavior. Use this skill whenever the user needs: designing multi-agent architectures,
  building agent-based simulations, implementing coordination protocols, applying game
  theory to agent interactions, simulating emergent phenomena, or any task involving
  multiple interacting autonomous agents. This skill covers agent architectures,
  communication protocols, coordination mechanisms, and applications in robotics,
  distributed systems, and social simulation.
license: MIT
compatibility: opencode
metadata:
  audience: researchers
  category: machine-learning

# Multi-Agent Systems — Distributed AI and Agent-Based Modeling

Covers: **Agent Architectures · Coordination Protocols · Game Theory · Emergent Behavior · Swarms · Distributed AI · Agent Communication · Reinforcement Learning in MAS**

-----

## Agent Architectures

### Types of Agent Architectures

```python
# Base agent class
class Agent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.state = {}
        self.observations = []
        self.actions = []
    
    def perceive(self, environment):
        """Update observations from environment"""
        self.observations = environment.get_observations(self.id)
        return self.observations
    
    def decide(self):
        """Decide on action based on observations"""
        raise NotImplementedError
    
    def act(self, action, environment):
        """Execute action in environment"""
        environment.apply_action(self.id, action)
        self.actions.append(action)
    
    def learn(self, reward):
        """Update internal state based on reward"""
        pass

# Reactive (stimulus-response) agent
class ReactiveAgent(Agent):
    def __init__(self, agent_id, behavior_rules):
        super().__init__(agent_id)
        self.rules = behavior_rules  # {observation_pattern: action}
    
    def decide(self):
        for pattern, action in self.rules.items():
            if self.matches(pattern):
                return action
        return None
    
    def matches(self, pattern):
        """Check if observation matches pattern"""
        return all(self.observations.get(k) == v for k, v in pattern.items())

# Deliberative (planning) agent
class DeliberativeAgent(Agent):
    def __init__(self, agent_id, planner):
        super().__init__(agent_id)
        self.planner = planner
        self.beliefs = {}
        self.desires = []
        self.intentions = []
    
    def decide(self):
        # BDI cycle: beliefs → desires → intentions → planning → execution
        self.update_beliefs()
        self.generate_desires()
        self.filter_intentions()
        return self.planner.plan(self.intentions, self.beliefs)

# Hybrid agent architecture
class HybridAgent(Agent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.reactive_layer = ReactiveLayer()
        self.deliberative_layer = DeliberativeLayer()
        self.meta_reasoner = MetaReasoner()
    
    def decide(self):
        obs = self.observations
        
        # Reactive handles immediate situations
        if self.reactive_layer.applicable(obs):
            return self.reactive_layer.select_action(obs)
        
        # Deliberative handles complex planning
        return self.deliberative_layer.deliberate(obs)
```

### Belief-Desire-Intention (BDI) Model

```python
# BDI Agent Implementation
class BDIAgent:
    def __init__(self, agent_id):
        self.beliefs = {}      # Current world state
        self.desires = []      # Goals to achieve
        self.intentions = []   # Committed goals + plans
        self.plans = {}        # Library of plan recipes
        self.events = []       # External events
    
    def run(self):
        """Main BDI execution cycle"""
        while True:
            # 1. Observe environment
            new_beliefs = self.observe()
            self.beliefs.update(new_beliefs)
            
            # 2. Process events
            self.process_events()
            
            # 3. Reconsider intentions ( Options generation)
            options = self.generate_options()
            
            # 4. Filter options (Deliberation)
            self.deliberate(options)
            
            # 5. Execute current intention
            if self.intentions:
                self.execute_intention()
            
            # 6. Learn from execution
            self.learn()
    
    def generate_options(self):
        """Generate possible actions based on beliefs and desires"""
        options = []
        for desire in self.desires:
            # Check if desire is achievable
            if self.achievable(desire):
                # Get applicable plans
                applicable = self.plans.get_plans(desire, self.beliefs)
                options.extend(applicable)
        return options
    
    def deliberate(self, options):
        """Select intentions from options"""
        # Filter by means-ends
        feasible = [o for o in options if self.appropriate(o)]
        
        # Weight by desire strength and importance
        ranked = self.rank(feasible)
        
        # Commit to top intentions
        self.intentions = ranked[:self.max_intentions]
    
    def execute_intention(self):
        """Execute current intention"""
        intention = self.intentions[0]
        
        if intention.is_plan():
            # Execute next step
            next_action = intention.next_step(self.beliefs)
            return next_action
        else:
            # Atomic action
            return intention
```

-----

## Agent Communication

### Communication Languages

```python
# FIPA ACL message structure
class ACLMessage:
    def __init__(self):
        self.sender = None
        self.receivers = []
        self.performative = None  # request, inform, query, etc.
        self.content = None
        self.language = None
        self.ontology = None
        self.protocol = None
        self.reply_with = None
        self.in_reply_to = None
    
    def to_dict(self):
        return {
            'sender': self.sender,
            'receivers': self.receivers,
            'performative': self.performative,
            'content': self.content,
            'language': self.language,
            'ontology': self.ontology
        }

# FIPA Performatives
fipa_performatives = {
    'request': 'Receiver should perform the action',
    'request_when': 'Receiver should perform when condition is true',
    'request_Whenever': 'Receiver should perform whenever condition becomes true',
    'query_if': 'Ask if a proposition is true',
    'query_ref': 'Ask for a reference matching criteria',
    'inform': 'Inform receiver of truth of proposition',
    'confirm': 'Confirm proposition if true',
    'disconfirm': 'Disconfirm proposition if false',
    'subscribe': 'Subscribe to information',
    'propose': 'Propose action to be performed',
    'accept_proposal': 'Accept proposed action',
    'reject_proposal': 'Reject proposed action'
}

# KQML (Knowledge Query and Manipulation Language)
kqml_performatives = {
    'ask-one': 'Request single response',
    'ask-all': 'Request all matching responses',
    'tell': 'Inform of true proposition',
    'untell': 'Inform that proposition is no longer true',
    'deny': 'Inform of false proposition',
    'insert': 'Add proposition to KB',
    'delete-one': 'Remove one matching proposition',
    'delete-all': 'Remove all matching propositions',
    'achieve': 'Request another agent achieve a state'
}
```

### Message Passing Patterns

```python
# Publish-subscribe communication
class MessageBroker:
    def __init__(self):
        self.subscribers = {}  # topic -> [agents]
        self.message_log = []
    
    def subscribe(self, agent, topic):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        if agent not in self.subscribers[topic]:
            self.subscribers[topic].append(agent)
    
    def publish(self, sender, topic, message):
        msg = {
            'sender': sender,
            'topic': topic,
            'content': message,
            'timestamp': time.time()
        }
        self.message_log.append(msg)
        
        if topic in self.subscribers:
            for agent in self.subscribers[topic]:
                agent.receive_message(msg)

# Direct message passing
class MessagePassingAgent(Agent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.inbox = []
        self.outbox = []
    
    def send_message(self, receiver, message):
        msg = ACLMessage()
        msg.sender = self.id
        msg.receivers = [receiver]
        msg.content = message
        self.outbox.append(msg)
    
    def receive_message(self, message):
        self.inbox.append(message)
```

-----

## Coordination Protocols

### Multi-Agent Coordination Mechanisms

```python
# Contract Net Protocol
class ContractNet:
    def __init__(self):
        self.initiators = []
        self.participants = []
        self.contracts = {}
    
    def initiate_tender(self, initiator, task, deadline):
        """Initiator announces task to participants"""
        call_for_proposals = {
            'type': 'cfp',
            'task': task,
            'deadline': deadline,
            'initiator': initiator
        }
        
        proposals = []
        for participant in self.participants:
            if participant.can_execute(task):
                proposal = participant.make_proposal(task)
                proposals.append(proposal)
        
        # Select best proposal
        best = self.select_best(proposals)
        
        # Award contract
        contract = {
            'initiator': initiator,
            'participant': best.participant,
            'task': task,
            'terms': best.terms
        }
        
        return contract
    
    def select_best(self, proposals):
        """Select best proposal based on criteria"""
        # Rank by cost, capability, reliability
        ranked = sorted(proposals, key=lambda p: p.cost)
        return ranked[0]

# Market-based coordination
class Auction:
    def __init__(self):
        self.bidders = []
        self.current_bid = 0
        self.highest_bidder = None
    
    def english_auction(self, item, starting_price):
        self.current_bid = starting_price
        
        while True:
            # Check for new bids
            new_bids = [b.get_bid(self.current_bid) for b in self.bidders]
            max_bid = max(new_bids)
            
            if max_bid > self.current_bid:
                self.current_bid = max_bid
                self.highest_bidder = self.get_bidder(max_bid)
            else:
                break
        
        return self.highest_bidder, self.current_bid
    
    def dutch_auction(self, item, starting_price):
        """Price decreases until someone bids"""
        price = starting_price
        
        while True:
            bids = [b.accept(price) for b in self.bidders]
            if any(bids):
                winner = self.bidders[bids.index(True)]
                return winner, price
            
            price -= self.price_step
            if price < self.reserve_price:
                return None, None

# Blackboard system
class Blackboard:
    def __init__(self):
        self.knowledge_sources = []
        self.blackboard = {}  # Structured data
    
    def post(self, source, knowledge):
        """Knowledge source posts to blackboard"""
        key = self.make_key(knowledge)
        self.blackboard[key] = {
            'content': knowledge,
            'source': source,
            'timestamp': time.time()
        }
        
        # Notify other knowledge sources
        for ks in self.knowledge_sources:
            if ks.can_use(knowledge):
                ks.trigger(knowledge)
```

### Negotiation Strategies

```python
# Negotiation framework
class NegotiationAgent:
    def __init__(self, agent_id, reservation_value):
        self.id = agent_id
        self.reservation_value = reservation_value
        self.offers_received = []
        self.offers_made = []
    
    def make_offer(self, opponent_history):
        """Generate offer based on opponent's history"""
        # Strategy:Tit-for-tat
        if not opponent_history:
            # First offer: midpoint
            return self.calculate_fair_offer()
        
        last_offer = opponent_history[-1]
        
        # Accept if good enough
        if self.accept(last_offer):
            return 'ACCEPT'
        
        # Otherwise, concede
        return self.concede(last_offer)
    
    def accept(self, offer):
        return offer >= self.reservation_value
    
    def concede(self, last_offer):
        # Linear concession
        return {
            'price': last_offer['price'] * 0.9,
            'quality': last_offer['quality'] * 1.05
        }
```

-----

## Game Theory in Multi-Agent Systems

### Strategic Games

```python
# Normal form game
class NormalFormGame:
    def __init__(self, players, payoff_matrices):
        self.players = players  # List of player IDs
        self.payoff_matrices = payoff_matrices  # {player: matrix}
    
    def get_payoff(self, profile):
        """Get payoff for action profile"""
        return {
            p: self.payoff_matrices[p][profile]
            for p in self.players
        }

# Prisoner's Dilemma
pd_game = NormalFormGame(
    players=['A', 'B'],
    payoff_matrices={
        'A': {  # Rows: A's actions
            ('C', 'C'): 3,  # Both cooperate
            ('C', 'D'): 0,  # A cooperates, B defects
            ('D', 'C'): 5,  # A defects, B cooperates
            ('D', 'D'): 1   # Both defect
        },
        'B': {  # Columns: B's actions
            ('C', 'C'): 3,
            ('C', 'D'): 5,
            ('D', 'C'): 0,
            ('D', 'D'): 1
        }
    }
)

# Nash Equilibrium solver
def find_nash_equilibria(game):
    """Find pure strategy Nash equilibria"""
    equilibria = []
    
    # For small games, check each profile
    for profile in game.payoff_matrices[game.players[0]].keys():
        is_equilibrium = True
        
        # Check each player's unilateral deviation
        for player in game.players:
            current_payoff = game.get_payoff(profile)[player]
            
            # Get all possible deviations
            other_actions = [profile[p] for p in game.players if p != player]
            
            for deviated_action in game.get_actions(player):
                deviated_profile = profile.copy()
                deviated_profile[player] = deviated_action
                
                deviated_payoff = game.get_payoff(deviated_profile)[player]
                
                if deviated_payoff > current_payoff:
                    is_equilibrium = False
                    break
            
            if not is_equilibrium:
                break
        
        if is_equilibrium:
            equilibria.append(profile)
    
    return equilibria
```

### Evolutionary Game Theory

```python
# Replicator dynamics
def replicator_dynamics(population, payoffs, fitness_fn):
    """
    Simulate evolutionary dynamics.
    population: vector of strategy frequencies
    payoffs: payoff matrix
    """
    n = len(population)
    avg_payoff = sum(population[i] * payoffs[i] for i in range(n))
    
    new_population = []
    for i in range(n):
        # Growth rate = fitness - average fitness
        fitness = fitness_fn(payoffs[i], population)
        growth = fitness - avg_payoff
        new_population.append(population[i] * (1 + growth))
    
    # Normalize
    total = sum(new_population)
    return [p / total for p in new_population]
```

-----

## Swarms and Emergent Behavior

### Swarm Intelligence

```python
# Particle Swarm Optimization
class ParticleSwarm:
    def __init__(self, n_particles, dim, fitness_fn):
        self.n_particles = n_particles
        self.dim = dim
        self.fitness_fn = fitness_fn
        
        # Initialize particles
        self.positions = np.random.rand(n_particles, dim)
        self.velocities = np.random.rand(n_particles, dim) * 0.1
        
        # Personal best
        self.p_best = self.positions.copy()
        self.p_best_fitness = [fitness_fn(p) for p in self.positions]
        
        # Global best
        best_idx = np.argmin(self.p_best_fitness)
        self.g_best = self.positions[best_idx].copy()
        self.g_best_fitness = self.p_best_fitness[best_idx]
    
    def update(self, w=0.7, c1=1.5, c2=1.5):
        """Update particle positions"""
        r1, r2 = np.random.rand(2)
        
        # Update velocity
        cognitive = c1 * r1 * (self.p_best - self.positions)
        social = c2 * r2 * (self.g_best - self.positions)
        self.velocities = w * self.velocities + cognitive + social
        
        # Update position
        self.positions += self.velocities
        
        # Update personal best
        for i in range(self.n_particles):
            fitness = self.fitness_fn(self.positions[i])
            if fitness < self.p_best_fitness[i]:
                self.p_best[i] = self.positions[i].copy()
                self.p_best_fitness[i] = fitness
                
                if fitness < self.g_best_fitness:
                    self.g_best = self.positions[i].copy()
                    self.g_best_fitness = fitness
        
        return self.g_best_fitness
```

### Ant Colony Optimization

```python
class AntColony:
    def __init__(self, n_ants, n_cities, distances):
        self.n_ants = n_ants
        self.n_cities = n_cities
        self.distances = distances
        self.pheromones = np.ones((n_cities, n_cities))
        self.alpha = 1.0  # Pheromone importance
        self.beta = 2.0   # Distance importance
        self.evaporation = 0.5
    
    def construct_solutions(self):
        """Construct tours for all ants"""
        solutions = []
        
        for _ in range(self.n_ants):
            tour = [np.random.randint(self.n_cities)]
            
            for _ in range(self.n_cities - 1):
                current = tour[-1]
                next_city = self.select_next(current, tour)
                tour.append(next_city)
            
            solutions.append(tour)
        
        return solutions
    
    def select_next(self, current, visited):
        """Select next city using probabilistic rule"""
        unvisited = [i for i in range(self.n_cities) if i not in visited]
        
        probabilities = []
        for city in unvisited:
            tau = self.pheromones[current][city] ** self.alpha
            eta = (1.0 / self.distances[current][city]) ** self.beta
            probabilities.append(tau * eta)
        
        # Normalize
        probabilities = np.array(probabilities)
        probabilities /= probabilities.sum()
        
        # Roulette wheel selection
        return unvisited[np.random.choice(len(unvisited), p=probabilities)]
    
    def update_pheromones(self, solutions):
        """Update pheromone trails"""
        # Evaporation
        self.pheromones *= (1 - self.evaporation)
        
        # Add new pheromones
        for tour in solutions:
            length = self.tour_length(tour)
            for i in range(len(tour) - 1):
                self.pheromones[tour[i]][tour[j+1]] += 1.0 / length
    
    def tour_length(self, tour):
        return sum(self.distances[tour[i]][tour[i+1]] for i in range(len(tour)-1))
```

-----

## Learning in Multi-Agent Systems

### Multi-Agent Reinforcement Learning

```python
# Independent Q-Learning
class IndependentQLearning:
    def __init__(self, n_agents, state_dim, action_dim, learning_rate=0.1, gamma=0.9):
        self.n_agents = n_agents
        self.q_tables = [
            np.zeros((state_dim, action_dim))
            for _ in range(n_agents)
        ]
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = 1.0
        self.epsilon_decay = 0.99
        self.epsilon_min = 0.01
    
    def select_action(self, agent_id, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.q_tables[agent_id].shape[1])
        else:
            return np.argmax(self.q_tables[agent_id][state])
    
    def update(self, agent_id, state, action, reward, next_state):
        current_q = self.q_tables[agent_id][state, action]
        max_next_q = np.max(self.q_tables[agent_id][next_state])
        
        td_error = reward + self.gamma * max_next_q - current_q
        self.q_tables[agent_id][state, action] += self.lr * td_error
    
    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

# Centralized Training with Decentralized Execution (CTDE)
class CTDEAgent:
    def __init__(self, n_agents):
        self.n_agents = n_agents
        # Centralized critic during training
        self.critic = CentralizedCritic(n_agents)
        # Decentralized actors
        self.actors = [DecentralizedActor() for _ in range(n_agents)]
    
    def train(self, joint_state, joint_action, rewards, next_joint_state):
        # Use global information for training
        critic_loss = self.critic.update(joint_state, joint_action, rewards, next_joint_state)
        
        # Each actor updates based on local observations
        for i, actor in enumerate(self.actors):
            local_obs = joint_state[i]
            actor.update(critic_loss.gradients[i])
        
        return critic_loss
```

-----

## Applications

| Application | Description | Examples |
|-------------|-------------|----------|
| **Robotics** | Multiple robots coordinating | Warehouse robots, drone swarms |
| **Traffic** | Vehicle coordination | Autonomous vehicles, traffic lights |
| **Economics** | Market simulations | Auction systems, trading agents |
| **Social** | Human behavior modeling | Opinion dynamics, segregation |
| **Biology** | Biological systems | Flocking, flocking, immune systems |
| **Resource Management** | Distributed optimization | Sensor networks, cloud computing |

-----

## Common Errors to Avoid

- **Ignoring agent autonomy**: Agents should make own decisions
- **Over-simplifying communication**: Real-world communication is complex
- **Not handling conflicts**: Expect and plan for disagreements
- **Assuming rational agents**: Bounded rationality is more realistic
- **Neglecting scalability**: Test with many agents
- **Ignoring environment dynamics**: Worlds change over time
- **Not considering security**: Malicious agents may exist
- **Confusing emergence with design**: Emergent behavior isn't directly programmed
- **Overlooking partial observability**: Agents rarely see everything
- **Ignoring timing issues**: Communication delays matter
