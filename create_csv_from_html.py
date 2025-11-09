'''Converts HTML page of apple music library (idea that you transfer it from shazam)
to CSV'''

from bs4 import BeautifulSoup
import pandas as pd

input_file = 'faking_skladbe.html'
output_file = 'shazam_tracks.csv'

# Preberi HTML
with open(input_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Najdi vse vrstice skladb
rows = soup.find_all('div', class_='songs-list-row', attrs={'data-testid': 'track-list-item'})

tracks = []
for row in rows:
    aria_label = row.get('aria-label', '').strip()

    # Apple Music zapiše npr. "Reality (feat. Janieck Devy), Lost Frequencies"
    if ',' in aria_label:
        parts = [p.strip() for p in aria_label.split(',', 1)]
        title = parts[0]
        artist = parts[1]
    else:
        title = aria_label
        artist = 'Unknown'

    # Album
    album_elem = row.find('div', class_='songs-list__col--tertiary')
    album = album_elem.get_text(strip=True) if album_elem else 'Unknown'

    # Trajanje
    time_elem = row.find('time', class_='songs-list-row__length')
    duration = time_elem.get_text(strip=True) if time_elem else 'Unknown'

    tracks.append({
        'Title': title,
        'Artist': artist,
        'Album': album,
        'Duration': duration
    })

df = pd.DataFrame(tracks)
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"Izvučenih {len(df)} skladb v '{output_file}'!")
print(df.head())
