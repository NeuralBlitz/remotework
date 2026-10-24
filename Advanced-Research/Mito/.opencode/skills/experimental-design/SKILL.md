---
name: experimental-design
description: Experimental design, A/B testing, statistical hypothesis testing, and research methodology
license: MIT
compatibility: opencode
metadata:
  audience: data-science
  category: data-science
---

## What I do
- Design rigorous experiments
- Create proper control and treatment groups
- Analyze experimental results statistically
- Ensure internal and external validity
- Calculate sample sizes
- Avoid common pitfalls

## When to use me
When running A/B tests, experiments, or any controlled study to measure causal effects.

## Experimental Design Types

### Randomized Controlled Trial (RCT)
- Random assignment to groups
- Gold standard for causal inference
- Controls for confounding

### A/B Testing
- Two variants (A = control, B = treatment)
- Random assignment
- Measure conversion/r engagement

### Multivariate Testing
- Multiple variables simultaneously
- Factorial design
- Interaction effects

### Sequential Testing
- Pre-specified stopping rules
- Always-valid inference
- Reduce sample size

## Key Concepts

### Hypothesis
- **Null (H0)**: No effect
- **Alternative (H1)**: Effect exists
- One-sided vs two-sided

### Statistical Power
- Probability of detecting true effect
- 80% power is standard
- Affected by: effect size, sample size, alpha

### Sample Size Calculation
```python
# Example: Two-sample t-test
from scipy import stats
import numpy as np

effect_size = 0.5  # Cohen's d
alpha = 0.05
power = 0.80

n = int(np.ceil(2 * (stats.norm.ppf(1-alpha/2) + stats.norm.ppf(power))**2 / effect_size**2))
# n per group
```

### Variables
- **Independent**: Treatment
- **Dependent**: Outcome
- **Control**: Variables held constant
- **Confounding**: Variables that affect both

## Common Designs

### Between-Subjects
- Different people in each group
- Pros: No carryover effects
- Cons: Individual differences

### Within-Subjects
- Same people in all conditions
- Pros: More power, less variance
- Cons: Order effects, carryover

### Factorial Design
- Multiple independent variables
- Main effects and interactions
- 2x2, 3x2, etc.

## Analysis Methods

### Frequentist
- T-tests
- ANOVA
- Chi-square
- Regression

### Bayesian
- Posterior distributions
- Bayes factors
- Credible intervals

### Bootstrapping
- Resampling
- Distribution-free
- Confidence intervals

## Threats to Validity

### Internal
- Selection bias
- History effects
- Maturation
- Attrition
- Instrumentation

### External
- Sample representativeness
- Ecological validity
- Treatment diffusion

## Best Practices
- Pre-register hypotheses
- Use adequate sample sizes
- Randomize properly
- Monitor for issues
- Report all results
- Consider effect size
- Replicate findings
