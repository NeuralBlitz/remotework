-----
name: attention-mechanisms
description: >
  Expert in attention mechanisms and transformer architectures for deep learning. 
  Use this skill for implementing attention-based models, understanding self-attention, 
  cross-attention, multi-head attention, and optimizing transformer models. Covers 
  transformer variants, efficient attention patterns, and applications in NLP, vision, 
  and multimodal learning.
license: MIT
compatibility: opencode
metadata:
  audience: machine-learning-engineers
  category: artificial-intelligence
  tags: [transformers, attention, deep-learning, nlp, computer-vision]

# Attention Mechanisms in Neural Networks

Covers: **Self-Attention · Multi-Head Attention · Cross-Attention · Transformer Architecture · Efficient Attention · Vision Transformers · Multi-Modal Learning**

-----

## Attention Fundamentals

### The Attention Mechanism

Attention allows models to focus on relevant parts of the input when processing each element. The core attention formula computes a weighted sum of values based on query-key similarity:

```
Attention(Q, K, V) = softmax(QK^T / √d_k)V

Where:
- Q (Query): What we're looking for
- K (Key): What each position offers
- V (Value): What each position contains
- d_k: Dimension of keys (scaling factor)
```

### Why Attention Works

| Aspect | Benefit |
|--------|---------|
| **Parallelization** | Unlike RNNs, attention can be computed in parallel |
| **Long-range dependencies** | Direct connections between any positions |
| **Interpretability** | Attention weights show what model focuses on |
| **Flexibility** | Works with any sequence length |

### Mathematical Foundations

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class ScaledDotProductAttention(nn.Module):
    """Scaled dot-product attention"""
    
    def __init__(self, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, Q: torch.Tensor, K: torch.Tensor, 
               V: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        """
        Args:
            Q: Query tensor [batch, heads, seq_len, d_k]
            K: Key tensor [batch, heads, seq_len, d_k]
            V: Value tensor [batch, heads, seq_len, d_v]
            mask: Optional mask [batch, 1, 1, seq_len] or [batch, heads, seq_len, seq_len]
        Returns:
            Attention output [batch, heads, seq_len, d_v]
        """
        d_k = Q.size(-1)
        
        # Compute attention scores
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
        
        # Apply mask if provided
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        # Attention weights
        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        # Apply attention to values
        output = torch.matmul(attn_weights, V)
        
        return output, attn_weights
```

-----

## Multi-Head Attention

### Architecture

Multi-head attention runs multiple attention operations in parallel, allowing the model to attend to different representation subspaces:

```python
class MultiHeadAttention(nn.Module):
    """Multi-head attention mechanism"""
    
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.d_v = d_model // num_heads
        
        # Linear projections
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
    
    def split_heads(self, x: torch.Tensor) -> torch.Tensor:
        """Split last dimension into (num_heads, d_k)"""
        batch_size, seq_len, d_model = x.size()
        x = x.view(batch_size, seq_len, self.num_heads, self.d_k)
        return x.permute(0, 2, 1, 3)  # [batch, heads, seq_len, d_k]
    
    def forward(self, Q: torch.Tensor, K: torch.Tensor, 
               V: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        batch_size = Q.size(0)
        
        # Linear projections and split heads
        Q = self.split_heads(self.W_q(Q))
        K = self.split_heads(self.W_k(K))
        V = self.split_heads(self.W_v(V))
        
        # Scaled dot-product attention
        attn_output, _ = ScaledDotProductAttention()(Q, K, V, mask)
        
        # Merge heads
        attn_output = attn_output.permute(0, 2, 1, 3).contiguous()
        attn_output = attn_output.view(batch_size, -1, self.d_model)
        
        # Final linear projection
        output = self.W_o(attn_output)
        
        return output
    
    def compute_attention_weights(self, Q: torch.Tensor, K: torch.Tensor) -> torch.Tensor:
        """Compute and return attention weights without applying to values"""
        Q = self.split_heads(self.W_q(Q))
        K = self.split_heads(self.W_k(K))
        
        d_k = Q.size(-1)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
        return F.softmax(scores, dim=-1)
```

### Causal (Masked) Attention

```python
def create_causal_mask(seq_len: int, device: torch.device) -> torch.Tensor:
    """Create causal mask for autoregressive modeling"""
    mask = torch.tril(torch.ones(seq_len, seq_len, device=device))
    return mask.unsqueeze(0).unsqueeze(0)  # [1, 1, seq_len, seq_len]

class CausalMultiHeadAttention(MultiHeadAttention):
    """Multi-head attention with causal masking"""
    
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__(d_model, num_heads, dropout)
    
    def forward(self, Q: torch.Tensor, K: torch.Tensor, 
               V: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        batch_size, seq_len = Q.size(0), Q.size(1)
        
        # Create causal mask
        causal_mask = create_causal_mask(seq_len, Q.device)
        
        # Combine with any additional mask
        if mask is not None:
            mask = causal_mask & mask
        else:
            mask = causal_mask
        
        return super().forward(Q, K, V, mask)
```

-----

## Transformer Architecture

### Full Transformer Encoder

```python
class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding"""
    
    def __init__(self, d_model: int, max_len: int = 5000, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        
        # Create positional encoding
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                            (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)  # [1, max_len, d_model]
        
        self.register_buffer('pe', pe)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Add positional encoding to input"""
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


class TransformerEncoderLayer(nn.Module):
    """Single transformer encoder layer"""
    
    def __init__(self, d_model: int, num_heads: int, d_ff: int = 2048,
                 dropout: float = 0.1):
        super().__init__()
        
        self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.feed_forward = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model)
        )
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
    
    def forward(self, x: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        # Self attention with residual
        attn_output = self.self_attn(x, x, x, mask)
        x = self.norm1(x + self.dropout1(attn_output))
        
        # Feed forward with residual
        ff_output = self.feed_forward(x)
        x = self.norm2(x + self.dropout2(ff_output))
        
        return x


class TransformerEncoder(nn.Module):
    """Full transformer encoder"""
    
    def __init__(self, num_layers: int, d_model: int, num_heads: int,
                 d_ff: int, vocab_size: int, dropout: float = 0.1):
        super().__init__()
        
        self.d_model = d_model
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model, dropout=dropout)
        
        self.layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        
        self.norm = nn.LayerNorm(d_model)
    
    def forward(self, x: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        # Embed and add positional encoding
        x = self.embedding(x) * math.sqrt(self.d_model)
        x = self.pos_encoding(x)
        
        # Pass through layers
        for layer in self.layers:
            x = layer(x, mask)
        
        return self.norm(x)
```

### Transformer Decoder

```python
class TransformerDecoderLayer(nn.Module):
    """Single transformer decoder layer with cross-attention"""
    
    def __init__(self, d_model: int, num_heads: int, d_ff: int = 2048,
                 dropout: float = 0.1):
        super().__init__()
        
        self.self_attn = CausalMultiHeadAttention(d_model, num_heads, dropout)
        self.cross_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.feed_forward = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model)
        )
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        self.dropout3 = nn.Dropout(dropout)
    
    def forward(self, x: torch.Tensor, encoder_output: torch.Tensor,
                src_mask: torch.Tensor = None, tgt_mask: torch.Tensor = None) -> torch.Tensor:
        # Self attention (causal)
        attn1 = self.self_attn(x, x, x, tgt_mask)
        x = self.norm1(x + self.dropout1(attn1))
        
        # Cross attention
        attn2 = self.cross_attn(x, encoder_output, encoder_output, src_mask)
        x = self.norm2(x + self.dropout2(attn2))
        
        # Feed forward
        ff = self.feed_forward(x)
        x = self.norm3(x + self.dropout3(ff))
        
        return x


