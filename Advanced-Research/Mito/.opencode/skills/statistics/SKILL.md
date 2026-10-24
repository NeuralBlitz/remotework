-----
name: statistics
description: >
  Expert in statistical analysis, hypothesis testing, probability distributions, 
  regression analysis, and statistical inference. Use this skill for analyzing data, 
  designing experiments, interpreting results, and making data-driven decisions. 
  Covers descriptive statistics, inferential statistics, Bayesian analysis, 
  non-parametric methods, and statistical modeling.
license: MIT
compatibility: opencode
metadata:
  audience: data-science
  category: data-science
  tags: [statistics, hypothesis-testing, probability, regression, bayesian]

# Statistical Analysis

Covers: **Descriptive Statistics · Probability Distributions · Hypothesis Testing · Regression · Bayesian Analysis · Non-Parametric Methods · Experimental Design**

-----

## Descriptive Statistics

### Summary Statistics

```python
import numpy as np
from scipy import stats
from typing import List, Dict, Any
import math

class DescriptiveStatistics:
    """Calculate descriptive statistics"""
    
    def __init__(self, data: List[float]):
        self.data = np.array(data)
        self.n = len(self.data)
    
    def mean(self) -> float:
        return np.mean(self.data)
    
    def median(self) -> float:
        return np.median(self.data)
    
    def mode(self) -> float:
        """Most frequent value"""
        result = stats.mode(self.data, keepdims=True)
        return result.mode[0]
    
    def variance(self, population: bool = False) -> float:
        if population:
            return np.var(self.data)
        return np.var(self.data, ddof=1)
    
    def standard_deviation(self, population: bool = False) -> float:
        if population:
            return np.std(self.data)
        return np.std(self.data, ddof=1)
    
    def coefficient_of_variation(self) -> float:
        """CV = (SD / Mean) * 100%"""
        return (self.standard_deviation() / self.mean()) * 100
    
    def skewness(self) -> float:
        """Measure of asymmetry"""
        return stats.skew(self.data)
    
    def kurtosis(self) -> float:
        """Measure of tail heaviness (excess kurtosis)"""
        return stats.kurtosis(self.data)
    
    def range_(self) -> float:
        return np.max(self.data) - np.min(self.data)
    
    def interquartile_range(self) -> float:
        q1 = np.percentile(self.data, 25)
        q3 = np.percentile(self.data, 75)
        return q3 - q1
    
    def quartiles(self) -> Dict[str, float]:
        return {
            'q1': np.percentile(self.data, 25),
            'q2': np.percentile(self.data, 50),
            'q3': np.percentile(self.data, 75)
        }
    
    def five_number_summary(self) -> Dict[str, float]:
        return {
            'min': np.min(self.data),
            'q1': np.percentile(self.data, 25),
            'median': np.median(self.data),
            'q3': np.percentile(self.data, 75),
            'max': np.max(self.data)
        }
    
    def summary(self) -> Dict[str, float]:
        return {
            'n': self.n,
            'mean': self.mean(),
            'std': self.standard_deviation(),
            'min': np.min(self.data),
            'q1': np.percentile(self.data, 25),
            'median': self.median(),
            'q3': np.percentile(self.data, 75),
            'max': np.max(self.data),
            'range': self.range_(),
            'iqr': self.interquartile_range(),
            'cv': self.coefficient_of_variation(),
            'skewness': self.skewness(),
            'kurtosis': self.kurtosis()
        }


class CorrelationAnalysis:
    """Correlation analysis methods"""
    
    @staticmethod
    def pearson_correlation(x: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Pearson correlation coefficient"""
        r, p = stats.pearsonr(x, y)
        return {'r': r, 'p_value': p}
    
    @staticmethod
    def spearman_correlation(x: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Spearman rank correlation"""
        r, p = stats.spearmanr(x, y)
        return {'rho': r, 'p_value': p}
    
    @staticmethod
    def kendall_correlation(x: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Kendall tau correlation"""
        tau, p = stats.kendalltau(x, y)
        return {'tau': tau, 'p_value': p}
    
    @staticmethod
    def correlation_matrix(df) -> np.ndarray:
        """Correlation matrix for DataFrame"""
        return df.corr().values
```

### Data Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

