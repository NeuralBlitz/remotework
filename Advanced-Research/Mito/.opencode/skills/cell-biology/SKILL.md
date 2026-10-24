---

## name: cell-biology
description: >
  Cell biology expert for understanding cell structure, function, and processes. Use this
  skill whenever the user needs: studying cell morphology and organization, analyzing
  cell signaling pathways, investigating cell cycle regulation, researching cancer biology,
  studying organelle function, understanding cell death mechanisms, working with cell
  culture, or any task involving the fundamental biology of cells. This skill covers
  cell structure, molecular biology, cell physiology, and experimental methods.
license: MIT
compatibility: opencode
metadata:
  audience: cell biologists
  category: biology

# Cell Biology — Structure, Function, and Processes

Covers: **Cell Structure · Organelles · Cell Signaling · Cell Cycle · Cell Death · Metabolism · Cytoskeleton · Cell Culture Techniques**

-----

## Cell Structure Overview

### Prokaryotic vs. Eukaryotic Cells

| Feature | Prokaryotic | Eukaryotic |
|---------|--------------|------------|
| **Nucleus** | No | Yes |
| **Size** | 0.1-5 μm | 10-100 μm |
| **DNA** | Circular chromosome | Linear chromosomes |
| **Membrane** | Yes | Yes |
| **Organelles** | Few | Many |
| **Cell wall** | Yes (most) | Only plants/fungi |
| **Ribosomes** | 70S | 80S (cytoplasm) |

### Cell Theory

```python
# Cell theory principles
cell_theory = {
    'principle_1': 'All living organisms are composed of one or more cells',
    'principle_2': 'The cell is the basic unit of structure and organization',
    'principle_3': 'Cells arise from pre-existing cells',
    'principle_4': 'Energy flows within cells (biochemistry)',
    'principle_5': 'Genetic information is passed from cell to cell'
}
```

### Cell Size Limitations

```python
# Factors limiting cell size
size_limitations = {
    'surface_area_to_volume_ratio': {
        'description': 'As cell grows, SA/V decreases',
        'impact': 'Limits nutrient/waste exchange',
        'formula': 'SA/V = 3/r for sphere'
    },
    'nuclear_size': {
        'description': 'Nucleus can only control limited cytoplasmic volume',
        'impact': 'Limits gene expression capacity'
    },
    'diffusion_time': {
        'description': 'Molecules take time to diffuse',
        'impact': 'Limits intracellular signaling speed'
    },
    'organelle_density': {
        'description': 'Organelles occupy finite space',
        'impact': 'Limits metabolic capacity'
    }
}
```

-----

## Major Organelles

### Nucleus

```python
# Nuclear structure and function
nucleus = {
    'structure': {
        'nuclear_envelope': 'Double membrane with nuclear pores',
        'nucleolus': 'rRNA synthesis and ribosome assembly',
        'chromatin': 'DNA + histone proteins'
    },
    'functions': [
        'DNA replication',
        'RNA transcription',
        'Ribosome biogenesis',
        'Chromosome organization',
        'Nuclear transport'
    ],
    'diameter': '5-10 μm',
    'pores': '4000-7000 per nucleus in mammalian cells'
}

# Nuclear transport
nuclear_transport = {
    'nuclear_localization_signal': 'PKKKRKV (basic, NLS)',
    'nuclear_export_signal': 'LEU-rich (NES)',
    'transport': 'Importin/Exportin mediated',
    'energy': 'Ran-GTP gradient'
}
```

### Mitochondria

```python
# Mitochondrial structure and function
mitochondria = {
    'structure': {
        'outer_membrane': 'Porous, contains porins',
        'intermembrane_space': 'Similar to cytosol',
        'inner_membrane': 'Cristae, site of ETC',
        'matrix': 'Krebs cycle, DNA, ribosomes'
    },
    'functions': [
        'ATP production (oxidative phosphorylation)',
        'Citric acid cycle',
        'Fatty acid oxidation',
        'Apoptosis initiation',
        'Heat production (thermogenesis)'
    ],
    'genome': 'Circular DNA, 16.5 kb in humans',
    'origin': 'Endosymbiotic (derived from α-proteobacteria)'
}

# Electron transport chain
etc_complexes = {
    'Complex_I': 'NADH dehydrogenase',
    'Complex_II': 'Succinate dehydrogenase',
    'Complex_III': 'Cytochrome bc1 complex',
    'Complex_IV': 'Cytochrome c oxidase',
    'Complex_V': 'ATP synthase'
}

def calculate_atp_production(nadh, fadh2):
    """Calculate theoretical ATP yield"""
    atp_from_nadh = nadh * 2.5  # P/O ratio
    atp_from_fadh2 = fadh2 * 1.5
    return atp_from_nadh + atp_from_fadh2
```