class Transformer(nn.Module):
    """Full transformer (encoder-decoder)"""
    
    def __init__(self, src_vocab_size: int, tgt_vocab_size: int,
                 d_model: int = 512, num_heads: int = 8,
                 num_encoder_layers: int = 6, num_decoder_layers: int = 6,
                 d_ff: int = 2048, dropout: float = 0.1):
        super().__init__()
        
        self.encoder = TransformerEncoder(
            num_encoder_layers, d_model, num_heads, d_ff, src_vocab_size, dropout
        )
        
        # Decoder layers
        self.decoder_layers = nn.ModuleList([
            TransformerDecoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_decoder_layers)
        ])
        
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model, dropout=dropout)
        self.output_projection = nn.Linear(d_model, tgt_vocab_size)
    
    def forward(self, src: torch.Tensor, tgt: torch.Tensor,
                src_mask: torch.Tensor = None, tgt_mask: torch.Tensor = None):
        # Encode source
        encoder_output = self.encoder(src, src_mask)
        
        # Decode target
        tgt_emb = self.tgt_embedding(tgt) * math.sqrt(self.d_model)
        tgt_emb = self.pos_encoding(tgt_emb)
        
        for layer in self.decoder_layers:
            tgt_emb = layer(tgt_emb, encoder_output, src_mask, tgt_mask)
        
        return self.output_projection(tgt_emb)