class StatisticsVisualizer:
    """Visualization for statistical analysis"""
    
    @staticmethod
    def histogram_with_stats(data: np.ndarray, bins: int = 30):
        """Histogram with mean and median lines"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(data, bins=bins, edgecolor='black', alpha=0.7)
        
        mean = np.mean(data)
        median = np.median(data)
        
        ax.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean:.2f}')
        ax.axvline(median, color='green', linestyle='--', linewidth=2, label=f'Median: {median:.2f}')
        
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.legend()
        
        return fig
    
    @staticmethod
    def box_plot_groups(groups: Dict[str, np.ndarray]):
        """Box plot for multiple groups"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        data = list(groups.values())
        labels = list(groups.keys())
        
        bp = ax.boxplot(data, labels=labels, patch_artist=True)
        
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
        
        ax.set_xlabel('Group')
        ax.set_ylabel('Value')
        ax.grid(True, alpha=0.3)
        
        return fig
    
    @staticmethod
    def qq_plot(data: np.ndarray):
        """Q-Q plot for normality assessment"""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        stats.probplot(data, dist="norm", plot=ax)
        ax.set_title('Q-Q Plot')
        
        return fig
    
    @staticmethod
    def heatmap_correlation(corr_matrix: np.ndarray, labels: List[str]):
        """Correlation heatmap"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', 
                   center=0, xticklabels=labels, yticklabels=labels, ax=ax)
        
        return fig
```

-----

## Probability Distributions

### Discrete Distributions

```python
class DiscreteDistributions:
    """Discrete probability distributions"""
    
    @staticmethod
    def binomial_pmf(n: int, p: float, k: int) -> float:
        """Binomial probability mass function"""
        return stats.binom.pmf(k, n, p)
    
    @staticmethod
    def binomial_cdf(n: int, p: float, k: int) -> float:
        """Binomial cumulative distribution"""
        return stats.binom.cdf(k, n, p)
    
    @staticmethod
    def poisson_pmf(lambda_: float, k: int) -> float:
        """Poisson probability mass function"""
        return stats.poisson.pmf(k, lambda_)
    
    @staticmethod
    def poisson_cdf(lambda_: float, k: int) -> float:
        """Poisson cumulative distribution"""
        return stats.poisson.cdf(k, lambda_)
    
    @staticmethod
    def geometric_pmf(p: float, k: int) -> float:
        """Geometric probability (k failures before first success)"""
        return stats.geom.pmf(k, p)
    
    @staticmethod
    def negative_binomial_pmf(r: int, p: float, k: int) -> float:
        """Negative binomial probability"""
        return stats.nbinom.pmf(k, r, p)


class ContinuousDistributions:
    """Continuous probability distributions"""
    
    @staticmethod
    def normal_pdf(x: float, mu: float, sigma: float) -> float:
        """Normal probability density"""
        return stats.norm.pdf(x, loc=mu, scale=sigma)
    
    @staticmethod
    def normal_cdf(x: float, mu: float, sigma: float) -> float:
        """Normal cumulative distribution"""
        return stats.norm.cdf(x, loc=mu, scale=sigma)
    
    @staticmethod
    def exponential_pdf(x: float, lambda_: float) -> float:
        """Exponential probability density"""
        return stats.expon.pdf(x, scale=1/lambda_)
    
    @staticmethod
    def t_pdf(x: float, df: int) -> float:
        """Student's t probability density"""
        return stats.t.pdf(x, df)
    
    @staticmethod
    def chi2_pdf(x: float, df: int) -> float:
        """Chi-squared probability density"""
        return stats.chi2.pdf(x, df)
    
    @staticmethod
    def f_pdf(x: float, dfn: int, dfd: int) -> float:
        """F probability density"""
        return stats.f.pdf(x, dfn, dfd)
    
    @staticmethod
    def uniform_pdf(x: float, a: float, b: float) -> float:
        """Uniform probability density"""
        return stats.uniform.pdf(x, loc=a, scale=b-a)


