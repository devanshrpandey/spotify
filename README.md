# spotify-danceability

- To use the code with your own API keys, go to https://developer.spotify.com/dashboard/applications and then create an application with redirect URI as http://localhost:9090 in the application settings. **To run the code using your own API keys, simply set the env variables as follows:**

```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-uri'
```

- To use the code with my API keys (if you don't want to deal w/ it or don't have premium) DM me @devansh on Discord and I can add you as an authorized user of the application.

- To run the danceability code, run:
```
pip install -r requirements.txt
python danceability.py --help
```
You'll get a list of flags that you can use to customize and modify the playlist that gets created.

### How does it work?
The danceability tool searches through the last N playlists added to Your Library (*including* any playlists you've added or saved, even if they're made by other people.) It then ranks all of these songs by some metric - like danceability, or energy, or acousticness, and creates a playlist with the top N songs along this category.


## spotify-exploration

**THE EXPLORATION CODE IS CURRENTLY UNDER CONSTRUCTION AND IS NOT YET READY FOR USE**

- Same thing w/r/t API keys above

- To run the exploration code, **first edit the code to your liking (it has not yet become flagged)** and then run:
```
pip install -r requirements.txt
python exploration.py
```