```

-----

## Efficient Attention Patterns

### Sparse Attention

```python
class SparseAttention(nn.Module):
    """Fixed sparse attention pattern"""
    
    def __init__(self, d_model: int, num_heads: int, 
                 window_size: int = 128, dropout: float = 0.1):
        super().__init__()
        self.window_size = window_size
        self.attn = MultiHeadAttention(d_model, num_heads, dropout)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, d_model = x.size()
        
        # Create sliding window mask
        mask = torch.ones(seq_len, seq_len, device=x.device)
        mask = torch.triu(mask, diagonal=-self.window_size)
        mask = torch.tril(mask, diagonal=0)
        mask = mask.masked_fill(mask == 0, float('-inf'))
        mask = mask.masked_fill(mask == 1, 0)
        mask = mask.unsqueeze(0).unsqueeze(0)  # [1, 1, seq_len, seq_len]
        
        return self.attn(x, x, x, mask)


class LocalGlobalAttention(nn.Module):
    """Combine local and global attention"""
    
    def __init__(self, d_model: int, num_heads: int, 
                 local_window: int = 128, dropout: float = 0.1):
        super().__init__()
        self.local_window = local_window
        self.local_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.global_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.projection = nn.Linear(d_model, d_model)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, d_model = x.size()
        
        # Global attention (all-to-all)
        global_output = self.global_attn(x, x, x)
        
        # Local attention
        mask = torch.zeros(seq_len, seq_len, device=x.device)
        for i in range(seq_len):
            start = max(0, i - self.local_window)
            end = min(seq_len, i + self.local_window + 1)
            mask[i, start:end] = 1
        mask = mask.unsqueeze(0).unsqueeze(0)
        
        local_output = self.local_attn(x, x, x, mask)
        
        # Combine
        combined = global_output + local_output
        return self.projection(combined)
```

### Linear Attention

```python
class LinearAttention(nn.Module):
    """Linear attention using kernel approximation"""
    
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.query_projection = nn.Linear(d_model, d_model)
        self.key_projection = nn.Linear(d_model, d_model)
        self.value_projection = nn.Linear(d_model, d_model)
        self.output_projection = nn.Linear(d_model, d_model)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, d_model = x.size()
        
        Q = self.query_projection(x).view(batch_size, seq_len, self.num_heads, self.d_k)
        K = self.key_projection(x).view(batch_size, seq_len, self.num_heads, self.d_k)
        V = self.value_projection(x).view(batch_size, seq_len, self.num_heads, self.d_k)
        
        # Apply ELU activation for kernel approximation
        K = F.elu(K) + 1
        
        # Linear attention computation
        KV = torch.einsum('nskd,nskv->nsdv', K, V)
        QK = torch.einsum('nsnd,nsdv->nsnv', Q, K)
        
        attn_weights = QK / (QK.sum(dim=-1, keepdim=True) + 1e-6)
        output = torch.einsum('nsnv,nsdv->nsnd', attn_weights, KV)
        
        output = output.contiguous().view(batch_size, seq_len, d_model)
        return self.output_projection(output)
```

### Flash Attention

```python
# Note: FlashAttention requires the flash_attn package
# pip install flash-attn

