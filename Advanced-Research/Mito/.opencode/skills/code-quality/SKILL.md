---
name: code-quality
description: >
  Expert guidance on code quality metrics and improvement strategies. Use for: measuring code 
  quality, identifying code smells, implementing quality gates, static analysis, tracking 
  technical debt, improving code maintainability, setting quality standards, automated testing, 
  and code review practices.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: code-quality
  tags: [code-quality, static-analysis, technical-debt, testing]
---

# Code Quality — Implementation Guide

Covers: **Metrics · Static Analysis · Testing · Technical Debt · Code Review · Automation**

-----

## Code Quality Metrics

### Complexity Metrics

Understanding and tracking complexity metrics helps identify problematic code that may be difficult to maintain, test, or extend. Different metrics provide different insights into code quality.

**Cyclomatic Complexity** measures the number of linearly independent paths through code. Higher values indicate more decision points and increased testing difficulty. A function with complexity above 10 becomes difficult to test thoroughly, while complexity above 20 indicates urgent refactoring need.

**Cognitive Complexity** measures how difficult code is to understand conceptually. Unlike cyclomatic complexity, cognitive complexity accounts for nested structures and logical constructs that make code harder for humans to parse mentally. This metric aligns better with actual maintainability.

**Coupling** measures dependencies between modules. High coupling means changes in one module require changes in others, increasing maintenance burden. Aim for loose coupling with clear interfaces.

**Cohesion** measures how related the responsibilities of a single module are. High cohesion (single responsibility) makes code easier to understand, test, and maintain.

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Cyclomatic Complexity | < 10 | 10-20 | > 20 |
| Cognitive Complexity | < 15 | 15-30 | > 30 |
| Lines per Function | < 20 | 20-50 | > 50 |
| Parameters per Function | < 3 | 3-5 | > 5 |
| Coupling | < 5 | 5-10 | > 10 |

### Code Analysis Tools

```python
# Python example with multiple tools

# 1. pylint - Comprehensive Python linter
# Configuration: .pylintrc
[MESSAGES CONTROL]
disable=C0111,C0103,R0903,R0913

[FORMAT]
max-line-length=100
indent-string='    '

[DESIGN]
max-args=5
max-attributes=7
max-branches=12
max-locals=15
min-public-methods=2

[COMPLEXITY]
disable=too-complex

# Run: pylint mymodule.py --output-format=text

# 2. ruff - Fast Python linter (written in Rust)
# Configuration: pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
]
ignore = [
    "E501",  # line too long (handled by formatter)
    "B008",  # do not perform function calls in argument defaults
]

# Run: ruff check mymodule.py

# 3. mypy - Static type checker
# Configuration: mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = False
disallow_incomplete_defs = True
check_untyped_defs = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True

[mypy-tests.*]
disallow_untyped_defs = False

# Run: mypy mymodule.py
```

### JavaScript/TypeScript Analysis

```javascript
// ESLint configuration: .eslintrc.js
module.exports = {
  root: true,
  env: {
    browser: true,
    es2022: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  plugins: ['@typescript-eslint', 'react', 'react-hooks'],
  rules: {
    // TypeScript rules
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-explicit-any': 'warn',
    
    // React rules
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off', // Use TypeScript instead
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};

// Prettier integration in ESLint
// npm install --save-dev eslint-config-prettier
// Add to extends: 'prettier'
```

-----

## Technical Debt

### Identifying and Tracking

Technical debt accumulates when teams take shortcuts that create future maintenance burden. Understanding, tracking, and systematically addressing technical debt is essential for long-term project health.

**Common Sources of Technical Debt:**

- Duplicated code across the codebase
- Missing or inadequate documentation
- Complex conditional logic without clear structure
- Tight coupling between components
- Lack of automated tests
- Using deprecated libraries or patterns
- Hardcoded configuration values
- Inconsistent naming or coding standards

### Debt Tracking Tools

```yaml
# SonarQube quality gates configuration
# sonar-project.properties
sonar.projectKey=my-project
sonar.projectName=My Project
sonar.projectVersion=1.0
sonar.sources=src
sonar.tests=tests
sonar.sourceEncoding=UTF-8

# Quality gates thresholds
sonar.qualitygate.wait=true

# Quality profiles
sonar.technicalDebt.qualityProfiles=rule:python:S1130

# Issue tracking
sonar.issue.ignore.allFile=true

# Exclusions
sonar.exclusions=**/*.test.js,**/node_modules/**,**/dist/**
```

