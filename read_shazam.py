import pandas as pd
from datetime import datetime

# Prilagodi pot do tvoje CSV datoteke
file_path = 'shazamlibrary.csv'  # Ali ime, ki ga imaš

try:
    # Preberi CSV: Preskoči prvo vrstico (naslov), potem uporabi drugo kot header
    df = pd.read_csv(file_path, skiprows=1, encoding='utf-8')

    # Prikaz osnovnih info
    print("Število vnosov:", len(df))
    print("\nStolpci v datoteki:", list(df.columns))
    print("\nPrvih 5 vnosov:")
    print(df.head())

    # Preveri, ali stolpca obstajata, preden čisti
    if 'Artist' in df.columns and 'Title' in df.columns:
        # Čiščenje: Odstrani prazne vrstice ali duplicati
        df = df.dropna(subset=['Artist', 'Title'])
        df = df.drop_duplicates(subset=['Artist', 'Title'])
        print(f"\nPo čiščenju: {len(df)} unikatnih vnosov")
    else:
        print("\nOpozorilo: Ni stolpcev 'Artist' ali 'Title' – preveri stolpce zgoraj!")

    # Primeri analiz (samo če stolpca obstajata)
    if 'Artist' in df.columns:
        top_artists = df['Artist'].value_counts().head(10)
        print("\nTop 10 izvajalcev:")
        print(top_artists)

    if 'TagTime' in df.columns:
        df['TagTime'] = pd.to_datetime(df['TagTime'], errors='coerce')
        recent = df.nlargest(5, 'TagTime')
        print("\nNajnovejših 5 shazamov:")
        print(recent[['Artist', 'Title', 'TagTime']])

    # Shrani očiščeno verzijo (če je čiščenje poteklo)
    if 'Artist' in df.columns and 'Title' in df.columns:
        clean_file = f'clean_shazam_{datetime.now().strftime("%Y%m%d")}.csv'
        df.to_csv(clean_file, index=False, encoding='utf-8')
        print(f"\nOčiščena datoteka shranjena kot '{clean_file}'")
    else:
        print("\nNi očiščene datoteke – popravi stolpce ročno v Excelu, če rabiš.")

except FileNotFoundError:
    print(f"Datoteka '{file_path}' ni najdena. Preveri ime!")
except Exception as e:
    print(f"Napaka: {e}. Pošlji mi izhod za pomoč.")