-----

## name: calculus
description: >
  Expert calculus assistant for mathematicians, scientists, and engineers. Use this skill whenever the user needs:
  help with differentiation and integration, solving differential equations, applying Taylor series,
  understanding multivariable calculus, working with vector calculus, or analyzing convergence of series.
  Includes both fundamental techniques and advanced applications.
trigger: Any mathematical problem involving rates of change, accumulation, optimization, or mathematical
  modeling where calculus provides the analytical framework.
license: MIT
compatibility: opencode
metadata:
  audience: mathematicians
  category: mathematics

# Calculus — Differential and Integral Methods

Covers: **Single Variable Calculus · Multivariable Calculus · Differential Equations · Series · Vector Calculus**

-----

## Foundational Concepts

### The Derivative

The derivative measures instantaneous rate of change:

```
f'(x) = lim_{h→0} [f(x+h) - f(x)]/h = df/dx
```

Geometrically: slope of tangent line at point.

### Basic Differentiation Rules

| Function f(x) | Derivative f'(x) |
|--------------|------------------|
| x^n | nx^{n-1} |
| sin(x) | cos(x) |
| cos(x) | -sin(x) |
| e^x | e^x |
| ln(x) | 1/x |
| a^x | a^x ln(a) |
| tan(x) | sec²(x) |
| sec(x) | sec(x)tan(x) |

### Product Rule

```
(uv)' = u'v + uv'
```

### Quotient Rule

```
(u/v)' = (u'v - uv')/v²
```

### Chain Rule

```
(f∘g)'(x) = f'(g(x)) · g'(x)
```

In Leibniz notation:
```
dy/dx = (dy/du)(du/dx)
```

### Implicit Differentiation

For F(x,y) = 0:
```
dy/dx = -∂F/∂x / ∂F/∂y
```

Example: x² + y² = r²
```
2x + 2y dy/dx = 0 → dy/dx = -x/y
```

### Higher Derivatives

```
f''(x) = d²f/dx²
f^(n)(x) = d^n f/dx^n
```

-----

## Integration Fundamentals

### The Integral as Antiderivative

```
∫f(x)dx = F(x) + C
```

Where F'(x) = f(x)

### Fundamental Theorem of Calculus

If F is any antiderivative of f:

```
∫_a^b f(x)dx = F(b) - F(a)
```

This connects differentiation and integration as inverse operations.

### Basic Integration Formulas

| Integral | Result |
|----------|--------|
| ∫x^n dx | x^{n+1}/(n+1) + C (n ≠ -1) |
| ∫1/x dx | ln|x| + C |
| ∫e^x dx | e^x + C |
| ∫sin(x) dx | -cos(x) + C |
| ∫cos(x) dx | sin(x) + C |
| ∫sec²(x) dx | tan(x) + C |
| ∫dx/√(a²-x²) | arcsin(x/a) + C |
| ∫dx/(a²+x²) | (1/a) arctan(x/a) + C |

### Integration by Parts

```
∫u dv = uv - ∫v du
```

LIATE rule: Choose u in order: **L**ogarithmic, **I**nverse trig, **A**lgebraic, **T**rigonometric, **E**xponential

Example: ∫x e^x dx
- u = x, dv = e^x dx
- du = dx, v = e^x
- = x e^x - ∫e^x dx = x e^x - e^x + C

### Trigonometric Integrals

**Powers of sin and cos**: Use identities:
- sin²x = (1 - cos(2x))/2
- cos²x = (1 + cos(2x))/2
- sin x cos x = sin(2x)/2

**For odd powers**: Save one factor, convert rest using sin²x + cos²x = 1

### Trigonometric Substitution

| Expression | Substitution | Result |
|------------|-------------|--------|
| √(a² - x²) | x = a sinθ | a cosθ |
| √(a² + x²) | x = a tanθ | a secθ |
| √(x² - a²) | x = a secθ | a tanθ |

### Partial Fractions

For rational functions P(x)/Q(x):
1. Divide if degree(P) ≥ degree(Q)
2. Factor Q(x) into linear/quadratic factors
3. Set up partial fraction decomposition
4. Solve for coefficients

### Rationalizing Substitutions

For integrals involving √{ax + b}: let u = √{ax + b}

-----

## Applications of Integration

### Area Under Curve

```
A = ∫_a^b f(x)dx (f(x) ≥ 0)
```

Between two curves:
```
A = ∫_a^b |f(x) - g(x)| dx
```

### Volume of Revolution

**Washer method** (around x-axis):
```
V = π∫_a^b [f(x)]² dx
```

**Shell method** (around y-axis):
```
V = 2π∫_a^b x f(x) dx
```

### Arc Length

