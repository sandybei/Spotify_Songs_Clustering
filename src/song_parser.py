import spotipy
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import spotipy.util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans, DBSCAN
import spotipy.util as util
from config import *


SCOPE = "user-library-read"

client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
auth_manager = SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=SCOPE,
                            show_dialog=True)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager,
                     auth_manager=auth_manager)


def get_all_saved_tracks():
    """
    function that returns all saved tracks of the user, not only the paginated results.

    :return:  ....
    """
    results = sp.current_user_saved_tracks()
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


tracks = get_all_saved_tracks()


def get_track_info():
    """
    returns a dataframe with the songs names, song ids and artists 
    """
    tracks_names = []
    artists_names = []
    tracks_ids = []
    for track in tracks:
        song = track['track']
        tracks_ids.append(song['id'])
        tracks_names.append(song['name'])
        artists_names.append(song['artists'][0]['name'])

    songs = pd.DataFrame({'name': tracks_names, 'id': tracks_ids, 'artist': artists_names})
    return songs



def get_tracks_audio_features(ids):
    """
     function that return a dataframe with track names, artists and track ids

    :param ids: a list with track ids
    :return: a dataframe of the audio features of all tracks
    """
    dfs_to_concat = []
    i = 0
    while i <= len(ids):
        audio_features = sp.audio_features(tracks=ids[i:i+100])
        audio_features_df = pd.DataFrame(audio_features)
        dfs_to_concat.append(audio_features_df)
        i += 100

    audio_features = pd.concat(dfs_to_concat, ignore_index=True)
    return audio_features

# load audio-features data to csv
songs = get_track_info()
features = get_tracks_audio_features(songs['id'])
features.to_csv(r'data/features.csv')  # added to gitignore

