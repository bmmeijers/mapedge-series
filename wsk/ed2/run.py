import glob
import os

folder_in = "/scratch/iiif_cache/waterstaatskaart_edition_2/"
folder_settings = "./series/wsk/ed2/"
for id, filename in enumerate(sorted(glob.glob(os.path.join(folder_in, "*.json")))):
    # if id >= 55:
    print(
        f".venv/bin/mapedge trace -s {os.path.join(folder_settings, 'settings.json')} '{filename}' {id}"
    )
