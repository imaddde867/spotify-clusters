# 🎵 Unsupervised Music Recommendation System Using Spotify Data

A project that leverages **unsupervised machine learning** to analyze Spotify track features, cluster similar songs, and generate personalized music recommendations.

📄 **[View Full Analysis (PDF)](main.pdf)** – Explore the complete results without running any code!

---

## 🔗 Useful Links

- [Python](https://www.python.org)  
- [scikit-learn](https://scikit-learn.org)  
- [Pandas](https://pandas.pydata.org)  
- [NumPy](https://numpy.org)  
- [Matplotlib](https://matplotlib.org)  
- [Seaborn](https://seaborn.pydata.org)  
- [Jupyter](https://jupyter.org)  
- [License](LICENSE)

---

## 📋 Overview

This project applies unsupervised learning techniques to Spotify track data to identify song clusters and generate smart music recommendations. By combining **clustering algorithms**, **dimensionality reduction**, and **content-based filtering**, the system reveals hidden structures in musical data and suggests songs based on audio similarities.

---

## 🎯 Objectives

- Analyze and extract meaningful features from Spotify track data  
- Group songs by audio characteristics using clustering techniques  
- Visualize complex patterns in high-dimensional data  
- Build a basic recommendation engine to suggest similar tracks  
- Deliver an interpretable and visually engaging analysis  

---

## ⚙️ Techniques Used

### Clustering Algorithms
- K-Means  
- Hierarchical Clustering  
- DBSCAN  
- Gaussian Mixture Models (GMM)

### Dimensionality Reduction
- Principal Component Analysis (PCA)  
- t-SNE  
- UMAP

### Recommendation Approaches
- Content-Based Filtering  
- Collaborative Filtering (planned)  
- Matrix Factorization (planned)

---

## 📁 Project Structure

```
.
├── data/
│   └── spotify_data.csv        # Main dataset
├── main.ipynb                  # Jupyter notebook with full analysis
├── main.pdf                    # PDF version of the notebook
├── README.md                   # Project README file
└── LICENSE                     # MIT License
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- Jupyter Notebook

### 💾 Installation

```bash
# Clone the repository
git clone https://github.com/imaddde867/unsupervised-learning-ecommerce-analysis.git
cd unsupervised-learning-ecommerce-analysis

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install jupyter pandas numpy matplotlib seaborn scikit-learn scipy spotipy
```

### ▶️ Run the Notebook

```bash
jupyter notebook main.ipynb
```

---

## 📈 Analysis Workflow

1. **Data Preprocessing** – Cleaning and formatting the dataset  
2. **Exploratory Data Analysis (EDA)** – Understanding trends and correlations  
3. **Feature Engineering** – Extracting and refining audio features  
4. **Dimensionality Reduction** – Visualizing patterns in lower dimensions  
5. **Clustering** – Grouping similar songs using ML models  
6. **Recommendation System** – Suggesting songs based on similarity  
7. **Insights & Evaluation** – Interpreting results and findings  

---

## 🔮 Future Enhancements

- 🌐 Build an interactive web interface for recommendations  
- 🎧 Auto-generate playlists based on user mood and song clusters  
- 👥 Integrate collaborative filtering and user profiles  
- 📊 Incorporate listening behavior for dynamic suggestions  

---

## 📄 License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for more information.

---

## 🙌 Acknowledgments

- Spotify Web API  
- scikit-learn Documentation  
- *Hands-On Machine Learning with Scikit-Learn & TensorFlow* by Aurélien Géron  
