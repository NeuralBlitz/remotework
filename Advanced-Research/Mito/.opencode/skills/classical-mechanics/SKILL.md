---

## name: classical-mechanics
description: >
  Classical mechanics expert for analyzing motion, forces, energy, and mechanical systems.
  Use this skill whenever the user needs: solving dynamics problems, applying Newton's
  laws, using Lagrangian and Hamiltonian mechanics, analyzing orbital motion, studying
  oscillations and waves, modeling collisions, or any task involving the physical analysis
  of mechanical systems. This skill covers Newtonian mechanics, analytical mechanics, and
  their applications to real-world engineering and physics problems.
license: MIT
compatibility: opencode
metadata:
  audience: physicists
  category: physics

# Classical Mechanics — Newtonian Dynamics and Motion Analysis

Covers: **Newton's Laws · Lagrangian Mechanics · Hamiltonian Mechanics · Central Forces · Orbital Dynamics · Rigid Body Motion · Oscillations · Collisions**

-----

## Newton's Laws and Particle Dynamics

### Newton's Three Laws

**First Law (Inertia):** A particle remains at rest or in uniform motion unless acted upon by a force.

**Second Law:** The rate of change of momentum equals the applied force:
```
F = dp/dt = d(mv)/dt
```

For constant mass:
```
F = ma
```

**Third Law:** For every action, there is an equal and opposite reaction.

### Solving Newton's Equations

```python
import numpy as np
from scipy.integrate import odeint

# Numerical solution of Newton's equations
def newton_solver(forces, initial_conditions, t_span, mass=1.0):
    """
    Solve particle motion under given forces.
    
    Parameters:
    - forces: function returning F(t, state) = [Fx, Fy, Fz]
    - initial_conditions: [x0, y0, z0, vx0, vy0, vz0]
    - t_span: (t0, tf) or array of time points
    - mass: particle mass
    """
    def derivatives(state, t):
        x, y, z, vx, vy, vz = state
        Fx, Fy, Fz = forces(state, t)
        
        return [vx, vy, vz, Fx/mass, Fy/mass, Fz/mass]
    
    solution = odeint(derivatives, initial_conditions, t_span)
    return solution

# Example: Projectile motion with drag
def projectile_drag(state, t):
    x, y, vx, vy = state
    
    # Drag force: F = -k * v
    k = 0.1  # drag coefficient
    v = np.sqrt(vx**2 + vy**2)
    Fx = -k * vx
    Fy = -9.81 * mass - k * vy
    
    return [vx, vy, Fx/mass, Fy/mass]

# Solve
t = np.linspace(0, 2, 100)
mass = 1.0
initial = [0, 0, 10, 5]  # x, y, vx, vy
sol = newton_solver(projectile_drag, initial, t, mass)
```

### Constraint Forces

```python
# Constraint types
constraint_types = {
    'holonomic': {
        'equation': 'f(r₁, r₂, ..., t) = 0',
        'example': 'Bead on a wire: f(x,y,z) = 0'
    },
    'nonholonomic': {
        'equation': 'f(r, v, t) = 0 (not integrable)',
        'example': 'Rolling without slipping: v = rω'
    },
    ' scleronomous': 'No explicit time dependence',
    'rheonomous': 'Time-dependent constraints'
}

# Lagrange multipliers for constraint forces
def constraint_force(constraint_eq, lambda_mult, position):
    """
    Calculate constraint force using Lagrange multiplier.
    """
    # For constraint f(r) = 0, force is F = -λ∇f
    grad_f = np.gradient(constraint_eq, position)
    F_constraint = -lambda_mult * grad_f
    return F_constraint
```

-----

## Work, Energy, and Conservation

### Work-Energy Theorem

The work done by all forces equals the change in kinetic energy:

