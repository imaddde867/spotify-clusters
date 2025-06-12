# 🎵 Spotify AI Music Recommendation System

A sophisticated machine learning-powered music recommendation system that analyzes audio features to suggest similar tracks.

## ✨ Features

- **AI-Powered Recommendations**: Uses K-means clustering and PCA for intelligent music suggestions
- **1.1M+ Track Dataset**: Comprehensive Spotify dataset with audio features
- **Smart Fallback System**: Works with or without Spotify API access
- **Clean Web Interface**: Modern, responsive web application
- **Real-time Processing**: Fast recommendations using pre-trained models

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   ./run.sh
   ```

3. **Open Browser**: Navigate to `http://localhost:5001`

## 🔧 Configuration

Set your Spotify API credentials in `.env`:
```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
```

## 📊 How It Works

1. **Data Processing**: 1.1M+ tracks analyzed with audio features
2. **Feature Engineering**: Custom musical dimensions created
3. **Dimensionality Reduction**: PCA captures 91.99% of variance
4. **Clustering**: K-means groups similar tracks
5. **Recommendations**: Cosine similarity finds matching songs

## 🎯 System Status

✅ **Data Alignment**: Perfect alignment between all components  
✅ **ML Models**: Updated to latest scikit-learn version  
✅ **API Integration**: Spotify API with intelligent fallback  
✅ **Web Interface**: Clean, responsive design  
✅ **Recommendation Engine**: Smart AI-based suggestions  

## 📁 Project Structure

```
spotify-clusters/
├── src/
│   ├── recommendation_engine.py    # Core ML engine
│   ├── models/                     # Trained models & data
│   └── web/                        # Web application
├── notebooks/                      # Analysis notebooks
├── data/                          # Dataset files
└── run.sh                         # Launch script
```

## 🔮 Technical Details

- **Machine Learning**: K-means clustering, PCA, StandardScaler
- **Web Framework**: Flask with modern frontend
- **Data Processing**: Pandas, NumPy for 1.1M+ records
- **API Integration**: Spotipy for Spotify Web API
- **Deployment**: Production-ready with proper error handling

---

**Status**: ✅ Production Ready | **Last Updated**: June 2025