"""
class FlashAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, Q, K, V, mask=None):
        from flash_attn.flash_attn_interface import flash_attn_func
        
        # Project and reshape
        Q = self.W_q(Q).view(Q.size(0), Q.size(1), self.num_heads, self.d_k)
        K = self.W_k(K).view(K.size(0), K.size(1), self.num_heads, self.d_k)
        V = self.W_v(V).view(V.size(0), V.size(1), self.num_heads, self.d_k)
        
        # Flash attention
        output = flash_attn_func(Q, K, V, dropout_p=self.dropout.p if self.training else 0.0,
                                 softmax_scale=None, causal=False)
        
        output = output.view(output.size(0), output.size(1), self.d_model)
        return self.W_o(output)
"""
```

-----

## Vision Transformers (ViT)

### ViT Architecture

```python
class PatchEmbedding(nn.Module):
    """Convert image to patch embeddings"""
    
    def __init__(self, img_size: int = 224, patch_size: int = 16, 
                 in_channels: int = 3, d_model: int = 768):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.n_patches = (img_size // patch_size) ** 2
        
        # Conv2d for patch projection (more efficient than linear)
        self.projection = nn.Conv2d(in_channels, d_model, 
                                   kernel_size=patch_size, 
                                   stride=patch_size)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: [batch, channels, height, width]
        returns: [batch, n_patches, d_model]
        """
        x = self.projection(x)  # [B, d_model, h/p, w/p]
        x = x.flatten(2)  # [B, d_model, n_patches]
        x = x.transpose(1, 2)  # [B, n_patches, d_model]
        return x


class ViTTransformer(nn.Module):
    """Vision Transformer"""
    
    def __init__(self, img_size: int = 224, patch_size: int = 16,
                 in_channels: int = 3, num_classes: int = 1000,
                 d_model: int = 768, num_heads: int = 12,
                 num_layers: int = 12, d_ff: int = 3072,
                 dropout: float = 0.1):
        super().__init__()
        
        self.patch_embedding = PatchEmbedding(img_size, patch_size, 
                                               in_channels, d_model)
        
        # Class token and position embeddings
        self.cls_token = nn.Parameter(torch.zeros(1, 1, d_model))
        self.pos_embedding = nn.Parameter(
            torch.zeros(1, self.patch_embedding.n_patches + 1, d_model)
        )
        self.pos_dropout = nn.Dropout(dropout)
        
        # Transformer encoder
        self.transformer = nn.Sequential(*[
            TransformerEncoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        
        # Classification head
        self.norm = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, num_classes)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size = x.size(0)
        
        # Patch embedding
        x = self.patch_embedding(x)  # [B, n_patches, d_model]
        
        # Add class token
        cls_tokens = self.cls_token.expand(batch_size, -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)  # [B, n_patches+1, d_model]
        
        # Add position embedding
        x = x + self.pos_embedding
        x = self.pos_dropout(x)
        
        # Transform
        x = self.transformer(x)
        x = self.norm(x)
        
        # Return class token output
        return self.head(x[:, 0])
```

-----

## Attention Variants

### Cross-Attention

```python
class CrossAttention(nn.Module):
    """Cross-attention for encoder-decoder or multimodal"""
    
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        self.attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.norm = nn.LayerNorm(d_model)
    
    def forward(self, query: torch.Tensor, key: torch.Tensor, 
               value: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        """
        query: From decoder [batch, tgt_len, d_model]
        key: From encoder [batch, src_len, d_model]
        value: From encoder [batch, src_len, d_model]
        """
        attn_output = self.attn(query, key, value, mask)
        return self.norm(query + attn_output)
```

### Performer (Random Fourier Features)

```python
class PerformerAttention(nn.Module):
    """Fast Attention via Positive Orthogonal Random Features"""
    
    def __init__(self, d_model: int, num_heads: int, 
                 num_features: int = 256, dropout: float = 0.1):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.num_features = num_features
        
        # Random projection matrices
        self.register_buffer('R', torch.randn(num_heads, self.d_k, num_features))
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, _ = x.size()
        
        Q = self.W_q(x).view(batch_size, seq_len, self.num_heads, self.d_k)
        K = self.W_k(x).view(batch_size, seq_len, self.num_heads, self.d_k)
        V = self.W_v(x).view(batch_size, seq_len, self.num_heads, self.d_k)
        
        # Positive random feature projection
        K = F.relu(torch.einsum('bhkd,dkf->bhf', K, self.R))
        
        # Attention via FAVOR
        KV = torch.einsum('bhf,bhv->bhfv', K, V)
        K_sum = K.sum(dim=2, keepdim=True)
        
        attn_output = torch.einsum('bhfv,bhf->bhv', KV, Q) / (K_sum + 1e-6)
        attn_output = attn_output.contiguous().view(batch_size, seq_len, self.d_model)
        
        return self.W_o(attn_output)
```

-----

## Practical Tips

### Attention Visualization

```python
def visualize_attention(attention_weights: torch.Tensor, 
                      tokens: list, save_path: str = 'attention.png'):
    """Visualize attention weights"""
    import matplotlib.pyplot as plt
    
    # Take first head and first batch
    attn = attention_weights[0, 0].cpu().detach().numpy()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(attn, cmap='viridis')
    
    ax.set_xticks(range(len(tokens)))
    ax.set_yticks(range(len(tokens)))
    ax.set_xticklabels(tokens, rotation=45, ha='right')
    ax.set_yticklabels(tokens)
    
    plt.colorbar(im, ax=ax)
    ax.set_title('Attention Weights')
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def get_attention_patterns(model: nn.Module, input_ids: torch.Tensor,
                           layer_idx: int = -1) -> torch.Tensor:
    """Extract attention patterns from a trained model"""
    # Hook into attention weights
    attention_weights = []
    
    def hook(module, input, output):
        attention_weights.append(output[1])  # Attention weights
    
    # Register hook on specific layer
    model.transformer.layers[layer_idx].self_attn.register_forward_hook(hook)
    
    # Forward pass
    model(input_ids)
    
    return attention_weights[0] if attention_weights else None
```

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| **No positional encoding** | Always add positional encodings |
| **Missing attention mask** | Use causal mask for generation |
| **Wrong mask shape** | Check mask dimensions carefully |
| **Numerical instability** | Use scaled attention (divide by √d_k) |
| **Memory issues with long sequences** | Use sparse/linear attention |

### Architecture Selection Guide

| Use Case | Recommended Architecture |
|----------|-------------------------|
| **Text classification** | BERT, RoBERTa |
| **Text generation** | GPT, Transformer Decoder |
| **Machine translation** | Full Transformer |
| **Image classification** | ViT, DeiT |
| **Object detection** | DETR |
| **Multimodal** | CLIP, Flamingo |
| **Long sequences** | Longformer, Performer |