```json
// GitHub issue labels for technical debt
{
  "labels": [
    {
      "name": "tech-debt",
      "color": "FC4C02",
      "description": "Technical debt that needs addressing"
    },
    {
      "name": "refactoring",
      "color": "A2EEEF",
      "description": "Code refactoring task"
    },
    {
      "name": "performance",
      "color": "D93F0B",
      "description": "Performance improvement"
    },
    {
      "name": "security",
      "color": "B60205",
      "description": "Security improvement"
    }
  ]
}
```

### Debt Prioritization Matrix

| Impact \ Effort | Low | Medium | High |
|-----------------|-----|--------|------|
| **High** | Quick wins | Plan this quarter | Strategic initiative |
| **Medium** | When available | Schedule for later | Define scope |
| **Low** | Backlog | Backlog | Maybe never |

-----

## Testing Strategies

### Test Pyramid

The test pyramid provides a framework for structuring automated tests. At the base are numerous fast unit tests, followed by fewer integration tests, and finally a small number of slow end-to-end tests. This structure provides fast feedback while maintaining good coverage.

**Unit Tests** test individual functions, methods, or classes in isolation. They should be fast, isolated, and test one thing. Mock or stub all external dependencies. Target 70-80% of your test coverage with unit tests.

**Integration Tests** test how components work together. These might test database operations, API calls, or interaction between multiple services. They are slower than unit tests but catch integration issues.

**End-to-End Tests** test complete user workflows from the UI or API layer. They are slow and brittle but verify the entire system works correctly. Keep these to a minimum.

```python
# Example: Unit test with pytest
import pytest
from unittest.mock import Mock, patch

# Source code to test
def calculate_discount(price: float, discount_percent: float, member: bool = False) -> float:
    """Calculate final price with discount"""
    if price <= 0:
        raise ValueError("Price must be positive")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    
    discount = price * (discount_percent / 100)
    
    # Members get extra 10%
    if member:
        discount += price * 0.1
    
    return round(price - discount, 2)

class TestCalculateDiscount:
    """Unit tests for calculate_discount"""
    
    def test_basic_discount(self):
        """Test basic discount calculation"""
        result = calculate_discount(100, 10)
        assert result == 90.00
    
    def test_zero_discount(self):
        """Test no discount applied"""
        result = calculate_discount(50, 0)
        assert result == 50.00
    
    def test_full_discount(self):
        """Test 100% discount"""
        result = calculate_discount(100, 100)
        assert result == 0.00
    
    def test_member_discount(self):
        """Test member gets extra 10%"""
        result = calculate_discount(100, 10, member=True)
        assert result == 80.00  # 10% + 10% member = 20% off
    
    def test_invalid_price(self):
        """Test negative price raises error"""
        with pytest.raises(ValueError, match="Price must be positive"):
            calculate_discount(-10, 10)
    
    def test_invalid_discount(self):
        """Test discount out of range"""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            calculate_discount(100, 150)
    
    @pytest.mark.parametrize("price,discount,expected", [
        (100, 10, 90.00),
        (50, 20, 40.00),
        (200, 25, 150.00),
    ])
    def test_various_discounts(self, price, discount, expected):
        """Parametrized test for various scenarios"""
        result = calculate_discount(price, discount)
        assert result == expected
    
    @patch('__main__.get_member_discount')
    def test_member_discount_from_api(self, mock_get_discount):
        """Test member discount fetched from API"""
        mock_get_discount.return_value = 0.15
        # Implementation would call external service
        # mock_get_discount.assert_called_once()
```

### Test Coverage

```python
# pytest configuration: pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=html
    --cov-report=term-missing:skip-covered
    --cov-fail-under=80
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration: marks tests as unit tests

# tests
    unit Coverage configuration: .coveragerc
[run]
source = src
omit =
    */tests/*
    */test_*.py
    */__init__.py

[report]
precision = 2
show_missing = True
skip_covered = False
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
```

-----

## Code Review

### Guidelines for Effective Reviews

Code review is one of the most effective ways to improve code quality and share knowledge across teams. Effective reviews require clear standards, constructive feedback, and balanced effort between authors and reviewers.

**For Reviewers:**

- Review within 24-48 hours to avoid blocking progress
- Focus on substantive issues, not style preferences (use linters)
- Ask questions rather than making demands
- Suggest solutions, don't just point out problems
- Praise good code, not just criticize
- Be consistent in what you look for

**For Authors:**

- Keep PRs small (under 400 lines)
- Write clear descriptions explaining the what and why
- Self-review before requesting others
- Respond to feedback constructively
- Don't take feedback personally

### Review Checklist

