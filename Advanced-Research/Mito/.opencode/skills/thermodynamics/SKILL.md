-----

## name: thermodynamics
description: >
  Expert thermodynamics assistant for physicists and engineers. Use this skill whenever the user needs:
  help with thermodynamic laws, heat engines, entropy, phase transitions, or thermodynamic potentials.
  Includes both classical and statistical mechanics perspectives.
trigger: Any physics or engineering problem involving heat, work, energy, or entropy.
license: MIT
compatibility: opencode
metadata:
  audience: physicists
  category: physics

# Thermodynamics — Energy, Heat, and Entropy

Covers: **Laws of Thermodynamics · Thermodynamic Potentials · Heat Engines · Phase Transitions · Kinetic Theory · Statistical Mechanics**

-----

## The Four Laws

### Zeroth Law

If system A is in equilibrium with B, and B with C, then A is in equilibrium with C.

Establishes temperature as property of equilibrium.

### First Law

Energy conservation:
```
ΔU = Q - W
```

Or differential:
```
dU = δQ - δW
```

U is state function.

Forms of work:
- PdV work: δW = P dV
- Electrical: δW = μdq
- Surface: δW = γ dA

### Second Law

Entropy increases in isolated system:
```
ΔS ≥ 0
```

Kelvin-Planck: No process converting all heat to work.
Clausius: No process transferring heat from cold to hot spontaneously.

### Third Law (Nernst)

As T → 0, S → S₀ (often 0 for perfect crystal).
Cannot reach absolute zero in finite steps.

### Carnot Theorem

Maximum efficiency for heat engine:
```
η_C = 1 - T_C/T_H
```

All reversible engines have same efficiency.

### Clausius Inequality

For any cyclic process:
```
∮ δQ/T ≤ 0
```

Equality for reversible cycles.

### Entropy Definition

For reversible process:
```
dS = δQ_rev/T
```

Statistical (Boltzmann):
```
S = k_B ln Ω
```

-----

## Thermodynamic Potentials

### Internal Energy

U = U(S, V, N)
Fundamental equation.

### Enthalpy

```
H = U + PV
```

H = H(S, P, N)

Useful for constant pressure processes.

### Helmholtz Free Energy

```
F = U - TS
```

F = F(T, V, N)

Useful at constant T, V.

### Gibbs Free Energy

```
G = H - TS = μN
```

G = G(T, P, N)

Useful at constant T, P.

### Gibbs Potential

```
Φ = μN
```

Grand canonical: J = G - μN.

### Maxwell Relations

From fundamental equations:
```
(∂S/∂V)_T = (∂P/∂T)_V
(∂S/∂P)_T = -(∂V/∂T)_P
(∂V/∂S)_P = (∂T/∂P)_S
(∂P/∂S)_V = -(∂T/∂V)_S
```

General pattern: switch variables, sign changes.

### Thermodynamic Identities

```
dU = T dS - P dV + μ dN
dH = T dS + V dP + μ dN
dF = -S dT - P dV + μ dN
dG = -S dT + V dP + μ dN
```

### Euler Relations

Extensive variables homogeneous of degree 1:
```
U = TS - PV + μN
H = TS + μN
F = -TS + μN
G = μN
```

-----

## State Equations

### Ideal Gas

```
PV = nRT
```

Molecular: m v²/2 = 3kT/2

### Van der Waals

```
(P + a n²/V²)(V - nb) = nRT
```

a: attractive
b: excluded volume

### Virial Expansion

```
Z = PV/RT = 1 + B(T)/V + C(T)/V² + ...
```

### Compressibility

Isothermal:
```
κ_T = - (1/V) (∂V/∂P)_T
```

Adiabatic:
```
κ_S = - (1/V) (∂V/∂P)_S
```

### Thermal Expansion

```
α = (1/V) (∂V/∂T)_P
```

### Heat Capacities

```
C_V = (∂U/∂T)_V
C_P = (∂H/∂T)_P
```

Relation:
```
C_P - C_V = TVα²/(κ_T)
```

For ideal gas: C_P - C_V = nR

### Gamma Ratio

```
γ = C_P/C_V
```

Monatomic ideal: γ = 5/3
Diatomic: γ = 7/5

-----

## Heat Engines and Refrigerators

### Heat Engine

Device converting heat to work:
```
η = W/Q_H = 1 - Q_C/Q_H
```

Carnot efficiency:
```
η_C = 1 - T_C/T_H
```

### Otto Cycle

