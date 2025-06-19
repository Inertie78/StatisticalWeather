import requests
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# STAC Items endpoint
URL_ITEMS = "https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-smn/items"

TEMP_DIR = "donnees_temp"
LOG_FILE = "erreurs_log.txt"

# Création du répertoire temporaire
os.makedirs(TEMP_DIR, exist_ok=True)

def telecharger_csv(item):
    """Télécharge un fichier CSV associé à un item STAC"""
    assets = item.get("assets", {})
    for name, asset in assets.items():
        if asset["type"] == "text/csv":
            csv_url = asset["href"]
            local_path = os.path.join(TEMP_DIR, f"{item['id']}.csv")
            try:
                response = requests.get(csv_url, timeout=10)
                response.raise_for_status()
                with open(local_path, "wb") as f:
                    f.write(response.content)
                print(f"Téléchargé : {csv_url}")
                return local_path
            except Exception as e:
                with open(LOG_FILE, "a") as log:
                    log.write(f"Erreur sur {csv_url} : {e}\n")
                print(f"Erreur sur {csv_url} : {e}")
                return None
    return None
def updateData():
    # Récupération des items STAC avec pagination
    print("📡 Récupération des items avec pagination...")
    items = []
    url = URL_ITEMS
    while url:
        try:
            response = requests.get(url)
            data = response.json()
            items.extend(data["features"])
            url = next((link["href"] for link in data.get("links", []) if link.get("rel") == "next"), None)
        except Exception as e:
            print(f"Erreur de récupération des items STAC : {e}")
            break

    print(f"📂 {len(items)} fichiers STAC trouvés")

    # Téléchargement en parallèle
    csv_files = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(telecharger_csv, items)

    csv_files = [file for file in results if file]



    ### 🛠 **Fusion intelligente des fichiers CSV**
    #Cette méthode combine les fichiers CSV même s'ils ont des colonnes différentes :

def combines():

    df_list = []
    current_directory = os.getcwd()

    folder_path = current_directory + "\\data\\dataTemp\\month"
    csv_files = os.listdir(folder_path)

    OUTPUT_CSV = "\\data\\dataWeather.csv"

    for file in csv_files:
        try:
            file_path = folder_path + '\\' + file
            # Get the file size in bytes
            file_size = os.path.getsize(file_path) / 1024

            if file_size > 1000:
                df = pd.read_csv(folder_path + '\\' + file)
                df_list.append(df)
    
        except Exception as e:
            print(f"⚠️ Erreur de lecture {file} : {e}")

    # Concaténation avec gestion des colonnes manquantes
    if df_list:
        df_final = pd.concat(df_list, ignore_index=True, sort=False)
        df_final.to_csv(current_directory + OUTPUT_CSV, index=False)
        print(f"✅ Fichier final enregistré sous {OUTPUT_CSV}")


#updateData()
combines()