### Endomembrane System

```python
# Endomembrane system components
endomembrane = {
    'endoplasmic_reticulum': {
        'rough_ER': 'Protein synthesis, ribosome-bound',
        'smooth_ER': 'Lipid synthesis, detoxification',
        'functions': [
            'Protein folding and modification',
            'Lipid biosynthesis',
            'Calcium storage'
        ]
    },
    'golgi_apparatus': {
        'cis': 'Receiving (cis-face)',
        'medial': 'Processing',
        'trans': 'Sorting (trans-face)',
        'functions': [
            'Protein modification (glycosylation)',
            'Protein sorting',
            'Lipid modification'
        ]
    },
    'lysosomes': {
        'function': 'Intracellular digestion',
        'enzymes': 'Acid hydrolases (pH 4.5-5)',
        'substrates': 'Proteins, nucleic acids, lipids, carbohydrates'
    },
    'endosomes': {
        'early': 'Sorting endosomes',
        'late': 'Maturation to lysosomes'
    }
}
```

### Cytoskeleton

```python
# Cytoskeletal components
cytoskeleton = {
    'microtubules': {
        'diameter': '25 nm',
        'subunit': 'α/β-tubulin dimer',
        'GTP': 'Required for polymerization',
        'motor_proteins': 'Kinesin (anterograde), Dynein (retrograde)',
        'organization': 'Centrosome (animal cells)'
    },
    'actin_filaments': {
        'diameter': '7 nm',
        'subunit': 'G-actin monomer',
        'ATP': 'Required for polymerization',
        'motor_proteins': 'Myosin',
        'organization': 'Cortical, stress fibers'
    },
    'intermediate_filaments': {
        'diameter': '10 nm',
        'types': 'Vimentin, keratin, lamin',
        'function': 'Structural support'
    }
}
```

-----

## Cell Signaling

### Types of Cell Signaling

```python
# Signaling types
signaling_types = {
    'autocrine': {
        'description': 'Cell signals to itself',
        'example': 'Cytokine signaling in immune cells'
    },
    'paracrine': {
        'description': 'Local signaling to nearby cells',
        'example': 'Synaptic signaling'
    },
    'endocrine': {
        'description': 'Long-distance via bloodstream',
        'example': 'Hormone signaling'
    },
    'juxtacrine': {
        'description': 'Direct cell-cell contact',
        'example': 'Notch signaling'
    }
}

# Signal transduction types
signal_types = {
    'lipid_second_messengers': ['DAG', 'IP3', 'cAMP', 'cGMP'],
    'calcium_signaling': ['Ca²⁺ release from ER', 'store-operated calcium entry'],
    'kinase_cascades': ['MAPK pathway', 'PI3K/Akt pathway'],
    'ion_channels': ['Ligand-gated', 'Voltage-gated']
}
```

### Major Signaling Pathways

```python
# Receptor tyrosine kinase (RTK) signaling
rtk_signaling = {
    'receptors': ['EGFR', 'InsR', 'FGFR', 'PDGFR'],
    'ligands': ['EGF', 'Insulin', 'FGF', 'PDGF'],
    'pathway': [
        '1. Ligand binding → receptor dimerization',
        '2. Autophosphorylation of tyrosine residues',
        '3. Adapter proteins bind phosphotyrosines',
        '4. RAS/MAPK, PI3K/Akt pathways activated'
    ],
    'downstream': ['MAPK/ERK', 'PI3K/Akt', 'PLCγ']
}

# G protein-coupled receptor (GPCR) signaling
gpcr_signaling = {
    'structure': '7 transmembrane domains',
    'G_proteins': ['Gs (stimulatory)', 'Gi (inhibitory)', 'Gq (phospholipase C)'],
    'pathways': [
        'Gs → Adenylyl cyclase → cAMP → PKA',
        'Gq → PLC → IP3/DAG → PKC',
        'Gi → Adenylyl cyclase inhibition'
    ]
}

# Nuclear receptor signaling
nuclear_receptor_signaling = {
    'receptors': ['ER', 'GR', 'TR', 'RAR', 'VDR'],
    'ligands': ['Steroid hormones', 'Thyroid hormone', 'Retinoic acid', 'Vitamin D'],
    'mechanism': 'Lipid-soluble → cytoplasm → nucleus → gene transcription'
}
```

