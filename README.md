# E-commerce Customer Behavior Analysis

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Latest-orange.svg)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/pandas-Latest-green.svg)](https://pandas.pydata.org)
[![NumPy](https://img.shields.io/badge/numpy-Latest-blue.svg)](https://numpy.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Latest-yellow.svg)](https://matplotlib.org)
[![Seaborn](https://img.shields.io/badge/seaborn-Latest-lightgrey.svg)](https://seaborn.pydata.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Latest-orange.svg)](https://jupyter.org)

This project applies unsupervised machine learning techniques to analyze customer purchasing patterns and build a product recommendation system using real-world e-commerce transaction data.

## Project Overview

The repository contains a comprehensive analysis of the "Online Retail" dataset from the UCI Machine Learning Repository, exploring customer segmentation and product associations through multiple unsupervised learning algorithms.

## Features

- **Customer Segmentation** using multiple clustering techniques:
  - K-Means Clustering
  - Hierarchical Clustering
  - DBSCAN
  - Gaussian Mixture Models

- **Dimensionality Reduction** for visualization and analysis:
  - Principal Component Analysis (PCA)
  - t-SNE

- **Market Basket Analysis** using association rule mining

- **Recommendation System** implementation:
  - Collaborative Filtering
  - Matrix Factorization

## Dataset

The project uses the [Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/Online+Retail), which contains actual transactions from a UK-based online retailer.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/unsupervised-learning-ecommerce-analysis.git
cd unsupervised-learning-ecommerce-analysis

# Create and activate a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

## Usage

The analysis is structured in Jupyter notebooks:

1. `1_Data_Preprocessing.ipynb` - Data cleaning and feature engineering
2. `2_Customer_Segmentation.ipynb` - Multiple clustering approaches
3. `3_Dimensionality_Reduction.ipynb` - PCA and t-SNE analysis
4. `4_Association_Rules.ipynb` - Market basket analysis
5. `5_Recommendation_System.ipynb` - Building recommendation engines

## Requirements

- Python 3.8+
- scikit-learn
- pandas
- numpy
- matplotlib
- seaborn
- mlxtend
- scipy
- jupyter

## License

This project is licensed under the MIT License - see the LICENSE file for details.
