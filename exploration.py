import random
from spotipy_scripts import oauth,playlists

exit()
sp = oauth.authenticate()
myID = sp.me()["id"]


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

ids = playlists.get_all_user_tracks(sp,myID)
recs = generate_and_filter_recs(ids,number_of_songs=50,min_danceability=0.8,target_energy=1)
sp.playlist_add_items("5LUbuD9sYHdR5TspHLObu3", recs)


# create_playlist(recs,"this is a name")