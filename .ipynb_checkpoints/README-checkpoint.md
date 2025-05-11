# 🎵 Advanced Music Recommendation System

![Music Recommendation System](https://img.shields.io/badge/Project-Music%20Recommendation-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Latest-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Latest-blue)
![Status](https://img.shields.io/badge/Status-Operational-success)

## Project Overview

This project implements a sophisticated music recommendation system using machine learning techniques on Spotify audio feature data. The system analyzes track characteristics and identifies similar songs based on audio features rather than traditional metadata approaches, allowing for the discovery of sonically similar tracks across diverse genres and artists.

## 📊 Data

The system leverages a comprehensive Spotify dataset containing over 1.1 million tracks with the following key features:

- **Audio characteristics:** danceability, energy, key, loudness, mode, etc.
- **Track metadata:** artist name, track name, track ID, genre, etc.
- **Performance metrics:** popularity, duration, etc.

## 🔬 Technical Approach

The recommendation engine employs a multi-stage machine learning pipeline:

### 1. Data Preprocessing & Feature Engineering

- **Initial cleaning:** Removed NAs and duplicates (1,159,764 → 1,159,748 records)
- **Feature selection:** Focused on intrinsic audio characteristics
- **Feature engineering:**
  - Created composite features like `energy_to_acousticness_ratio` and `vocal_character`
  - Developed music-specific components (`energy_dynamics`, `dance_rhythm`, `emotional_content`, etc.)
- **Feature normalization:** Applied MinMax and StandardScaler transforms

### 2. Dimensionality Reduction

- **Principal Component Analysis (PCA):** Reduced feature space to 6 principal components while preserving 91.99% of variance
- **3D visualization:** Mapped songs into a comprehensible 3D audio feature space

### 3. Clustering & Similarity Modeling

- **K-means clustering:** Identified optimal cluster count (35) using multiple evaluation metrics:
  - Silhouette Score
  - Davies-Bouldin Index
  - Calinski-Harabasz Index
- **Recommendation generation:** Combined cluster assignment with cosine similarity to identify most similar tracks

### 4. Performance Metrics

- Achieved Silhouette Score of 0.1667, indicating reasonable cluster separation given the complex audio feature space
- Clear visual clustering in PCA-reduced dimensions

## 🔧 Implementation Details

The system incorporates several advanced techniques:

- **Correlation analysis:** Identified and addressed highly correlated features
- **Feature importance analysis:** Used Random Forest to determine most influential audio characteristics
- **Extensive hyperparameter optimization:** Determined optimal clusters through comprehensive evaluation
- **Efficient large dataset handling:** Processing strategies for 1M+ records

## 🚀 Usage

```python
# Load recommendation model
import pandas as pd
df_pca = pd.read_pickle('df_pca.pkl')
df_clean = pd.read_pickle('df_clean.pkl')

# Get recommendations for a track
def recommend_songs(track_id, df_pca, df_clean, n_recommendations=5):
    if track_id not in df_pca.index:
        return "Track ID not found."
    
    cluster = df_pca.loc[track_id, 'cluster']
    similar_songs = df_pca[df_pca['cluster'] == cluster].drop('cluster', axis=1)
    
    if len(similar_songs) <= 1:
        return "Not enough songs in the same cluster."
    
    # Calculate cosine similarity
    track_features = similar_songs.loc[track_id].values.reshape(1, -1)
    similarities = cosine_similarity(track_features, similar_songs)[0]
    
    # Get top similar songs
    similar_indices = similar_songs.index[np.argsort(similarities)[::-1][1:n_recommendations+1]]
    recommendations = df_clean.loc[df_clean['track_id'].isin(similar_indices),
                             ['track_id', 'track_name', 'artist_name', 'genre', 'popularity']]
    
    return recommendations

# Example usage
track_id = "0lOonb8Xn49VXJ1Ukb2vgh"  # Disturbed - "Enough"
recommendations = recommend_songs(track_id, df_pca, df_clean)
```

## 📈 Results & Visualizations

The system effectively groups songs with similar audio characteristics:

![Cluster Visualization](cluster_visualization.png)

When presented with a metal track like Disturbed's "Enough", the system recommends other high-energy tracks with similar audio profiles across rock subgenres:

```
Selected track: "Enough" by Disturbed
Genre: metal

Recommendations:
- "Play My Game" by The Donnas (power-pop)
- "Live And Let Die" by Bass Modulators (hardstyle)
- "30/30-150" by Stone Sour (alt-rock)
- "Sahara" by Relient K (alt-rock)
- "Area 1" by All Ends (goth)
```

## 🔍 Future Enhancements

- Hybrid recommendation approach combining audio features with collaborative filtering
- Integration of lyrical content and sentiment analysis
- Real-time recommendation API
- User feedback mechanism to improve recommendations
- Genre-specific models to capture nuanced differences within genres

## 🛠️ Technologies Used

- **Python** for core implementation
- **Pandas** for data manipulation
- **Scikit-learn** for machine learning components
- **Seaborn/Matplotlib** for visualizations
- **NumPy** for numerical operations

## 📚 References

This project builds on research in music information retrieval (MIR) and content-based recommendation systems:

- Logan, B. (2004). Mel frequency cepstral coefficients for music modeling.
- Schedl, M., Gómez, E., & Urbano, J. (2014). Music information retrieval: Recent developments and applications.
- van den Oord, A., Dieleman, S., & Schrauwen, B. (2013). Deep content-based music recommendation.