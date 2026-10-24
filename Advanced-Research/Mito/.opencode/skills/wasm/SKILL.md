---

## name: wasm
description: >
  WebAssembly (WASM) expert for high-performance browser and server code execution.
  Use this skill whenever the user needs: writing WebAssembly modules, optimizing
  performance-critical code, integrating WASM in web applications, using Rust or
  AssemblyScript for WASM development, debugging WASM binaries, understanding WASM
  runtime environments, or any task requiring near-native performance in web or
  server contexts. WebAssembly is ideal for computationally intensive tasks like
  image processing, video encoding, physics simulations, game engines, and
  cryptographic operations. This skill covers both the WebAssembly text format
  (WAT) and binary format, along with JavaScript integration and toolchains.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: web-development

# WebAssembly — High-Performance Code Execution

Covers: **WASM Modules · Rust/AssemblyScript Toolchains · JavaScript Integration · Performance Optimization · Binary Format · Debugging**

-----

## WebAssembly Fundamentals

### What is WebAssembly?

WebAssembly (WASM) is a binary instruction format for a stack-based virtual machine. It is designed as a portable compilation target for programming languages, enabling deployment on the web for client and server applications. WASM provides a near-native execution speed while maintaining a secure sandbox execution environment.

Key characteristics:
- **Binary format**: Compact and fast to parse, typically 10-20% of equivalent JavaScript size
- **Stack-based VM**: Simple execution model that is easy to implement in hardware and software
- **Type-safe**: Strong typing system with four primary types (i32, i64, f32, f64, v128)
- **Memory-safe**: Linear memory model with explicit bounds checking
- **Sandboxed**: Cannot access the host system directly; must use explicit imports

### WebAssembly Text Format (WAT)

The text format is a human-readable representation of WASM binaries. It uses S-expressions:

```wat
(module
  (func $add (param $a i32) (param $b i32) (result i32)
    local.get $a
    local.get $b
    i32.add)
  
  (export "add" (func $add))
)
```

The equivalent binary can be generated using tools like Wasmtime or wabt.

### Core Data Types

| Type | Description | Use Case |
|------|-------------|----------|
| `i32` | 32-bit integer | General computation, array indices |
| `i64` | 64-bit integer | Large numbers, timestamps |
| `f32` | 32-bit float | Graphics, physics |
| `f64` | 64-bit float | Scientific computation |
| `v128` | 128-bit vector | SIMD operations |

### Memory Model

WebAssembly has linear memory—a contiguous, mutable array of bytes:

```wat
;; Declare 1 page of memory (64KB)
(memory 1)

;; Or with export
(memory (export "mem") 1)
```

Memory can be grown dynamically using the `memory.grow` instruction.

-----

## Rust to WebAssembly

### Setting Up the Toolchain

Install the Rust WASM target and wasm-pack:

```bash
rustup target add wasm32-unknown-unknown
cargo install wasm-pack
```

### Basic Rust Function

```rust
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[no_mangle]
pub extern "C" fn fibonacci(n: i32) -> i32 {
    match n {
        0 => 0,
        1 => 1,
        _ => {
            let mut a = 0;
            let mut b = 1;
            for _ in 2..=n {
                let temp = a + b;
                a = b;
                b = temp;
            }
            b
        }
    }
}
```

### Building with wasm-pack

```bash
# Create a library project
cargo new --lib my-wasm

# Add to Cargo.toml
[lib]
crate-type = ["cdylib"]

[dependencies]
wasm-bindgen = "0.2"

# Build for web
wasm-pack build --target web
```

### Using wasm-bindgen

The wasm-bindgen crate simplifies JavaScript interoperability:

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[wasm_bindgen]
pub struct Vector2 {
    x: f32,
    y: f32,
}

#[wasm_bindgen]
impl Vector2 {
    #[wasm_bindgen(constructor)]
    pub fn new(x: f32, y: f32) -> Vector2 {
        Vector2 { x, y }
    }
    
    pub fn magnitude(&self) -> f32 {
        (self.x * self.x + self.y * self.y).sqrt()
    }
    
