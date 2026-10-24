---
name: ray
description: >
  Expert guidance on Ray distributed computing framework for scaling AI and Python 
  applications. Use for: distributed training, hyperparameter tuning with Ray Tune, 
  reinforcement learning with Ray RLlib, model serving with Ray Serve, batch inference, 
  scaling Python applications from single machines to clusters, and Ray Core tasks and actors.
license: MIT
compatibility: opencode
metadata:
  audience: ml-engineers, data-scientists
  category: distributed-computing
  tags: [ray, distributed-computing, machine-learning, scaling]
---

# Ray — Distributed Computing for AI

Covers: **Ray Core · Distributed Training · Ray Tune · Ray RLlib · Ray Serve · Ray Datasets**

-----

## Understanding Ray

### What is Ray?

Ray is a distributed computing framework designed to scale Python applications from a single machine to a large cluster. Originally developed at UC Berkeley's RISELab, Ray provides a unified set of primitives for building distributed applications, making it particularly well-suited for machine learning workloads.

Ray addresses the challenge of distributing Python code across multiple machines without requiring developers to become distributed systems experts. It provides a simple API that abstracts away the complexities of cluster management, fault tolerance, and inter-process communication.

**Core Components:**

- **Ray Core** — The foundational distributed computing primitives: tasks, actors, and objects.

- **Ray Tune** — Scalable hyperparameter optimization with support for various search algorithms and schedulers.

- **Ray RLlib** — Reinforcement learning library with distributed training support and many built-in algorithms.

- **Ray Serve** — Scalable model serving framework for building production inference services.

- **Ray Datasets** — Distributed data processing for ML workloads, integrated with popular data formats.

### When to Use Ray

| Use Case | Recommended Ray Component |
|----------|---------------------------|
| Parallelizing Python functions | Ray Tasks |
| Stateful services with shared memory | Ray Actors |
| Hyperparameter tuning | Ray Tune |
| Reinforcement learning | Ray RLlib |
| Model serving | Ray Serve |
| Large-scale data processing | Ray Datasets |
| Distributed training | Ray Train |

-----

## Ray Core Fundamentals

### Ray Tasks (Stateless Functions)

Ray tasks are stateless functions that can be executed asynchronously across a Ray cluster. They're ideal for parallelizing pure functions that don't require maintaining state between invocations.

```python
import ray
import time
from typing import List

# Initialize Ray
ray.init()

# Define a function to be executed remotely
@ray.remote
def download_url(url: str) -> str:
    """Simulate downloading content from a URL"""
    import random
    # Simulate network delay
    time.sleep(random.uniform(0.5, 2.0))
    return f"Content from {url}"

@ray.remote
def process_content(content: str) -> int:
    """Process content and return result"""
    # Simulate some processing
    return len(content)

# Execute tasks remotely
urls = [
    "https://example.com/article1",
    "https://example.com/article2",
    "https://example.com/article3",
    "https://example.com/article4",
    "https://example.com/article5"
]

# Launch all downloads in parallel
download_futures = [download_url.remote(url) for url in urls]

# Wait for all to complete and get results
contents = ray.get(download_futures)

# Chain with processing
process_futures = [process_content.remote(content) for content in contents]
results = ray.get(process_futures)

print(f"Processed {len(results)} URLs, results: {results}")

# For larger workflows, use ray.get with timeout
# results = ray.get(futures, timeout=30)
```

### Ray Actors (Stateful Services)

Ray actors are stateful workers that maintain state across method calls. They're perfect for scenarios where you need shared state, counters, or services that benefit from keeping data in memory.

