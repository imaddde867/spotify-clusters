import pandas as pd
import joblib

# Load saved components
kmeans = joblib.load('kmeans_model.pkl')
pca = joblib.load('pca_transformer.pkl')
scaler_opt = joblib.load('standard_scaler.pkl')
scaler_tempo = joblib.load('minmax_scaler_tempo.pkl')
df_pca = pd.read_pickle('df_pca.pkl')
df_clean = pd.read_pickle('df_clean.pkl')

# Load list of top features
with open('top_features.txt', 'r') as f:
    top_features = f.read().splitlines()

print("All components loaded successfully.")

# Function to preprocess new song data
def preprocess_song(song_data, scaler_tempo, scaler_opt, pca, top_features):
    '''
    Preprocess new song data to match the format of the preprocessed dataset used to train the model
    Parameters:
        song_data (dict): A dictionary containing song data.
        scaler tempo (MinMaxScaler): The scaler used to scale the tempo feature.
        scaler opt (StandardScaler): The scaler used to scale the other features.
        pca (PCA): The PCA transformer used to reduce the dimensionality of the data.
        top features (list): The list of top features used to train the model.

    Returns:
        pca_features (array): The PCA features of the song.
        '''
    # conver the song_data to a pandas dataframe if necessary
    if not isinstance(song_data, pd.DataFrame):
        song_data = pd.DataFrame(song_data, index=[0])

    # ensure all necessary columns are present
    raw_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    for feature in raw_features:
        if feature not in song_data.columns:
            raise ValueError(f"Missing required feature: {feature}")

    # create new features
    song_data['energy_to_acousticness_ratio'] = song_data['energy'] / (song_data['acousticness'] + 0.01)
    song_data['energy_dynamics'] = song_data['energy']
    song_data['dance_rhythm'] = 0.6 * song_data['danceability'] + 0.4 * song_data['tempo']
    song_data['emotional_content'] = song_data['valence']
    song_data['vocal_presence'] = song_data['speechiness'] - 0.5 * song_data['instrumentalness']
    song_data['performance_style'] = song_data['liveness']

    song_df = song_data[top_features]

    # Apply StandardScaler
    song_scaled = scaler_opt.transform(song_df)
    song_scaled_df = pd.DataFrame(song_scaled, columns=song_df.columns)

    # Apply PCA
    pca_features = pca.transform(song_scaled_df)
    pca_features_df = pd.DataFrame(pca_features, columns=[f'PC{i+1}' for i in range(pca.n_components_)])

    return pca_features_df

# Song finder function
