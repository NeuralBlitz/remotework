---

## name: biotechnology
description: >
  Biotechnology expert for applying biological systems to develop products and processes. Use
  this skill whenever the user needs: developing recombinant proteins, designing bioprocesses,
  applying genetic engineering, working with fermentation, creating biosensors, optimizing
  bioreactors, or any task involving the technological application of biology. This skill
  covers genetic engineering, bioprocess engineering, protein production, industrial
  biotechnology, and modern biotechnological applications.
license: MIT
compatibility: opencode
metadata:
  audience: biotechnologists
  category: biology

# Biotechnology — Biological Technology and Applications

Covers: **Genetic Engineering · Bioprocess Engineering · Recombinant Proteins · Fermentation · CRISPR · Industrial Enzymes · Biosensors · Biopharmaceuticals**

-----

## Genetic Engineering

### Molecular Cloning

```python
# Basic cloning workflow
cloning_workflow = {
    'step1': 'Isolate vector and insert DNA',
    'step2': 'Digest with restriction enzymes',
    'step3': 'Ligate insert into vector',
    'step4': 'Transform into host cells',
    'step5': 'Screen for recombinants',
    'step6': 'Verify with sequencing'
}

# Restriction enzyme types
restriction_enzyme_types = {
    'Type_II': {
        'description': 'Cleave at specific sequence',
        'examples': ['EcoRI', 'BamHI', 'HindIII'],
        'recognition': 'Palindromic, 4-8 bp'
    },
    'Type_III': {
        'description': 'Cleave away from site',
        'examples': ['EcoPI', 'HinfI']
    },
    'Type_IV': {
        'description': 'Modified DNA',
        'examples': ['McrBC']
    }
}

# Ligation
def calculate_ligation_efficiency(insert_ng, vector_ng, insert_size, vector_size, molar_ratio=3):
    """
    Calculate optimal ligation conditions.
    """
    # Moles calculation
    vector_moles = vector_ng / (vector_size * 650)  # 650 Da per bp
    insert_moles = insert_ng / (insert_size * 650) * molar_ratio
    
    return vector_moles, insert_moles
```

### PCR Applications

```python
# PCR types
pcr_types = {
    'standard': 'Basic amplification',
    'hot_start': 'Reduced non-specific products',
    'multiplex': 'Multiple targets',
    'quantitative': 'qPCR for quantification',
    'digital': 'dPCR for absolute quantification',
    'reverse_transcription': 'RT-PCR for RNA'
}

# Primer design rules
primer_design = {
    'length': '18-25 nucleotides',
    'tm': '55-65°C (within 5°C of each other)',
    'gc_content': '40-60%',
    'avoid': ['Hairpins', 'Dimers', 'Repeats'],
    'gc_clamp': '1-2 bp at 3\' end',
    'product_size': '100-3000 bp typical'
}

# qPCR analysis
qpcr_analysis = {
    'reference_genes': ['GAPDH', 'ACTB', '18S rRNA'],
    'normalization': 'ΔCt method',
    'comparison': 'ΔΔCt method',
    'efficiency': 'E = 10^(-1/slope) - 1'
}
```

### CRISPR-Cas Systems

```python
# CRISPR system types
crispr_types = {
    'Cas9': {
        'type': 'Class 2, Type II',
        'function': 'Double-strand break',
        'pam': 'NGG',
        'applications': 'Knockout, knockin'
    },
    'Cas12a': {
        'type': 'Class 2, Type V',
        'function': 'Staggered cut',
        'pam': 'TTTV',
        'applications': 'Cleavage, diagnostics'
    },
    'Cas13': {
        'type': 'Class 2, Type VI',
        'function': 'RNA cleavage',
        'pam': 'PFS',
        'applications': 'RNA editing, detection'
    },
    'prime_editing': {
        'type': 'Cas9-nickase + RT',
        'function': 'All 12 types of mutation',
        'no_double_strand_break': True
    }
}

# sgRNA design
def design_sgrna(target_sequence, pam='NGG', gc_range=(0.3, 0.7)):
    """
    Design single guide RNA targets.
    """
    targets = []
    
    for i in range(len(target_sequence) - 22):
        if target_sequence[i+21:i+23] == pam[:2]:
            protospacer = target_sequence[i:i+20]
            
            # Check GC content
            gc = (protospacer.count('G') + protospacer.count('C')) / 20
            if gc_range[0] <= gc <= gc_range[1]:
                targets.append({
                    'position': i,
                    'protospacer': protospacer,
                    'pam': target_sequence[i+20:i+23]
                })
    
    return targets
```