### Second Messengers

```python
# Second messenger systems
second_messengers = {
    'cAMP': {
        'synthesized_by': 'Adenylyl cyclase',
        'degraded_by': 'Phosphodiesterase',
        'effectors': ['PKA', 'EPAC', 'CNG channels'],
        'pathway': 'G_s → AC → cAMP → PKA'
    },
    'IP3_DAG': {
        'synthesized_by': 'Phospholipase C',
        'targets': ['IP3 → ER Ca²⁺ release', 'DAG → PKC activation'],
        'pathway': 'G_q → PLC → IP3/DAG'
    },
    'calcium': {
        'sources': ['ER (via IP3R)', 'Extracellular', 'Mitochondria'],
        'buffers': 'Calmodulin, parvalbumin',
        'effectors': 'Calmodulin, PKC, CaMK'
    },
    'cGMP': {
        'synthesized_by': 'Guanylyl cyclase',
        'degraded_by': 'Phosphodiesterase',
        'effectors': ['PKG', 'CNG channels', 'PDEs']
    }
}
```

-----

## Cell Cycle Regulation

### Cell Cycle Phases

```python
# Cell cycle phases
cell_cycle = {
    'G1': {
        'duration': 'Variable (hours to days)',
        'events': [
            'Cell growth',
            'Protein synthesis',
            'Organelle replication',
            'G1 checkpoint (restriction point)'
        ],
        'cyclins': 'Cyclin D binds CDK4/6'
    },
    'S': {
        'duration': '8-10 hours (human)',
        'events': [
            'DNA replication',
            'Histone synthesis',
            'Centrosome duplication'
        ],
        'cyclins': 'Cyclin E (early), Cyclin A (later)'
    },
    'G2': {
        'duration': '4-6 hours',
        'events': [
            'Cell growth',
            'Protein synthesis',
            'G2 checkpoint'
        ],
        'cyclins': 'Cyclin A binds CDK1'
    },
    'M': {
        'duration': '1-2 hours',
        'events': [
            'Prophase: Chromatin condensation',
            'Metaphase: Chromosome alignment',
            'Anaphase: Sister chromatid separation',
            'Telophase/Cytokinesis: Cell division'
        ],
        'cyclins': 'Cyclin B binds CDK1 (M-phase promoting factor)'
    }
}

# Cell cycle checkpoints
checkpoints = {
    'G1_S_checkpoint': {
        'restrictions': 'DNA damage', 'nutrient status', 'cell size',
        'key_proteins': 'p53, p21, Rb'
    },
    'G2_M_checkpoint': {
        'restrictions': 'DNA replication complete', 'DNA damage',
        'key_proteins': 'Chk1, Chk2, Cdc25'
    },
    'M_checkpoint': {
        'restrictions': 'Chromosome attachment to spindle',
        'key_proteins': 'Mad2, BubR1, APC/C'
    }
}
```

### Cyclins and CDKs

```python
# Cyclin-CDK complexes
cyclin_cdk = {
    'G1_CDK': {
        'cyclins': ['Cyclin D'],
        'cdks': ['CDK4', 'CDK6'],
        'substrates': ['Rb protein'],
        'function': 'G1 progression'
    },
    'G1_S_transition': {
        'cyclins': ['Cyclin E'],
        'cdks': ['CDK2'],
        'substrates': ['Rb protein'],
        'function': 'S phase entry'
    },
    'S_phase': {
        'cyclins': ['Cyclin A'],
        'cdks': ['CDK2'],
        'function': 'DNA replication'
    },
    'G2_M_transition': {
        'cyclins': ['Cyclin A', 'Cyclin B'],
        'cdks': ['CDK1'],
        'function': 'M phase entry'
    }
}

# Cell cycle regulators
regulators = {
    'positive': ['Cyclins', 'CDK1/2/4/6', 'CDC25'],
    'negative': ['p21', 'p27', 'p16', 'p53']
}
```

-----

## Cell Death Pathways

### Apoptosis