```python
import ray
from dataclasses import dataclass

ray.init()

@dataclass
class TrainingMetrics:
    epoch: int
    loss: float
    accuracy: float

@ray.remote
class ParameterServer:
    """Parameter server for distributed training"""
    
    def __init__(self):
        self.parameters = {}
        self.version = 0
    
    def get_parameters(self, key: str) -> dict:
        return self.parameters.get(key, {})
    
    def update_parameters(self, key: str, updates: dict):
        if key not in self.parameters:
            self.parameters[key] = {}
        self.parameters[key].update(updates)
        self.version += 1
        return self.version

@ray.remote
class DataLoader:
    """Distributed data loader actor"""
    
    def __init__(self, data_path: str, batch_size: int = 32):
        self.data_path = data_path
        self.batch_size = batch_size
        self.current_index = 0
        self.data = self._load_data()
    
    def _load_data(self):
        # Load data (simplified)
        import numpy as np
        return np.random.randn(1000, 10)
    
    def get_batch(self) -> List[List[float]]:
        start = self.current_index
        end = min(start + self.batch_size, len(self.data))
        
        if start >= len(self.data):
            self.current_index = 0
            start = 0
            end = min(self.batch_size, len(self.data))
        
        batch = self.data[start:end].tolist()
        self.current_index = end
        
        return batch
    
    def reset(self):
        self.current_index = 0
        return True

# Create actors
ps = ParameterServer.remote()
loader = DataLoader.remote("/data/train.csv", batch_size=32)

# Interact with actors
ray.get(ps.update_parameters.remote("model_v1", {"weights": [1, 2, 3]}))
params = ray.get(ps.get_parameters.remote("model_v1"))
batch = ray.get(loader.get_batch.remote())

# Get actor handle from within another actor
# Inside another actor:
# ray.get(loader.get_batch.remote())
```

### Resource Management

```python
import ray

ray.init(num_cpus=4, num_gpus=1)

# Specify resource requirements for tasks
@ray.remote(num_cpus=2, num_gpus=0.5)
def train_model_batch(data, config):
    """Train a model on a batch using GPU"""
    import torch
    # Training code here
    return {"loss": 0.5, "accuracy": 0.9}

# Use custom resources for specific hardware
@ray.remote(resources={"GPU_TYPE_A100": 1})
def run_on_a100():
    return "Running on A100 GPU"

# Actor resource management
@ray.remote(num_cpus=1, num_gpus=0.25)
class GPUWorker:
    def __init__(self):
        self.device = "cuda:0"
    
    def process(self, data):
        # Process on GPU
        return len(data)

# Automatic resource allocation with placement groups
placement_group = ray.util.placement_group(
    [{"CPU": 2, "GPU": 1}],
    strategy="PACK"
)

@ray.remote(num_cpus=2, num_gpus=1)
def scheduled_task():
    return "Running in placement group"

# Wait for placement group to be ready
ray.get(scheduled_task.options(
    placement_group=placement_group,
    placement_group_bundle_index=0
).remote())
```

-----

## Ray Tune (Hyperparameter Optimization)

### Basic Configuration

```python
import ray
from ray import tune

ray.init(num_cpus=4)

def trainable_function(config: dict):
    """Training function to optimize"""
    import time
    import numpy as np
    
    # Extract hyperparameters
    learning_rate = config.get("learning_rate", 0.01)
    batch_size = config.get("batch_size", 32)
    hidden_units = config.get("hidden_units", 64)
    dropout = config.get("dropout", 0.1)
    
    # Simulate training
    metrics = {"loss": 1.0, "accuracy": 0.1}
    
    for step in range(100):
        # Simulate training loop
        loss = np.random.uniform(0.1, 1.0) * (learning_rate / 0.01)
        accuracy = 1.0 - loss + np.random.uniform(-0.1, 0.1)
        
        # Report metrics to Tune
        tune.report(
            loss=loss,
            accuracy=max(0, min(1, accuracy)),
            step=step,
            learning_rate=learning_rate
        )
        
        time.sleep(0.1)
    
    return {"loss": loss, "accuracy": accuracy}

# Run basic search
analysis = tune.run(
    trainable_function,
    config={
        "learning_rate": tune.choice([0.001, 0.01, 0.1]),
        "batch_size": tune.choice([16, 32, 64, 128]),
        "hidden_units": tune.choice([32, 64, 128, 256]),
        "dropout": tune.uniform(0.0, 0.5)
    },
    num_samples=20,
    metric="loss",
    mode="min",
    verbose=1
)

# Get best configuration
best_config = analysis.best_config
best_loss = analysis.best_result["loss"]
print(f"Best config: {best_config}")
print(f"Best loss: {best_loss}")
```