-----

## Bioprocess Engineering

### Fermentation Systems

```python
# Fermentation types
fermentation_types = {
    'batch': {
        'description': 'Closed system, no addition during run',
        'advantages': ['Simple', 'Low contamination risk'],
        'disadvantages': ['Low productivity', 'Catabolite repression']
    },
    'fed_batch': {
        'description': 'Feed substrate during run',
        'advantages': ['High cell density', 'Controlled feeding'],
        'applications': ['Recombinant protein', 'High yield']
    },
    'continuous': {
        'description': 'Continuous inlet/outlet',
        'advantages': ['Steady state', 'High productivity'],
        'disadvantages': ['Stability issues', 'Contamination risk']
    },
    'perfusion': {
        'description': 'Cell retention, product removal',
        'advantages': ['High cell density', 'Continuous harvest'],
        'applications': ['Cell therapy', 'Biopharmaceuticals']
    }
}

# Growth kinetics
class MicrobialKinetics:
    @staticmethod
    def monod_equation(mu, mu_max, ks, s):
        """
        Monod growth model.
        mu: Specific growth rate
        mu_max: Maximum growth rate
        ks: Half-saturation constant
        s: Substrate concentration
        """
        return mu_max * s / (ks + s)
    
    @staticmethod
    def yield_coefficient(s0, sf, x0, xf):
        """
        Calculate biomass yield.
        """
        Yx_s = (xf - x0) / (s0 - sf)
        return Yx_s
    
    @staticmethod
    def product_formation(x, yp_x, s):
        """
        Product formation kinetics.
        """
        # Luedeking-Piret model
        alpha = 0.1  # Growth-associated
        beta = 0.01  # Non-growth-associated
        return alpha * x + beta * x
```

### Bioreactor Design

```python
# Bioreactor types
bioreactor_types = {
    'stirred_tank': {
        'agitation': 'Impeller',
        'scale_up': 'Power/volume constant',
        'applications': 'Most common'
    },
    'airlift': {
        'description': 'Internal/external circulation',
        'applications': 'Shear-sensitive cultures'
    },
    'wave_bioreactor': {
        'description': 'Wave-induced mixing',
        'applications': 'Cell therapy, vaccines'
    },
    'hollow_fiber': {
        'description': 'Semi-permeable membranes',
        'applications': 'High-value products'
    }
}

# Scale-up criteria
scaleup_criteria = {
    'power_per_volume': 'Constant P/V',
    'tip_speed': 'Constant impeller tip speed',
    'oxygen_transfer': 'Constant kLa',
    'mixing_time': 'Constant mixing time',
    'shear': 'Constant average shear rate'
}
```

-----

## Recombinant Protein Production

### Expression Systems

```python
# Expression system comparison
expression_systems = {
    'E_coli': {
        'pros': ['Fast', 'Cheap', 'Well-characterized'],
        'cons': ['No post-translation', 'Inclusion bodies possible'],
        'best_for': 'Simple proteins, enzymes'
    },
    'S_cerevisiae': {
        'pros': ['Eukaryotic', 'Secretion possible'],
        'cons': ['Lower yield', 'Hyperglycosylation'],
        'best_for': 'Secreted proteins'
    },
    'Pichia_pastoris': {
        'pros': ['High yield', 'Secretion', 'Glycosylation'],
        'cons': ['Methanol requirement'],
        'best_for': 'Secreted proteins, scale-up'
    },
    'Insect_cells': {
        'pros': ['Complex proteins', 'Post-translation'],
        'cons': ['Lower yield', 'More expensive'],
        'best_for': 'Complex eukaryotic proteins'
    },
    'Mammalian_cells': {
        'pros': 'Human-like glycosylation',
        'cons': ['Slow', 'Expensive'],
        'best_for': 'Therapeutic antibodies'
    }
}

# Optimization strategies
protein_optimization = {
    'codon_optimization': 'Match host tRNA usage',
    'promoter_choice': 'Inducible vs constitutive',
    'signal_peptide': 'Secretion signal',
    'fusion_tags': 'His, GST, MBP, SUMO',
    'folding': ' chaperone co-expression',
    'solubility': 'Solubility enhancers'
}
```

