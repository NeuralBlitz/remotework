-----
name: time-series
description: >
  Expert in time-series data analysis, forecasting, and processing. Use this skill 
  whenever working with temporal data including data ingestion, aggregation, windowing, 
  forecasting models, anomaly detection, visualization, and real-time stream processing. 
  Covers InfluxDB, TimescaleDB, Prometheus, custom implementations, and statistical/machine 
  learning approaches to temporal data analysis.
license: MIT
compatibility: opencode
metadata:
  audience: developers, data-engineers, data-scientists
  category: databases
  tags: [time-series, databases, monitoring, iot, analytics]

# Time Series Data Handling

Covers: **Data Modeling · Query Languages · Aggregation · Windowing · Forecasting · Anomaly Detection · Stream Processing · Visualization**

-----

## Time-Series Database Fundamentals

### Characteristics of Time-Series Data

Time-series data differs fundamentally from relational or document data:

- **Timestamped**: Every data point has an associated time
- **Append-only**: New data is typically added, rarely updated
- **Ordered by time**: Natural ordering is temporal
- **High volume**: Often generated continuously from sensors, metrics, applications
- **Retention policies**: Data often aggregated or deleted after time periods

### Data Modeling Patterns

```
# Tag-based model (InfluxDB-style)
measurement, tags timestamp value
cpu,host=server1,region=us-east 1706832000000000000 85.5

# Relational model
CREATE TABLE cpu_metrics (
    id BIGSERIAL PRIMARY KEY,
    host VARCHAR(50) NOT NULL,
    region VARCHAR(20) NOT NULL,
    value FLOAT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_cpu_timestamp ON cpu_metrics(timestamp);
CREATE INDEX idx_cpu_host_time ON cpu_metrics(host, timestamp);
```

### Key Design Considerations

| Aspect | Recommendation |
|--------|---------------|
| **Partitioning** | Partition by time (daily/monthly) for query performance |
| **Compression** | Use time-series compression algorithms ( Gorilla, COGS) |
| **Retention** | Define tiered retention (raw → aggregated → downsampled) |
| **Tags** | Keep cardinality low; avoid high-cardinality tag values |
| **Write patterns** | Batch writes for throughput; avoid random time writes |

-----

## Query Languages and Operations

### Time-Series Specific Functions

```sql
-- Time-weighted averages (prevent skew from irregular sampling)
SELECT time_weighted_mean(timestamp, value) 
FROM cpu_metrics 
WHERE host = 'server1' 
  AND timestamp > NOW() - INTERVAL '1 hour';

-- Gap filling (linear interpolation for missing data)
SELECT timestamp, 
       interpolate(value) 
FROM cpu_metrics 
WHERE host = 'server1'
FILL LINEAR;

-- Moving averages with various window sizes
SELECT timestamp, 
       value,
       AVG(value) OVER (ORDER BY timestamp ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as ma_5,
       AVG(value) OVER (ORDER BY timestamp ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) as ma_30
FROM cpu_metrics
WHERE host = 'server1';
```

### Aggregation Windows

| Window Type | Use Case | Example |
|-------------|----------|---------|
| **Tumbling** | Fixed, non-overlapping | 5-minute averages |
| **Hopping** | Overlapping windows | Every 1 minute, 5-minute window |
| **Session** | Activity-based | User session duration |
| **Calendar** | Aligned to calendar | Hourly, daily aggregations |

```python
# Python: Time-windowed aggregation
from collections import deque
from datetime import datetime, timedelta

class TimeWindowAggregator:
    def __init__(self, window_seconds: int):
        self.window = timedelta(seconds=window_seconds)
        self.data = deque()
    
    def add(self, timestamp: datetime, value: float):
        cutoff = timestamp - self.window
        # Remove expired data
        while self.data and self.data[0][0] < cutoff:
            self.data.popleft()
        self.data.append((timestamp, value))
    
    def aggregate(self, agg_type: str = 'mean'):
        if not self.data:
            return None
        values = [v for _, v in self.data]
        if agg_type == 'mean':
            return sum(values) / len(values)
        elif agg_type == 'min':
            return min(values)
        elif agg_type == 'max':
            return max(values)
        elif agg_type == 'sum':
            return sum(values)
        return None
```

