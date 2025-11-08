import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv  # Dodano za .env
import os  # Za branje spremenljivk

# Naloži .env datoteko
load_dotenv()

# TVOJI PODATKI
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = 'https://localhost:8888/callback'
SCOPE = 'playlist-modify-public playlist-modify-private'
USERNAME = os.getenv('USERNAME')


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))

# Naloži CSV
df = pd.read_csv('clean_shazam_20251106.csv')  # Prilagodi ime

# Primer: Kategoriziraj po desetletju (uporabi Spotify search za release year)
df['Decade'] = 'Unknown'
uris = []

for idx, row in df.iterrows():
    try:
        results = sp.search(q=f"track:{row['Title']} artist:{row['Artist']}", type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            release_year = int(track['album']['release_date'][:4]) if track['album']['release_date'] else 0
            decade = f"{(release_year // 10) * 10}s"
            df.at[idx, 'Decade'] = decade
            df.at[idx, 'Spotify URI'] = track['uri']
            uris.append(track['uri'])  # Za eno veliko playlisto
    except:
        pass

# Ustvari playliste po kategorijah
unique_decades = df['Decade'].unique()
for decade in unique_decades:
    if decade != 'Unknown':
        playlist_df = df[df['Decade'] == decade]
        playlist_uris = playlist_df['Spotify URI'].dropna().tolist()
        if playlist_uris:
            playlist = sp.user_playlist_create(USERNAME, f"My Shazam {decade}", public=True, description=f"{len(playlist_uris)} pesmi iz Shazama")
            sp.playlist_add_items(playlist['id'], playlist_uris)
            print(f"Ustvarjen playlist '{decade}': {len(playlist_uris)} pesmi!")

# Bonus: Ena velika "All Shazam" playlista
if uris:
    all_playlist = sp.user_playlist_create(USERNAME, "All My Shazams", public=True)
    sp.playlist_add_items(all_playlist['id'], uris[:100])  # Limit 100 na klic, dodaj loop če več
    print("Ustvarjena 'All My Shazams' playlista!")

df.to_csv('shazam_with_uris.csv', index=False)
print("Končano! Preveri v Spotify app-u.")