### Advanced Search Strategies

```python
from ray import tune
from ray.tuners import Tuner
import ray

ray.init(num_cpus=8)

# Bayesian Optimization with Optuna
def optimize_with_optuna(search_space):
    from ray.tune.search.optuna import OptunaSearch
    
    optuna_search = OptunaSearch(
        metric="accuracy",
        mode="max",
        points_to_evaluate=[
            {"learning_rate": 0.01, "batch_size": 32}
        ]
    )
    
    return tune.Tuner(
        trainable_function,
        tune_config=tune.TuneConfig(
            search_alg=optuna_search,
            num_samples=50,
            time_budget_s=3600  # 1 hour
        ),
        param_space=search_space
    )

# HyperBand for early stopping
def run_with_hyperband(search_space):
    return tune.Tuner(
        trainable_function,
        tune_config=tune.TuneConfig(
            scheduler=tune.schedulers.HyperBandScheduler(
                time_attr="step",
                max_t=100,
                stop_last_triple=True
            ),
            num_samples=100,
            max_concurrent_trials=8
        ),
        param_space=search_space
    )

# Population-Based Training (PBT)
def run_with_pbt(search_space):
    return tune.Tuner(
        trainable_function,
        tune_config=tune.TuneConfig(
            scheduler=tune.schedulers.PopulationBasedTraining(
                time_attr="step",
                perturbation_interval=10,
                hyperparam_mutations={
                    "learning_rate": tune.loguniform(1e-4, 1e-2),
                    "dropout": tune.uniform(0.0, 0.5)
                }
            ),
            num_samples=20
        ),
        param_space=search_space
    )

# Define search space
search_space = {
    "learning_rate": tune.loguniform(1e-4, 1e-2),
    "batch_size": tune.choice([16, 32, 64, 128]),
    "hidden_units": tune.choice([64, 128, 256, 512]),
    "dropout": tune.uniform(0.0, 0.5),
    "optimizer": tune.choice(["adam", "sgd", "rmsprop"]),
    "activation": tune.choice(["relu", "tanh", "gelu"])
}

# Run with PBT (often best for neural network tuning)
analysis = run_with_pbt(search_space).fit()
```

### Custom Trainables

```python
from ray import tune
import numpy as np

class CustomTrainable(tune.Trainable):
    """Custom trainable with state management"""
    
    def setup(self, config):
        """Initialize training state"""
        self.model = Model(config)
        self.optimizer = Optimizer(self.model, config["learning_rate"])
        self.step_count = 0
        
        # Load data
        self.train_data = np.random.randn(1000, 10)
        self.labels = np.random.randint(0, 2, 1000)
    
    def step(self):
        """Execute one training step"""
        # Sample batch
        indices = np.random.choice(len(self.train_data), 32)
        batch_x = self.train_data[indices]
        batch_y = self.labels[indices]
        
        # Train
        loss = self.model.train_step(batch_x, batch_y)
        accuracy = self.model.evaluate(batch_x, batch_y)
        
        self.step_count += 1
        
        return {
            "loss": loss,
            "accuracy": accuracy,
            "step": self.step_count
        }
    
    def save_checkpoint(self, checkpoint_dir):
        """Save checkpoint"""
        path = f"{checkpoint_dir}/model.npy"
        np.save(path, self.model.weights)
        return path
    
    def load_checkpoint(self, checkpoint_path):
        """Load checkpoint"""
        self.model.weights = np.load(checkpoint_path)


class Model:
    def __init__(self, config):
        self.hidden_units = config.get("hidden_units", 64)
        self.weights = np.random.randn(10, self.hidden_units)
    
    def train_step(self, x, y):
        """Simulate training"""
        return np.random.uniform(0.1, 1.0)
    
    def evaluate(self, x, y):
        return np.random.uniform(0.5, 0.95)


class Optimizer:
    def __init__(self, model, lr):
        self.model = model
        self.lr = lr


# Run custom trainable
analysis = tune.run(
    CustomTrainable,
    config={
        "learning_rate": tune.choice([0.001, 0.01, 0.1]),
        "hidden_units": tune.choice([32, 64, 128])
    },
    num_samples=10,
    checkpoint_at_end=True,
    checkpoint_freq=10
)
```

