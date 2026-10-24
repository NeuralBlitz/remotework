---

## name: cheminformatics
description: >
  Expert cheminformatics assistant for computational chemists and researchers. Use this skill whenever the user needs:
  understanding molecular descriptors, chemical file formats, QSAR/QSPR modeling, molecular similarity, database searching,
  virtual screening, or any rigorous academic treatment of cheminformatics. Covers molecular fingerprints, machine learning
  in drug discovery, and chemical data management.
license: MIT
compatibility: opencode
metadata:
  audience: cheminformaticians, computational chemists, researchers
  category: chemistry

# Cheminformatics — Academic Research Assistant

Covers: **Molecular Descriptors · Chemical File Formats · QSAR/QSPR · Molecular Similarity · Virtual Screening · Chemical Databases · Machine Learning in Chemistry**

---

## Molecular Descriptors

### Constitutional Descriptors

|Descriptor|Definition|Example Use|
|-----------|-----------|------------|
|Molecular weight|Sum of atomic masses|Drug-likeness filter|
|Atom counts|Number of C, H, O, N, etc.|Functional group count|
|Ring count|Number of rings|Aromaticity|
|Fragments|SMARTS patterns|Substructure search|

### Topological Descriptors

|Descriptor|Formula|Interpretation|
|-----------|--------|---------------|
|Wiener index|W(G)|Molecular size, Wiener path|
|Balaban index|J|G Graphs with more cycles|
|Hosoya index|Z(G)|Count of independent sets|
|Connectivity indices|χ|Shape descriptors|

```python
class MolecularDescriptors:
    """Calculate molecular descriptors"""
    
    def wiener_index(self, adjacency_matrix):
        """Wiener index - sum of shortest paths"""
        import networkx as nx
        G = nx.from_numpy_array(adjacency_matrix)
        paths = dict(nx.all_pairs_shortest_path_length(G))
        
        wiener = 0
        for i in paths:
            for j in paths[i]:
                if i < j:
                    wiener += paths[i][j]
        
        return wiener
    
    def calculate_logp(self, smiles):
        """
        LogP prediction (fragment-based)
        Fragment contributions + correction factors
        """
        # Fragment contributions
        fragments = {
            'C': 0.133, 'H': 0.0, 'O': -0.567,
            'N': -1.02, 'F': 0.374, 'Cl': 0.064,
            'Br': 0.274, 'I': 0.592, 'S': -0.79,
            'Ring': -0.669, 'Double bond': 0.355
        }
        
        # Simplified calculation
        return sum(fragments.get(f, 0) for f in fragments)
    
    def hbond_donors_acceptors(self, smiles):
        """
        Count H-bond donors (OH, NH) and acceptors (O, N)
        """
        donors = smiles.count('O') + smiles.count('N')
        acceptors = smiles.count('O') + smiles.count('N')
        
        return donors, acceptors
    
    def topological_polar_surface_area(self, fragments):
        """
        PSA = Σ(fragment contributions)
        """
        psa_contributions = {
            'OH': 20.23, 'NH': 21.94,
            'COOH': 37.30, 'CO': 17.07,
            'CN': 21.94, 'O': 23.06,
            'N': 21.94
        }
        
        return sum(psa_contributions.get(f, 0) for f in fragments)
```

### Molecular Fingerprints