### Protein Purification

```python
# Purification strategies
purification_methods = {
    'affinity': {
        'tags': ['His-tag (Ni-NTA)', 'GST', 'MBP', 'Strep'],
        'principle': 'Specific binding',
        'advantage': 'High purity in one step'
    },
    'ion_exchange': {
        'anion': 'Bind at pH > pI',
        'cation': 'Bind at pH < pI',
        'principle': 'Charge interaction'
    },
    'hydrophobic_interaction': {
        'principle': 'Hydrophobic patches',
        'high_salt': 'Promotes binding'
    },
    'size_exclusion': {
        'principle': 'Molecular size',
        'desalting': 'Buffer exchange'
    }
}

# Chromatography parameters
chromatography_params = {
    'binding_capacity': 'mg protein/mL resin',
    'flow_rate': 'cm/hr or mL/min',
    'resolution': 'Separation of peaks',
    'yield': 'Recovery percentage',
    'purity': 'Target purity level'
}
```

-----

## Industrial Enzymes

### Enzyme Classes

```python
# Industrial enzyme types
industrial_enzymes = {
    'hydrolases': {
        'examples': ['Amylase', 'Protease', 'Lipase', 'Cellulase'],
        'applications': ['Starch processing', 'Detergents', 'Baking']
    },
    'oxidoreductases': {
        'examples': ['Glucose oxidase', 'Laccase', 'Peroxidase'],
        'applications': ['Food industry', 'Textile', 'Biosensors']
    },
    'transferases': {
        'examples': ['Transglutaminase', 'Glycosyltransferase'],
        'applications': ['Crosslinking', 'Glycosylation']
    },
    'lyases': {
        'examples': ['Pectin lyase', 'Alginate lyase'],
        'applications': ['Fruit processing', 'Algae processing']
    },
    'isomerases': {
        'examples': ['Glucose isomerase', 'Racemase'],
        'applications': 'HFCS production'
    }
}

# Enzyme kinetics
class EnzymeKinetics:
    @staticmethod
    def michaelis_menten(v, vmax, km, s):
        """
        Michaelis-Menten equation.
        v = (Vmax * [S]) / (Km + [S])
        """
        return vmax * s / (km + s)
    
    @staticmethod
    def lineweaver_burk(v, vmax, km, s):
        """
        Double reciprocal plot.
        1/v = (Km/Vmax)(1/[S]) + 1/Vmax
        """
        return 1/v if v != 0 else float('inf')
    
    @staticmethod
    def inhibition_types(km_app, vmax_app, i_type):
        """
        Enzyme inhibition.
        """
        if i_type == 'competitive':
            return {'km_increased': True, 'vmax_same': True}
        elif i_type == 'noncompetitive':
            return {'km_same': True, 'vmax_decreased': True}
        elif i_type == 'uncompetitive':
            return {'km_decreased': True, 'vmax_decreased': True}
```

### Enzyme Engineering

```python
# Directed evolution
directed_evolution = {
    'error_prone_pcr': 'Introduce random mutations',
    'dna_shuffling': 'Recombine related sequences',
    'saturation_mutagenesis': 'Target specific positions',
    'computational_design': 'AI/ML-guided design'
}

# Rational design
rational_design = {
    'structure_based': 'Use 3D structure',
    'sequence_based': 'Conserved regions',
    'machine_learning': 'Predict function'
}
```

-----

## Biosensors

### Biosensor Components

```python
# Biosensor structure
biosensor_components = {
    'biorecognition_element': {
        'types': [
            'Enzyme',
            'Antibody',
            'Nucleic acid',
            'Cell receptor',
            'Whole cell',
            'Tissue'
        ]
    },
    'transducer': {
        'electrochemical': ['Amperometric', 'Potentiometric', 'Conductometric'],
        'optical': ['Fluorescence', 'SPR', 'Colorimetric'],
        'mass_sensitive': ['QCM', 'SAW', 'Piezoelectric'],
        'thermal': ['Calorimetric']
    },
    'detector': 'Signal processing and display'
}

# Common biosensors
common_biosensors = {
    'glucose_monitor': {
        'element': 'Glucose oxidase',
        'transducer': 'Electrochemical',
        'market': 'Largest biosensor market'
    },
    'pregnancy_test': {
        'element': 'Anti-hCG antibody',
        'transducer': 'Colorimetric (Lateral flow)'
    },
    'PCR_detector': {
        'element': 'DNA probe',
        'transducer': 'Fluorescent'
    }
}
```