```python
def work_kinetic_energy(forces, trajectory):
    """
    Calculate work and verify work-energy theorem.
    """
    kinetic_energies = []
    works = []
    work = 0
    
    for i in range(len(trajectory) - 1):
        # Kinetic energy: T = ½mv²
        v = trajectory[i, 3:6]  # velocities
        T = 0.5 * np.dot(v, v)
        kinetic_energies.append(T)
        
        # Work: W = ∫F·dr
        dr = trajectory[i+1, :3] - trajectory[i, :3]
        F = forces(trajectory[i], 0)[:3]
        dW = np.dot(F, dr)
        work += dW
        works.append(work)
    
    return works, kinetic_energies

# Conservative forces and potential energy
conservative_forces = {
    'gravity': {
        'force': 'F = -mgĵ',
        'potential': 'U = mgy'
    },
    'spring': {
        'force': 'F = -kx',
        'potential': 'U = ½kx²'
    },
    'gravitational': {
        'force': 'F = -GMm/r² r̂',
        'potential': 'U = -GMm/r'
    },
    'Coulomb': {
        'force': 'F = kq₁q₂/r² r̂',
        'potential': 'U = kq₁q₂/r'
    }
}
```

### Conservation Laws

| Quantity | Condition | Mathematical Statement |
|----------|-----------|----------------------|
| **Linear Momentum** | No external force | dp/dt = 0 |
| **Angular Momentum** | No external torque | dL/dt = 0 |
| **Energy** | Conservative forces | E = T + U = constant |
| **Center of Mass** | No external forces | R_cm = constant |

```python
# Check conservation laws
def check_conservation(solution, mass):
    """Verify conservation of momentum and energy."""
    # Extract positions and velocities
    positions = solution[:, :3]
    velocities = solution[:, 3:6]
    
    # Total momentum (should be constant)
    total_momentum = mass * np.sum(velocities, axis=0)
    
    # Total angular momentum (about origin)
    angular_momentum = np.cross(positions, mass * velocities)
    L_total = np.sum(angular_momentum, axis=0)
    
    # Total energy (if conservative)
    v_squared = np.sum(velocities**2, axis=1)
    kinetic = 0.5 * mass * v_squared
    
    return {
        'linear_momentum': total_momentum,
        'angular_momentum': L_total,
        'kinetic_energy': kinetic
    }
```

-----

## Lagrangian Mechanics

### The Lagrangian Formalism

The Lagrangian L = T - V describes a dynamical system. The Euler-Lagrange equations give the equations of motion:

```
d/dt(∂L/∂q̇ᵢ) - ∂L/∂qᵢ = 0
```

```python
# Lagrangian mechanics examples
lagrangians = {
    'free_particle': {
        'L': '½m(ẋ² + ẏ² + ż²)',
        'equations': 'mẍ = 0, mÿ = 0, mz̈ = 0'
    },
    'harmonic_oscillator': {
        'L': '½mẋ² - ½kx²',
        'equations': 'mẍ + kx = 0'
    },
    'pendulum': {
        'L': '½mL²θ̇² + mgL cos(θ)',
        'equations': 'θ̈ + (g/L) sin(θ) = 0'
    },
    'particle_in_potential': {
        'L': '½mẋ² - V(x)',
        'equations': 'mẍ + dV/dx = 0'
    }
}

# Implementing Euler-Lagrange
def euler_lagrange(L, q, qdot, t, params):
    """
    Compute Euler-Lagrange equations.
    L: Lagrangian function L(q, qdot, t)
    q: generalized coordinates
    qdot: generalized velocities
    """
    from scipy.misc import derivative
    
    # Compute partial derivatives
    dL_dqdot = []
    dL_dq = []
    
    for i in range(len(q)):
        # ∂L/∂q̇ᵢ (numerical)
        def partial_qdot(xi):
            qdot_modified = qdot.copy()
            qdot_modified[i] = xi
            return L(q, qdot_modified, t)
        dL_dqdot.append(derivative(partial_qdot, qdot[i], dx=1e-6))
        
        # ∂L/∂qᵢ
        def partial_q(xi):
            q_modified = q.copy()
            q_modified[i] = xi
            return L(q_modified, qdot, t)
        dL_dq.append(derivative(partial_q, q[i], dx=1e-6))
    
    # d/dt(∂L/∂q̇) - ∂L/∂q = 0
    # This gives accelerations
    return dL_dqdot  # Simplified - would need time derivative
```

### Generalized Coordinates

