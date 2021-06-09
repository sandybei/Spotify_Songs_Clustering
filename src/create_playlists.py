import spotipy
import pandas as pd
import spotipy.util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from song_clustering import n_clusters
from config import *

X = pd.read_csv(r'data/track_ids_clusters.csv')
X['id'] = features['id']


client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
SCOPE = "playlist-modify-private"
auth_manager = SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=SCOPE,
                            show_dialog=True)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager,
                     auth_manager=auth_manager)


# create new empty playlists for each cluster
for i in range(n_clusters):
    playlist_name = 'cluster {}'.format(i + 1)
    sp.user_playlist_create(user=user_id,
                            name=playlist_name,
                            public=False,
                            collaborative=False,
                            description='A playlist created by clustering.'
                            )


# add tracks of each cluster to new playlists 
cluster_playlists = [playlist_id_1, playlist_id_2, playlist_id_3, playlist_id_4]  # the playlist ids have been found manually
for i, playlist in enumerate(cluster_playlists):
    j = 0
    length = len(X['id'][X['cluster'] == i])
    while j <= length:
        results = sp.playlist_add_items(playlist_id=playlist,
                                        items=X['id'][X['cluster'] == i].iloc[i:i + 100],
                                        position=None)
        j += 100

