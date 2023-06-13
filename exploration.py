import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import random

os.environ["SPOTIPY_CLIENT_ID"] = "375c8e4a9f8d4243996d256ff41daa62"
os.environ["SPOTIPY_CLIENT_SECRET"] = "1472274bf789453bbd1ed42c9ee181da"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:9090"
scope = "user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-read-playback-position user-top-read user-read-recently-played user-library-read user-library-modify"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
myID = sp.me()["id"]

def getsongIDs(numberOfPLstoSearch=50,user=myID):
    if numberOfPLstoSearch > 50:
        numberOfPLstoSearch = 50
        print("Number of playlists searched has been capped at 50 as that is the maximum the Spotify API allows.")
    pls = sp.user_playlists(user,limit=numberOfPLstoSearch)["items"]
    allPlaylists = []
    for pl in pls: 
        allPlaylists.append(pl["id"]) #create an array of all playlist ids

    songIDs = []
    for playlist in allPlaylists: 
        plTracks = sp.user_playlist_tracks(playlist_id=playlist) 
        for item in plTracks["items"]:
            try:
                songIDs.append(item["track"]["id"])
            except:
                continue
    random.shuffle(songIDs)
    return songIDs

def split_list(old_list):
        new_list = []
        for i in range(0, len(old_list), 5):
            try:
                new_list.append(old_list[i:i+5])
            except:
                break
    #splits list into lists of 5 songs each
        random.shuffle(new_list)
        return new_list

def generate_and_filter_recs(song_IDs,temperature=0.25,final_length=100,**kwargs): #temperature = what # of songs to use, # final_length = number of songs in final playlist

    recs = []

    split_ids = split_list(song_IDs)
    length_of_gens = round(len(split_ids)*temperature)
    split_ids = split_ids[:length_of_gens]
    songs_per_rec = round(final_length/length_of_gens)

    for songs in split_ids:
        recdict = sp.recommendations(seed_tracks=songs,limit=songs_per_rec)
        for rec in recdict["tracks"]:
            if rec not in song_IDs:
                recs.append(rec["id"])
    return recs

def create_playlist(tracks,playlist_name):
    new_playlist = (sp.user_playlist_create(myID,playlist_name)) # creates a new playlist
    sp.playlist_add_items(new_playlist["id"], tracks)
    return new_playlist

ids = getsongIDs()
recs = generate_and_filter_recs(ids,number_of_songs=25,min_danceability=0.8,target_energy=1)

create_playlist(recs,"this is a name")