```python
class MolecularFingerprints:
    """Generate molecular fingerprints"""
    
    def morgan_fingerprint(self, molecule, radius=2, nBits=2048):
        """
        Morgan/ECFP fingerprint
        - Circular fingerprints
        - Environment around each atom
        - Radius determines neighborhood size
        """
        # Simplified representation
        features = self.extract_substructures(molecule, radius)
        bit_vector = self.encode_as_bits(features, nBits)
        
        return {
            'type': 'Morgan/ECFP',
            'radius': radius,
            'bits': nBits,
            'features': features,
            'bit_vector': bit_vector
        }
    
    def maccs_keys(self, molecule):
        """
        MACCS keys - 166 predefined structural keys
        """
        keys = [0] * 166
        
        # Check for presence of predefined fragments
        # 1: Has C-C single bond
        # 2: Has aromatic ring
        # ...
        
        return keys
    
    def topological_fingerprint(self, molecule, fpSize=2048):
        """
        Topological fingerprints (Daylight)
        - All paths of length 1 to specified
        - Hash to bit vector
        """
        paths = self.enumerate_paths(molecule)
        return self.hash_to_bits(paths, fpSize)
    
    def atom_pair_fingerprint(self, molecule):
        """
        Atom pair fingerprints
        - Pairs of atoms with distance
        - Type of each atom
        """
        pairs = []
        for i in range(len(molecule)):
            for j in range(i + 2, len(molecule)):
                atom1 = molecule[i]
                atom2 = molecule[j]
                distance = j - i
                pairs.append((atom1, atom2, distance))
        
        return self.encode_pairs(pairs)
```

---

## Chemical File Formats

|Format|Extension|Description|
|-------|----------|------------|
|SMILES|.smi|String representation|
|SDF|.sdf|Multiple structures with data|
|MOL/.mol|.mol|MDL molfile|
|PDB|.pdb|3D structure with atoms|
|InChI|.ich|IUPAC identifier|
|SMILES|SMILES|Simplified format|

```python
class ChemicalFileFormats:
    """Chemical file format handling"""
    
    def parse_smiles(self, smiles):
        """Parse SMILES string"""
        # Canonicalization
        # Stereochemistry handling
        # Aromaticity detection
        return self.build_molecule(smiles)
    
    def write_sdf(self, molecules, properties):
        """
        Write SDF format
        Structure:
        - Molblock (atoms, bonds)
        - > <property_name>
        - property_value
        - ...
        - $$$$
        """
        output = ""
        for mol in molecules:
            output += self.molblock(mol)
            for prop_name, prop_value in properties.items():
                output += f">  <{prop_name}>\n{prop_value}\n\n"
            output += "$$$$\$\n"
        
        return output
    
    def pdb_to_mol2(self, pdb_file):
        """
        Convert PDB to MOL2 format
        - Atom types
        - Charges
        - Bonds
        """
        pass
```

---

## Molecular Similarity

### Similarity Coefficients

```python
class MolecularSimilarity:
    """Calculate molecular similarity"""
    
    def tanimoto_coefficient(self, fp1, fp2):
        """
        Tanimoto (Jaccard) coefficient
        Tc = c / (a + b - c)
        where:
        - a = bits set in fp1
        - b = bits set in fp2
        - c = bits set in both
        """
        a = sum(fp1)
        b = sum(fp2)
        c = sum([1 for i in range(len(fp1)) if fp1[i] and fp2[i]])
        
        if a + b - c == 0:
            return 0
        
        return c / (a + b - c)
    
    def dice_similarity(self, fp1, fp2):
        """
        Dice coefficient
        Dice = 2c / (a + b)
        """
        a = sum(fp1)
        b = sum(fp2)
        c = sum([1 for i in range(len(fp1)) if fp1[i] and fp2[i]])
        
        if a + b == 0:
            return 0
        
        return 2 * c / (a + b)
    
    def cosine_similarity(self, fp1, fp2):
        """
        Cosine similarity
        Cosine = (A · B) / (||A|| × ||B||)
        """
        import numpy as np
        
        dot = sum([f1 * f2 for f1, f2 in zip(fp1, fp2)])
        norm1 = np.sqrt(sum([f**2 for f in fp1]))
        norm2 = np.sqrt(sum([f**2 for f in fp2]))
        
        if norm1 * norm2 == 0:
            return 0
        
        return dot / (norm1 * norm2)
    
    def euclidean_distance(self, fp1, fp2):
        """Euclidean distance"""
        import numpy as np
        return np.sqrt(sum([(f1 - f2)**2 for f1, f2 in zip(fp1, fp2)]))
```

---

## QSAR/QSPR Modeling

### Model Building Pipeline