For y = f(x):
```
s = ∫_a^b √[1 + (f'(x))²] dx
```

### Surface Area of Revolution

Around x-axis:
```
S = 2π∫_a^b f(x) √[1 + (f'(x))²] dx
```

### Center of Mass

For region with density ρ(x):
```
x̄ = (∫_a^b xρ(x)f(x)dx) / (∫_a^b ρ(x)f(x)dx)
```

### Work Problems

```
W = ∫F(x)dx
```

Examples:
- Spring: W = ½kx²
- Lifting: W = ∫mg dy
- Pumping: W = ∫ρg A(y) dy

-----

## Sequences and Series

### Convergence Tests

| Test | Application | Statement |
|------|-------------|-----------|
| **nth-term** | All series | lim a_n ≠ 0 → diverges |
| **Geometric** | a_n = ar^{n-1} | \|r\| < 1 converges |
| **p-series** | a_n = 1/n^p | p > 1 converges |
| **Integral** | a_n = f(n), f decreasing | ∫f converges ↔ series converges |
| **Comparison** | a_n ≤ b_n | b converges → a converges |
| **Limit Comparison** | lim a_n/b_n = L | Both converge or diverge |
| **Ratio** | lim |a_{n+1}/a_n| = r | r < 1 converges |
| **Root** | lim sup |a_n|^{1/n} = r | r < 1 converges |
| **Alternating** | a_n ≥ 0, decreasing | Alternating series converges |

### Power Series

Series of form:
```
Σ a_n (x - c)^n
```

**Radius of convergence** (Cauchy-Hadamard):
```
R = 1/limsup |a_n|^{1/n}
```

### Taylor Series

Taylor expansion about x = a:
```
f(x) = Σ f^{(n)}(a)/n! · (x - a)^n
```

**Maclaurin series**: Taylor series about x = 0

Common expansions:
```
e^x = Σ x^n/n! = 1 + x + x²/2! + ...
sin x = Σ (-1)^n x^{2n+1}/(2n+1)! 
cos x = Σ (-1)^n x^{2n}/(2n)!
ln(1+x) = Σ (-1)^{n+1} x^n/n  (|x| < 1)
(1+x)^α = Σ C(α,n) x^n
```

### Remainder Estimation

For Taylor series, remainder after n terms:
```
|R_n(x)| ≤ M|x-a|^{n+1}/(n+1)!
```

### Fourier Series

For periodic function f(x) with period 2L:
```
f(x) = a₀/2 + Σ [a_n cos(nπx/L) + b_n sin(nπx/L)]
```

Coefficients:
```
a_n = (1/L) ∫_{-L}^L f(x) cos(nπx/L) dx
b_n = (1/L) ∫_{-L}^L f(x) sin(nπx/L) dx
```

-----

## Multivariable Calculus

### Partial Derivatives

For f(x,y):
```
∂f/∂x = lim_{h→0} [f(x+h,y) - f(x,y)]/h
∂f/∂y = lim_{h→0} [f(x,y+h) - f(x,y)]/h
```

### Chain Rule (Multivariable)

For z = f(x,y), x = g(t), y = h(t):
```
dz/dt = ∂f/∂x · dx/dt + ∂f/∂y · dy/dt
```

For z = f(x,y), x = g(u,v), y = h(u,v):
```
∂z/∂u = ∂f/∂x ∂x/∂u + ∂f/∂y ∂y/∂u
∂z/∂v = ∂f/∂x ∂x/∂v + ∂f/∂y ∂y/∂v
```

### Gradient

```
∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z)
```

Direction of steepest ascent; magnitude = maximum directional derivative.

### Directional Derivative

```
D_uf = ∇f · û
```

Where û is unit vector in direction.

### Multiple Integrals

**Double integral** over region R:
```
∬_R f(x,y) dA
```

**Triple integral**:
```
∭_V f(x,y,z) dV
```

Change of variables with Jacobian:
```
∭_V f dV = ∭_{V'} f(x(u,v,w),y(...),z(...)) |J| du dv dw
```

Common coordinate systems:
- Polar: dA = r dr dθ
- Cylindrical: dV = r dr dθ dz
- Spherical: dV = r² sinφ dr dφ dθ

### Line Integrals

For vector field F and curve C:
```
∫_C F · dr = ∫ F · T ds
```

For scalar field:
```
∫_C f ds = ∫ f |r'(t)| dt
```

### Surface Integrals

For surface S with normal n̂:
```
∬_S F · n̂ dS = ∬_D F(r(u,v)) · (r_u × r_v) du dv
```

-----

## Vector Calculus

### Gradient, Divergence, and Curl

