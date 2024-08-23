import glob

for id, filename in enumerate(
    sorted(glob.glob("/scratch/iiif_cache/waterstaatskaart_edition_1/*.json"))
):
    # if id >= 55:
    print(f"mapedge trace -s ./series/wsk/ed1/settings.json '{filename}' {id}")