-----

## Ray RLlib (Reinforcement Learning)

### Quick Start with Built-in Algorithms

```python
import ray
import ray.rllib.algorithms as algo

ray.init(num_cpus=4)

# Configure PPO algorithm
config = algo.ppo.PPOConfig()
config = config.environment("CartPole-v1")
config = config.framework("torch")
config = config.rollout_fragment_length(200)
config = config.train_batch_size(4000)
config = config.num_workers(2)

# Build algorithm
ppo = config.build()

# Train for multiple iterations
for i in range(50):
    result = ppo.train()
    
    if i % 10 == 0:
        print(f"Iteration {i}:")
        print(f"  Episode reward mean: {result['episode_reward_mean']:.2f}")
        print(f"  Episode length mean: {result['episode_len_mean']:.2f}")

# Evaluate trained agent
evaluation = ppo.evaluate()
print(f"Evaluation reward: {evaluation['evaluation']['episode_reward_mean']}")

# Save and restore
ppo.save("/tmp/checkpoint")
ppo.restore("/tmp/checkpoint")
```

### Custom RL Environment

```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class WarehouseEnv(gym.Env):
    """Custom warehouse environment for RL"""
    
    metadata = {"render_modes": ["human"]}
    
    def __init__(self, config=None):
        super().__init__()
        self.config = config or {}
        
        # Define action space: 0=move_left, 1=move_right, 2=move_up, 3=move_down, 4=pickup, 5=dropoff
        self.action_space = spaces.Discrete(6)
        
        # Define observation space
        self.observation_space = spaces.Box(
            low=0, high=100, shape=(20,), dtype=np.float32
        )
        
        self.position = [0, 0]
        self.holding_item = False
        self.deliveries = 0
        self.steps = 0
        self.max_steps = 100
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.position = [0, 0]
        self.holding_item = False
        self.deliveries = 0
        self.steps = 0
        
        obs = self._get_obs()
        info = {}
        
        return obs, info
    
    def step(self, action):
        self.steps += 1
        
        # Execute action
        if action == 0:
            self.position[0] = max(0, self.position[0] - 1)
        elif action == 1:
            self.position[0] = min(9, self.position[0] + 1)
        elif action == 2:
            self.position[1] = min(9, self.position[1] + 1)
        elif action == 3:
            self.position[1] = max(0, self.position[1] - 1)
        elif action == 4 and not self.holding_item:
            self.holding_item = True
        elif action == 5 and self.holding_item:
            self.holding_item = False
            self.deliveries += 1
        
        # Calculate reward
        reward = 1.0 if self.deliveries > 0 else 0.0
        reward -= 0.01  # Step penalty
        
        terminated = self.steps >= self.max_steps
        truncated = False
        
        return self._get_obs(), reward, terminated, truncated, {}
    
    def _get_obs(self):
        obs = np.zeros(20, dtype=np.float32)
        obs[0] = self.position[0] / 10.0
        obs[1] = self.position[1] / 10.0
        obs[2] = float(self.holding_item)
        obs[3] = self.deliveries / 10.0
        return obs


# Train on custom environment
from ray import tune
from ray.rllib.algorithms import PPOConfig

config = (
    PPOConfig()
    .environment(WarehouseEnv)
    .framework("torch")
    .rollout_fragment_length(200)
    .train_batch_size(4000)
)

tune.Tuner(
    "PPO",
    param_space=config.to_dict(),
    run_config=tune.RunConfig(stop={"episode_reward_mean": 50})
).fit()
```

### Multi-Agent Training

