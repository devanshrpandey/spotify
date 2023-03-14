import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ast

#sets environment variables and allows all permissions
os.environ["SPOTIPY_CLIENT_ID"] = "375c8e4a9f8d4243996d256ff41daa62"
os.environ["SPOTIPY_CLIENT_SECRET"] = "1472274bf789453bbd1ed42c9ee181da"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:9090"
scope = "user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-read-playback-position user-top-read user-read-recently-played user-library-read user-library-modify"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


pls = sp.current_user_playlists()["items"] #get the last 50 playlists
allPlaylists = []
for pl in pls: 
    allPlaylists.append(pl["id"]) #create an array of all playlist ids

scores = {}
typeOfScore = "danceability" #can be replaces with energy, speechiness, acousticness, instrumentalness, liveness, valence, tempo


"""for playlist in allPlaylists:
    plTracks = sp.user_playlist_tracks(playlist_id=playlist)
    ids = []

    for item in plTracks["items"]:
        ids.append(item["track"]["id"])
    
    features = sp.audio_features(ids)
    for i in range(len(ids)):
        name = (plTracks["items"][i]["track"]["name"])
        scores[name] = features[i]["danceability"] """


print(sp.audio_features("https://open.spotify.com/track/2BzVkisodhQOPOPVJ9UKEI?si=858162fa68bc4400")[0])

