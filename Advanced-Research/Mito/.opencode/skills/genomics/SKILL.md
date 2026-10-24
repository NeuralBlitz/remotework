---

## name: genomics
description: >
  Genomics expert for DNA analysis, genome sequencing, and computational biology. Use this skill
  whenever the user needs: analyzing DNA sequences, working with sequencing data, performing genome
  assembly, identifying genetic variants, conducting comparative genomics, or any task involving
  the study of genomes and genetic information. This skill covers sequencing technologies,
  bioinformatics pipelines, variant calling, genome assembly, and functional genomics.
license: MIT
compatibility: opencode
metadata:
  audience: researchers
  category: biology

# Genomics — Genome Analysis and DNA Sequencing

Covers: **DNA Sequencing Technologies · Variant Calling · Genome Assembly · Comparative Genomics · Functional Genomics · Bioinformatics Tools · Population Genetics**

-----

## DNA Sequencing Technologies

### Sequencing Generations

| Generation | Technology | Read Length | Throughput | Applications |
|------------|------------|-------------|------------|--------------|
| **First** | Sanger | 500-1000 bp | Low | Validation, small targets |
| **Second** | Illumina | 50-300 bp | Very High | Whole genome, exome |
| **Third** | PacBio | 10-15 kb | High | Assembly, structural variants |
| **Third** | Oxford Nanopore | 100s kb | High | Real-time, long reads |
| **Fourth** | 10x Genomics | Linked reads | High | Haplotypes, SVs |

```python
# Sequencing quality scores (Phred)
def phred_to_prob(Q):
    """
    Convert Phred quality score to error probability.
    Q = -10 * log10(p_error)
    """
    return 10 ** (-Q / 10)

def prob_to_phred(p):
    """
    Convert error probability to Phred score.
    """
    return -10 * np.log10(p)

# FASTQ format processing
def parse_fastq(fastq_file):
    """
    Parse FASTQ file and yield sequences.
    FASTQ format: @seqID\nsequence\n+\nqualities\n
    """
    with open(fastq_file, 'r') as f:
        while True:
            try:
                seq_id = next(f).strip()[1:]  # Remove @
                sequence = next(f).strip()
                plus = next(f).strip()
                quality = next(f).strip()
                
                yield {
                    'id': seq_id,
                    'sequence': sequence,
                    'quality': quality,
                    'qual_scores': [ord(c) - 33 for c in quality]
                }
            except StopIteration:
                break
```

### Sequence Alignment

```python
# Bowtie/BWA-style alignment concepts
def simple_align(query, reference, max_mismatches=2):
    """
    Simple exact matching alignment.
    In practice, use BWA, Bowtie2, or minimap2.
    """
    matches = []
    ref_len = len(reference)
    query_len = len(query)
    
    for i in range(ref_len - query_len + 1):
        mismatches = sum(1 for j in range(query_len) 
                        if reference[i+j] != query[j])
        if mismatches <= max_mismatches:
            matches.append({
                'position': i,
                'mismatches': mismatches,
                'cigar': f'{query_len}M'  # Simplified
            })
    
    return matches

# SAM/BAM format
sam_format = {
    'header': '@HD, @SQ, @RG, @PG',
    'columns': [
        'QNAME', 'FLAG', 'RNAME', 'POS', 'MAPQ', 'CIGAR',
        'RNEXT', 'PNEXT', 'TLEN', 'SEQ', 'QUAL'
    ],
    'flags': {
        'paired': 1,
        'properly_paired': 2,
        'unmapped': 4,
        'mate_unmapped': 8,
        'reverse': 16,
        'mate_reverse': 32,
        'read1': 64,
        'read2': 128
    }
}
```

### Variant Calling

