# Unsupervised Music Recommendation System using Spotify Data

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Latest-orange.svg)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/pandas-Latest-green.svg)](https://pandas.pydata.org)
[![NumPy](https://img.shields.io/badge/numpy-Latest-blue.svg)](https://numpy.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Latest-yellow.svg)](https://matplotlib.org)
[![Seaborn](https://img.shields.io/badge/seaborn-Latest-lightgrey.svg)](https://seaborn.pydata.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Latest-orange.svg)](https://jupyter.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

This project applies advanced unsupervised machine learning techniques to analyze Spotify track features, cluster similar songs together, and generate personalized music recommendations. By leveraging various clustering algorithms and dimensionality reduction techniques, the analysis provides valuable insights into music patterns and user preferences.

**[📄 View Complete Analysis (PDF)](main.pdf)** • View the detailed analysis and results without running the code.

## 🔍 Key Objectives

• Extract and analyze audio features from Spotify tracks
• Segment songs based on their audio characteristics
• Discover hidden patterns in music data
• Build a recommendation system for personalized music suggestions
• Visualize complex relationships in high-dimensional audio data

## 📊 Techniques Used

• **Clustering Algorithms**:
  • K-Means Clustering
  • Hierarchical Clustering
  • DBSCAN
  • Gaussian Mixture Models

• **Dimensionality Reduction**:
  • Principal Component Analysis (PCA)
  • t-Distributed Stochastic Neighbor Embedding (t-SNE)
  • UMAP (Uniform Manifold Approximation and Projection)

• **Recommendation Systems**:
  • Content-Based Filtering
  • Collaborative Filtering
  • Matrix Factorization

## 📂 Project Structure

```
.
├── data/
│   └── spotify_data.csv      # Music streaming dataset
├── main.ipynb                # Jupyter notebook containing the analysis
├── main.pdf                  # PDF version of the notebook for easy viewing
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## 🚀 Getting Started

### Prerequisites

• Python 3.8+
• Jupyter Notebook

### Installation

```bash
# Clone the repository
git clone https://github.com/imaddde867/unsupervised-learning-ecommerce-analysis.git
cd unsupervised-learning-ecommerce-analysis

# Create and activate a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install required packages
pip install jupyter pandas numpy matplotlib seaborn scikit-learn scipy spotipy
```

### Usage

Open and run the Jupyter notebook:

```bash
jupyter notebook main.ipynb
```

## 📈 Analysis Workflow

1. **Data Preprocessing**: Cleaning the data, handling missing values, and feature engineering
2. **Exploratory Data Analysis**: Understanding the distribution and relationships in audio features
3. **Feature Extraction**: Analyzing and processing Spotify audio features
4. **Dimensionality Reduction**: Using PCA, t-SNE, and UMAP for visualization and feature extraction
5. **Clustering**: Applying multiple clustering algorithms to group similar songs
6. **Recommendation System**: Building personalized music recommendation engines
7. **Evaluation & Insights**: Interpreting results and extracting musical insights

You can explore the complete analysis in the [main.pdf](main.pdf) document without needing to run any code.

## 🔄 Future Enhancements

• Create an interactive web interface for recommendations
• Implement playlist generation features
• Add collaborative filtering components
• Extend analysis to include user behavior patterns

## 📝 License

This project is licensed under the MIT License • see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

• [@imaddde867](https://github.com/imaddde867)

## 🙏 Acknowledgments

• Spotify Web API
• scikit-learn documentation
• "Hands-On Machine Learning with Scikit-Learn & TensorFlow"
