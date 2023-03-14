import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#
#
#EDIT THE FOLLOWING
typeOfScore = "danceability" #can be replaces with danceability, energy, speechiness, acousticness, instrumentalness, liveness, valence, tempo
maximum = True #TRUE for maximum danceability / energy etc, FALSE for minimum
numberOfSongs = 75
playlistName = "dance 'till we die"
#  
#
#


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

nameScores = {}
scoreIDs = {}
ids = []
features = []

for playlist in allPlaylists: 
    plTracks = sp.user_playlist_tracks(playlist_id=playlist) 

    for item in plTracks["items"]:
        try:
            ids.append(item["track"]["id"])
        except:
            continue
    
idCopy = ids
while len(idCopy) > 100:
    features.extend(sp.audio_features(idCopy[:100])) #getting around API limit of 100 tracks per "sp.audio_features"
    idCopy = idCopy[100:] # removing the first 100 tracks from the copy of "ids" and then looping
features.extend(sp.audio_features(idCopy)) # putting the final tracks into features


for i in range(len(ids)):
    score = features[i][typeOfScore]
    scoreIDs[score] = ids[i]

#sorting the dictionary by score:
keys = list(scoreIDs.keys())
keys.sort(reverse=maximum)
newScoreIDs = {i: scoreIDs[i] for i in keys}



finalTracks = [] # final X tracks to be put into the playlist
n = 0
for score in newScoreIDs:
    finalTracks.append(newScoreIDs[score]) # gets the ID from the dictionary and puts it in finaltracks
    n += 1
    if n == numberOfSongs:
        break

myID = sp.me()["id"]

newPlaylist = (sp.user_playlist_create(myID,playlistName))["id"] # creates a new playlist and gets the id
sp.playlist_add_items(newPlaylist, finalTracks)