```python
# Variant types
variant_types = {
    'SNP': {
        'name': 'Single Nucleotide Polymorphism',
        'description': 'Single base pair changes'
    },
    'INDEL': {
        'name': 'Insertion/Deletion',
        'description': 'Small insertions or deletions (typically <50bp)'
    },
    'SV': {
        'name': 'Structural Variant',
        'description': 'Large changes (>50bp)',
        'types': ['Deletion', 'Duplication', 'Inversion', 'Translocation']
    },
    'CNV': {
        'name': 'Copy Number Variation',
        'description': 'Copy number changes'
    }
}

# VCF format
vcf_format = {
    'header': '#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT',
    'required_fields': ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER'],
    'info_fields': {
        'DP': 'Total depth',
        'AF': 'Allele frequency',
        'QD': 'Quality by depth',
        'FS': 'Fisher strand bias',
        'MQ': 'RMS mapping quality'
    },
    'genotype_fields': {
        'GT': 'Genotype',
        'AD': 'Allelic depths',
        'DP': 'Read depth',
        'GQ': 'Genotype quality',
        'PL': 'Phred-scaled genotype likelihoods'
    }
}
```

### Variant Calling Workflow

```python
# Variant calling pipeline steps
variant_calling_pipeline = [
    '1. Quality control (FastQC)',
    '2. Trimming (Trimmomatic, Cutadapt)',
    '3. Alignment (BWA, Bowtie2)',
    '4. Sorting and indexing (SAMtools)',
    '5. Mark duplicates (Picard)',
    '6. Local realignment (GATK)',
    '7. Base quality recalibration (GATK)',
    '8. Variant calling (GATK HaplotypeCaller, FreeBayes)',
    '9. Filtering (GATK VariantFiltration)',
    '10. Annotation (SnpEff, ANNOVAR)'
]

# GATK Best Practices
gatk_pipeline = {
    'data_preprocessing': [
        'Align to reference',
        'Sort SAM/BAM',
        'Mark duplicates',
        'Add read groups',
        'BQSR (Base Quality Score Recalibration)'
    ],
    'haplotype_calling': [
        'HaplotypeCaller per sample',
        'GenotypeGVCFs for cohort',
        'VariantRecalibrator',
        'ApplyRecalibration'
    ],
    'filtering': {
        'QD': '< 2.0',
        'FS': '> 60.0',
        'MQ': '< 40.0',
        'SOR': '> 3.0',
        'MQRankSum': '< -12.5',
        'ReadPosRankSum': '< -8.0'
    }
}
```

-----

## Genome Assembly

### Assembly Algorithms

```python
# Genome assembly approaches
assembly_algorithms = {
    'overlap_layoutconsensus': {
        'description': 'Find overlaps between reads, build layout, consensus',
        'good_for': 'Long reads (PacBio, Nanopore)',
        'tools': ['Canu', 'Flye', 'wtdbg2']
    },
    'de_bruijn': {
        'description': 'Build k-mer graph, find Eulerian path',
        'good_for': 'Short reads (Illumina)',
        'tools': ['SPAdes', 'Velvet', 'ABySS']
    }
}

# K-mer analysis
def kmer_spectrum(sequences, k):
    """
    Generate k-mer frequency spectrum.
    """
    kmer_counts = {}
    
    for seq in sequences:
        for i in range(len(seq) - k + 1):
            kmer = seq[i:i+k]
            kmer_counts[kmer] = kmer_counts.get(kmer, 0) + 1
    
    return kmer_counts

def find_error_kmers(kmer_counts, threshold=3):
    """
    Identify likely error k-mers (low frequency).
    """
    return {k: v for k, v in kmer_counts.items() if v <= threshold}

# Assembly metrics
assembly_metrics = {
    'contigs': 'Continuous sequences',
    'N50': '50% of assembly in contigs >= N50',
    'L50': 'Number of contigs >= N50',
    'NG50': 'Similar to N50 but compared to reference',
    'scaffolds': 'Contigs joined with gaps',
    'BUSCO': 'Complete, fragmented, missing gene percentages'
}
```

### Long-read Assembly