```markdown
# Code Review Checklist

## Correctness
- [ ] Does the code work as intended?
- [ ] Are edge cases handled properly?
- [ ] Are there any potential bugs?
- [ ] Is the logic sound?

## Design
- [ ] Does the code follow project conventions?
- [ ] Is the design appropriate for the problem?
- [ ] Is there unnecessary complexity?
- [ ] Could the code be simpler?

## Functionality
- [ ] Does this match the requirements?
- [ ] Are there any missing features?
- [ ] Are error cases handled?
- [ ] Does it handle concurrent access if applicable?

## Testing
- [ ] Are there adequate tests?
- [ ] Do tests cover edge cases?
- [ ] Are tests maintainable?
- [ ] Are integration tests included where needed?

## Security
- [ ] Are there any security vulnerabilities?
- [ ] Is sensitive data handled properly?
- [ ] Are inputs validated?
- [ ] Are secrets properly managed?

## Performance
- [ ] Are there obvious performance issues?
- [ ] Are there unnecessary database calls?
- [ ] Is caching considered where appropriate?
- [ ] Are large data sets handled efficiently?

## Readability
- [ ] Is the code clear and understandable?
- [ ] Are names descriptive?
- [ ] Are there helpful comments for complex logic?
- [ ] Is the code properly formatted?

## Documentation
- [ ] Is the public API documented?
- [ ] Are complex algorithms explained?
- [ ] Are configuration requirements documented?
- [ ] Is there a CHANGELOG entry if needed?
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict
      - id: check-toml
      - id: debug-statements
      - id: mixed-line-ending

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ['--profile=black']

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      - id: ruff
        args: ['--fix']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: ['--strict', '--ignore-missing-imports']
```

-----

## Quality Gates

### CI/CD Integration

```yaml
# GitHub Actions: .github/workflows/quality.yml
name: Code Quality

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install ruff black mypy
          
      - name: Check formatting with Black
        run: black --check src/
        
      - name: Check import order with isort
        run: ruff check --select I src/
        
      - name: Lint with ruff
        run: ruff check src/
        
      - name: Type check with mypy
        run: mypy src/

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install pytest pytest-cov
      
      - name: Run tests with coverage
        run: pytest --cov=src --cov-report=xml --cov-fail-under=80
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### SonarQube Quality Gates

```groovy
// Jenkinsfile with SonarQube
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test -- --coverage'
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=my-project \
                        -Dsonar.sources=src \
                        -Dsonar.tests=tests \
                        -Dsonar.coverage.jacoco.xmlReportPath=coverage/jacoco.xml
                    '''
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                waitForQualityGate abortPipeline: true
            }
        }
    }
}
```

-----

## Documentation Standards

### Docstring Formats

```python
# Google Style Docstrings
def calculate_statistics(data: list[float], include_outliers: bool = False) -> dict:
    """Calculate statistical measures for a dataset.
    
    Args:
        data: List of numerical values to analyze.
        include_outliers: Whether to include outlier values in calculations.
            When False, values beyond 1.5 * IQR are excluded.
    
    Returns:
        Dictionary containing:
            - mean: Arithmetic average
            - median: Middle value
            - std: Standard deviation
            - min: Minimum value
            - max: Maximum value
            - count: Number of valid values
    
    Raises:
        ValueError: If data is empty or contains non-numeric values.
        TypeError: If data is not a list.
    
    Example:
        >>> calculate_statistics([1, 2, 3, 4, 5])
        {'mean': 3.0, 'median': 3.0, 'std': 1.41, ...}
    
    Note:
        For large datasets (>10,000 elements), consider using
        numpy's statistical functions for better performance.
    """
    pass
```

### README Template

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
pip install project-name
```

## Usage

```python
from project import Module

result = Module.function(arg1, arg2)
print(result)
```

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| option1 | string | "default" | Description |
| option2 | bool | true | Description |

## Development

### Setup

```bash
pip install -r requirements-dev.txt
npm install
```

### Testing

```bash
pytest --cov=src
```

### Code Style

This project uses:
- Black for formatting
- isort for import sorting
- mypy for type checking

## License

MIT License - see LICENSE file
```

-----

## Best Practices

1. **Automate where possible** — Use linters, formatters, and static analysis.

2. **Set clear standards** — Document coding conventions and enforce them.

3. **Review regularly** — Make code review part of the workflow.

4. **Measure quality** — Track metrics over time to identify trends.

5. **Address debt proactively** — Allocate time for improvement.

6. **Test thoroughly** — Prioritize tests that catch real bugs.

7. **Document decisions** — Record why you made architectural choices.

8. **Refactor continuously** — Small improvements add up.

9. **Share knowledge** — Pair programming and code reviews help.

10. **Iterate** — Quality is an ongoing process, not a destination.
