import glob

for id, filename in enumerate(
    sorted(glob.glob("/scratch/iiif_cache/tmk_hires/*.json"))
):
    # if id >= 55:
    print(f"mapedge trace -s ./settings/tmk.json {filename} {id}")