```python
# Long-read assembly pipeline
long_read_pipeline = {
    'preprocessing': [
        'Read quality filtering',
        'Remove adapters',
        'Length filtering'
    ],
    'correction': [
        'Self-correction (Canu)',
        'Racon polishing',
        'Medaka polishing'
    ],
    'assembly': [
        'Canu: Overlap-Layout-Consensus',
        'Flye: Repeat graph',
        'Shasta: MinHash'
    ],
    'polishing': [
        'Racon: Long-read polishing',
        'Pilon: Short-read polishing',
        'Medaka: Neural network polishing'
    ]
}

# Hi-C scaffolding
hic_scaffolding = {
    'description': 'Use chromatin contact data to scaffold',
    'library': 'Hi-C (proximity ligation)',
    'software': ['HiCanu', 'SALSA', '3D-DNA'],
    'advantage': 'Chromosome-level assembly'
}
```

-----

## Comparative Genomics

### Sequence Comparison

```python
# Pairwise sequence alignment (simplified)
def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2):
    """
    Global alignment using dynamic programming.
    """
    m, n = len(seq1), len(seq2)
    
    # Initialize scoring matrix
    score = np.zeros((m+1, n+1))
    
    # Initialize first row and column
    for i in range(m+1):
        score[i][0] = i * gap
    for j in range(n+1):
        score[0][j] = j * gap
    
    # Fill matrix
    for i in range(1, m+1):
        for j in range(1, n+1):
            match_score = match if seq1[i-1] == seq2[j-1] else mismatch
            score[i][j] = max(
                score[i-1][j-1] + match_score,  # Match/Mismatch
                score[i-1][j] + gap,           # Delete
                score[i][j-1] + gap             # Insert
            )
    
    return score[m][n]

# BLAST algorithm
blast_pipeline = {
    'step1': 'Make k-mer words from query',
    'step2': 'Scan database for matching words',
    'step3': 'Extend hits',
    'step4': 'Score extensions',
    'step5': 'Report statistically significant alignments'
}

# Multiple sequence alignment
msa_tools = {
    'progressive': ['ClustalW', 'MUSCLE', 'MAFFT'],
    'iterative': ['MAFFT', 'PRANK'],
    'exact': ['PAM', 'BLOSUM']
}
```

### Phylogenomics

```python
# Orthology detection
orthology_methods = {
    'graph_based': ['OrthoMCL', 'InParanoid'],
    'tree_based': ['PhyloTreePruner', 'OrthoFinder'],
    'distance_based': ['OI', 'RBH']
}

# Gene family analysis
def gene_family_expansion(families, species_tree):
    """
    Analyze gene family size across species.
    """
    expansions = []
    contractions = []
    
    for family, counts in families.items():
        # Compare across species
        # Expansion: count significantly increased
        # Contraction: count significantly decreased
        pass
    
    return expansions, contractions
```

-----

## Functional Genomics

### Gene Expression Analysis

```python
# RNA-seq workflow
rnaseq_pipeline = {
    'qc': ['FastQC', 'MultiQC'],
    'trimming': ['Trimmomatic', 'Cutadapt'],
    'alignment': ['STAR', 'HISAT2', 'Bowtie2'],
    'quantification': ['featureCounts', 'HTSeq', 'Salmon'],
    'normalization': ['TMM', 'RPKM', 'FPKM', 'TPM'],
    'differential': ['DESeq2', 'edgeR', 'limma-voom'],
    'enrichment': ['GSEA', 'GO enrichment']
}

# Expression normalization
normalization_methods = {
    'RPKM': 'Reads Per Kilobase Million',
    'FPKM': 'Fragments Per Kilobase Million',
    'TPM': 'Transcripts Per Million (recommended)',
    'TMM': 'Trimmed Mean of M-values'
}

# Differential expression
def deseq2_analysis(counts, condition):
    """
    Simplified DESeq2 analysis steps.
    """
    # 1. Create DESeqDataSet
    # 2. Run DESeq
    # 3. Extract results
    # 4. Shrink log fold changes
    # 5. Filter and padjust
    pass
```

### Epigenomics