Intake → compression → combustion → exhaust.
Spark ignition engine.
Efficiency: η = 1 - r^{γ-1}

### Diesel Cycle

Compression → injection → combustion → exhaust.
Compression ignition.
Efficiency: η = 1 - 1/r^{γ-1}(T_3 - T_1)/(T_4 - T_2)

### Rankine Cycle

Steam power cycle:
- Boiler → turbine → condenser → pump → boiler

Superheat, regeneration improve efficiency.

### Brayton Cycle

Gas turbine:
- Compressor → combustion → turbine → exhaust

### Refrigerator

Heat pump from cold to hot:
```
COP = Q_C/W = T_C/(T_H - T_C)
```

### Heat Pump

```
COP = Q_H/W = T_H/(T_H - T_C)
```

### Carnot Refrigerator

```
COP_max = T_C/(T_H - T_C)
```

### Coefficient of Performance

Carnot is maximum, all real devices less efficient.

-----

## Kinetic Theory

### Pressure

From molecular collisions:
```
P = (1/3) n m ⟨v²⟩
```

For ideal gas:
```
P = n k T
```

### Temperature

Average kinetic energy:
```
⟨KE⟩ = (3/2) k T
```

Translational only.

### Maxwell-Boltzmann Distribution

Speed distribution:
```
f(v) = 4π (m/2πkT)^{3/2} v² e^{-mv²/2kT}
```

Most probable: v_mp = √(2kT/m)
Mean: ⟨v⟩ = √(8kT/πm)
RMS: √(3kT/m)

### Mean Free Path

```
λ = 1/(√2 n σ)
```

For hard spheres: σ = πd²

### Transport Coefficients

Viscosity: η = (1/3) n m v̄ λ
Thermal conductivity: κ = (1/3) n c_v v̄ λ
Diffusion: D = (1/3) v̄ λ

### Chapman-Enskog

Solve Boltzmann equation.
Corrections to simple kinetic theory.

### Diffusion

Fick's first law:
```
J = -D ∇n
```

Second law:
```
∂n/∂t = D ∇²n
```

### Brownian Motion

Random walk:
⟨x²⟩ = 2Dt

Einstein relation:
```
D = kT/ξ
```

-----

## Statistical Mechanics

### Microstates and Macrostates

- Microstate: exact specification
- Macrostate: macroscopic variables

Boltzmann: S = k_B ln Ω

### Partition Function

```
Z = Σ_i e^{-βE_i}
```

For canonical ensemble.

### Thermodynamic quantities

U = -∂ ln Z/∂β
S = k_B (ln Z + βU)
F = -k_B T ln Z

### Maxwell-Boltzmann Statistics

Distinguishable particles:
```
f(E) = e^{-βE}
```

Applies to classical ideal gas.

### Fermi-Dirac Statistics

Indistinguishable, half-integer spin:
```
f(E) = 1/(e^{(E-μ)/kT} + 1)
```

Pauli principle.

### Bose-Einstein Statistics

Indistinguishable, integer spin:
```
f(E) = 1/(e^{(E-μ)/kT} - 1)
```

Bosons can condense.

### Quantum Statistics

At high T → MB limit.
At low T: degeneracy important.

### Degeneracy Temperature

Fermi:
```
T_F = E_F/k
```

Bose:
```
T_c = 2πℏ²/(mk)[n/ζ(3/2)]^{2/3}
```

### Blackbody Radiation

Photon gas:
```
u = a T⁴
```

Energy density: u = σ/c T⁴
Stefan-Boltzmann: σ = π²k⁴/(60ℏ³c²)

### Debye Model

Phonons in solid:
- 3 acoustic branches
- Cutoff frequency (Debye)

Heat capacity: C ~ T³ at low T.

-----

## Phase Transitions

### Phase Equilibrium

Gibbs phase rule:
```
F = C - P + 2
```

C components, P phases.

### Clausius-Clapeyron

For phase boundary:
```
dP/dT = ΔS/ΔV = ΔH/(TΔV)
```

### Clapeyron Equation

For liquid-vapor:
```
dP/dT = L/(TΔV)
```

### Latent Heat

Heat absorbed/released:
```
L = T ΔS = ΔH
```

### Phase Diagrams

Lines of equilibrium:
- Triple point
- Critical point

### Critical Point

Properties diverge:
- Heat capacity
- Correlation length

Critical exponents.

### Order Parameter

Zero in disordered phase:
- Magnetization
- Density difference

Breaks symmetry.

### First Order

