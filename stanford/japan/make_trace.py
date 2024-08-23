import glob

print('date +"%Y-%m-%dT%H:%M:%S%z" > time.txt')
for id, filename in enumerate(sorted(glob.glob("/scratch/iiif_cache/japan/*.json"))):
    # if id >= 55:
    print(f"mapedge trace -s ./series/stanford/japan/default.json {filename} {id}")
    print('date +"%Y-%m-%dT%H:%M:%S%z" >> time.txt')
