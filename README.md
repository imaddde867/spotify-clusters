# Spotify AI Music Recommendation System

An advanced machine learning-powered music recommendation engine that leverages audio feature analysis and unsupervised clustering algorithms to deliver personalized music suggestions. Built with production-grade architecture and comprehensive fallback mechanisms.

## Overview

This system implements a sophisticated recommendation engine using Principal Component Analysis (PCA) and K-means clustering on a dataset of over 1.1 million Spotify tracks. The application provides intelligent music recommendations based on audio feature similarity, with both API-driven and dataset-based recommendation modes.

## Key Features

### Machine Learning Architecture
- **Dimensionality Reduction**: PCA implementation for feature optimization and noise reduction
- **Clustering Algorithm**: K-means clustering with 35 optimized clusters for music categorization
- **Feature Engineering**: Advanced audio feature processing including energy-to-acousticness ratios and vocal character analysis
- **Similarity Computation**: Cosine similarity calculations for precise track matching

### Production-Ready Web Application
- **Flask-based REST API**: Scalable web service with comprehensive error handling
- **Responsive Frontend**: Modern web interface with dark mode support and accessibility features
- **Real-time Processing**: Sub-second recommendation generation using pre-trained models
- **Fallback Systems**: Multiple recommendation strategies ensuring consistent service availability

### Data Processing Pipeline
- **Large-scale Dataset**: 1,159,764 Spotify tracks with comprehensive audio features
- **Feature Selection**: 11 core audio features plus engineered composite features
- **Data Validation**: Robust preprocessing with missing value handling and outlier detection
- **Model Persistence**: Optimized model serialization for production deployment

## Technical Architecture

### Core Components

```
├── Machine Learning Engine (src/recommendation_engine.py)
│   ├── PCA Transformer (91.99% variance preservation)
│   ├── K-means Clustering (35 clusters)
│   ├── Feature Scalers (MinMax, Standard)
│   └── Similarity Calculator
├── Web Application (src/web/)
│   ├── Flask API Server
│   ├── Frontend Interface
│   └── Static Assets
├── Data Pipeline (notebooks/main.ipynb)
│   ├── Feature Engineering
│   ├── Model Training
│   └── Validation Metrics
└── Model Artifacts (src/models/)
    ├── Trained Models (.pkl files)
    ├── Preprocessed Data
    └── Feature Definitions
```

### Audio Features Analyzed

| Feature | Description | Processing |
|---------|-------------|------------|
| **Danceability** | Rhythmic suitability for dancing | Normalized (0.0-1.0) |
| **Energy** | Perceptual intensity and activity | Normalized (0.0-1.0) |
| **Valence** | Musical positiveness conveyed | Normalized (0.0-1.0) |
| **Acousticness** | Acoustic vs. electronic confidence | Normalized (0.0-1.0) |
| **Instrumentalness** | Vocal content prediction | Normalized (0.0-1.0) |
| **Liveness** | Live performance detection | Normalized (0.0-1.0) |
| **Speechiness** | Spoken word detection | Normalized (0.0-1.0) |
| **Tempo** | Track speed in BPM | MinMax scaled |
| **Loudness** | Overall loudness in dB | Standard scaled |
| **Key** | Musical key detection | One-hot encoded |
| **Mode** | Major/minor modality | One-hot encoded |

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Spotify Developer Account (for API access)
- 4GB+ RAM (for model loading)

### Environment Configuration

1. **Clone Repository**:
   ```bash
   git clone https://github.com/imaddde867/spotify-clusters.git
   cd spotify-clusters
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Spotify API**:
   ```bash
   cp .env.example .env
   # Edit .env with your Spotify API credentials
   ```

   Required environment variables:
   ```env
   SPOTIPY_CLIENT_ID=your_spotify_client_id
   SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   FLASK_ENV=production
   ```

### Spotify API Setup

1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new application
3. Note your Client ID and Client Secret
4. Add credentials to your `.env` file

**Security Notice**: Never commit API credentials to version control. The `.env` file is excluded via `.gitignore`.

## Application Deployment

### Development Mode
```bash
# Start the development server
python src/web/app.py
# Or use the convenience script
./run.sh
```

### Production Deployment
```bash
# Using Gunicorn (recommended)
gunicorn --bind 0.0.0.0:5000 --workers 4 src.web.app:app

# Using Flask development server (not recommended for production)
export FLASK_ENV=production
python src/web/app.py
```

The application will be available at `http://localhost:5001` (development) or `http://localhost:5000` (production).

## API Documentation

### Endpoints

#### GET `/`
Main application interface

#### POST `/recommend`
Generate music recommendations

**Request Body:**
```json
{
  "song_name": "Bohemian Rhapsody",
  "artist_name": "Queen",
  "playlist_size": 10
}
```