Discontinuous change:
- Latent heat
- Hysteresis

### Second Order

Continuous change:
- Heat capacity divergence
- Critical opalescence

### Ehrenfest Classification

First derivatives discontinuous: 1st order
Second derivatives discontinuous: 2nd order

### Landau Theory

Expand free energy in order parameter:
F = F₀ + a(T-T₀)φ² + b φ⁴ + ...

Predicts mean-field exponents.

### Scaling

Near critical point:
```
X ~ |t|^{-γ}, t = (T-T_c)/T_c
```

Universal exponents.

### Renormalization Group

Wilsonian:
- Integrate out short wavelengths
- Fixed points → critical points

### Ginzburg Criterion

Mean-field valid when fluctuations small:
```
|(T-T_c)/T_c| >> Gi
```

### Superfluidity

Bose-Einstein of ⁴He.
Critical velocity.
Lambda point.

### Superconductivity

Zero resistance.
Meissner effect.
Cooper pairs.

### Phase Transitions in Fields

- Magnetic field for ferromagnets
- Electric field for ferroelectrics

-----

## Mixtures and Solutions

### Chemical Potential

For component i:
```
μ_i = (∂G/∂n_i)_{T,P,n_j≠i}
```

Equilibrium: μ_i equal in all phases.

### Partial Molar Properties

Partial molar volume:
```
V̄_i = (∂V/∂n_i)_{T,P,n_j}
```

### Gibbs-Duhem

```
Σ n_i dμ_i = 0
```

### Raoult's Law

For ideal solution:
```
p_i = x_i p_i*
```

### Henry's Law

For dilute solution:
```
p_i = x_i k_i
```

### Activity

```
a_i = γ_i x_i
```

Corrects non-ideality.

### Free Energy of Mixing

```
ΔF_mix = nRT Σ x_i ln x_i
```

Negative → mixing spontaneous.

### Colligative Properties

- Boiling point elevation
- Freezing point depression
- Osmotic pressure

### Gibbs Phase Rule

For non-reactive system:
F = C - P + 2

### Eutectic

Complete liquid miscibility, solid immiscibility.

### Lever Rule

Phase diagram analysis:
Amounts = lever arm lengths.

-----

## Non-Equilibrium

### Local Equilibrium

Near equilibrium: local variables well-defined.

### Entropy Production

Rate of entropy increase:
```
σ = Σ J_i X_i
```

Fluxes × forces.

### Onsager Reciprocal Relations

Linear response:
```
J_L = Σ L_{lk} X_k
```

L_{lk} = L_{kl}.

### Fourier's Law

Heat conduction:
```
q = -κ ∇T
```

### Newton's Law

Viscosity:
```
τ = η γ̇
```

### Fick's Law

Diffusion:
```
J = -D ∇c
```

### Linear Response

Transport coefficients related.

### Boltzmann Equation

Distribution function evolution:
```
∂f/∂t + v·∇_x f + F/m·∇_v f = (∂f/∂t)_c
```

Collision term.

### H-Theorem

Entropy increases:
```
∂S/∂t ≥ 0
```

Approaches equilibrium.

### Green-Kubo

Transport from equilibrium fluctuations:
```
D = ∫₀^∞ ⟨v(t)v(0)⟩ dt
```

### Chapman-Enskog

From Boltzmann to hydrodynamics:
- Euler equations
- Navier-Stokes

### Hydrodynamic Equations

Continuity: ∂ρ/∂t + ∇·(ρv) = 0
Momentum: ρDv/Dt = -∇P + η∇²v
Energy: ρC_v dT/dt = κ∇²T

### Irreversible Processes

Thermoelectric effects:
- Seebeck
- Peltier
- Thomson

-----

## Common Errors to Avoid

- Confusing heat and temperature
- Using wrong sign conventions for work
- Applying reversible formulas to irreversible processes
- Confusing internal energy with enthalpy
- Forgetting that entropy is a state function
- Using ideal gas for high-pressure conditions
- Confusing partial molar with molar properties
- Applying equilibrium formulas to non-equilibrium
- Ignoring third law when computing entropy differences
- Confusing spontaneous with reversible processes
- Using mean-field exponents for low dimensions

-----

## Key References

- **Thermodynamics** by Callen — Elegant introduction
- **Statistical Physics** by Landau & Lifshitz — Comprehensive
- **Physical Chemistry** by McQuarrie — Chemistry focus
- **Heat and Thermodynamics** by Zemansky — Classical approach