-----

## Forecasting Methods

### Statistical Forecasting

```python
import numpy as np
from scipy import stats

class SimpleExponentialSmoothing:
    """Simple exponential smoothing for level-only series"""
    
    def __init__(self, alpha: float = 0.3):
        self.alpha = alpha
        self.level = None
    
    def fit(self, values: list):
        self.level = values[0]
        for v in values[1:]:
            self.level = self.alpha * v + (1 - self.alpha) * self.level
        return self
    
    def forecast(self, horizon: int) -> list:
        return [self.level] * horizon

class HoltWinters:
    """Holt-Winters with trend and seasonality"""
    
    def __init__(self, alpha: float = 0.3, beta: float = 0.1, 
                 gamma: float = 0.1, seasonal_period: int = 12):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.seasonal_period = seasonal_period
    
    def fit(self, values: list):
        n = len(values)
        # Initialize level, trend, seasonal components
        self.level = sum(values[:self.seasonal_period]) / self.seasonal_period
        self.trend = (sum(values[self.seasonal_period:2*self.seasonal_period]) - 
                      sum(values[:self.seasonal_period])) / self.seasonal_period
        self.seasonal = [values[i] - self.level for i in range(self.seasonal_period)]
        
        # Fit model
        for t in range(self.seasonal_period, n):
            last_level = self.level
            self.level = self.alpha * (values[t] - self.seasonal[t % self.seasonal_period]) + \
                        (1 - self.alpha) * (last_level + self.trend)
            self.trend = self.beta * (self.level - last_level) + \
                        (1 - self.beta) * self.trend
            self.seasonal[t % self.seasonal_period] = \
                self.gamma * (values[t] - self.level) + \
                (1 - self.gamma) * self.seasonal[t % self.seasonal_period]
        return self
    
    def forecast(self, horizon: int) -> list:
        forecasts = []
        for h in range(1, horizon + 1):
            seasonal_idx = (self.seasonal_period - 1 + h) % self.seasonal_period
            forecast = self.level + h * self.trend + self.seasonal[seasonal_idx]
            forecasts.append(forecast)
        return forecasts

# Usage
data = [100, 112, 108, 120, 125, 130, 128, 135, 140, 138, 145, 150]
model = HoltWinters(alpha=0.3, beta=0.1, gamma=0.2, seasonal_period=4)
model.fit(data)
predictions = model.forecast(horizon=4)
print(f"Forecast: {predictions}")
```

### ARIMA Models

```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

def check_stationarity(series):
    """Augmented Dickey-Fuller test"""
    result = adfuller(series.dropna())
    return {
        'statistic': result[0],
        'p_value': result[1],
        'stationary': result[1] < 0.05
    }

def fit_arima(series, order=(1,1,1)):
    """Fit ARIMA model"""
    model = ARIMA(series, order=order)
    fitted = model.fit()
    return fitted

def auto_arima(series, max_p=5, max_d=2, max_q=5):
    """Automatic ARIMA order selection using AIC"""
    best_aic = float('inf')
    best_order = None
    best_model = None
    
    for p in range(max_p + 1):
        for d in range(max_d + 1):
            for q in range(max_q + 1):
                try:
                    model = ARIMA(series, order=(p, d, q))
                    fitted = model.fit()
                    if fitted.aic < best_aic:
                        best_aic = fitted.aic
                        best_order = (p, d, q)
                        best_model = fitted
                except:
                    continue
    
    return best_model, best_order
```

-----

## Anomaly Detection

### Statistical Methods

