import os
import pandas as pd

print("Concaténer tous les fichiers CSV")

current_directory = os.getcwd()

folder_path = current_directory + "\\data\\dataTemp"

csv_files = os.listdir(folder_path)

OUTPUT_CSV = current_directory + "\\data\\dataWeather.csv"

# Concaténer tous les fichiers CSV
dfs = []
for file in csv_files:
    try:
        df = pd.read_csv(folder_path + "\\" + file)
        dfs.append(df)
    except Exception as e:
        print(f"Erreur lecture {file} : {e}")

if dfs:
    df_concat = pd.concat(dfs, ignore_index=True)
    df_concat.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ CSV final généré : {OUTPUT_CSV} ({len(df_concat)} lignes)")
else:
    print("❌ Aucun fichier valide trouvé.")