```python
# Example: Double pendulum using Lagrangian
def double_pendulum_lagrangian(state, t, m1, m2, L1, L2, g):
    """
    Double pendulum equations of motion.
    State: [θ1, θ2, ω1, ω2]
    """
    theta1, theta2, omega1, omega2 = state
    
    # Simplified equations (would use full Lagrangian)
    delta = theta2 - theta1
    denom = (m1 + m2) * L1 - m2 * L1 * np.cos(delta)**2
    
    alpha1 = (m2 * L1 * omega1**2 * np.sin(delta) * np.cos(delta) +
              m2 * g * np.sin(theta2) * np.cos(delta) +
              m2 * L2 * omega2**2 * np.sin(delta) -
              (m1 + m2) * g * np.sin(theta1)) / denom
    
    alpha2 = (-m2 * L2 * omega2**2 * np.sin(delta) * np.cos(delta) +
              (m1 + m2) * g * np.sin(theta1) * np.cos(delta) -
              (m1 + m2) * L1 * omega1**2 * np.sin(delta) -
              (m1 + m2) * g * np.sin(theta2)) / denom
    
    return [omega1, omega2, alpha1, alpha2]
```

-----

## Hamiltonian Mechanics

### Hamiltonian Formulation

The Hamiltonian H = T + V (total energy) is the Legendre transform of the Lagrangian:

```
pᵢ = ∂L/∂q̇ᵢ
H = Σ pᵇq̇ᵇ - L
```

Hamilton's equations:
```
q̇ᵢ = ∂H/∂pᵢ
ṗᵢ = -∂H/∂qᵢ
```

```python
# Hamiltonian dynamics
def hamilton_equations(state, t, H):
    """
    Compute Hamilton's equations.
    State: [q1, q2, ..., pn]
    """
    n = len(state) // 2
    q = state[:n]
    p = state[n:]
    
    # Compute derivatives
    dq_dt = []
    dp_dt = []
    
    for i in range(n):
        # q̇ᵢ = ∂H/∂pᵢ
        dq_dt.append(partial_derivative(H, i, p, q, t))
        
        # ṗᵢ = -∂H/∂qᵢ
        dp_dt.append(-partial_derivative(H, n+i, q, p, t))
    
    return dq_dt + dp_dt

# Example: Harmonic oscillator
def harmonic_oscillator_hamiltonian(q, p, m, k):
    """H = p²/2m + ½kq²"""
    return p**2 / (2*m) + 0.5 * k * q**2
```

### Phase Space and Integrals of Motion

```python
# Phase space trajectories
def phase_space_portrait(H, q_range, p_range, resolution=100):
    """Plot phase space portrait for 1D system."""
    q_vals = np.linspace(q_range[0], q_range[1], resolution)
    p_vals = np.linspace(p_range[0], p_range[1], resolution)
    
    energy_levels = []
    for q in q_vals:
        for p in p_vals:
            E = H(q, p)
            energy_levels.append((q, p, E))
    
    return energy_levels
```

-----

## Central Forces and Orbital Mechanics

### Central Force Motion

For a central force F(r) = f(r)r̂, angular momentum is conserved, reducing the problem to an effective 1D problem:

```python
# Effective potential
def effective_potential(r, angular_momentum, V):
    """
    Veff(r) = L²/2mr² + V(r)
    """
    return angular_momentum**2 / (2 * r**2) + V(r)

# Gravitational potential
def gravitational_potential(r, M, m, G):
    """V(r) = -GMm/r"""
    return -G * M * m / r

# Orbital equations
def orbital_equation(r, theta, params):
    """
    Derive orbital equation from central force.
    Using u = 1/r transformation:
    d²u/dθ² + u = -m/L² * dV/du
    """
    u = 1/r
    L = params['angular_momentum']
    m = params['mass']
    GM = params['GM']
    
    # For gravitational potential V = -GMm/r = -GMm*u
    # dV/du = GMm
    d2u_dtheta2 = -u + m * GM / L**2
    
    return d2u_dtheta2

# Kepler's Laws
keplers_laws = {
    'First': 'Orbits are ellipses with the Sun at one focus',
    'Second': 'Equal areas in equal times (conservation of L)',
    'Third': 'T² ∝ a³ (orbital period squared proportional to semi-major axis cubed)'
}
```

### Orbital Elements

