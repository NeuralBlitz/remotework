-----
name: eda
description: >
  Expert in Exploratory Data Analysis for understanding data structure, identifying 
  patterns, detecting anomalies, and generating insights. Use this skill for initial 
  data exploration, data cleaning, visualization, and preparing analysis pipelines. 
  Covers data profiling, statistical summaries, visualization techniques, and 
  feature engineering guidance.
license: MIT
compatibility: opencode
metadata:
  audience: data-analysts
  category: data-science
  tags: [eda, data-analysis, visualization, data-cleaning, exploration]

# Exploratory Data Analysis

Covers: **Data Profiling · Statistical Summaries · Visualization · Outlier Detection · Missing Values · Feature Engineering · Correlation Analysis**

-----

## Data Exploration Fundamentals

### The EDA Mindset

Exploratory Data Analysis (EDA) is the process of systematically examining datasets to:
- Understand the data structure and variables
- Discover patterns and relationships
- Identify anomalies and outliers
- Generate hypotheses for further analysis
- Guide feature selection and engineering

### EDA Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    EDA PROCESS FLOW                             │
├─────────────────────────────────────────────────────────────────┤
│  1. Define Objectives     → What questions to answer?          │
│  2. Collect Data         → Load from various sources            │
│  3. Data Structure       → Shape, types, memory                │
│  4. Summary Statistics   → Central tendency, spread            │
│  5. Data Quality         → Missing, duplicates, outliers       │
│  6. Visual Exploration   → Plots, distributions, relationships  │
│  7. Feature Engineering  → Create new features                 │
│  8. Document Findings    → Record insights and limitations     │
└─────────────────────────────────────────────────────────────────┘
```

-----

## Data Loading and Structure Analysis

### Loading Data

```python
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class DataLoader:
    """Data loading utilities"""
    
    @staticmethod
    def load_csv(filepath: str, **kwargs) -> pd.DataFrame:
        """Load CSV with common options"""
        df = pd.read_csv(filepath, **kwargs)
        return df
    
    @staticmethod
    def load_excel(filepath: str, sheet_name: str = 0) -> pd.DataFrame:
        """Load Excel file"""
        return pd.read_excel(filepath, sheet_name=sheet_name)
    
    @staticmethod
    def load_json(filepath: str, orient: str = 'records') -> pd.DataFrame:
        """Load JSON file"""
        return pd.read_json(filepath, orient=orient)
    
    @staticmethod
    def infer_datetime(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
        """Infer and convert datetime columns"""
        df = df.copy()
        
        if columns is None:
            # Try to infer from column names
            columns = [col for col in df.columns 
                       if any(dt in col.lower() for dt in 
                              ['date', 'time', 'created', 'updated'])]
        
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df


class DataStructureAnalyzer:
    """Analyze data structure"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def overview(self) -> dict:
        """Get data overview"""
        return {
            'shape': self.df.shape,
            'n_rows': self.df.shape[0],
            'n_columns': self.df.shape[1],
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
            'column_names': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict()
        }
    
    def column_types_summary(self) -> pd.DataFrame:
        """Summary of column data types"""
        return self.df.dtypes.value_counts().to_frame('count')
    
    def missing_summary(self) -> pd.DataFrame:
        """Missing values summary"""
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        return pd.DataFrame({
            'missing_count': missing,
            'missing_percent': missing_pct
        }).query('missing_count > 0').sort_values('missing_percent', ascending=False)
    
    def duplicate_summary(self) -> dict:
        """Duplicate analysis"""
        n_duplicates = self.df.duplicated().sum()
        return {
            'n_duplicates': n_duplicates,
            'duplicate_percent': (n_duplicates / len(self.df)) * 100
        }
    
    def cardinality(self) -> pd.DataFrame:
        """Unique values per column"""
        return pd.DataFrame({
            'unique': self.df.nunique(),
            'unique_percent': (self.df.nunique() / len(self.df)) * 100,
            'is_unique': self.df.nunique() == len(self.df)
        })
    
    def full_report(self) -> dict:
        """Generate comprehensive structure report"""
        return {
            'overview': self.overview(),
            'column_types': self.column_types_summary(),
            'missing': self.missing_summary() if self.df.isnull().any().any() else pd.DataFrame(),
            'duplicates': self.duplicate_summary(),
            'cardinality': self.cardinality()
        }
```

### Data Type Handling

```python
class DataTypeAnalyzer:
    """Analyze and convert data types"""
    
    @staticmethod
    def identify_column_types(df: pd.DataFrame) -> dict:
        """Categorize columns by type"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        bool_cols = df.select_dtypes(include=[bool]).columns.tolist()
        
        return {
            'numeric': numeric_cols,
            'categorical': categorical_cols,
            'datetime': datetime_cols,
            'boolean': bool_cols,
            'other': [c for c in df.columns if c not in numeric_cols + 
                     categorical_cols + datetime_cols + bool_cols]
        }
    
    @staticmethod
    def suggest_type_conversions(df: pd.DataFrame) -> dict:
        """Suggest type conversions for optimization"""
        suggestions = {}
        
        for col in df.columns:
            # Check if numeric stored as string
            if df[col].dtype == 'object':
                try:
                    pd.to_numeric(df[col], errors='raise')
                    suggestions[col] = 'convert_to_numeric'
                except:
                    pass
            
            # Check if categorical should be category type
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio < 0.5 and df[col].dtype == 'object':
                suggestions[col] = 'convert_to_category'
        
        return suggestions
    
    @staticmethod
    def convert_categoricals(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
        """Convert low-cardinality strings to category type"""
        df = df.copy()
        
        for col in df.select_dtypes(include=['object']).columns:
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio < threshold:
                df[col] = df[col].astype('category')
        
        return df
```

-----

## Statistical Analysis

### Numerical Statistics

```python
class NumericalStatistics:
    """Comprehensive numerical statistics"""
    
    @staticmethod
    def summary_statistics(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
        """Generate summary statistics for numerical columns"""
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        stats = df[columns].describe(percentiles=[.01, .05, .10, .25, .50, .75, .90, .95, .99]).T
        
        # Add additional statistics
        stats['variance'] = df[columns].var()
        stats['range'] = stats['max'] - stats['min']
        stats['iqr'] = stats['75%'] - stats['25%']
        stats['skewness'] = df[columns].skew()
        stats['kurtosis'] = df[columns].kurtosis()
        stats['cv'] = (stats['std'] / stats['mean']) * 100  # Coefficient of variation
        
        return stats
    
    @staticmethod
    def distribution_shape(df: pd.DataFrame, column: str) -> dict:
        """Analyze distribution shape"""
        data = df[column].dropna()
        
        skew = stats.skew(data)
        kurt = stats.kurtosis(data)
        
        shape = 'normal'
        if abs(skew) > 1:
            shape = 'highly skewed'
        elif abs(skew) > 0.5:
            shape = 'moderately skewed'
        
        if kurt > 3:
            shape += ', heavy-tailed'
        elif kurt < -1:
            shape += ', light-tailed'
        
        return {
            'skewness': skew,
            'kurtosis': kurt,
            'shape': shape,
            'interpretation': 'Right-skewed' if skew > 0 else 'Left-skewed' if skew < 0 else 'Symmetric'
        }
    
    @staticmethod
    def normality_tests(df: pd.DataFrame, column: str) -> dict:
        """Test for normality"""
        data = df[column].dropna()
        
        # Shapiro-Wilk (for smaller samples)
        shapiro_stat, shapiro_p = stats.shapiro(data) if len(data) <= 5000 else (None, None)
        
        # D'Agostino-Pearson
        dagostino_stat, dagostino_p = stats.normaltest(data)
        
        # K-S test
        ks_stat, ks_p = stats.kstest(data, 'norm', 
                                     args=(data.mean(), data.std()))
        
        return {
            'shapiro': {'stat': shapiro_stat, 'p': shapiro_p, 
                       'normal': shapiro_p > 0.05 if shapiro_p else None},
            'dagostino': {'stat': dagostino_stat, 'p': dagostino_p, 
                         'normal': dagostino_p > 0.05},
            'ks': {'stat': ks_stat, 'p': ks_p, 
                  'normal': ks_p > 0.05}
        }


class CategoricalStatistics:
    """Statistics for categorical variables"""
    
    @staticmethod
    def frequency_table(df: pd.DataFrame, column: str, 
                       include_pct: bool = True) -> pd.DataFrame:
        """Generate frequency table"""
        freq = df[column].value_counts()
        
        if include_pct:
            pct = (freq / len(df)) * 100
            return pd.DataFrame({
                'frequency': freq,
                'percent': pct,
                'cumulative_freq': freq.cumsum(),
                'cumulative_percent': pct.cumsum()
            })
        
        return pd.DataFrame({'frequency': freq})
    
    @staticmethod
    def cross_tabulation(df: pd.DataFrame, col1: str, col2: str,
                        normalize: bool = False) -> pd.DataFrame:
        """Create cross-tabulation"""
        if normalize:
            return pd.crosstab(df[col1], df[col2], normalize=normalize)
        return pd.crosstab(df[col1], df[col2], margins=True)
    
    @staticmethod
    def chi_square_test(df: pd.DataFrame, col1: str, col2: str) -> dict:
        """Chi-square test of independence"""
        contingency = pd.crosstab(df[col1], df[col2])
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
        
        # Cramér's V effect size
        n = len(df)
        min_dim = min(contingency.shape[0], contingency.shape[1]) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
        
        return {
            'chi2': chi2,
            'p_value': p_value,
            'dof': dof,
            'cramers_v': cramers_v,
            'independent': p_value > 0.05
        }
```

-----

## Missing Data Analysis

```python
class MissingDataAnalyzer:
    """Analyze missing data patterns"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def missing_summary(self) -> pd.DataFrame:
        """Comprehensive missing value summary"""
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        summary = pd.DataFrame({
            'column': self.df.columns,
            'missing_count': missing.values,
            'missing_percent': missing_pct.values,
            'dtype': self.df.dtypes.values
        })
        
        # Identify pattern
        summary['missing_pattern'] = summary['missing_count'].apply(
            lambda x: 'complete' if x == 0 else 
                     ('>50%' if x > len(self.df) * 0.5 else 
                      ('10-50%' if x > len(self.df) * 0.1 else '<10%'))
        )
        
        return summary.sort_values('missing_percent', ascending=False)
    
    def missing_correlation(self) -> pd.DataFrame:
        """Find correlations in missing patterns"""
        # Create binary missing indicators
        missing_matrix = self.df.isnull().astype(int)
        
        # Calculate correlation
        corr = missing_matrix.corr()
        
        # Return only pairs with correlation
        high_corr = []
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                if abs(corr.iloc[i, j]) > 0.5:
                    high_corr.append({
                        'column_1': corr.columns[i],
                        'column_2': corr.columns[j],
                        'correlation': corr.iloc[i, j]
                    })
        
        return pd.DataFrame(high_corr) if high_corr else pd.DataFrame()
    
    def missing_by_group(self, group_col: str) -> pd.DataFrame:
        """Analyze missing values by group"""
        results = []
        
        for group in self.df[group_col].unique():
            group_data = self.df[self.df[group_col] == group]
            for col in self.df.columns:
                missing_pct = (group_data[col].isnull().sum() / len(group_data)) * 100
                results.append({
                    'group': group,
                    'column': col,
                    'missing_percent': missing_pct
                })
        
        return pd.DataFrame(results)


class MissingDataImputation:
    """Missing data imputation strategies"""
    
    @staticmethod
    def mean_impute(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Mean imputation"""
        df = df.copy()
        for col in columns:
            df[col].fillna(df[col].mean(), inplace=True)
        return df
    
    @staticmethod
    def median_impute(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Median imputation (robust to outliers)"""
        df = df.copy()
        for col in columns:
            df[col].fillna(df[col].median(), inplace=True)
        return df
    
    @staticmethod
    def mode_impute(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Mode imputation for categorical"""
        df = df.copy()
        for col in columns:
            df[col].fillna(df[col].mode()[0], inplace=True)
        return df
    
    @staticmethod
    def forward_fill(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Forward fill time series data"""
        df = df.copy()
        for col in columns:
            df[col].fillna(method='ffill', inplace=True)
        return df
    
    @staticmethod
    def knn_impute(df: pd.DataFrame, n_neighbors: int = 5) -> pd.DataFrame:
        """KNN imputation"""
        from sklearn.impute import KNNImputer
        
        df_numeric = df.select_dtypes(include=[np.number])
        imputer = KNNImputer(n_neighbors=n_neighbors)
        imputed = imputer.fit_transform(df_numeric)
        
        result = df.copy()
        result[df_numeric.columns] = imputed
        return result
```

-----

## Outlier Detection

```python
class OutlierDetector:
    """Detect outliers in data"""
    
    @staticmethod
    def iqr_method(df: pd.DataFrame, column: str, 
                   multiplier: float = 1.5) -> dict:
        """IQR-based outlier detection"""
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        
        return {
            'method': 'IQR',
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'n_outliers': len(outliers),
            'outlier_percent': (len(outliers) / len(df)) * 100,
            'outlier_indices': outliers.index.tolist()
        }
    
    @staticmethod
    def zscore_method(df: pd.DataFrame, column: str, 
                      threshold: float = 3.0) -> dict:
        """Z-score based outlier detection"""
        mean = df[column].mean()
        std = df[column].std()
        
        z_scores = np.abs((df[column] - mean) / std)
        outliers = df[z_scores > threshold]
        
        return {
            'method': 'Z-score',
            'threshold': threshold,
            'n_outliers': len(outliers),
            'outlier_percent': (len(outliers) / len(df)) * 100,
            'outlier_indices': outliers.index.tolist()
        }
    
    @staticmethod
    def modified_zscore(df: pd.DataFrame, column: str,
                       threshold: float = 3.5) -> dict:
        """Modified Z-score (using median)"""
        median = df[column].median()
        mad = np.median(np.abs(df[column] - median))
        
        modified_z = 0.6745 * (df[column] - median) / mad
        outliers = df[np.abs(modified_z) > threshold]
        
        return {
            'method': 'Modified Z-score',
            'threshold': threshold,
            'n_outliers': len(outliers),
            'outlier_percent': (len(outliers) / len(df)) * 100,
            'outlier_indices': outliers.index.tolist()
        }
    
    @staticmethod
    def isolation_forest(df: pd.DataFrame, contamination: float = 0.1) -> dict:
        """Isolation Forest for outlier detection"""
        from sklearn.ensemble import IsolationForest
        
        X = df.select_dtypes(include=[np.number]).fillna(df.median())
        
        clf = IsolationForest(contamination=contamination, random_state=42)
        predictions = clf.fit_predict(X)
        
        outlier_indices = df.index[predictions == -1].tolist()
        
        return {
            'method': 'Isolation Forest',
            'contamination': contamination,
            'n_outliers': len(outlier_indices),
            'outlier_percent': (len(outlier_indices) / len(df)) * 100,
            'outlier_indices': outlier_indices
        }
    
    @staticmethod
    def percentile_method(df: pd.DataFrame, column: str,
                          lower_pct: float = 0.01, 
                          upper_pct: float = 0.99) -> dict:
        """Percentile-based outlier detection"""
        lower = df[column].quantile(lower_pct)
        upper = df[column].quantile(upper_pct)
        
        outliers = df[(df[column] < lower) | (df[column] > upper)]
        
        return {
            'method': 'Percentile',
            'lower_bound': lower,
            'upper_bound': upper,
            'n_outliers': len(outliers),
            'outlier_percent': (len(outliers) / len(df)) * 100,
            'outlier_indices': outliers.index.tolist()
        }
```

-----

## Visualization Techniques

### Univariate Plots

```python
import matplotlib.pyplot as plt
import seaborn as sns

class UnivariateVisualizer:
    """Univariate visualization"""
    
    @staticmethod
    def histogram_with_kde(df: pd.DataFrame, column: str, bins: int = 30):
        """Histogram with KDE overlay"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.histplot(df[column].dropna(), bins=bins, kde=True, ax=ax)
        ax.axvline(df[column].mean(), color='red', linestyle='--', 
                  label=f"Mean: {df[column].mean():.2f}")
        ax.axvline(df[column].median(), color='green', linestyle='--', 
                  label=f"Median: {df[column].median():.2f}")
        
        ax.set_title(f'Distribution of {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        ax.legend()
        
        return fig
    
    @staticmethod
    def box_plot(df: pd.DataFrame, column: str, by: str = None):
        """Box plot"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if by:
            sns.boxplot(data=df, x=by, y=column, ax=ax)
        else:
            sns.boxplot(data=df[column], ax=ax)
        
        ax.set_title(f'Box Plot of {column}' + (f' by {by}' if by else ''))
        
        return fig
    
    @staticmethod
    def violin_plot(df: pd.DataFrame, column: str, by: str = None):
        """Violin plot"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if by:
            sns.violinplot(data=df, x=by, y=column, ax=ax)
        else:
            sns.violinplot(data=df[column], ax=ax)
        
        ax.set_title(f'Violin Plot of {column}')
        
        return fig
    
    @staticmethod
    def bar_chart(df: pd.DataFrame, column: str, top_n: int = 20):
        """Bar chart for categorical"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        value_counts = df[column].value_counts().head(top_n)
        sns.barplot(x=value_counts.values, y=value_counts.index, ax=ax)
        
        ax.set_title(f'Top {top_n} Values in {column}')
        ax.set_xlabel('Count')
        
        return fig
```

### Bivariate Plots

```python
class BivariateVisualizer:
    """Bivariate visualization"""
    
    @staticmethod
    def scatter_plot(df: pd.DataFrame, x: str, y: str, 
                    hue: str = None, trendline: bool = True):
        """Scatter plot"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if hue:
            sns.scatterplot(data=df, x=x, y=y, hue=hue, ax=ax, alpha=0.6)
        else:
            sns.scatterplot(data=df, x=x, y=y, ax=ax, alpha=0.6)
        
        if trendline:
            sns.regplot(data=df, x=x, y=y, ax=ax, scatter=False, 
                       color='red', label='Trendline')
        
        ax.set_title(f'{y} vs {x}')
        
        return fig
    
    @staticmethod
    def correlation_heatmap(df: pd.DataFrame, method: str = 'pearson'):
        """Correlation heatmap"""
        corr = df.corr(method=method)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', 
                   cmap='coolwarm', center=0, ax=ax,
                   square=True, linewidths=0.5)
        
        ax.set_title(f'{method.capitalize()} Correlation Matrix')
        
        return fig
    
    @staticmethod
    def pair_plot(df: pd.DataFrame, columns: list, hue: str = None, 
                  sample_size: int = 1000):
        """Pair plot (sampled)"""
        if len(df) > sample_size:
            df_sample = df.sample(sample_size, random_state=42)
        else:
            df_sample = df
        
        g = sns.pairplot(df_sample[columns], hue=hue, diag_kind='kde',
                        plot_kws={'alpha': 0.5})
        
        return g.fig
    
    @staticmethod
    def hexbin_plot(df: pd.DataFrame, x: str, y: str):
        """Hexbin plot for large datasets"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        df.plot.hexbin(x=x, y=y, gridsize=30, cmap='YlOrRd', ax=ax)
        
        ax.set_title(f'Hexbin: {y} vs {x}')
        
        return fig
```

-----

## Correlation Analysis

```python
class CorrelationAnalyzer:
    """Comprehensive correlation analysis"""
    
    @staticmethod
    def correlation_matrix(df: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame:
        """Calculate correlation matrix"""
        return df.corr(method=method)
    
    @staticmethod
    def top_correlations(df: pd.DataFrame, threshold: float = 0.7) -> pd.DataFrame:
        """Find highly correlated pairs"""
        corr = df.corr()
        
        # Get upper triangle
        upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        
        # Stack and filter
        correlations = []
        for col in upper.columns:
            for idx in upper.index:
                val = upper.loc[idx, col]
                if pd.notna(val) and abs(val) >= threshold:
                    correlations.append({
                        'variable_1': idx,
                        'variable_2': col,
                        'correlation': val
                    })
        
        return pd.DataFrame(correlations).sort_values('correlation', 
                                                      key=abs, ascending=False)
    
    @staticmethod
    def correlation_with_target(df: pd.DataFrame, target: str, 
                               method: str = 'pearson') -> pd.DataFrame:
        """Correlations with target variable"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        correlations = []
        for col in numeric_cols:
            if col != target:
                corr, p_value = df[col].corr(df[target], method=method), \
                               stats.pearsonr(df[col].dropna(), df[target].dropna())[1]
                correlations.append({
                    'variable': col,
                    'correlation': corr,
                    'abs_correlation': abs(corr),
                    'p_value': p_value
                })
        
        return pd.DataFrame(correlations).sort_values('abs_correlation', 
                                                       ascending=False)
    
    @staticmethod
    def partial_correlation(df: pd.DataFrame, var1: str, var2: str,
                            control_vars: list) -> float:
        """Calculate partial correlation"""
        from sklearn.linear_model import LinearRegression
        
        # Residuals after controlling for other variables
        all_vars = [var1, var2] + control_vars
        X = df[all_vars].dropna()
        
        # Regress var1 on control vars
        model1 = LinearRegression().fit(X[control_vars], X[var1])
        resid1 = X[var1] - model1.predict(X[control_vars])
        
        # Regress var2 on control vars
        model2 = LinearRegression().fit(X[control_vars], X[var2])
        resid2 = X[var2] - model2.predict(X[control_vars])
        
        # Correlation of residuals
        return resid1.corr(resid2)
```

-----

## Feature Engineering Insights

```python
class FeatureEngineeringEDA:
    """EDA-driven feature engineering"""
    
    @staticmethod
    def suggest_features(df: pd.DataFrame) -> dict:
        """Suggest potential features based on EDA"""
        suggestions = {}
        
        for col in df.select_dtypes(include=[np.number]).columns:
            features = []
            
            # Check for datetime
            if any(dt in col.lower() for dt in ['date', 'time']):
                features.extend(['year', 'month', 'day', 'dayofweek', 'hour'])
            
            # Check for potential interactions
            if df[col].nunique() > 20:
                features.extend(['binned', 'log_transformed'])
            
            if df[col].min() < 0:
                features.append('shifted')
            
            if features:
                suggestions[col] = features
        
        return suggestions
    
    @staticmethod
    def create_bins(df: pd.DataFrame, column: str, n_bins: int = 5,
                   strategy: str = 'quantile') -> pd.DataFrame:
        """Create binned version of numeric column"""
        df = df.copy()
        
        if strategy == 'quantile':
            df[f'{column}_binned'] = pd.qcut(df[column], q=n_bins, 
                                            duplicates='drop')
        elif strategy == 'uniform':
            df[f'{column}_binned'] = pd.cut(df[column], bins=n_bins)
        
        return df
    
    @staticmethod
    def encode_cyclic(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Create cyclic encoding for periodic features"""
        df = df.copy()
        
        if column in df.columns:
            if 'month' in column.lower():
                df[f'{column}_sin'] = np.sin(2 * np.pi * df[column] / 12)
                df[f'{column}_cos'] = np.cos(2 * np.pi * df[column] / 12)
            elif 'day' in column.lower() or 'weekday' in column.lower():
                df[f'{column}_sin'] = np.sin(2 * np.pi * df[column] / 7)
                df[f'{column}_cos'] = np.cos(2 * np.pi * df[column] / 7)
            elif 'hour' in column.lower():
                df[f'{column}_sin'] = np.sin(2 * np.pi * df[column] / 24)
                df[f'{column}_cos'] = np.cos(2 * np.pi * df[column] / 24)
        
        return df
```

-----

## EDA Reporting

```python
class EDAReport:
    """Generate comprehensive EDA reports"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def generate_report(self) -> dict:
        """Generate full EDA report"""
        structure = DataStructureAnalyzer(self.df)
        
        report = {
            'title': 'Explatory Data Analysis Report',
            'overview': structure.overview(),
            'missing': structure.missing_summary().to_dict() if self.df.isnull().any().any() else {},
            'duplicates': structure.duplicate_summary(),
            'numerical_summary': NumericalStatistics.summary_statistics(self.df).to_dict(),
            'column_types': DataTypeAnalyzer.identify_column_types(self.df),
            'cardinality': structure.cardinality().to_dict()
        }
        
        # Add correlations
        numeric_df = self.df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 1:
            corr = numeric_df.corr()
            report['top_correlations'] = CorrelationAnalyzer.top_correlations(
                numeric_df, threshold=0.5).to_dict('records')
        
        return report
    
    def generate_html_report(self, output_path: str = 'eda_report.html'):
        """Generate HTML report"""
        # This would generate a comprehensive HTML report
        # Using pandas-profiling or sweetviz recommended
        pass
```
