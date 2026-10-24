# GraNT Framework - Deployment Guide

## Quick Start (Docker)

### 1. Build Docker Image

```bash
docker build -t grant-framework:latest .
```

### 2. Run Container

```bash
docker run -it --rm \
  -v $(pwd)/data:/data \
  -v $(pwd)/outputs:/outputs \
  grant-framework:latest
```

### 3. Run Demo

```bash
docker exec -it <container_id> python examples/complete_demo.py
```

---

## Manual Installation

### Requirements

- Python 3.8+
- PyTorch 2.0+ (CPU or CUDA)
- NumPy 1.20+

### Install from Source

```bash
git clone https://github.com/neuralblitz/grant
cd grant
pip install -e .
```

### Verify Installation

```bash
python -c "import grant; print(grant.__version__)"
python examples/complete_demo.py
python -m pytest tests/ -v
```

---

## Production Deployment

### 1. Cloud Deployment (AWS/GCP/Azure)

#### AWS SageMaker

```python
from sagemaker.pytorch import PyTorchModel

model = PyTorchModel(
    model_data='s3://my-bucket/grant-model.tar.gz',
    role='SageMakerRole',
    entry_point='inference.py',
    framework_version='2.0',
    py_version='py39'
)

predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.m5.xlarge'
)
```

#### Google Cloud AI Platform

```bash
gcloud ai-platform models create grant_model --region us-central1
gcloud ai-platform versions create v1 \
  --model grant_model \
  --origin gs://my-bucket/grant-model/ \
  --runtime-version 2.8 \
  --framework PYTORCH
```

### 2. Edge Deployment

#### Mobile (TensorFlow Lite conversion)

```python
from grant.core.sheaf_attention import SheafTransformer
import torch

model = SheafTransformer(vocab_size=10000, d_model=128)
model.eval()

# Export to ONNX
dummy_input = torch.randint(0, 10000, (1, 64))
torch.onnx.export(
    model,
    dummy_input,
    "sheaf_former.onnx",
    input_names=['input_ids'],
    output_names=['logits'],
    dynamic_axes={'input_ids': {0: 'batch', 1: 'sequence'}}
)
```

#### IoT Devices (Quantization)

```python
import torch.quantization as quant

# Post-training quantization
model_int8 = quant.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8
)

# Size reduction: ~4x smaller
torch.save(model_int8.state_dict(), 'model_quantized.pth')
```

---

## Performance Optimization

### 1. Mixed Precision Training

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in dataloader:
    optimizer.zero_grad()
    
    with autocast():
        output = model(batch)
        loss = criterion(output, labels)
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

### 2. Distributed Training

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel

# Initialize process group
dist.init_process_group(backend='nccl')

# Wrap model
model = SheafTransformer(...)
model = DistributedDataParallel(model)

# Train as usual
```

### 3. Caching and Optimization

```python
from functools import lru_cache

class OptimizedSheafTransformer(SheafTransformer):
    @lru_cache(maxsize=1000)
    def _cached_attention(self, key_hash):
        # Cache attention patterns for repeated inputs
        return super().forward(...)
```

---

## Monitoring and Logging

### 1. TensorBoard Integration

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/grant_experiment')

for epoch in range(num_epochs):
    loss = train_epoch(model, dataloader)
    
    writer.add_scalar('Loss/train', loss, epoch)
    writer.add_scalar('Confidence/mean', mean_confidence, epoch)

writer.close()
```

### 2. Weights & Biases

```python
import wandb

wandb.init(project="grant-framework", config={
    "d_model": 256,
    "n_layers": 4,
    "temperature": 0.7
})

wandb.watch(model, log_freq=100)

for epoch in range(num_epochs):
    metrics = train_epoch(model, dataloader)
    wandb.log(metrics)
```

### 3. Production Metrics

```python
from grant.workflows.sepa import SEPAEngine
import prometheus_client as prom

# Define metrics
request_count = prom.Counter('grant_requests_total', 'Total requests')
latency_hist = prom.Histogram('grant_latency_seconds', 'Request latency')
confidence_gauge = prom.Gauge('grant_confidence', 'Model confidence')

@latency_hist.time()
def process_request(goal):
    request_count.inc()
    solution = engine.investigate(goal)
    confidence_gauge.set(solution.performance.get('confidence', 0.5))
    return solution
```

---

## Security and Best Practices

### 1. Model Encryption

```python
import cryptography.fernet as fernet

# Encrypt model weights
key = fernet.Fernet.generate_key()
cipher = fernet.Fernet(key)

with open('model.pth', 'rb') as f:
    encrypted = cipher.encrypt(f.read())

with open('model.encrypted', 'wb') as f:
    f.write(encrypted)
```

### 2. Input Validation

```python
from grant.workflows.auto_cognition import ResearchGoal

def validate_goal(goal: ResearchGoal):
    """Validate and sanitize user inputs."""
    # Check constraints
    if 'latency_ms' in goal.constraints:
        assert goal.constraints['latency_ms'] > 0, "Latency must be positive"
    
    # Sanitize description
    goal.description = goal.description[:1000]  # Limit length
    
    # Remove harmful content
    forbidden = ['<script>', 'eval(', 'exec(']
    for pattern in forbidden:
        assert pattern not in goal.description, "Invalid input"
    
    return goal
```

### 3. Resource Limits

```python
import resource
import signal

def limit_resources():
    """Set resource limits for safety."""
    # CPU time limit: 5 minutes
    resource.setrlimit(resource.RLIMIT_CPU, (300, 300))
    
    # Memory limit: 4GB
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    
    # Timeout handler
    def timeout_handler(signum, frame):
        raise TimeoutError("Execution exceeded time limit")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(600)  # 10 minute wall time
```

---

## Troubleshooting

### Common Issues

#### 1. Out of Memory

**Problem**: `RuntimeError: CUDA out of memory`

**Solutions**:
```python
# Reduce batch size
batch_size = 16  # instead of 32

# Enable gradient checkpointing
model.gradient_checkpointing_enable()

# Use smaller model
model = SheafTransformer(d_model=128, n_layers=2)  # instead of 512/6
```

#### 2. Slow Inference

**Problem**: Latency exceeds target

**Solutions**:
```python
# Enable TorchScript compilation
model = torch.jit.script(model)

# Use ONNX Runtime
import onnxruntime as ort
session = ort.InferenceSession("model.onnx")

# Batch requests
outputs = model(torch.cat(requests, dim=0))
```

#### 3. Numerical Instability

**Problem**: NaN or Inf in outputs

**Solutions**:
```python
# Clip gradients
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# Use more stable attention
attn = CocycleAttention(d_model=256, temperature=1.0)  # Higher temp

# Enable anomaly detection
torch.autograd.set_detect_anomaly(True)
```

---

## API Reference

See [docs/api/](docs/api/) for complete API documentation.

---

## Support

- **Issues**: https://github.com/neuralblitz/grant/issues
- **Discussions**: https://github.com/neuralblitz/grant/discussions
- **Email**: NuralNexus@icloud.com

---

## License

MIT License - see LICENSE file for details.
