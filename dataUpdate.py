import requests
import csv
import pandas as pd
import os

# STAC Items endpoint
URL_ITEMS = "https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-smn/items"

OUTPUT_CSV = "toutes_mesures_concatenees.csv"
TEMP_DIR = "donnees_temp"

os.makedirs(TEMP_DIR, exist_ok=True)

# Récupérer tous les items avec pagination
print("Récupérer tous les items avec pagination")
items = []
url = URL_ITEMS
while url:
    r = requests.get(url)
    data = r.json()
    items.extend(data["features"])
   # url = data.get("links", {}).get("next", None)
     
    url = next((link["href"] for link in data.get("links", []) if link.get("rel") == "next"), None)

print(f"{len(items)} fichiers STAC trouvés")

# Télécharger les CSV associés
csv_files = []
for item in items:
    assets = item.get("assets", {})
    for name, asset in assets.items():
        if asset["type"] == "text/csv":
            csv_url = asset["href"]
            local_path = os.path.join(TEMP_DIR, f"{item['id']}.csv")
            try:
                r = requests.get(csv_url)
                r.raise_for_status()
                with open(local_path, "wb") as f:
                    f.write(r.content)
                csv_files.append(local_path)
                print(f"Téléchargé : {csv_url}")
            except Exception as e:
                print(f"Erreur sur {csv_url} : {e}")