```python
# Apoptosis pathways
apoptosis = {
    'intrinsic_mitochondrial': {
        'triggers': ['DNA damage', 'Oxidative stress', 'Growth factor withdrawal'],
        'key_events': [
            'Mitochondrial outer membrane permeabilization (MOMP)',
            'Cytochrome c release',
            'Caspase-9 activation',
            'Apoptosome formation'
        ],
        'regulators': ['Bcl-2 family', 'p53', 'IAPs']
    },
    'extrinsic_death_receptor': {
        'receptors': ['Fas/CD95', 'TNF-R1', 'TRAIL-R'],
        'pathways': ['Fas → FADD → Caspase-8', 'TNF → TRADD → Caspase-8'],
        'key_events': [
            'Death receptor activation',
            'DISC formation',
            'Caspase-8 activation'
        ]
    }
}

# Caspase cascade
caspases = {
    'initiator_caspases': ['Caspase-8', 'Caspase-9', 'Caspase-10'],
    'executioner_caspases': ['Caspase-3', 'Caspase-6', 'Caspase-7'],
    'substrates': ['PARP', 'Lamin', 'Actin', 'DNA repair proteins']
}
```

### Other Cell Death Types

```python
# Necrosis
necrosis = {
    'characteristics': [
        'Cell swelling',
        'Membrane rupture',
        'Release of cellular contents',
        'Inflammation'
    ],
    'triggers': ['Physical injury', 'Toxins', 'Ischemia']
}

# Autophagy
autophagy = {
    'types': ['Macroautophagy', 'Microautophagy', 'Chaperone-mediated'],
    'process': [
        'Initiation: ULK1 complex',
        'Nucleation: PI3K complex',
        'Elongation: LC3 conjugation',
        'Fusion: Autophagosome with lysosome'
    ],
    'functions': 'Recycling, stress survival, quality control'
}

# Ferroptosis
ferroptosis = {
    'characteristics': ['Iron-dependent', 'Lipid peroxidation', 'No caspase activation'],
    'triggers': ['GPX4 inhibition', 'Iron overload', 'Lipid ROS accumulation'],
    'inhibitors': ['Ferrostatin-1', 'Liproxstatin-1']
}
```

-----

## Cell Culture Techniques

### Basic Cell Culture

```python
# Cell culture fundamentals
culture_conditions = {
    'temperature': '37°C (mammalian)',
    'co2': '5% CO₂',
    'ph': '7.2-7.4',
    'osmolarity': '280-310 mOsm',
    'serum': '10% FBS (typically)'
}

# Common cell lines
cell_lines = {
    'HeLa': {
        'origin': 'Human cervical cancer',
        'type': 'Epithelial',
        'applications': 'General transfection, protein expression'
    },
    'HEK293': {
        'origin': 'Human embryonic kidney',
        'type': 'Epithelial',
        'applications': 'Transfection, protein production'
    },
    'COS-7': {
        'origin': 'African green monkey kidney',
        'type': 'Fibroblast',
        'applications': 'Transient expression'
    },
    'NIH-3T3': {
        'origin': 'Mouse embryo',
        'type': 'Fibroblast',
        'applications': 'Transfection, transformation'
    }
}

# Cell counting
def calculate_cell_concentration(count, dilution_factor, hemocytometer_squares):
    """
    Calculate cell concentration.
    """
    cells_per_ml = (count / hemocytometer_squares) * dilution_factor * 10**4
    return cells_per_ml
```

### Transfection Methods

```python
# Transfection methods comparison
transfection_methods = {
    'lipofection': {
        'efficiency': 'High',
        'toxicity': 'Moderate',
        'applications': 'Transient transfection'
    },
    'electroporation': {
        'efficiency': 'High (cell type dependent)',
        'toxicity': 'High',
        'applications': 'Stable transfection, primary cells'
    },
    'calcium_phosphate': {
        'efficiency': 'Moderate',
        'toxicity': 'Low',
        'applications': 'Stable transfection, HEK293'
    },
    'viral': {
        'efficiency': 'Very high',
        'toxicity': 'Variable',
        'applications': 'Gene delivery, difficult cells'
    }
}
```

-----

## Common Errors to Avoid

- **Contamination**: Aseptic technique is essential
- **Mycoplasma**: Regular testing recommended
- **Cell line authentication**: Verify identity
- **P-assage number**: Limit passages for primary cells
- **Media/serum variability**: Test lots
- **Freezing damage**: Use DMSO, controlled rates
- **Over confluency**: Subculture before contact inhibition
- **Temperature shifts**: Keep cells at 37°C
- **pH drift**: CO₂ incubator essential
- **Ignoring morphology**: Changes indicate problems