```python
# Orbital elements definition
orbital_elements = {
    'a': 'Semi-major axis',
    'e': 'Eccentricity',
    'i': 'Inclination (to ecliptic)',
    'Ω': 'Longitude of ascending node',
    'ω': 'Argument of periapsis',
    'ν': 'True anomaly (position in orbit)'
}

# Orbital parameters from state vectors
def orbital_elements_from_state(r_vec, v_vec, mu):
    """
    Calculate orbital elements from position and velocity vectors.
    """
    import numpy as np
    
    r = np.linalg.norm(r_vec)
    v = np.linalg.norm(v_vec)
    
    # Specific angular momentum
    h = np.cross(r_vec, v_vec)
    h_mag = np.linalg.norm(h)
    
    # Specific mechanical energy
    epsilon = v**2 / 2 - mu / r
    
    # Semi-major axis
    a = -mu / (2 * epsilon)
    
    # Eccentricity vector
    e_vec = (np.cross(v, h) / mu) - (r_vec / r)
    e = np.linalg.norm(e_vec)
    
    return {'a': a, 'e': e, 'h': h_mag, 'energy': epsilon}
```

-----

## Rigid Body Dynamics

### Moment of Inertia

```python
# Moment of inertia tensor
def moment_of_inertia_tensor(mass_distribution):
    """
    Calculate inertia tensor for mass distribution.
    I_ij = ∫ρ(r)(δ_ij r² - r_i r_j)dV
    """
    I = np.zeros((3, 3))
    
    for mass, position in mass_distribution:
        r2 = np.dot(position, position)
        I[0, 0] += mass * (position[1]**2 + position[2]**2)
        I[1, 1] += mass * (position[0]**2 + position[2]**2)
        I[2, 2] += mass * (position[0]**2 + position[1]**2)
        I[0, 1] -= mass * position[0] * position[1]
        I[0, 2] -= mass * position[0] * position[2]
        I[1, 2] -= mass * position[1] * position[2]
    
    # Symmetric
    I[1, 0] = I[0, 1]
    I[2, 0] = I[0, 2]
    I[2, 1] = I[1, 2]
    
    return I

# Common moments of inertia
common_moments = {
    'solid_sphere': '2/5 MR²',
    'thin_spherical_shell': '2/3 MR²',
    'solid_cylinder': '1/2 MR²',
    'thin_rod_about_center': '1/12 ML²',
    'thin_rod_about_end': '1/3 ML²',
    'rectangular_plate': 'I_x = 1/12 M(b²+h²)'
}
```

### Euler's Equations

For rigid body rotation:

```
I₁ω̇₁ - (I₂ - I₃)ω₂ω₃ = M₁
I₂ω̇₂ - (I₃ - I₁)ω₃ω₁ = M₂
I₃ω̇₃ - (I₁ - I₂)ω₁ω₂ = M₃
```

```python
# Euler angles and rotation
def rotation_matrix_euler(phi, theta, psi):
    """
    Euler angles (3-1-3 convention) to rotation matrix.
    """
    R = np.zeros((3, 3))
    
    # Pre-compute trig functions
    cphi = np.cos(phi); sphi = np.sin(phi)
    ctheta = np.cos(theta); stheta = np.sin(theta)
    cpsi = np.cos(psi); spsi = np.sin(psi)
    
    R[0, 0] = cphi * ctheta * cpsi - sphi * spsi
    R[0, 1] = -cphi * ctheta * spsi - sphi * cpsi
    R[0, 2] = cphi * stheta
    R[1, 0] = sphi * ctheta * cpsi + cphi * spsi
    R[1, 1] = -sphi * ctheta * spsi + cphi * cpsi
    R[1, 2] = sphi * stheta
    R[2, 0] = -stheta * cpsi
    R[2, 1] = stheta * spsi
    R[2, 2] = ctheta
    
    return R
```

### Gyroscopic Motion

```python
# Precession of a spinning top
def gyroscopic_precession(omega_spin, I, m, g, r_cm):
    """
    Calculate precession rate for symmetric top.
    Ω = mgr_cm / (I_3 * omega_spin)
    """
    return m * g * r_cm / (I * omega_spin)
```

-----

## Oscillations and Waves

### Simple Harmonic Motion