```python
from ray.rllib.algorithms import PPOConfig
from ray.rllib.env.multi_agent_env import MultiAgentEnv
import numpy as np

class MultiAgentWarehouse(MultiAgentEnv):
    def __init__(self, config=None):
        super().__init__()
        self.num_agents = 3
        self.observation_space = spaces.Box(low=0, high=100, shape=(10,))
        self.action_space = spaces.Discrete(4)
    
    def reset(self):
        return {
            f"agent_{i}": self.observation_space.sample() 
            for i in range(self.num_agents)
        }
    
    def step(self, action_dict):
        obs = {
            f"agent_{i}": self.observation_space.sample()
            for i in range(self.num_agents)
        }
        
        rewards = {f"agent_{i}": np.random.random() for i in range(self.num_agents)}
        
        terminateds = {"__all__": False}
        truncateds = {"__all__": False}
        
        infos = {f"agent_{i}": {} for i in range(self.num_agents)}
        
        return obs, rewards, terminateds, truncateds, infos


config = (
    PPOConfig()
    .environment(MultiAgentWarehouse)
    .framework("torch")
    .training(train_batch_size=2000)
    .rollout_fragment_length(100)
    .multi_agent(
        policies={
            "shared_policy": (
                None,
                self.observation_space,
                self.action_space,
                {}
            )
        },
        policy_mapping_fn=lambda agent_id: "shared_policy"
    )
)
```

-----

## Ray Serve (Model Serving)

### Basic Deployment

```python
from ray import serve
import requests
from transformers import pipeline

# Initialize Ray Serve
serve.start()

@serve.deployment
class TextClassifier:
    def __init__(self):
        # Load model in constructor
        self.classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    
    def __call__(self, request):
        # Get text from request
        text = request.query_params.get("text", "")
        
        # Run inference
        result = self.classifier(text)[0]
        
        return result

# Deploy the model
TextClassifier.deploy()

# Make requests
response = requests.get("http://localhost:8000/TextClassifier?text=I love Ray!")
print(response.json())
```

### Complex Deployment with Preprocessing

```python
from ray import serve
from typing import List, Dict
import asyncio

@serve.deployment(
    num_replicas=2,
    ray_actor_options={"num_cpus": 1}
)
class TextPreprocessor:
    """Preprocess text before passing to model"""
    
    def __init__(self):
        import re
        self.url_pattern = re.compile(r'https?://\S+')
        self.email_pattern = re.compile(r'\S+@\S+\.\S+')
    
    async def preprocess(self, text: str) -> str:
        # Remove URLs
        text = self.url_pattern.sub('[URL]', text)
        # Remove emails
        text = self.email_pattern.sub('[EMAIL]', text)
        # Lowercase
        text = text.lower()
        
        return text
    
    async def batch_preprocess(self, texts: List[str]) -> List[str]:
        return await asyncio.gather(*[self.preprocess(t) for t in texts])


@serve.deployment(
    num_replicas=2,
    ray_actor_options={"num_cpus": 1, "num_gpus": 0.5}
)
class TextModel:
    """Model deployment"""
    
    def __init__(self):
        import torch
        from transformers import AutoTokenizer, AutoModel
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased").to(self.device)
        self.model.eval()
    
    async def __call__(self, request):
        import torch
        
        text = await request.body()
        
        # Tokenize
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True
        ).to(self.device)
        
        # Inference
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Return embedding
        embedding = outputs.last_hidden_state[:, 0, :].cpu().tolist()
        
        return {"embedding": embedding}


# Chain deployments
TextPreprocessor.deploy()
TextModel.deploy(handle_annotation=TextPreprocessor)


# Or use ingress with explicit pipeline
@serve.deployment(route_prefix="/predict")
class Ingress:
    def __init__(self):
        import requests
        self.preprocessor = serve.get_deployment_handle("TextPreprocessor")
        self.model = serve.get_deployment_handle("TextModel")
    
    async def __call__(self, request):
        text = await request.body()
        
        # Chain calls
        processed = await self.preprocessor.preprocess.remote(text)
        result = await self.model.remote(processed)
        
        return result

Ingress.deploy()
```

### Model Composition