class DistributionFitting:
    """Fit distributions to data"""
    
    @staticmethod
    def fit_normal(data: np.ndarray) -> Dict[str, float]:
        """Fit normal distribution"""
        mu, sigma = stats.norm.fit(data)
        return {'mu': mu, 'sigma': sigma}
    
    @staticmethod
    def fit_exponential(data: np.ndarray) -> Dict[str, float]:
        """Fit exponential distribution"""
        loc, scale = stats.expon.fit(data)
        return {'lambda': 1/scale}
    
    @staticmethod
    def fit_poisson(data: np.ndarray) -> Dict[str, float]:
        """Fit Poisson distribution (estimate lambda)"""
        return {'lambda': np.mean(data)}
    
    @staticmethod
    def normality_test(data: np.ndarray) -> Dict[str, float]:
        """Test if data follows normal distribution"""
        stat, p = stats.shapiro(data)
        return {'shapiro_stat': stat, 'shapiro_p': p}
```

-----

## Hypothesis Testing

### Parametric Tests

```python
class ParametricTests:
    """Parametric hypothesis tests"""
    
    @staticmethod
    def one_sample_t_test(data: np.ndarray, mu0: float) -> Dict[str, Any]:
        """One-sample t-test"""
        t_stat, p_value = stats.ttest_1samp(data, mu0)
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'ci_95': stats.t.interval(0.95, len(data)-1, 
                                     loc=np.mean(data), 
                                     scale=stats.sem(data))
        }
    
    @staticmethod
    def paired_t_test(data1: np.ndarray, data2: np.ndarray) -> Dict[str, Any]:
        """Paired t-test"""
        t_stat, p_value = stats.ttest_rel(data1, data2)
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'mean_difference': np.mean(data1 - data2)
        }
    
    @staticmethod
    def independent_t_test(data1: np.ndarray, data2: np.ndarray, 
                          equal_var: bool = True) -> Dict[str, Any]:
        """Independent samples t-test"""
        t_stat, p_value = stats.ttest_ind(data1, data2, equal_var=equal_var)
        
        # Cohen's d effect size
        pooled_std = np.sqrt(((len(data1)-1)*np.std(data1, ddof=1)**2 + 
                             (len(data2)-1)*np.std(data2, ddof=1)**2) / 
                            (len(data1)+len(data2)-2))
        cohens_d = (np.mean(data1) - np.mean(data2)) / pooled_std
        
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'cohens_d': cohens_d,
            'effect_size': 'small' if abs(cohens_d) < 0.5 else \
                          'medium' if abs(cohens_d) < 0.8 else 'large'
        }
    
    @staticmethod
    def one_way_anova(*groups: np.ndarray) -> Dict[str, Any]:
        """One-way ANOVA"""
        f_stat, p_value = stats.f_oneway(*groups)
        
        # Effect size (eta-squared)
        all_data = np.concatenate(groups)
        grand_mean = np.mean(all_data)
        ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
        ss_total = np.sum((all_data - grand_mean)**2)
        eta_squared = ss_between / ss_total
        
        return {
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'eta_squared': eta_squared
        }
    
    @staticmethod
    def two_way_anova(data: np.ndarray, 
                     factor_a: np.ndarray, 
                     factor_b: np.ndarray) -> Dict[str, Any]:
        """Two-way ANOVA (simplified)"""
        # Using scipy for one-way; for two-way use statsmodels
        import statsmodels.api as sm
        from statsmodels.formula.api import ols
        
        # Create DataFrame and run ANOVA
        # This is a placeholder - use statsmodels for full ANOVA
        return {'message': 'Use statsmodels for full two-way ANOVA'}


class CorrelationTests:
    """Correlation hypothesis tests"""
    
    @staticmethod
    def test_correlation(r: float, n: int, alpha: float = 0.05) -> Dict[str, Any]:
        """Test if correlation is significant"""
        # t-test for correlation
        t_stat = r * np.sqrt((n-2) / (1-r**2))
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n-2))
        
        # Confidence interval
        z = np.arctanh(r)
        se = 1 / np.sqrt(n-3)
        ci_low = np.tanh(z - stats.norm.ppf(1-alpha/2) * se)
        ci_high = np.tanh(z + stats.norm.ppf(1-alpha/2) * se)
        
        return {
            'r': r,
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < alpha,
            'ci_95': (ci_low, ci_high)
        }
