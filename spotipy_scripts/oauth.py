import spotipy
import os

def authenticate(id="375c8e4a9f8d4243996d256ff41daa62",secret="1472274bf789453bbd1ed42c9ee181da",uri="http://localhost:9090"):
    os.environ["SPOTIPY_CLIENT_ID"] = id
    os.environ["SPOTIPY_CLIENT_SECRET"] = secret
    os.environ["SPOTIPY_REDIRECT_URI"] = uri
    scope = "user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-read-playback-position user-top-read user-read-recently-played user-library-read user-library-modify"
    sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(scope=scope))
    return sp

if __name__ == "__main__":
    sp = authenticate()
    print(sp.me()["id"])