    pub fn add(&self, other: &Vector2) -> Vector2 {
        Vector2 {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}
```

### Performance Tips for Rust WASM

1. **Enable link-time optimization**: Add `lto = true` and `opt-level = 3` to Cargo.toml
2. **Use release builds**: Debug builds are for debugging only
3. **Avoid allocations in hot paths**: Pre-allocate buffers, reuse memory
4. **Profile with wasm-bindgen-test**: Measure actual performance
5. **Consider wasm-opt**: Run wasm-opt after building for additional optimizations

```toml
[profile.release]
lto = true
opt-level = 3
codegen-units = 1
```

-----

## JavaScript WebAssembly Integration

### Loading WASM Modules

```javascript
// Method 1: instantiateStreaming (recommended)
async function loadWasm1(url) {
  const response = await fetch(url);
  const { instance } = await WebAssembly.instantiateStreaming(response);
  return instance.exports;
}

// Method 2: ArrayBuffer
async function loadWasm2(url) {
  const response = await fetch(url);
  const buffer = await response.arrayBuffer();
  const { instance } = await WebAssembly.instantiate(buffer);
  return instance.exports;
}

// Method 3: Using importObject
async function loadWasm3(url, importObject = {}) {
  const response = await fetch(url);
  const { instance } = await WebAssembly.instantiateStreaming(
    response,
    importObject
  );
  return instance.exports;
}

// Usage
const wasm = await loadWasm1('/add.wasm');
console.log(wasm.add(1, 2)); // 3
```

### Calling WASM from JavaScript

```javascript
// Initialize WASM module
const wasmModule = await WebAssembly.instantiateStreaming(
  fetch('compute.wasm')
);

const { add, fibonacci, memory } = wasmModule.instance.exports;

// Simple function call
const result = fibonacci(20);

// Reading from WASM memory
const dataView = new DataView(memory.buffer);
const offset = 100;
const value = dataView.getInt32(offset, true); // little-endian

// Writing to WASM memory
dataView.setInt32(offset, 42, true);
```

### Exporting JavaScript Functions to WASM

```javascript
const importObject = {
  env: {
    // Math functions
    sin: Math.sin,
    cos: Math.cos,
    exp: Math.exp,
    log: Math.log,
    
    // Custom functions
    console_log: (ptr) => {
      console.log("From WASM:", ptr);
    },
    
    // Random number generation
    random: () => Math.random(),
    
    // Timestamps
    current_time: () => Date.now(),
  },
  wasi_snapshot_preview1: {
    // WASI imports if needed
    proc_exit: (code) => {
      console.log("Exit with code:", code);
      throw new Error("Exit");
    }
  }
};

const wasm = await WebAssembly.instantiateStreaming(
  fetch('module.wasm'),
  importObject
);
```

### Shared Array Buffer for Multi-threading

```javascript
// Check for SharedArrayBuffer support
if (!crossOriginIsolated) {
  console.warn("SharedArrayBuffer requires cross-origin isolation");
}

// Create shared buffer
const sharedBuffer = new SharedArrayBuffer(1024);
const sharedArray = new Int32Array(sharedBuffer);

// Pass to WASM
const wasm = await WebAssembly.instantiateStreaming(fetch('threaded.wasm'), {
  env: {
    memory: new WebAssembly.Memory({ initial: 1, shared: true }),
    shared_buffer: sharedBuffer
  }
});
```

-----

## AssemblyScript for WebAssembly

### Why AssemblyScript?

AssemblyScript uses TypeScript-like syntax and compiles to WASM. It's easier to learn than Rust for developers familiar with TypeScript/JavaScript.

### Basic Example

```typescript
// Basic function
export function add(a: i32, b: i32): i32 {
  return a + b;
}

// Using imported functions
@external("env", "console_log")
declare function console_log(ptr: i32): void;

// String handling
export function greet(name: string): string {
  return "Hello, " + name + "!";
}

// Custom memory allocation
@inline
export function computeChecksum(data: Uint8Array): u32 {
  let checksum: u32 = 0;
  for (let i = 0; i < data.length; i++) {
    checksum += data[i];
  }
  return checksum;
}

// Class definitions
export class Vector3 {
  constructor(
    public x: f32 = 0,
    public y: f32 = 0,
    public z: f32 = 0
  ) {}

  magnitude(): f32 {
    return Mathf.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
  }

  normalize(): void {
    const mag = this.magnitude();
    if (mag > 0) {
      this.x /= mag;
      this.y /= mag;
      this.z /= mag;
    }
  }
}
```

### Building with AssemblyScript

```bash
# Install AssemblyScript
npm install assemblyscript

# Compile to WASM
asc source.ts --outFile output.wasm --optimize

# Generate WASI binary
asc source.ts --outFile output.wasm --target wasi
```

-----

## WASM Use Cases and Examples

### Image Processing Pipeline

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn grayscale(pixels: &mut [u8], width: u32, height: u32) {
    for i in (0..pixels.len()).step_by(4) {
        let r = pixels[i] as f32;
        let g = pixels[i + 1] as f32;
        let b = pixels[i + 2] as f32;
        
        let gray = (0.299 * r + 0.587 * g + 0.114 * b) as u8;
        
        pixels[i] = gray;
        pixels[i + 1] = gray;
        pixels[i + 2] = gray;
    }
}

#[wasm_bindgen]
pub fn blur(pixels: &mut [u8], width: u32, height: u32, radius: u32) {
    let mut output = pixels.to_vec();
    let kernel_size = (radius * 2 + 1) as usize;
    let kernel_area = kernel_size * kernel_size;
    
    for y in radius..(height - radius) {
        for x in radius..(width - radius) {
            let mut r_sum = 0u32;
            let mut g_sum = 0u32;
            let mut b_sum = 0u32;
            
            for ky in 0..kernel_size {
                for kx in 0..kernel_size {
                    let px = (x + kx as u32 - radius) as usize;
                    let py = (y + ky as u32 - radius) as usize;
                    let idx = (py * width as usize + px) * 4;
                    
                    r_sum += pixels[idx] as u32;
                    g_sum += pixels[idx + 1] as u32;
                    b_sum += pixels[idx + 2] as u32;
                }
            }
            
            let idx = (y * width + x) as usize * 4;
            output[idx] = (r_sum / kernel_area as u32) as u8;
            output[idx + 1] = (g_sum / kernel_area as u32) as u8;
            output[idx + 2] = (b_sum / kernel_area as u32) as u8;
        }
    }
    
    pixels.copy_from_slice(&output);
}
```

### Physics Simulation

```rust
#[wasm_bindgen]
pub struct Particle {
    x: f32,
    y: f32,
    vx: f32,
    vy: f32,
    mass: f32,
}

#[wasm_bindgen]
impl Particle {
    #[wasm_bindgen(constructor)]
    pub fn new(x: f32, y: f32, vx: f32, vy: f32, mass: f32) -> Particle {
        Particle { x, y, vx, vy, mass }
    }
    
    pub fn update(&mut self, dt: f32, gravity: f32) {
        self.vy += gravity * dt;
        self.x += self.vx * dt;
        self.y += self.vy * dt;
    }
    
    pub fn get_x(&self) -> f32 { self.x }
    pub fn get_y(&self) -> f32 { self.y }
}

#[wasm_bindgen]
pub struct Simulation {
    particles: Vec<Particle>,
    width: f32,
    height: f32,
}

#[wasm_bindgen]
impl Simulation {
    #[wasm_bindgen(constructor)]
    pub fn new(width: f32, height: f32) -> Simulation {
        Simulation {
            particles: Vec::new(),
            width,
            height,
        }
    }
    
    pub fn add_particle(&mut self, x: f32, y: f32, vx: f32, vy: f32, mass: f32) {
        self.particles.push(Particle::new(x, y, vx, vy, mass));
    }
    
    pub fn step(&mut self, dt: f32) {
        for particle in &mut self.particles {
            particle.update(dt, 9.81);
            
            // Simple boundary collision
            if particle.y > self.height {
                particle.y = self.height;
                particle.vy *= -0.8;
            }
        }
    }
    
    pub fn get_particle_count(&self) -> usize {
        self.particles.len()
    }
}
```

-----

## Debugging and Tools

### wasm-objdump

```bash
# Disassemble WASM to WAT
wasm-objdump -d module.wasm -x

# Show sections
wasm-objdump -h module.wasm
```

### wasm-validate

```bash
# Validate a WASM binary
wasm-validate module.wasm
```

### wasm2wat

```bash
# Convert binary to text format
wasm2wat module.wasm -o module.wat
```

### wasm-opt

```bash
# Optimize for size
wasm-opt -O -o output.wasm input.wasm

# Optimize for speed
wasm-opt -O3 -o output.wasm input.wasm

# Remove debug info
wasm-opt --strip-debug -o output.wasm input.wasm
```

### Browser DevTools

Modern browsers provide WASM debugging in DevTools:
- View WASM source (with source maps)
- Set breakpoints in WAT view
- Inspect linear memory
- Profile WASM execution

-----

## Common Errors to Avoid

- **Forgetting #[no_mangle]**: Rust functions need this attribute to be exported
- **Using wrong types**: WASM has strict typing; use i32/f32 for web compatibility
- **Memory aliasing**: Don't hold pointers across WASM function calls
- **Not handling OOM**: Memory growth can fail; check for null returns
- **Debug vs Release**: Always test with release builds for performance
- **Assuming WASM is always faster**: For simple operations, JavaScript may be faster due to JS/WASM boundary overhead
