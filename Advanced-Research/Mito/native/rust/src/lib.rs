// Mito Core - Rust Extensions
// High-performance native implementations

use std::collections::HashMap;

/// Tokenizer for language models
pub struct Tokenizer {
    vocab: HashMap<String, usize>,
    reverse_vocab: Vec<String>,
}

impl Tokenizer {
    pub fn new() -> Self {
        Tokenizer {
            vocab: HashMap::new(),
            reverse_vocab: Vec::new(),
        }
    }
    
    pub fn load(&mut self, path: &str) -> Result<(), Box<dyn std::error::Error>> {
        // Load vocab from file
        Ok(())
    }
    
    pub fn encode(&self, text: &str) -> Vec<usize> {
        text.split_whitespace()
            .map(|w| self.vocab.get(w).copied().unwrap_or(0))
            .collect()
    }
    
    pub fn decode(&self, tokens: &[usize]) -> String {
        tokens
            .iter()
            .filter_map(|&i| self.reverse_vocab.get(i))
            .cloned()
            .collect::<Vec<_>>()
            .join(" ")
    }
}

/// Text embedding vector
#[derive(Clone, Debug)]
pub struct Embedding {
    pub vector: Vec<f32>,
}

impl Embedding {
    pub fn new(dimension: usize) -> Self {
        Embedding {
            vector: vec![0.0; dimension],
        }
    }
    
    pub fn cosine_similarity(&self, other: &Embedding) -> f32 {
        let dot: f32 = self.vector.iter().zip(other.vector.iter())
            .map(|(a, b)| a * b)
            .sum();
        
        let mag_a: f32 = self.vector.iter().map(|x| x * x).sum::<f32>().sqrt();
        let mag_b: f32 = other.vector.iter().map(|x| x * x).sum::<f32>().sqrt();
        
        if mag_a == 0.0 || mag_b == 0.0 {
            return 0.0;
        }
        
        dot / (mag_a * mag_b)
    }
    
    pub fn dimension(&self) -> usize {
        self.vector.len()
    }
}

/// N-dimensional tensor
#[derive(Clone)]
pub struct Tensor {
    shape: Vec<usize>,
    data: Vec<f32>,
}

impl Tensor {
    pub fn new(shape: Vec<usize>) -> Self {
        let size = shape.iter().product();
        Tensor {
            shape,
            data: vec![0.0; size],
        }
    }
    
    pub fn reshape(&mut self, new_shape: Vec<usize>) {
        let new_size = new_shape.iter().product();
        if new_size == self.data.len() {
            self.shape = new_shape;
        }
    }
    
    pub fn data(&self) -> &[f32] {
        &self.data
    }
    
    pub fn shape(&self) -> &[usize] {
        &self.shape
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_embedding_similarity() {
        let a = Embedding::new(3);
        let b = Embedding::new(3);
        assert_eq!(a.cosine_similarity(&b), 0.0);
    }
}