```python
# Simple harmonic oscillator
def shm_solution(A, omega, phi, t):
    """
    x(t) = A cos(ωt + φ)
    """
    return A * np.cos(omega * t + phi)

# Properties
shm_properties = {
    'period': 'T = 2π/ω',
    'frequency': 'f = 1/T = ω/2π',
    'velocity': 'v = -Aω sin(ωt + φ)',
    'acceleration': 'a = -Aω² cos(ωt + φ) = -ω²x',
    'energy': 'E = ½kA² = ½mω²A²'
}

# Damped harmonic oscillator
def damped_oscillator_solution(gamma, omega0, A, t):
    """
    Solutions depend on damping:
    - Underdamped: γ < ω₀ → oscillation with decay
    - Critically damped: γ = ω₀ → fastest return without oscillation
    - Overdamped: γ > ω₀ → exponential decay without oscillation
    """
    if gamma < omega0:  # Underdamped
        omega_d = np.sqrt(omega0**2 - gamma**2)
        return np.exp(-gamma * t) * np.cos(omega_d * t)
    elif gamma == omega0:  # Critical
        return (A + A * gamma * t) * np.exp(-gamma * t)
    else:  # Overdamped
        r1 = -gamma + np.sqrt(gamma**2 - omega0**2)
        r2 = -gamma - np.sqrt(gamma**2 - omega0**2)
        return A * (np.exp(r1 * t) - np.exp(r2 * t))
```

### Coupled Oscillations and Normal Modes

```python
# Normal mode analysis
def normal_modes(M, K):
    """
    Find normal modes for coupled oscillators.
    M: mass matrix
    K: stiffness matrix
    """
    # Solve eigenvalue problem: K v = ω² M v
    eigenvalues, eigenvectors = np.linalg.eig(np.linalg.inv(M) @ K)
    omega = np.sqrt(eigenvalues)
    
    return {'frequencies': omega, 'modes': eigenvectors}

# Beat phenomenon
def beat_frequency(omega1, omega2):
    """
    Beat frequency when two close frequencies interact.
    """
    return abs(omega1 - omega2) / (2 * np.pi)
```

-----

## Collisions and Impulse

### Collision Types

| Type | Energy | Momentum | Examples |
|------|--------|----------|----------|
| **Elastic** | Conserved | Conserved | Billiard balls |
| **Inelastic** | Not conserved | Conserved | Car crumple zones |
| **Perfectly inelastic** | Lost | Conserved | Muddy collision |
| **Explosive** | Added | Conserved | Rocket staging |

```python
# 1D elastic collision
def elastic_collision(m1, v1, m2, v2):
    """
    1D elastic collision formulas.
    """
    v1_final = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
    v2_final = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
    
    return v1_final, v2_final

# 2D/3D collision (impulse method)
def collision_impulse(r1, r2, v1, v2, m1, m2, e=1.0):
    """
    Calculate impulse for 2D collision.
    e: coefficient of restitution
    """
    # Relative velocity
    v_rel = v1 - v2
    
    # Line of centers
    r_rel = r1 - r2
    n = r_rel / np.linalg.norm(r_rel)
    
    # Relative velocity along normal
    v_rel_n = np.dot(v_rel, n)
    
    # Impulse magnitude
    j = -(1 + e) * v_rel_n / (1/m1 + 1/m2)
    
    # Impulse vector
    impulse = j * n
    
    # Final velocities
    v1_final = v1 + impulse / m1
    v2_final = v2 - impulse / m2
    
    return impulse, v1_final, v2_final
```

-----

## Common Errors to Avoid

- **Confusing mass and weight**: Weight is a force (mg), mass is intrinsic
- **Forgetting units**: Always use consistent units (SI recommended)
- **Ignoring signs**: Direction matters in vectors
- **Applying wrong conservation law**: Check conditions carefully
- **Using wrong coordinate system**: Choose appropriate for the problem
- **Neglecting initial conditions**: Different ICs give different solutions
- **Oversimplifying frictionless assumptions**: Real systems have dissipative forces
- **Confusing torque and force**: Torque requires both force and lever arm
- **Not understanding reference frames**: Mechanics is frame-dependent
- **Ignoring small angle approximations**: Only valid for θ << 1 radian
