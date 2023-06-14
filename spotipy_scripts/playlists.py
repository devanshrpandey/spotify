import random
import asyncio


async def get_playlist_track_ids_async(sp, playlist_id):
    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(None, sp.playlist_items, playlist_id, "items(track(id)),next")

    tracks = results["items"]
    while results["next"]:
        results = await loop.run_in_executor(None, sp.next, results)
        tracks.extend(results["items"])
    track_ids = [track["track"]["id"] for track in tracks if track["track"]["id"]]
    return track_ids

def get_playlist_track_ids(sp, playlist_id):
    """
    Returns a list of all tracks in a playlist given playlist ID.
    parameters:
        sp: spotipy object
        playlist_id: string, can be URL, URI, or the ID
    """
    return asyncio.run(get_playlist_track_ids_async(sp, playlist_id))



async def get_all_user_track_ids_async(sp,user_id,limit):

    if limit is not None and limit <= 50:
        playlists = sp.user_playlists(user_id,limit=limit)["items"]
    else:
        playlist_object = sp.user_playlists(user_id)
        playlists = playlist_object["items"]
        while playlist_object["next"]:
            playlist_object = sp.next(playlist_object)
            playlists.extend(playlist_object["items"])
    
    tasks = [get_playlist_track_ids_async(sp, playlist["id"]) for playlist in playlists]
    results = await asyncio.gather(*tasks)
    track_ids = []
    for playlist_track_ids in results:
        track_ids.extend(playlist_track_ids)
    return track_ids

def get_all_user_track_ids(sp,user_id,limit=None):
    """
    Returns a list of all tracks in all of a user's playlists.
    parameters:
        sp: spotipy object
        user_id: string, can be URL, URI, or the ID of any user
        return_type: string, either "tracks" or "ids"
    """
    return asyncio.run(get_all_user_track_ids_async(sp,user_id,limit=limit))


def create_new_playlist(sp,user_id,ids,name,public,description,shuffle):
    """
    Creates a new playlist and adds tracks to it given a list of ids.
    parameters:
        sp: spotipy object
        name: string, name of new playlist
        ids: list of strings, track IDs
        public: boolean, whether or not the playlist is public
        description: string, description of new playlist
        shuffle: boolean, whether or not to shuffle the playlist before writing
    """
    newPlaylist = sp.user_playlist_create(user_id, name)  # creates a new playlist
    sp.playlist_add_items(newPlaylist["id"], ids)
    return newPlaylist