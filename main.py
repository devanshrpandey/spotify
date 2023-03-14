import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#
#
#EDIT THE FOLLOWING
typeOfScore = "danceability" #can be replaces with energy, speechiness, acousticness, instrumentalness, liveness, valence, tempo
maximum = True #TRUE for maximum danceability / energy etc, FALSE for minimum
numberOfSongs = 100
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



for playlist in allPlaylists: 
    plTracks = sp.user_playlist_tracks(playlist_id=playlist) 
    ids = []

    for item in plTracks["items"]:
        ids.append(item["track"]["id"])
    
    features = sp.audio_features(ids) #looping it is how you get around the 100-track limit for sp. audio_features, but it does call the api once per playlist :/
    for i in range(len(ids)):
        
        score = features[i][typeOfScore]
        
        scoreIDs[score] = ids[i]
        #nameScores[name] = score 
        #name = (plTracks["items"][i]["track"]["name"])

#sorting the dictionary by score:
keys = list(scoreIDs.keys())
keys.sort(reverse=maximum)
newScoreIDs = {i: scoreIDs[i] for i in keys}

print(newScoreIDs)



finalTracks = [] # final X tracks to be put into the playlist
n = 0
for score in scoreIDs:
    finalTracks.append(scoreIDs[score]) # gets the ID from the dictionary and puts it in finaltracks
    n += 1
    if n == numberOfSongs:
        break

myID = sp.me()["id"]

newPlaylist = (sp.user_playlist_create(myID,playlistName))["id"] # creates a new playlist and gets the id

print(finalTracks)

sp.playlist_add_items(newPlaylist, finalTracks)


