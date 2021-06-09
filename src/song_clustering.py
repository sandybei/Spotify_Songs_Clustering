import spotipy
import pandas as pd
import spotipy.util
import matplotlib.pyplot as plt
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans, DBSCAN
import spotipy.util as util
from scipy.cluster.hierarchy import dendrogram, linkage
from song_parser import *


# load audio features data 
features = pd.read_csv(r'data/features.csv')

# print audio features
print(features.columns)
print(features.head())

# load audio features to csv file
audio_features = features.drop(['type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms'], axis=1)
audio_features.to_csv('data/audio_features.csv')

# keep important features
X = features[["acousticness", "danceability", "liveness", "energy", "instrumentalness", "loudness", "speechiness"]]


# data preprocessing

def scale(column):
    """
    function that scales data to the range [0,1]

    :param column: The column of the dataframe features_df for scaling
    """
    scaler = MinMaxScaler()
    column_array = features[column].to_numpy()
    column_array_scaled = scaler.fit_transform(column_array.reshape(-1, 1))
    features[column] = column_array_scaled


# scale features
columns_for_scaling = ['loudness'] #, 'tempo', 'key', 'time_signature']
for column in columns_for_scaling:
    scale(column)


# elbow technique
k_range = range(1, 15)
sse = []
for k in k_range:
    km = KMeans(n_clusters=k)
    km.fit(X)
    sse.append(km.inertia_)

# plot elbow
plt.plot(k_range, sse)
plt.title('Elbow Technique')
plt.xlabel('k')
plt.ylabel('Sum of Squared Error')
plt.show()
#plt.savefig('Spotify_Songs_Clustering/Elbow Technique.png')

# fit data to Kmeans
n_clusters = 4 
km = KMeans(n_clusters=n_clusters, random_state=0)
clusters = km.fit_predict(X)


# add column with clusters
X['cluster'] = clusters
X['id'] = features['id']

# load audio features data with their clusters to a csv file
track_ids_clusters = X[['cluster', 'id']]
track_ids_clusters.to_csv(r'data/track_ids_clusters.csv')  # added to gitignore



'''
# print songs of each cluster
songs = get_track_info()
for i in range(4):
    print(f'CLUSTER {i}:')
    print()
    ids = X['id'][X['cluster'] == i]
    for id in ids:
        print(songs[['name', 'artist']][songs['id'] == id].to_numpy())
    print('-------------------------------------')
'''