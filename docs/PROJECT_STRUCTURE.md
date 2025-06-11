# 📁 Project Structure

```
spotify-clusters/
├── 🎯 Core Application
│   └── src/
│       ├── recommendation_engine.py    # Core ML recommendation engine
│       ├── models/                     # Trained ML models and scalers
│       │   ├── kmeans_model.pkl
│       │   ├── pca_transformer.pkl
│       │   ├── standard_scaler.pkl
│       │   ├── minmax_scaler_tempo.pkl
│       │   ├── df_pca.pkl
│       │   ├── df_clean.pkl
│       │   └── top_features.txt
│       └── web/                        # Web application
│           ├── app.py                  # Flask web server
│           ├── templates/              # HTML templates
│           │   └── index.html
│           └── static/                 # Frontend assets
│               ├── css/style.css
│               ├── js/app.js
│               └── images/
├── 📊 Data & Analysis
│   ├── data/                          # Dataset files
│   │   └── spotify_data.csv
│   └── notebooks/                     # Jupyter notebooks
│       ├── main.ipynb                 # Original analysis notebook
│       └── main.pdf
├── 📚 Documentation
│   ├── docs/                          # Project documentation
│   │   ├── README_WEBAPP.md
│   │   ├── SETUP_COMPLETE.md
│   │   ├── cluster_metrics.png
│   │   └── cluster_visualization.png
│   └── README.md                      # Main project README
├── ⚙️ Configuration
│   ├── config/                        # Configuration files
│   │   └── .env.example
│   ├── requirements.txt               # Python dependencies
│   └── .gitignore                     # Git ignore rules
├── 🔧 Scripts
│   └── scripts/                       # Utility scripts
│       ├── cleanup_repo.py
│       └── run_webapp.py
└── 🧪 Testing (Future)
    └── tests/                         # Unit tests
```

## 🚀 Quick Start

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Run web app**: `python scripts/run_webapp.py`
3. **Open browser**: http://localhost:5001

## 📝 File Descriptions

- **src/recommendation_engine.py**: Core ML engine with PCA, K-means, and similarity calculations
- **src/web/app.py**: Flask web application with REST API
- **src/models/**: All trained ML models and preprocessed data
- **notebooks/main.ipynb**: Original research and model development
- **data/spotify_data.csv**: 1.1M+ Spotify tracks dataset