**Response:**
```json
{
  "success": true,
  "recommendations": [
    {
      "track_name": "Don't Stop Me Now",
      "artist_name": "Queen",
      "genre": "rock",
      "popularity": 85
    }
  ],
  "search_query": {
    "song_name": "Bohemian Rhapsody",
    "artist_name": "Queen",
    "playlist_size": 10
  }
}
```

#### GET `/api/popular-examples`
Retrieve popular song examples for the interface

#### GET `/health`
System health check endpoint

## Model Performance Metrics

| Metric | Value | Description |
|--------|-------|-------------|
| **Variance Preserved** | 91.99% | PCA dimensionality reduction efficiency |
| **Cluster Count** | 35 | Optimized K-means cluster configuration |
| **Dataset Coverage** | 1,159,764 tracks | Comprehensive music library |
| **Response Time** | <500ms | Average recommendation generation time |
| **Memory Usage** | ~2GB | Model loading and operation requirements |

## System Architecture

### Recommendation Pipeline

1. **Input Processing**: Song name and artist validation
2. **Spotify API Integration**: Audio feature extraction for new tracks
3. **Feature Preprocessing**: Scaling and transformation using trained models
4. **Cluster Assignment**: K-means prediction for optimal cluster placement
5. **Similarity Computation**: Cosine similarity within assigned cluster
6. **Result Ranking**: Distance-based recommendation ordering
7. **Fallback Handling**: Dataset-based recommendations when API unavailable

### Fallback Mechanisms

The system implements multiple fallback strategies:

- **Primary**: Spotify API + ML pipeline
- **Secondary**: Dataset fuzzy matching + clustering
- **Tertiary**: Random sampling from similar genres
- **Emergency**: Popular track recommendations

## Development and Contribution

### Project Structure

```
spotify-clusters/
├── src/
│   ├── recommendation_engine.py    # Core ML algorithms
│   ├── models/                     # Serialized model artifacts
│   │   ├── kmeans_model.pkl
│   │   ├── pca_transformer.pkl
│   │   ├── standard_scaler.pkl
│   │   ├── minmax_scaler_tempo.pkl
│   │   ├── df_pca.pkl
│   │   ├── df_clean.pkl
│   │   └── top_features.txt
│   └── web/                        # Web application
│       ├── app.py                  # Flask server
│       ├── templates/              # HTML templates
│       └── static/                 # CSS, JavaScript, assets
├── notebooks/
│   ├── main.ipynb                  # Model development and analysis
│   └── main.pdf                    # Research documentation
├── data/
│   └── spotify_data.csv            # Training dataset
├── docs/                           # Additional documentation
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Version control exclusions
└── run.sh                          # Application launcher
```

### Model Retraining

To retrain models with updated data:

1. **Update Dataset**: Replace `data/spotify_data.csv` with new data
2. **Run Notebook**: Execute `notebooks/main.ipynb` completely
3. **Verify Models**: Ensure all `.pkl` files are generated in `src/models/`
4. **Test Application**: Restart the web application and verify functionality

### Testing

```bash
# Install development dependencies
pip install pytest pytest-cov

# Run test suite (when implemented)
pytest tests/

# Check application health
curl http://localhost:5001/health
```

## Performance Optimization

### Memory Management

- Models are loaded once at application startup
- Lazy loading for large datasets
- Efficient numpy operations for similarity calculations

### Caching Strategy

- Spotify API responses cached locally
- Pre-computed cluster assignments
- Optimized feature transformations

### Scalability Considerations

- Stateless application design
- Horizontal scaling capability
- Database integration ready (currently file-based)

## Troubleshooting

### Common Issues

**Model files not found**
```bash
# Solution: Run the Jupyter notebook to generate models
jupyter notebook notebooks/main.ipynb
```

**Spotify API authentication errors**
```bash
# Solution: Verify credentials in .env file
cat .env
# Ensure SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET are set
```

**Port already in use**
```bash
# Solution: The application auto-detects available ports
# Or manually specify a port in app.py
```

**Memory errors during startup**
```bash
# Solution: Ensure sufficient RAM (4GB+ recommended)
# Consider reducing dataset size for development
```

## License and Attribution

This project is developed for educational and research purposes. The Spotify dataset is used under fair use for academic research. Spotify API integration requires compliance with Spotify's Terms of Service.

## Technical Specifications

- **Python Version**: 3.8+
- **Framework**: Flask 2.0+
- **ML Libraries**: scikit-learn, pandas, numpy
- **API Integration**: spotipy
- **Frontend**: Vanilla JavaScript, CSS3, HTML5
- **Deployment**: Gunicorn-ready, Docker-compatible

---

**Project Status**: Production Ready | **Maintained**: Active Development