# 🎵 Music Recommendation System Using Spotify Data

A sophisticated data science project leveraging advanced unsupervised machine learning techniques to analyze Spotify track features, identify meaningful musical patterns, and generate personalized recommendations based on audio similarity.

[![Music Visualization](https://img.shields.io/badge/Visualization-PCA%20%26%20Clustering-blueviolet)](cluster_visualization.png)
[![Dataset Size](https://img.shields.io/badge/Dataset-1.1M%2B%20Songs-brightgreen)](data/spotify_data.csv)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📊 Project Overview

This project applies sophisticated unsupervised learning techniques to a massive Spotify dataset (1.1M+ tracks) to:

- Extract and transform audio features into meaningful musical dimensions
- Reduce high-dimensional data complexity through Principal Component Analysis (PCA)
- Identify optimal clustering parameters through multiple evaluation metrics
- Build a content-based recommendation engine using audio similarity
- Provide data-driven insights into musical patterns and relationships

The system successfully identifies hidden structures in Spotify's audio features and creates musically coherent recommendations across diverse genres.

## 🔬 Key Technical Features

### Data Processing & Feature Engineering
- Initial dataset: **1,159,764 tracks** with 20 attributes
- **Custom musical dimensions** created from raw audio features:
  - `energy_dynamics`: Captures intensity and activity level
  - `dance_rhythm`: Combines danceability and tempo characteristics
  - `emotional_content`: Represents musical mood and positiveness
  - `vocal_presence`: Measures the balance of vocals vs. instrumental content
  - `performance_style`: Identifies live recording characteristics

### Advanced Dimensionality Reduction
- **Principal Component Analysis (PCA)** implementation with:
  - 6 principal components capturing **91.99% of total variance**
  - 3D visualization of component relationships
  - Meaningful mapping of audio features to latent space

### Optimization-Driven Clustering
- K-means clustering implemented with:
  - Comprehensive evaluation using **silhouette score, Davies-Bouldin, and Calinski-Harabasz metrics**
  - Automated optimal cluster detection (n=35)
  - Systematic approach to finding the ideal clustering configuration

### Recommendation Algorithm
- Content-based recommendation using:
  - Cluster membership as initial filtering mechanism
  - Cosine similarity to identify most similar tracks within clusters
  - Multi-factor similarity calculations in reduced dimensional space

## 🧪 Methodology & Workflow

### 1. Data Loading & Cleaning
- Loaded 1.1M+ tracks from Spotify dataset
- Identified and handled missing values (16 records dropped)
- Verified dataset integrity and duplicates (0 found)

### 2. Feature Selection & Engineering
- Selected 11 core audio features for analysis
- Created one-hot encoding for categorical variables (key, mode)
- Engineered composite features including energy-to-acousticness ratio

### 3. Statistical Analysis & Transformation
- Applied appropriate scaling techniques:
  - Min-max scaling for bounded features
  - Standard scaling for dimensional uniformity
- Correlation analysis to identify and handle feature redundancy

### 4. Feature Importance Analysis
- Implemented Random Forest for feature importance ranking
- Identified key features driving musical similarity:
  - energy_to_acousticness_ratio (highest importance)
  - danceability
  - tempo
  - valence
  - speechiness

### 5. Dimensionality Reduction & Clustering
- Applied PCA to reduce dimensions while preserving 91.99% variance
- Evaluated optimal cluster count using multiple metrics
- Implemented k-means clustering with silhouette score validation

### 6. Recommendation System
- Track recommendation based on cluster membership and cosine similarity
- Additional metadata integration for enhanced result presentation
- Evaluation through cross-genre recommendation quality

## 📊 Key Visualizations

The project includes multiple advanced visualizations:

1. **Correlation Matrix Heatmap**: Revealing relationships between audio features
2. **Feature Importance Ranking**: Identifying the most significant musical dimensions
3. **3D PCA Visualization**: Mapping the music feature space in three dimensions
4. **Clustering Metrics Analysis**: Multi-metric evaluation of cluster configurations
5. **Cluster Visualization**: Final 2D representation of the music landscape

## 🔧 Technical Stack

- **Data Processing**: Pandas, NumPy
- **Machine Learning**: scikit-learn (PCA, K-means, RandomForest)
- **Visualization**: Matplotlib, Seaborn
- **Performance Optimization**: Multiprocessing for parallel computation
- **Development Environment**: Jupyter Lab/Notebook

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Notebook/Lab
- Required libraries: pandas, numpy, scikit-learn, matplotlib, seaborn

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/music-recommendation-system.git
cd music-recommendation-system

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### Running the Analysis

```bash
jupyter notebook main.ipynb
```

## 🔮 Future Enhancements

1. **Hybrid Recommendation System**: Integrating collaborative filtering with content-based approach
2. **Real-time API Integration**: Connecting to Spotify API for dynamic recommendations
3. **Interactive Web Interface**: Building a user-friendly recommendation platform
4. **Time-Based Analysis**: Exploring evolution of music characteristics over decades
5. **Genre Classification**: Implementing supervised learning for genre prediction
6. **Playlist Generation**: Automated creation of coherent playlists

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Spotify for providing the rich audio feature dataset
- scikit-learn community for comprehensive ML implementation
- The academic research on music information retrieval systems