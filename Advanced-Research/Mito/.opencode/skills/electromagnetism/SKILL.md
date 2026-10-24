-----

## name: electromagnetism
description: >
  Expert electromagnetism assistant for physicists and engineers. Use this skill whenever the user needs:
  analysis of electrostatic and magnetostatic fields, solution of Maxwell's equations in various geometries,
  electromagnetic wave propagation and radiation calculations, antenna design and analysis,
  waveguides and transmission line analysis, or optical system design. Includes both theoretical
  foundations and practical applications.
trigger: Any physics or engineering problem involving electric or magnetic fields, electromagnetic waves,
  or radiation - from fundamental calculations to device design.
license: MIT
compatibility: opencode
metadata:
  audience: physicists
  category: physics

# Electromagnetism — Theory and Applications

Covers: **Electrostatics · Magnetostatics · Maxwell's Equations · Electromagnetic Waves · Radiation · Optics · Waveguides**

-----

## Fundamental Equations

### Maxwell's Equations (Differential Form)

| Equation | Differential | Integral Form | Physical Meaning |
|----------|-------------|---------------|------------------|
| Gauss's Law | ∇·E = ρ/ε₀ | ∮E·dA = Q/ε₀ | Electric charge creates divergence in E |
| Gauss's Law (Magnetism) | ∇·B = 0 | ∮B·dA = 0 | No magnetic monopoles |
| Faraday's Law | ∇×E = -∂B/∂t | ∮E·dl = -dΦ_B/dt | Changing B induces E |
| Ampère-Maxwell | ∇×B = μ₀J + μ₀ε₀∂E/∂t | ∮B·dl = μ₀I + μ₀ε₀dΦ_E/dt | Currents and changing E create B |

### Maxwell's Equations in Matter

```
∇·D = ρ_free
∇·B = 0
∇×E = -∂B/∂t
∇×H = J_free + ∂D/∂t
```

