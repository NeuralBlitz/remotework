---

## name: polymer-chemistry
description: >
  Expert polymer chemistry assistant for polymer chemists and researchers. Use this skill whenever the user needs:
  understanding polymer synthesis, characterization, structure-property relationships, polymer physics, or any rigorous academic 
  treatment of polymer chemistry. Covers polymerization methods, molecular weight determination, and polymer properties.
license: MIT
compatibility: opencode
metadata:
  audience: polymer chemists, materials scientists, researchers
  category: chemistry

# Polymer Chemistry — Academic Research Assistant

Covers: **Polymerization · Molecular Weight · Polymer Characterization · Structure-Property · Polymer Physics · Processing · Degradation**

---

## Polymerization Methods

### Step-Growth Polymerization

```
Requirements:
- Monomers must be difunctional or higher
- Each step involves independent reactions
- Molecular weight increases slowly at first
- Complete conversion needed for high MW

Carothers Equation:
X̄n = 1/(1-p)

Where p = conversion
```

### Chain-Growth Polymerization

|Initiation|Method|Examples|
|-----------|------|--------|
|Thermal homolysis|Radicals|AIBN|
|Photochemical|Radicals|Benzophenone|
|Chemical|Redox|Peroxides + amines|
|Ion cationic|Lewis acids|BF₃ + H₂O|

```python
class StepGrowthPolymerization:
    """Step-growth polymerization calculations"""
    
    def degree_of_polymerization(self, conversion, functionality):
        """
        X̄n = (1 + r) / (1 + r - 2rp)
        
        Where:
        - r = mole ratio of functional groups
        - p = conversion of limiting group
        """
        if conversion == 1:
            return float('inf')
        
        if functionality == 2:  # Linear
            return 1 / (1 - conversion)
        else:
            # Branched/crosslinked
            r = 1  # Equimolar
            return (1 + r) / (1 + r - 2 * r * conversion)
    
    def calculate_molecular_weight(self, degree_of_polymerization, monomer_mw):
        """
        Mn = X̄n × M0
        """
        return degree_of_polymerization * monomer_mw


class ChainGrowthPolymerization:
    """Chain-growth kinetics"""
    
    def rate_of_polymerization(self, kp, [M], [R•]):
        """
        Rp = kp[M][R•]
        """
        return kp * [M] * [R•]
    
    def kinetics(self, initiator_efficiency, kd, ki, kp, [I], [M]):
        """
        Overall rate depends on initiator decomposition
        """
        # Steady-state: Ri = Rd
        # [R•] = (fid[I])^0.5
        # Rp = kp[M](fid[I])^0.5
        pass
```

---

## Molecular Weight Distribution

### Average Molecular Weights

|Parameter|Formula|Meaning|
|---------|--------|--------|
|Mn (Number-average)|ΣNiMi/ΣNi|Statistical average|
|Mw (Weight-average)|ΣNiMi²/ΣNiMi|Bias toward high MW|
|Mz (Z-average)|ΣNiMi³/ΣNiMi²|High-weight bias|
|Mv (Viscosity-average)|[η] = KMᵅ|Between Mn and Mw|

### Polydispersity Index

```python
class MolecularWeightDistribution:
    """MWD analysis"""
    
    def calculate_averages(self, molecular_weights, counts):
        """
        Calculate Mn, Mw, Mz
        """
        import numpy as np
        
        weights = np.array(molecular_weights)
        counts = np.array(counts)
        
        NiMi = weights * counts
        NiMi2 = NiMi * weights
        NiMi3 = NiMi2 * weights
        
        Mn = sum(NiMi) / sum(counts)
        Mw = sum(NiMi2) / sum(NiMi)
        Mz = sum(NiMi3) / sum(NiMi2)
        
        return {"Mn": Mn, "Mw": Mw, "Mz": Mz}
    
    def calculate_pdi(self, Mw, Mn):
        """Polydispersity Index = Mw/Mn"""
        return Mw / Mn
    
    def distribution_spread(self, Mw, Mn, Mz):
        """
        Measure of distribution breadth
        """
        return {
            "PDI": Mw / Mn,
            "dispersity": (Mz - Mw) / Mw
        }
```

---

## Polymer Characterization

### Gel Permeation Chromatography