```python
# Epigenomic techniques
epigenomics = {
    'ATAC-seq': 'Open chromatin (accessibility)',
    'ChIP-seq': 'Protein-DNA binding (TF, histone)',
    'Methyl-seq': 'DNA methylation',
    'Hi-C': '3D genome structure'
}

# DNA methylation analysis
methylation_analysis = {
    'bisulfite_conversion': 'Converts unmethylated C to U',
    'alignment': 'Bismark, BSW',
    'calling': 'MethylDackel, BatMeth2',
    'types': ['CpG', 'CHG', 'CHH']
}
```

-----

## Population Genetics

### Genetic Diversity

```python
# Genetic diversity metrics
diversity_metrics = {
    'pi': 'Nucleotide diversity (pairwise differences)',
    'theta_w': 'Watterson\'s theta',
    'tajima_d': 'Test for selection/demography',
    'Fst': 'Population differentiation',
    'Heterozygosity': 'Proportion of heterozygotes'
}

def calculate_nucleotide_diversity(sequences):
    """
    Calculate π (pi) nucleotide diversity.
    """
    n = len(sequences)
    if n < 2:
        return 0
    
    pi_sum = 0
    total_sites = len(sequences[0])
    
    for site in range(total_sites):
        alleles = [seq[site] for seq in sequences]
        allele_counts = {}
        for a in alleles:
            allele_counts[a] = allele_counts.get(a, 0) + 1
        
        # Pairwise differences at this site
        n_alleles = len(allele_counts)
        if n_alleles > 1:
            sum_counts = sum(count**2 for count in allele_counts.values())
            pi_site = 1 - sum_counts / (n * n)
            pi_sum += pi_site
    
    return pi_sum / total_sites
```

### GWAS

```python
# Genome-wide association study
gwas_pipeline = {
    'qc_samples': ['Check ancestry', 'Remove relatedness', 'Check sex'],
    'qc_snps': ['MAF filter', 'HWE filter', 'Missingness filter'],
    'association': ['PLINK', 'REGENIE', 'SAIGE'],
    'correction': ['Multiple testing (Bonferroni, FDR)'],
    'meta_analysis': 'Combine studies'
}

# Heritability
heritability = {
    'narrow_sense': 'Additive genetic variance / phenotypic variance',
    'broad_sense': 'Total genetic variance / phenotypic variance',
    'SNP_heritability': 'Variance explained by SNPs'
}
```

-----

## Bioinformatics Tools

### Common Tools

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| **FastQC** | Quality control | FASTQ | HTML report |
| **BWA** | Short-read alignment | FASTQ + reference | SAM/BAM |
| **SAMtools** | BAM manipulation | BAM | BAM/BCF |
| **GATK** | Variant calling | BAM | VCF |
| **BEDTools** | Interval operations | BED/BAM | BED/VCF |
| **IGV** | Visualization | Multiple | GUI viewer |
| **Biopython** | Sequence analysis | FASTA | Python objects |

### File Formats

```python
# Common bioinformatics file formats
file_formats = {
    'FASTA': '>header\nSEQUENCE\n',
    'FASTQ': '@header\nSEQ\n+\nQUAL\n',
    'SAM': 'Tab-separated alignment',
    'BAM': 'Binary compressed SAM',
    'VCF': 'Variant Call Format',
    'BED': 'Genomic intervals',
    'GTF': 'Gene transfer format (annotation)',
    'GFF': 'General feature format'
}
```

-----

## Common Errors to Avoid

- **Ignoring read quality**: Always QC raw data
- **Not filtering low-quality reads**: Leads to false variants
- **Assuming one tool is best**: Different tools for different needs
- **Ignoring reference bias**: Choose appropriate reference
- **Not understanding coverage**: Depth affects variant detection
- **Neglecting repetitive regions**: Assembly collapses
- **Ignoring strand bias**: Can indicate false positives
- **Not accounting for duplicates**: MarkDuplicates important
- **Forgetting to normalize**: Normalization essential for comparison
- **Overfiltering**: Don't remove low-quality without reason
