# spotify-danceability

- To use the code with your own API keys, go to https://developer.spotify.com/dashboard/applications and then create an application with redirect URL as http://localhost:9090 in the application settings. You can then edit the client ID and client secret environment variables as you wish, edit the type of score, and run the code.

- To use the code with these API keys (if you don't want to deal w/ it or don't have premium) DM me at devansh#0001 and I can add you as an authorized user of the application.

Edit the code as you wish (in "EDIT THE FOLLOWING" on main.py) and then run it by navigating to the directory it's in and running

python3 main.py

You may have to install packages; "pip install spotipy" should be the only relevant one.

### How does it work?
Essentially, the tool searches through the last N playlists added to Your Library (*including* any playlists you've added or saved, even if they're made by other people.) It then ranks all of these songs by some metric - like danceability, or energy, or acousticness, and creates a playlist with the top N songs along this category.