### Diagnostic Applications

```python
# Point-of-care diagnostics
poc_diagnostics = {
    'lateral_flow': {
        'examples': 'Pregnancy, COVID-19, HIV',
        'advantages': 'Simple, fast, no equipment'
    },
    'electrochemical': {
        'examples': 'Glucose, lactate',
        'advantages': 'Sensitive, miniaturizable'
    },
    'surface_plasmon_resonance': {
        'examples': 'SPR biosensors',
        'advantages': 'Label-free, real-time'
    }
}
```

-----

## Biopharmaceuticals

### Therapeutic Proteins

```python
# Biopharmaceutical types
biopharmaceuticals = {
    'antibodies': {
        'types': ['Full mAb', 'Fragment', 'Bispecific', 'ADC'],
        'examples': ['Humira', 'Remicade', 'Keytruda'],
        'expression': 'CHO cells'
    },
    'hormones': {
        'examples': ['Insulin', 'Growth hormone', 'EPO'],
        'expression': 'E. coli, CHO'
    },
    'enzymes': {
        'examples': ['tPA', 'Streptokinase', 'Asparaginase'],
        'applications': 'Thrombolysis, cancer'
    },
    'vaccines': {
        'subunit': 'Hepatitis B, VLP',
        'mRNA': 'COVID-19',
        'viral_vector': 'Ebola, COVID-19'
    }
}

# Manufacturing process
biopharma_process = {
    'upstream': ['Cell bank', 'Bioreactor', 'Harvest'],
    'downstream': [
        'Clarification',
        'Capture chromatography',
        'Viral inactivation',
        'Polishing',
        'Viral filtration',
        'Formulation'
    ],
    'fill_finish': ['Bulk fill', 'Filtration', 'Lyophilization', 'Packaging']
}
```

### Regulatory Considerations

```python
# FDA/EMA requirements
regulatory_requirements = {
    'IND': 'Investigational New Drug (FDA)',
    'BLA': 'Biologics License Application',
    'CMC': 'Chemistry, Manufacturing, Controls',
    'GMP': 'Good Manufacturing Practice',
    'validation': ['Process', 'Analytical', 'Cleaning']
}

# Biosimilarity
biosimilar_requirements = {
    'comparability': 'Structure and function',
    'nonclinical': 'Animal studies',
    'clinical': 'PK/PD, efficacy, safety',
    'immunogenicity': 'Antibody formation'
}
```

-----

## Applications and Industry

### Market Applications

```python
# Biotechnology applications
biotech_applications = {
    'healthcare': [
        'Therapeutic proteins',
        'Gene therapy',
        'Cell therapy',
        'Vaccines',
        'Diagnostics'
    ],
    'agriculture': [
        'GM crops',
        'Biofertilizers',
        'Biostimulants',
        'Animal health'
    ],
    'industrial': [
        'Enzymes',
        'Biofuels',
        'Biopolymers',
        'Bioremediation'
    ],
    'food': [
        'Fermented foods',
        'Food additives',
        'Nutraceuticals',
        'Preservatives'
    ]
}
```

### Sustainable Biotechnology

```python
# Bioeconomy
bioeconomy = {
    'biofuels': {
        'ethanol': 'Corn, sugarcane, cellulose',
        'biodiesel': 'Vegetable oils, algae',
        'biogas': 'Anaerobic digestion'
    },
    'bioplastics': {
        'PLA': 'Corn starch',
        'PHA': 'Bacterial fermentation'
    },
    'biorefinery': 'Complete utilization of biomass'
}
```

-----

## Common Errors to Avoid

- **Ignoring biosafety**: Follow biosafety level requirements
- **Not validating processes**: Process validation is critical
- **Assuming scalability**: Lab to production is challenging
- **Ignoring host cell proteins**: HCP removal important
- **Neglecting viral safety**: Viral clearance required
- **Not understanding glycosylation**: Affects function
- **Ignoring stability**: Formulation development essential
- **Underestimating purification**: Often bottleneck
- **Not considering regulatory**: FDA/EMA requirements
- **Forgetting raw materials**: Quality affects product