```python
from ray import serve
from ray.serve.drivers import DefaultAPIDriver

@serve.deployment
class Summarizer:
    def __init__(self):
        # Load summarization model
        self.model = load_summarizer()
    
    def generate_summary(self, text: str) -> str:
        return self.model(text)


@serve.deployment
class SentimentAnalyzer:
    def __init__(self):
        # Load sentiment model
        self.model = load_sentiment_model()
    
    def analyze(self, text: str) -> str:
        return self.model(text)


@serve.deployment
class AnalysisPipeline:
    """Combined analysis pipeline"""
    
    def __init__(self):
        self.summarizer = serve.get_deployment_handle("Summarizer")
        self.sentiment = serve.get_deployment_handle("SentimentAnalyzer")
    
    async def analyze(self, text: str) -> Dict:
        # Run both in parallel
        summary, sentiment = await asyncio.gather(
            self.summarizer.generate_summary.remote(text),
            self.sentiment.analyze.remote(text)
        )
        
        return {
            "original_length": len(text),
            "summary": summary,
            "sentiment": sentiment,
            "key_topics": extract_topics(text)
        }

# Deploy all
Summarizer.deploy()
SentimentAnalyzer.deploy()
AnalysisPipeline.deploy()
```

-----

## Ray Datasets

```python
import ray

ray.init()

# Create dataset from various sources
# From NumPy
import numpy as np
numpy_array = np.random.randn(10000, 100)
dataset = ray.data.from_numpy(numpy_array)

# From pandas
import pandas as pd
df = pd.DataFrame({"a": range(1000), "b": range(1000, 2000)})
dataset = ray.data.from_pandas(df)

# From CSV
dataset = ray.data.read_csv("s3://bucket/data/*.csv")

# From Parquet
dataset = ray.data.read_parquet("s3://bucket/data/*.parquet")

# Transform data
def process_batch(batch: pd.DataFrame) -> pd.DataFrame:
    batch["processed"] = batch["a"] * 2
    return batch

processed = dataset.map_batches(process_batch, batch_size=1000)

# Filter data
filtered = dataset.filter(lambda row: row["a"] > 500)

# Shuffle
shuffled = dataset.random_shuffle()

# Split into train/val/test
train, val, test = shuffled.train_test_split(test_size=0.2)

# Repartition
repartitioned = train.repartition(num_blocks=10)

# Materialize to local cluster
repartitioned.fully_executed()

# Custom transformations
def add_features(row):
    row["new_feature"] = row["a"] ** 2
    return row

with_features = dataset.map(add_features)

# Group by and aggregate
aggregated = dataset.groupby("category").mean()

# Join datasets
dataset1 = ray.data.from_pandas(pd.DataFrame({"id": [1, 2, 3], "value": [10, 20, 30]}))
dataset2 = ray.data.from_pandas(pd.DataFrame({"id": [1, 2, 4], "other": ["a", "b", "c"]}))
joined = dataset1.join(dataset2, on="id", how="left")
```

-----

## Best Practices

### Performance Optimization

1. **Use ObjectRefs efficiently** — Don't get() immediately after each remote() call; batch when possible.

2. **Choose tasks vs actors wisely** — Use tasks for stateless parallelism, actors for stateful services.

3. **Configure resources correctly** — Specify CPU/GPU requirements to enable proper scheduling.

4. **Use placement groups** — For workloads requiring specific hardware configurations.

5. **Monitor with Ray Dashboard** — Use the dashboard to identify bottlenecks.

### Common Pitfalls

1. **Not handling exceptions** — Use try/except within remote functions and propagate errors properly.

2. **Excessive serialization** — Large objects passed between tasks incur serialization overhead. Use shared memory or ObjectRef passing.

3. **Ignoring cluster startup time** — For short jobs, the cluster overhead may outweigh benefits.

4. **Not checkpointing** — For long-running training, implement checkpointing to handle failures.

### Resources

- **Documentation**: docs.ray.io
- **GitHub**: github.com/ray-project/ray
- **Community**: discuss.ray.io
- **Related Skills**: distributed-systems, pytorch, tensorflow, kubernetes
