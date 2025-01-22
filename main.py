import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy import SpotifyOAuth
import os

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

user_input = input("What year do you want to travel to? (YYYY-MM-DD): ")
url = "https://www.billboard.com/charts/hot-100/" + user_input


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
}


response = requests.get(url=url, headers=header)
website = response.text
# print(website)

soup = BeautifulSoup(website, "html.parser")
song_name_spans = soup.select("li ul li h3")

song_title_list = [title.getText().strip() for title in song_name_spans]
# print(song_title_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://localhost:4304/auth/spotify/callback",
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt",
    username="alexanderpasaribu99"
    )
)

user_id = sp.current_user()["id"]

song_uris = []
year = user_input.split("-")[0]
for song in song_title_list:
    result = sp.search(q=f"Track:{song} Year: {year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
# print(song_uris)

playlist = sp.user_playlist_create(user=user_id, public=False, name=f"{user_input} Billboard 100")
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)