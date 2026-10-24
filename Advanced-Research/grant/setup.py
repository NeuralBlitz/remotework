"""
GraNT Package Setup
===================

Installation script for the GraNT framework.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="grant-framework",
    version="0.1.0",
    author="NeuralBlitz",
    author_email="NuralNexus@icloud.com",
    description="Granular Numerical Tensor Framework for Next-Generation AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neuralblitz/grant",
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "torch>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinx-autodoc-typehints>=1.19.0",
        ],
        "viz": [
            "matplotlib>=3.5.0",
            "seaborn>=0.12.0",
            "plotly>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "grant=grant.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "grant": ["py.typed"],
    },
    keywords=[
        "machine-learning",
        "deep-learning",
        "attention-mechanism",
        "sheaf-theory",
        "category-theory",
        "uncertainty-quantification",
        "automated-research",
    ],
    project_urls={
        "Bug Reports": "https://github.com/neuralblitz/grant/issues",
        "Source": "https://github.com/neuralblitz/grant",
        "Documentation": "https://neuralblitz.github.io/grant",
    },
)