```

### Non-Parametric Tests

```python
class NonParametricTests:
    """Non-parametric hypothesis tests"""
    
    @staticmethod
    def mann_whitney_u(data1: np.ndarray, data2: np.ndarray) -> Dict[str, Any]:
        """Mann-Whitney U test (Wilcoxon rank-sum)"""
        statistic, p_value = stats.mannwhitneyu(data1, data2)
        
        # Effect size (rank-biserial correlation)
        n1, n2 = len(data1), len(data2)
        r = 1 - (2*statistic) / (n1*n2)
        
        return {
            'u_statistic': statistic,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'effect_size_r': r
        }
    
    @staticmethod
    def wilcoxon_signed_rank(data1: np.ndarray, data2: np.ndarray) -> Dict[str, Any]:
        """Wilcoxon signed-rank test (paired)"""
        diff = data1 - data2
        statistic, p_value = stats.wilcoxon(diff)
        
        return {
            'w_statistic': statistic,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    @staticmethod
    def kruskal_wallis(*groups: np.ndarray) -> Dict[str, Any]:
        """Kruskal-Wallis H test (non-parametric ANOVA)"""
        h_stat, p_value = stats.kruskal(*groups)
        
        return {
            'h_statistic': h_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    @staticmethod
    def chi_square_test(observed: np.ndarray, 
                       expected: np.ndarray = None) -> Dict[str, Any]:
        """Chi-square test"""
        if expected is None:
            # Test of independence
            chi2, p_value, dof, expected = stats.chi2_contingency(observed)
        else:
            # Goodness of fit
            chi2, p_value = stats.chisquare(observed, expected)
            dof = len(observed) - 1
        
        # Effect size (Cramér's V)
        n = np.sum(observed)
        min_dim = min(observed.shape[0], observed.shape[1]) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
        
        return {
            'chi2_statistic': chi2,
            'p_value': p_value,
            'dof': dof,
            'significant': p_value < 0.05,
            'cramers_v': cramers_v
        }
    
    @staticmethod
    def kolmogorov_smirnov(data: np.ndarray, 
                          distribution: str = 'norm') -> Dict[str, Any]:
        """Kolmogorov-Smirnov test"""
        if distribution == 'norm':
            d_stat, p_value = stats.kstest(data, 'norm', 
                                          args=(np.mean(data), np.std(data)))
        else:
            d_stat, p_value = stats.kstest(data, distribution)
        
        return {
            'd_statistic': d_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
```

### Chi-Square Tests

```python
class ChiSquareAnalysis:
    """Chi-square test analysis"""
    
    @staticmethod
    def test_independence(contingency_table: np.ndarray) -> Dict[str, Any]:
        """Test independence in contingency table"""
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        # Cramér's V for effect size
        n = np.sum(contingency_table)
        min_dim = min(contingency_table.shape[0], contingency_table.shape[1]) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
        
        return {
            'chi2': chi2,
            'p_value': p_value,
            'dof': dof,
            'expected': expected,
            'cramers_v': cramers_v,
            'interpretation': 'Dependent' if p_value < 0.05 else 'Independent'
        }
    
    @staticmethod
    def goodness_of_fit(observed: np.ndarray, 
                       expected_probs: np.ndarray) -> Dict[str, Any]:
        """Test if observed frequencies match expected"""
        expected = expected_probs * np.sum(observed)
        
        chi2, p_value = stats.chisquare(observed, expected)
        dof = len(observed) - 1
        
        return {
            'chi2': chi2,
            'p_value': p_value,
            'dof': dof,
            'significant': p_value < 0.05
        }
```

-----

## Regression Analysis

### Simple Linear Regression

```python
class SimpleLinearRegression:
    """Simple linear regression: y = β0 + β1*x + ε"""
    
    def __init__(self):
        self.beta0 = None  # Intercept
        self.beta1 = None  # Slope
        self.r_squared = None
        self.residuals = None
    
    def fit(self, x: np.ndarray, y: np.ndarray):
        n = len(y)
        
        # Calculate means
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        # Calculate slope and intercept
        self.beta1 = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean)**2)
        self.beta0 = y_mean - self.beta1 * x_mean
        
        # Predictions and residuals
        y_pred = self.beta0 + self.beta1 * x
        self.residuals = y - y_pred
        
        # R-squared
        ss_res = np.sum(self.residuals**2)
        ss_tot = np.sum((y - y_mean)**2)
        self.r_squared = 1 - (ss_res / ss_tot)
        
        return self
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.beta0 + self.beta1 * x
    
    def coefficient_of_determination(self) -> float:
        return self.r_squared
    
    def standard_errors(self, x: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Calculate standard errors of coefficients"""
        n = len(y)
        mse = np.sum(self.residuals**2) / (n - 2)
        
        se_beta1 = np.sqrt(mse / np.sum((x - np.mean(x))**2))
        se_beta0 = np.sqrt(mse * (1/n + np.mean(x)**2 / np.sum((x - np.mean(x))**2)))
        
        return {'se_beta0': se_beta0, 'se_beta1': se_beta1}
    
    def confidence_intervals(self, x: np.ndarray, y: np.ndarray, 
                            alpha: float = 0.05) -> Dict[str, tuple]:
        """Calculate confidence intervals"""
        n = len(y)
        df = n - 2
        se = self.standard_errors(x, y)
        
        t_critical = stats.t.ppf(1 - alpha/2, df)
        
        ci_beta0 = (self.beta0 - t_critical * se['se_beta0'],
                   self.beta0 + t_critical * se['se_beta0'])
        ci_beta1 = (self.beta1 - t_critical * se['se_beta1'],
                   self.beta1 + t_critical * se['se_beta1'])
        
        return {'beta0': ci_beta0, 'beta1': ci_beta1}
```

### Multiple Linear Regression

```python
class MultipleLinearRegression:
    """Multiple linear regression: y = Xβ + ε"""
    
    def __init__(self):
        self.coefficients = None
        self.r_squared = None
        self.adj_r_squared = None
        self.residuals = None
    
    def fit(self, X: np.ndarray, y: np.ndarray, add_intercept: bool = True):
        if add_intercept:
            X = np.column_stack([np.ones(len(X)), X])
        
        # OLS: β = (X'X)^(-1) X'y
        XtX_inv = np.linalg.inv(X.T @ X)
        self.coefficients = XtX_inv @ X.T @ y
        
        # Predictions and residuals
        y_pred = X @ self.coefficients
        self.residuals = y - y_pred
        
        # R-squared
        ss_res = np.sum(self.residuals**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        self.r_squared = 1 - (ss_res / ss_tot)
        
        # Adjusted R-squared
        n = len(y)
        p = X.shape[1] - 1  # Number of predictors
        self.adj_r_squared = 1 - (1 - self.r_squared) * (n - 1) / (n - p - 1)
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        if len(X.shape) == 1:
            X = X.reshape(1, -1)
        X = np.column_stack([np.ones(len(X)), X])
        return X @ self.coefficients
    
    def summary(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """Generate regression summary"""
        n = len(y)
        p = len(self.coefficients) - 1
        
        # Standard errors
        mse = np.sum(self.residuals**2) / (n - p - 1)
        var_coef = mse * np.linalg.inv(X.T @ X)
        se = np.sqrt(np.diag(var_coef))
        
        # t-statistics and p-values
        t_stats = self.coefficients / se
        p_values = [2 * (1 - stats.t.cdf(abs(t), n-p-1)) for t in t_stats]
        
        return {
            'coefficients': self.coefficients,
            'std_errors': se,
            't_statistics': t_stats,
            'p_values': p_values,
            'r_squared': self.r_squared,
            'adj_r_squared': self.adj_r_squared,
            'mse': mse,
            'n': n,
            'p': p
        }
```

### Logistic Regression

```python
class LogisticRegression:
    """Binary logistic regression"""
    
    def __init__(self, learning_rate: float = 0.01, n_iterations: int = 1000):
        self.lr = learning_rate
        self.n_iter = n_iterations
        self.weights = None
        self.bias = None
    
    def _sigmoid(self, z: np.ndarray) -> np.ndarray:
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-z))
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        n_samples, n_features = X.shape
        
        # Initialize weights
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        # Gradient descent
        for _ in range(self.n_iter):
            linear = X @ self.weights + self.bias
            predictions = self._sigmoid(linear)
            
            # Gradients
            dw = (1/n_samples) * X.T @ (predictions - y)
            db = (1/n_samples) * np.sum(predictions - y)
            
            # Update
            self.weights -= self.lr * dw
            self.bias -= self.lr * db
        
        return self
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        linear = X @ self.weights + self.bias
        return self._sigmoid(linear)
    
    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(X) >= threshold).astype(int)
    
    def accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        predictions = self.predict(X)
        return np.mean(predictions == y)
```

-----

## Bayesian Analysis

### Bayesian Inference

```python
class BayesianAnalysis:
    """Bayesian statistical analysis"""
    
    @staticmethod
    def beta_posterior(alpha_prior: float, beta_prior: float,
                      successes: int, failures: int) -> Dict[str, float]:
        """Beta-Binomial posterior"""
        alpha_post = alpha_prior + successes
        beta_post = beta_prior + failures
        
        # Posterior mean
        mean_post = alpha_post / (alpha_post + beta_post)
        
        # Posterior variance
        var_post = (alpha_post * beta_post) / \
                  ((alpha_post + beta_post)**2 * (alpha_post + beta_post + 1))
        
        return {
            'alpha_posterior': alpha_post,
            'beta_posterior': beta_post,
            'mean': mean_post,
            'variance': var_post,
            'std': np.sqrt(var_post)
        }
    
    @staticmethod
    def normal_posterior(mu_prior: float, sigma_prior: float,
                        mu_likelihood: float, sigma_likelihood: float,
                        n_obs: int, sample_mean: float) -> Dict[str, float]:
        """Normal-Normal posterior (known variance)"""
        # Posterior precision
        precision_prior = 1 / sigma_prior**2
        precision_likelihood = n_obs / sigma_likelihood**2
        
        # Posterior mean (precision-weighted)
        mu_post = ((precision_prior * mu_prior + 
                   precision_likelihood * sample_mean) / 
                  (precision_prior + precision_likelihood))
        
        # Posterior variance
        sigma_post = np.sqrt(1 / (precision_prior + precision_likelihood))
        
        return {
            'mu_posterior': mu_post,
            'sigma_posterior': sigma_post,
            'ci_95': (mu_post - 1.96*sigma_post, mu_post + 1.96*sigma_post)
        }
    
    @staticmethod
    def credible_interval(alpha_post: float, beta_post: float,
                         cred_mass: float = 0.95) -> tuple:
        """Calculate credible interval for Beta posterior"""
        return stats.beta.ppf((1 - cred_mass)/2, alpha_post, beta_post), \
               stats.beta.ppf((1 + cred_mass)/2, alpha_post, beta_post)
```

### Bayesian A/B Testing

```python
class BayesianABTest:
    """Bayesian A/B testing"""
    
    def __init__(self, alpha_prior: float = 1, beta_prior: float = 1):
        self.alpha_prior = alpha_prior
        self.beta_prior = beta_prior
    
    def update(self, successes: int, failures: int):
        """Update posterior with new data"""
        self.alpha_posterior = self.alpha_prior + successes
        self.beta_posterior = self.beta_prior + failures
    
    def probability_a_beats_b(self, alpha_b: float, beta_b: float,
                             n_samples: int = 10000) -> float:
        """P(A > B) using Monte Carlo"""
        samples_a = np.random.beta(self.alpha_posterior, self.beta_posterior, 
                                   n_samples)
        samples_b = np.random.beta(alpha_b, beta_b, n_samples)
        
        return np.mean(samples_a > samples_b)
    
    def expected_loss(self, alpha_b: float, beta_b: float,
                     n_samples: int = 10000) -> float:
        """Expected loss of choosing A over B"""
        samples_a = np.random.beta(self.alpha_posterior, self.beta_posterior, 
                                   n_samples)
        samples_b = np.random.beta(alpha_b, beta_b, n_samples)
        
        return np.mean(np.maximum(samples_b - samples_a, 0))
```

-----

## Power Analysis

```python
class PowerAnalysis:
    """Statistical power analysis"""
    
    @staticmethod
    def sample_size_ttest(effect_size: float, alpha: float = 0.05, 
                         power: float = 0.8) -> int:
        """Calculate sample size for t-test"""
        # Using normal approximation
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
        return int(np.ceil(n))
    
    @staticmethod
    def power_ttest(n: int, effect_size: float, alpha: float = 0.05) -> float:
        """Calculate power for t-test"""
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = effect_size * np.sqrt(n/2) - z_alpha
        
        return stats.norm.cdf(z_beta)
    
    @staticmethod
    def effect_size_from_difference(mean1: float, mean2: float, 
                                    pooled_std: float) -> float:
        """Cohen's d effect size"""
        return abs(mean1 - mean2) / pooled_std
    
    @staticmethod
    def minimum_detectable_effect(alpha: float, power: float, n: int) -> float:
        """Minimum detectable effect size"""
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        return (z_alpha + z_beta) * np.sqrt(2 / n)
```
