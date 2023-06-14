import random
from spotipy_scripts import oauth, playlists
import string
import argparse
import os

sp = oauth.authenticate() # pass id=<CLIENT_ID> and
myID = sp.me()["id"]

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--length", help="Length of final playlist", type=int, default=100)
parser.add_argument("-c", "--characteristic", help="Type of characteristic to use. Choices are danceability,energy, speechiness, acousticness, instrumentalness, liveness, valence, tempo ", type=str, choices=["danceability", "energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"], default="danceability")
parser.add_argument("-m", "--maximum", help=" if True, then it'll find the songs with the highest score in the category and vice versa (so danceability / True would get the most danceable songs)", type=bool, default=True)
parser.add_argument("-u", "--user", help="User ID to search songs for", type=str, default=myID)
parser.add_argument("-n", "--name", help="Final playlist name", type=str, default=None)
parser.add_argument("-d", "--description", help="Final playlist description", type=str, default="https://github.com/devanshrpandey/spotify-danceability")
parser.add_argument("-p", "--public", help="Determines if the final playlist is public or not.", type=bool, default=True)
parser.add_argument("-s", "--shuffle", help="Determines whether or not to shuffle the final playlist values.", type=bool, default=True)
parser.add_argument("--limit", help="Number of playlists to search through", default=None, type=int)
args = parser.parse_args()







def getSortedScores(ids, characteristic, maximum=True):
    """
    gets the scores of the given characteristic for each song in the list of IDs and returns a dictionary with the scores as keys and the IDs as values, sorted by score
    parameters:
        ids: list of song IDs
        characteristic: string of the characteristic to be sorted by - "danceability", "energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"
        maximum: boolean - if True, then it'll find the songs w/ highest score in the category and vice versa (so "danceability" / True would get the most danceable songs)
    """
    idCopy = ids

    scoreIDmap = (
        {}
    )  # creates a dictionary with scores as keys and IDs as values, to later sort
    features = []

    while len(ids) > 100:
        features.extend(
            sp.audio_features(ids[:100])
        )  # getting around API limit of 100 tracks per "sp.audio_features"
        ids = ids[
            100:
        ]  # removing the first 100 tracks from the copy of "ids" and then looping
    features.extend(sp.audio_features(ids))  # pushing the final tracks into features

    for i in range(len(idCopy)):
        score = features[i][characteristic]
        scoreIDmap[score] = idCopy[i]
    # sorting the dictionary by score:
    keys = list(scoreIDmap.keys())
    keys.sort(reverse=maximum)
    sortedScores = {i: scoreIDmap[i] for i in keys}

    return sortedScores


def main(
    playlist_name, playlist_length, characteristic, maximum, user,description,public,shuffle,limit
):
    username = sp.user(user)["display_name"]

    if not playlist_name:
        playlist_name = string.capwords(f"{username}'s {characteristic} playlist")
                                        
    songIDs = playlists.get_all_user_track_ids(sp,user,limit=limit)

    scores = getSortedScores(songIDs, characteristic=characteristic, maximum=maximum)
    final_tracks = []  # final X tracks to be put into the playlist
    n = 0
    final_tracks = list(scores.values())[:playlist_length]

    score_list = list(scores.keys())[:playlist_length]

    avg_score = round(sum(score_list) / len(score_list),3)

    new_playlist = playlists.create_new_playlist(sp, user, ids=final_tracks,name=playlist_name,public=public,description=description,shuffle=shuffle)


    return characteristic, avg_score, new_playlist



characteristic, avg_score, new_playlist = main(
    playlist_name = args.name,
    playlist_length = args.length,
    characteristic = args.characteristic,
    maximum = args.maximum,
    user = args.user,
    description = args.description,
    public = args.public,
    shuffle = args.shuffle,
    limit = args.limit
    )


playlist_url = new_playlist["external_urls"]["spotify"]
print (f"Playlist created! The average {characteristic} score of this playlist is {avg_score}. Find the playlist here: {playlist_url}")