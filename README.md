### An unsupervised music recommendation system using Spotify track features

## Overview

`spotify-clusters` is a machine learning project that uses unsupervised learning techniques to analyze audio features from Spotify tracks, cluster similar songs together, and generate personalized music recommendations. The project explores advanced clustering algorithms beyond K-Means, dimensionality reduction techniques, and builds a practical recommendation system.

## Features

- Extract and analyze audio features from Spotify tracks
- Visualize music in lower-dimensional space using PCA, t-SNE, and UMAP
- Implement and compare multiple clustering algorithms (DBSCAN, Hierarchical Clustering, GMM)
- Generate personalized music recommendations based on content similarity
- Interactive visualizations of music clusters

## Getting Started

### Prerequisites

- Python 3.8+
- scikit-learn
- pandas
- matplotlib
- spotipy (Python library for Spotify Web API)
- Your Spotify account credentials (for personal data)

### Installation

```bash
git clone https://github.com/yourusername/spotify-clusters.git
cd spotify-clusters
pip install -r requirements.txt
```

### Quick Start

1. Set up your Spotify API credentials
2. Run data collection script to gather your music data
3. Execute the clustering notebook to analyze your music
4. Use the recommendation system to discover new songs

## Project Structure

- `data/` - Raw and processed data files
- `notebooks/` - Jupyter notebooks for exploration and visualization
- `src/` - Source code for the recommendation system
- `results/` - Saved model outputs and visualizations

## Next Steps

- Implement additional clustering algorithms
- Create a simple web interface for recommendations
- Add collaborative filtering components
- Extend to playlist generation

## License

MIT

## Acknowledgments

- Spotify Web API
- scikit-learn documentation
- "Hands-On Machine Learning with Scikit-Learn & TensorFlow"