| Operator | Definition | Output |
|----------|------------|--------|
| ∇f | (∂f/∂x, ∂f/∂y, ∂f/∂z) | Vector |
| ∇·F | ∂F_x/∂x + ∂F_y/∂y + ∂F_z/∂z | Scalar |
| ∇×F | (∂F_z/∂y - ∂F_y/∂z, ...) | Vector |

### Identities

```
∇·(∇×F) = 0 (divergence of curl = 0)
∇×(∇f) = 0 (curl of gradient = 0)
∇·(∇f) = ∇²f (Laplacian)
```

### Green's Theorem (2D)

```
∮_C P dx + Q dy = ∬_R (∂Q/∂x - ∂P/∂y) dA
```

### Stokes' Theorem

```
∮_C F · dr = ∬_S (∇×F) · n̂ dS
```

### Divergence Theorem

```
∬_S F · n̂ dS = ∭_V ∇·F dV
```

### Fundamental Theorem for Line Integrals

For conservative field F = ∇f:
```
∫_C F · dr = f(r_end) - f(r_start)
```

Path-independent for simply connected regions.

-----

## Differential Equations

### First-Order ODEs

**Separable**:
```
dy/dx = g(x)h(y)
∫ dy/h(y) = ∫ g(x) dx
```

**Linear** (integrating factor):
```
dy/dx + P(x)y = Q(x)
μ = exp(∫P dx)
d/dx(μy) = μQ
```

**Exact**:
```
M(x,y)dx + N(x,y)dy = 0
∂M/∂y = ∂N/∂x
```

### Second-Order Linear ODEs

Homogeneous with constant coefficients:
```
ay'' + by' + cy = 0
```

Characteristic equation:
```
ar² + br + c = 0
```

| Roots | Solution Form |
|-------|---------------|
| Real, r₁, r₂ | y = C₁e^{r₁x} + C₂e^{r₂x} |
| Real repeated r | y = (C₁ + C₂x)e^{rx} |
| Complex α ± iβ | y = e^{αx}(C₁cosβx + C₂sinβx) |

### Cauchy-Euler Equations

Form: ax²y'' + bxy' + cy = 0
Try solution y = x^r → characteristic equation.

### Power Series Solutions

For y'' + P(x)y' + Q(x)y = 0:
```
y = Σ a_n x^n
```

Find recurrence relation for coefficients.

### Special Functions

| Equation | Solution | Applications |
|----------|----------|--------------|
| Bessel | J_n(x), Y_n(x) | Cylindrical symmetry |
| Legendre | P_n(x), Q_n(x) | Spherical symmetry |
| Hermite | H_n(x) | Quantum harmonic oscillator |
| Laguerre | L_n(x) | Hydrogen atom |

### Laplace Transform

```
L{f(t)} = F(s) = ∫_0^∞ e^{-st} f(t) dt
```

Transforms:
- L{f'} = sF(s) - f(0)
- L{f''} = s²F(s) - sf(0) - f'(0)
- L{∫_0^t f(τ)dτ} = F(s)/s

### Solving PDEs

**Separation of variables**: Assume u(x,t) = X(x)T(t)
**Fourier series**: Expand initial conditions in eigenfunctions
**Transform methods**: Laplace (time), Fourier (space)

-----

## Series Solutions and Special Cases

### Convergence of Power Series

**Absolute convergence**: If Σ|a_n| converges
**Conditional convergence**: Converges but not absolutely

**Ratio test**:
```
lim |a_{n+1}/a_n| = L
L < 1 → converges
L > 1 → diverges
L = 1 → inconclusive
```

**Interval of convergence**: Always centered at expansion point; test endpoints separately.

### Operations on Power Series

- Differentiate term-by-term within radius of convergence
- Integrate term-by-term
- Add/subtract: combine coefficients
- Multiply: convolution of coefficients
- Compose: more complex, requires substitution

### Asymptotic Series

Series that approximate function as parameter → ∞ or → 0:
```
f(x) ~ a₀ + a₁/x + a₂/x² + ...
```

Useful when ordinary series diverge.

-----

## Common Errors to Avoid

- Forgetting constant of integration C
- Applying chain rule incorrectly
- Using wrong sign in integration by parts
- Confusing converge/diverged in series tests
- Forgetting to check endpoints in interval of convergence
- Mixing up gradient (vector) with partial derivatives
- Forgetting Jacobian in change of variables
- Incorrectly applying product rule in vector derivatives
- Confusing curl and divergence physically
- Forgetting initial/boundary conditions in ODEs/PDEs

-----

## Key References

- **Calculus** by Spivak — Rigorous introduction
- **Principles of Mathematical Analysis** by Rudin — Advanced calculus
- **Advanced Engineering Mathematics** by Kreyszig — Applied perspective
- **Mathematical Methods for Physicists** by Arfken — Physics applications

