import pandas as pd
import joblib

# Load saved components
kmeans = joblib.load('kmeans_model.pkl')
pca = joblib.load('pca_transformer.pkl')
scaler_opt = joblib.load('standard_scaler.pkl')
scaler_tempo = joblib.load('minmax_scaler_tempo.pkl')
df_pca = pd.read_pickle('df_pca.pkl')
df_clean = pd.read_pickle('df_clean.pkl')