```python
import numpy as np
from scipy import stats

class ZScoreDetector:
    """Detect anomalies using z-score thresholding"""
    
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold
        self.mean = None
        self.std = None
    
    def fit(self, values: list):
        self.mean = np.mean(values)
        self.std = np.std(values)
        return self
    
    def detect(self, value: float) -> dict:
        z_score = (value - self.mean) / self.std if self.std > 0 else 0
        return {
            'anomaly': abs(z_score) > self.threshold,
            'z_score': z_score,
            'value': value
        }

class IQRDetector:
    """Interquartile range based anomaly detection"""
    
    def __init__(self, multiplier: float = 1.5):
        self.multiplier = multiplier
    
    def fit(self, values: list):
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        self.iqr = q3 - q1
        self.lower = q1 - self.multiplier * self.iqr
        self.upper = q3 + self.multiplier * self.iqr
        return self
    
    def detect(self, value: float) -> dict:
        return {
            'anomaly': value < self.lower or value > self.upper,
            'value': value,
            'bounds': (self.lower, self.upper)
        }

class MovingAverageDetector:
    """Detect anomalies using deviation from moving average"""
    
    def __init__(self, window: int = 10, threshold: float = 2.0):
        self.window = window
        self.threshold = threshold
    
    def detect_batch(self, values: list) -> list:
        results = []
        for i in range(len(values)):
            if i < self.window:
                results.append({'anomaly': False, 'value': values[i]})
                continue
            
            window_vals = values[i-self.window:i]
            mean = np.mean(window_vals)
            std = np.std(window_vals)
            z = (values[i] - mean) / std if std > 0 else 0
            
            results.append({
                'anomaly': abs(z) > self.threshold,
                'z_score': z,
                'value': values[i]
            })
        
        return results
```

### Isolation Forest for Multivariate

```python
from sklearn.ensemble import IsolationForest
import numpy as np

class TimeSeriesAnomalyDetector:
    def __init__(self, contamination: float = 0.1, n_estimators: int = 100):
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.model = None
        self.scaler = None
    
    def _create_features(self, series: np.ndarray, window: int = 5) -> np.ndarray:
        """Create features from time series for multivariate detection"""
        features = []
        for i in range(window, len(series)):
            window_data = series[i-window:i]
            features.append([
                np.mean(window_data),
                np.std(window_data),
                np.min(window_data),
                np.max(window_data),
                series[i],  # Current value
                series[i] - np.mean(window_data),  # Difference from mean
            ])
        return np.array(features)
    
    def fit(self, values: list):
        from sklearn.preprocessing import StandardScaler
        
        series = np.array(values)
        X = self._create_features(series)
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = IsolationForest(
            contamination=self.contamination,
            n_estimators=self.n_estimators,
            random_state=42
        )
        self.model.fit(X_scaled)
        return self
    
    def predict(self, values: list) -> list:
        series = np.array(values)
        X = self._create_features(series)
        X_scaled = self.scaler.transform(X)
        
        predictions = self.model.predict(X_scaled)
        scores = self.model.score_samples(X_scaled)
        
        return [
            {'anomaly': pred == -1, 'score': score, 'index': i + 5}
            for i, (pred, score) in enumerate(zip(predictions, scores))
        ]
```

-----

## Stream Processing

### Real-Time Aggregation