```python
class GPCCalculations:
    """GPC/SEC analysis"""
    
    def universal_calibration(self, elution_volume, standards):
        """
        Use [η]M to create universal calibration
        Mark-Houwink equation:
        [η] = K × Mᵃ
        """
        pass
    
    def mark_houwink_parameters(self, polymer_solvent):
        """
        Mark-Houwink constants
        """
        parameters = {
            "polystyrene_tetrahydrofuran": {"K": 1.4e-4, "a": 0.70},
            "pmma_chloroform": {"K": 0.71e-4, "a": 0.82},
            "polyethylene_1,2,4-trichlorobenzene": {"K": 4.3e-4, "a": 0.67}
        }
        
        return parameters.get(polymer_solvent)
```

### Thermal Analysis

|Technique|Information|Key Parameters|
|---------|-----------|---------------|
|DSC|Thermal transitions|Tg, Tm, ΔCp, ΔHm|
|TGA|Thermal stability|Decomposition temperature|
|DMA|Mechanical properties|E', E'', Tg|

---

## Polymer Physics

### Glass Transition

```python
class GlassTransition:
    """Glass transition temperature factors"""
    
    # Factors affecting Tg
    Tg_MODIFIERS = {
        "flexible_backbone": ["Silicone (-127°C)", "Polyethylene (-120°C)"],
        "rigid_backbone": ["Polystyrene (100°C)", "Polycarbonate (147°C)"],
        "bulky_side_groups": ["PMMA (105°C)", "PTFE (-115°C)"],
        "hydrogen_bonding": ["Nylon 6,6 (70°C)", "Polyvinyl alcohol (85°C)"]
    }
    
    # Free volume theory
    def free_volume_fraction(self, T, Tg, α):
        """
        f = f_g + α(T - Tg)
        """
        f_g = 0.025  # Free volume at Tg
        return f_g + alpha * (T - Tg)
    
    # WLF equation
    def viscosity_wlf(self, T, Tg, C1, C2):
        """
        log(aT) = -C1(T - Tg)/(C2 + T - Tg)
        """
        import numpy as np
        return -C1 * (T - Tg) / (C2 + T - Tg)
```

### Crystallinity

|X-ray diffraction|Thermal (DSC)|Density|
|----------------|-------------|-------|
|Crystallinity index|% crystallinity|Apparent crystallinity|

---

## Important Polymers

### Commodity Polymers

|Polymer|Abbreviation|Monomer|Tg (°C)|Tm (°C)|Uses|
|-------|------------|-------|--------|--------|-----|
|Polyethylene|PE|Ethene|-120|130|Bags, pipes|
|Polypropylene|PP|Propene|-20|165|Containers, fibers|
|Polystyrene|PS|Styrene|100|240|Foam, packaging|
|Polyvinyl chloride|PVC|Vinyl chloride|70|180|Pipes, siding|
|PET|Polyester|Ethene glycol + terephthalic acid|70|260|Fibers, bottles|

### High-Performance Polymers

|Polymer|Tg (°C)|Tm (°C)|Properties|
|-------|--------|--------|-----------|
|PEEK|143|343|Chemical resistant|
|Kapton|260|None|Aromatic polyimide|
|PPS|85|280|Engineering|
|LCP|Variable|Variable|Rheological|

---

## Polymer Degradation

### Types of Degradation

|Mechanism|Trigger|Example|
|---------|--------|--------|
|Oxidation|Oxygen, heat|Polypropylene yellowing|
|Hydrolysis|Water, acid/base|Ester cleavage|
|UV degradation|Sunlight|Polyethylene embrittlement|
|Thermal degradation|Heat|PMMA depolymerization|

```python
class PolymerDegradation:
    """Degradation kinetics"""
    
    def arrhenius_kinetics(self, Ea, T1, T2, k1):
        """
        Arrhenius extrapolation
        ln(k2/k1) = -Ea/R(1/T2 - 1/T1)
        """
        import numpy as np
        R = 8.314  # J/mol·K
        
        log_ratio = -Ea / R * (1/T2 - 1/T1)
        k2 = k1 * np.exp(log_ratio)
        
        return k2
    
    def lifetime_prediction(self, k, failure_criterion):
        """
        t = ln(failure_criterion)/k
        """
        return np.log(failure_criterion) / k
```

---

## Common Errors to Avoid

1. **Confusing Mn and Mw** — Different averages for different purposes
2. **Ignoring polydispersity** — PDI affects properties significantly
3. **Not considering crystallinity** — Semi-crystalline behavior differs
4. **Forgetting molecular weight limits** — Too high causes degradation
5. **Overlooking Tg** — Determines application temperature range
6. **Ignoring processing effects** — Shear, cooling rate matter
7. **Not accounting for moisture** — Nylons absorb water
8. **Confusing degradation mechanisms** — Different triggers