Where constitutive relations connect fields:
- D = εE = ε₀ε_r E (electric displacement)
- B = μH = μ₀μ_r H (magnetic field intensity)
- J = σE (Ohm's law for conductors)

### Electromagnetic Wave Equation

In free space (ρ = 0, J = 0):

```
∇²E - μ₀ε₀∂²E/∂t² = 0
∇²B - μ₀ε₀∂²B/∂t² = 0
```

Wave speed: c = 1/√(μ₀ε₀) ≈ 3×10⁸ m/s

### Poynting Theorem (Energy Conservation)

```
-∂/∂t (U_EM) = ∇·S + J·E
```

Energy density:
```
U_EM = ½(εE² + μH²)
```

Poynting vector (power flow):
```
S = E × H [W/m²]
```

Momentum density:
```
g_EM = S/c²
```

-----

## Electrostatics

### Coulomb's Law

```
F = (1/4πε₀) q₁q₂ r̂/r²
```

Electric field from point charge:
```
E = (1/4πε₀) q r̂/r²
```

### Electric Potential

For a charge distribution:
```
φ(r) = (1/4πε₀) ∫ρ(r')/|r-r'| dV'
```

Potential satisfies Poisson's equation:
```
∇²φ = -ρ/ε₀
```

### Boundary Conditions at Interfaces

```
E₁∥ = E₂∥ (tangential continuous)
D₁⊥ - D₂⊥ = σ_free (normal discontinuity)
```

For perfect conductors:
```
E_internal = 0
σ_induced = ε₀E_external
```

### Method of Images

For point charge near conducting plane (grounded):
- Replace plane with image charge of opposite sign
- Force on real charge equals force from image

**Point charge + grounded sphere**: Image charge position and magnitude given by inversion.

### Solving Laplace's Equation (∇²φ = 0)

| Geometry | Method | Solution Form |
|----------|--------|---------------|
| Sphere | Separation of variables | Legendre polynomials |
| Cylinder | Bessel functions | Fourier-Bessel series |
| Infinite planes | Method of images | Image charges |

### Capacitance

Parallel plate capacitor:
```
C = εA/d
```

Energy stored:
```
U = ½CV² = ½Q²/C
```

### Dielectrics

Polarization:
```
P = χ_eε₀E
```

Clausius-Mossotti relation:
```
(ε_r - 1)/(ε_r + 2) = (4π/3) Nα
```

-----

## Magnetostatics

### Biot-Savart Law

```
B(r) = (μ₀/4π) ∫I dl' × r̂/r²
```

Magnetic field from straight wire:
```
B = (μ₀I)/(2πr) φ̂
```

### Ampère's Law

For steady currents:
```
∮B·dl = μ₀I_enc
```

### Magnetic Vector Potential

```
B = ∇ × A
A(r) = (μ₀/4π) ∫J(r')/|r-r'| dV'
```

For a straight wire: A = -(μ₀I/2π) ln(r) ẑ

### Magnetic Dipole

Field of small current loop:
```
B = (μ₀/4πr³)[3(m·r̂)r̂ - m] (far field)
B = (μ₀I/2r) (near field, loop center)
```

Magnetic dipole moment:
```
m = I A
```

### Magnetic Materials

 magnetization M relates to H and B:
```
B = μ₀(H + M) = μ₀μ_r H
```

- **Diamagnetism**: μ_r < 1 (weak repulsion)
- **Paramagnetism**: μ_r > 1 (weak attraction)  
- **Ferromagnetism**: μ_r >> 1 (strong, hysteresis)

### Curie Law (Paramagnets)

```
χ = C/T
```

### Ferromagnetism

Weiss molecular field theory:
```
M = NμL(μ₀Hm + λM)/kT
```

Critical temperature (Curie temperature): T_C

-----

## Electromagnetic Waves

### Plane Wave Solutions

In free space:
```
E(z,t) = E₀ cos(kz - ωt + φ)
B(z,t) = B₀ cos(kz - ωt + φ)
```

Relations:
```
|B| = |E|/c
B = (1/c) k̂ × E
```

### Wave Properties

| Quantity | Formula |
|----------|---------|
| Angular frequency | ω = 2πf |
| Wave number | k = ω/c = 2π/λ |
| Impedance (free space) | η₀ = √(μ₀/ε₀) ≈ 377 Ω |
| Intensity | I = ½cε₀E₀² = S_avg |

### Wave Propagation in Matter

For dielectric (σ ≈ 0):
```
v = 1/√(με) = c/n
n = √(μ_r ε_r)
```

### Reflection and Refraction

**Snell's Law**:
```
n₁ sinθ₁ = n₂ sinθ₂
```

**Fresnel Coefficients** (perpendicular polarization):
```
r_s = (n₁ cosθ₁ - n₂ cosθ₂)/(n₁ cosθ₁ + n₂ cosθ₂)
t_s = 2n₁ cosθ₁/(n₁ cosθ₁ + n₂ cosθ₂)
```

**Critical angle** (total internal reflection):
```
θ_c = arcsin(n₂/n₁) for n₁ > n₂
```

### Total Internal Reflection

At angles beyond critical:
- Evanescent wave penetrates ~wavelength into second medium
- Phase shift occurs
- Goos-Hänchen shift (lateral beam displacement)

### Absorption and Dispersion

Complex refractive index:
```
ñ = n + iκ
```

Beer-Lambert law:
```
I(z) = I₀ e^(-αz)
```

Dispersion relation for transparent media:
```
n(ω) ≈ 1 + (ω_p²/ω₀² - ω²)
```

### Wave Polarization

| Polarization | Electric Field | Applications |
|--------------|----------------|--------------|
| Linear | Single direction | Antennas, filters |
| Circular | Rotating (E₀_x = E₀_y, ±90° phase) | Communications |
| Elliptical | General case | General |

-----

## Radiation and Antennas

### Accelerated Charge Radiation

Larmor formula (non-relativistic):
```
P = (μ₀q²a²)/(6πc)
```

Relativistic (Lienard):
```
P = (μ₀q²γ⁶)/(6πc)[a² + (γ²v × a)²/c²]
```

### Electric Dipole Radiation

Far field (r >> λ):
```
E = (μ₀p₀ω²)/(4πr) sinθ e^(ikr - iωt) φ̂
B = (1/c) E × r̂
```

Radiated power:
```
P = (μ₀p₀²ω⁴)/(12πc)
```

### Antenna Fundamentals

| Parameter | Definition |
|-----------|------------|
| **Directivity** | D = P(θ,φ)/P_avg (max ratio) |
| **Gain** | G = ηD (includes efficiency) |
| **Effective aperture** | A_eff = λ²G/(4π) |
| **Input impedance** | Z_in = V_in/I_in |
| **Bandwidth** | Frequency range for acceptable SWR |

### Common Antenna Types

| Antenna | Description | Typical Gain |
|---------|-------------|--------------|
| Half-wave dipole | λ/2 length, resonant | 2.15 dBi |
| Quarter-wave monopole | λ/4 over ground plane | 2.15 dBi |
| Yagi-Uda | Director + reflector elements | 5-15 dBi |
| Helical | Axial mode for circular polarization | 10-15 dBi |
| Parabolic dish | Reflector focusing | 20-40 dBi |
| Microstrip | Planar, printed circuit | 2-10 dBi |

### Array Factor

For N isotropic elements with spacing d and phase shift δ:
```
AF(θ) = |sin(Nψ/2)/sin(ψ/2)| where ψ = kd cosθ + δ
```

Phased arrays enable electronic beam steering.

### Friis Transmission Equation

```
P_r = P_t G_t G_r λ²/(4πR)² L
```

Where L includes polarization and mismatch losses.

-----

## Waveguides and Transmission Lines

### Transmission Line Equations

Telegrapher's equations:
```
∂V/∂z = -L ∂I/∂t - RI
∂I/∂z = -C ∂V/∂t - GV
```

Characteristic impedance:
```
Z₀ = √[(R + iωL)/(G + iωC)]
```

### Lossless Line (R = G = 0)

```
Z₀ = √(L/C)
v = 1/√(LC) = c/√(ε_r)
```

### Standing Wave Ratio

```
SWR = (1 + |Γ|)/(1 - |Γ|)
```

Reflection coefficient:
```
Γ = (Z_L - Z₀)/(Z_L + Z₀)
```

### Waveguide Modes

**Rectangular waveguide** (a > b):

| Mode | Cutoff Frequency | Field Pattern |
|------|------------------|---------------|
| TE₁₀ | f_c = c/(2a) | Single half-sine in x |
| TM₁₁ | f_c = c√[(1/a)² + (1/b)²] | More complex |

TE modes have E_z = 0; TM modes have H_z = 0.

### Waveguide Impedance

```
Z_TE = η √(1 - (f_c/f)²)
Z_TM = η / √(1 - (f_c/f)²)
```

Below cutoff: evanescent modes (exponential decay).

### Cavity Resonators

For rectangular cavity (a × b × d):
```
f_mnl = (c/2) √[(m/a)² + (n/b)² + (l/d)²]
```

Quality factor:
```
Q = ω₀ × (stored energy)/(power loss)
```

-----

## Optics

### Lensmaker's Equation

For thin lens in air:
```
1/f = (n - 1)(1/R₁ - 1/R₂)
```

Sign conventions: R positive if center of curvature is to the right.

### Gaussian Beam Propagation

Complex beam parameter:
```
q(z) = z + i z_R
```

Where Rayleigh range:
```
z_R = πw₀²/λ
```

Beam waist:
```
w(z) = w₀ √[1 + (z/z_R)²]
```

### Beam Divergence

```
θ = λ/(πw₀)
```

### Optical Resonators (Fabry-Perot)

Free spectral range:
```
Δν_FSR = c/(2L)
```

Finesse:
```
F = π√R/(1 - R)
```

Peak width:
```
δν = Δν_FSR/F
```

### Nonlinear Optics

**Second harmonic generation**:
- Requires non-centrosymmetric material
- Phase matching required for efficiency
- Sellmeier equations for index dispersion

**Kerr effect** (intensity-dependent index):
```
n = n₀ + n₂ I
```

-----

## Relativistic Electromagnetism

### Transformation of Fields

Between frames moving at velocity v along x-axis:

```
E'∥ = E∥
E'⊥ = γ(E⊥ + v × B)
B'∥ = B∥
B'⊥ = γ(B⊥ - v × E/c²)
```

### Electromagnetic Tensor

```
F^{μν} = [0, -E_x/c, -E_y/c, -E_z/c;
          E_x/c, 0, -B_z, B_y;
          E_y/c, B_z, 0, -B_x;
          E_z/c, -B_y, B_x, 0]
```

Lorentz transformation of this 4-tensor gives field transformation.

-----

## Common Errors to Avoid

- Forgetting displacement current in Ampère's law (Maxwell's correction)
- Applying electrostatic formulas to dynamic situations
- Confusing B and H fields in materials
- Using incorrect sign conventions in image charge problems
- Confusing phase velocity with group velocity in dispersive media
- Neglecting skin effect at high frequencies in conductors
- Forgetting boundary conditions at dielectric interfaces
- Using ray optics when wave effects are significant

-----

## Key References

- **Classical Electrodynamics** by Jackson — Definitive graduate text
- **Introduction to Electrodynamics** by Griffiths — Excellent introduction
- **Antenna Theory** by Balanis — Comprehensive antenna design
- **Principles of Optics** by Born & Wolf — Classical optics reference