```python
from collections import deque
from datetime import datetime
import time

class SlidingWindowCounter:
    """Count events in sliding window"""
    
    def __init__(self, window_seconds: int):
        self.window = window_seconds
        self.events = deque()
    
    def add(self, event: dict):
        self.events.append({
            'timestamp': datetime.now(),
            'data': event
        })
        self._cleanup()
    
    def _cleanup(self):
        cutoff = datetime.now().timestamp() - self.window
        while self.events and self.events[0]['timestamp'].timestamp() < cutoff:
            self.events.popleft()
    
    def count(self) -> int:
        self._cleanup()
        return len(self.events)

class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, rate: int, per_seconds: int):
        self.rate = rate
        self.per_seconds = per_seconds
        self.tokens = rate
        self.last_update = time.time()
    
    def allow(self) -> bool:
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.rate, self.tokens + elapsed * (self.rate / self.per_seconds))
        self.last_update = now
        
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

class StreamingPercentile:
    """Compute percentiles on streaming data (t-digest)"""
    
    def __init__(self, delta: float = 0.01):
        self.delta = delta
        self.centroids = []
    
    def add(self, value: float):
        if not self.centroids:
            self.centroids = [{'mean': value, 'weight': 1}]
            return
        
        # Find nearest centroid
        nearest = min(self.centroids, key=lambda c: abs(c['mean'] - value))
        nearest['weight'] += 1
        
        # Merge if weight too high
        self._maybe_merge()
    
    def _maybe_merge(self):
        # Simplified merge logic
        self.centroids.sort(key=lambda c: c['mean'])
    
    def percentile(self, q: float) -> float:
        if not self.centroids:
            return 0
        total_weight = sum(c['weight'] for c in self.centroids)
        threshold = q * total_weight
        
        cumulative = 0
        for c in self.centroids:
            cumulative += c['weight']
            if cumulative >= threshold:
                return c['mean']
        return self.centroids[-1]['mean']
```

-----

## Visualization and Dashboards

### Time-Series Visualization Best Practices

| Principle | Implementation |
|-----------|----------------|
| **Show trend, not just points** | Use line charts, connect points |
| **Avoid misleading scales** | Start y-axis at zero or show break |
| **Highlight anomalies** | Use color or markers for anomalies |
| **Enable zoom/pan** | Allow exploration of time ranges |
| **Show uncertainty** | Confidence intervals for forecasts |
| **Multiple resolutions** | Show raw + smoothed on same chart |

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_time_series_with_forecast(dates, values, forecast_dates, forecast_values,
                                    confidence_lower, confidence_upper):
    """Create publication-quality time series plot"""
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot historical data
    ax.plot(dates, values, 'b-', linewidth=1.5, label='Historical', alpha=0.8)
    
    # Plot forecast
    ax.plot(forecast_dates, forecast_values, 'r--', linewidth=2, label='Forecast')
    
    # Confidence interval
    ax.fill_between(forecast_dates, confidence_lower, confidence_upper, 
                    color='red', alpha=0.2, label='95% CI')
    
    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    ax.set_title('Time Series Forecast', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig
```

-----

## Common Patterns and Anti-Patterns

### Common Mistakes to Avoid

- **Ignoring timezone handling** — Always use timezone-aware timestamps
- **Not handling missing data** — Decide on gap-filling strategy upfront
- **Using mean for highly variable data** — Consider median or time-weighted averages
- **Ignoring seasonality** — Account for periodic patterns in forecasting
- **Storing raw data forever** — Implement data lifecycle management
- **High cardinality tags** — Avoid unique tag values that explode index size
- **Random time writes** — Write time-series data in time order for compression

### Recommended Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐
│  Data       │───▶│ Time-Series  │───▶│  Analytics     │
│  Sources    │    │  Database    │    │  & Dashboards  │
└─────────────┘    └──────────────┘    └────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Retention   │
                  │  & Downsample│
                  └──────────────┘
```

-----

## Database-Specific Notes

### InfluxDB

- Use line protocol for high-throughput writes
- Prefer schema-on-write (tag-based)
- Use Continuous Queries for downsampling
- Leverage Flux for complex transformations

### TimescaleDB

- Hypertable partitions by time automatically
- Use chunk_interval configuration carefully
- Comfortable with PostgreSQL ecosystem
- Great for relational + time-series hybrid

### Prometheus

- Pull-based model by default
- 4-week default retention (configurable)
- Excellent for metrics and monitoring
- Use recording rules for complex queries