```
1. Data Collection
   └─> Curated dataset with measured values

2. Descriptor Calculation
   └─> Calculate molecular descriptors

3. Feature Selection
   └─> Remove correlated, uninformative features
   └─> Methods: variance, correlation, recursive feature elimination

4. Model Training
   └─> Split data (train/test/validation)
   └─> Select algorithm
   └─> Hyperparameter tuning

5. Validation
   └─> Internal: cross-validation, bootstrap
   └─> External: test set
   └─> Y-randomization

6. Interpretation
   └─> Feature importance
   └─> Applicability domain
```

```python
class QSARModel:
    """QSAR/QSPR modeling workflow"""
    
    def prepare_dataset(self, compounds, property_values):
        """Prepare dataset with descriptors"""
        from rdkit import Chem
        from rdkit.Chem import Descriptors
        
        dataset = []
        for smi, value in zip(compounds, property_values):
            mol = Chem.MolFromSmiles(smi)
            if mol:
                descriptors = {
                    'MolWt': Descriptors.MolWt(mol),
                    'LogP': Descriptors.MolLogP(mol),
                    'TPSA': Descriptors.TPSA(mol),
                    'NumHDonors': Descriptors.NumHDonors(mol),
                    'NumHAcceptors': Descriptors.NumHAcceptors(mol),
                    'NumRotatableBonds': Descriptors.NumRotatableBonds(mol),
                    'NumAromaticRings': Descriptors.NumAromaticRings(mol),
                    'property': value
                }
                dataset.append(descriptors)
        
        return dataset
    
    def applicability_domain(self, train_descriptors, test_descriptor, threshold=0.8):
        """
        Determine if test compound is in AD
        Methods: leverage, distance, density
        """
        from scipy.spatial.distance import mahalanobis
        
        # Leverage approach
        # Compare test to training set distribution
        pass
    
    def validate_model(self, y_true, y_pred):
        """Model validation metrics"""
        from sklearn.metrics import r2_score, mean_squared_error
        
        return {
            'R2': r2_score(y_true, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'MAE': mean_absolute_error(y_true, y_pred)
        }
```

---

## Virtual Screening

### Similarity-Based Screening

```python
class VirtualScreening:
    """Virtual screening workflows"""
    
    def screen_by_similarity(self, query_fp, database_fps, threshold=0.7):
        """
        Screen database by Tanimoto similarity
        Returns: sorted list of hits
        """
        hits = []
        
        for db_id, db_fp in database_fps:
            similarity = self.tanimoto_coefficient(query_fp, db_fp)
            if similarity >= threshold:
                hits.append((db_id, similarity))
        
        # Sort by similarity
        return sorted(hits, key=lambda x: x[1], reverse=True)
    
    def substructure_screen(self, query_smarts, database):
        """
        Screen for substructure matches
        """
        from rdkit import Chem
        
        pattern = Chem.MolFromSmarts(query_smarts)
        
        hits = []
        for db_id, smi in database:
            mol = Chem.MolFromSmiles(smi)
            if mol.HasSubstructMatch(pattern):
                hits.append(db_id)
        
        return hits
```

---

## Chemical Databases

|Database|URL|Content|
|--------|---|--------|
|ChEMBL|chembl.unichem.ac.uk|Bioactivity data|
|PubChem|pubchem.ncbi.nlm.nih.gov|Compounds, bioactivity|
|ZINC|zinc15.docking.org|Commercial compounds|
|ChemSpider|chemspider.com|Property data|
|DrugBank|drugbank.com|Drug information|

---

## Common Errors to Avoid

1. **Using wrong fingerprint type** — Different fingerprints for different purposes
2. **Ignoring stereochemistry** — Can dramatically affect activity
3. **Not checking data quality** — Bad data → bad models
4. **Overfitting models** — Always validate externally
5. **Ignoring applicability domain** — Model only valid within training space
6. **Not normalizing descriptors** — Different scales affect ML models
7. **Forgetting tautomeric forms** — Different forms = different SMILES
8. **Confusing SMILES with canonical SMILES** — Different representations possible

