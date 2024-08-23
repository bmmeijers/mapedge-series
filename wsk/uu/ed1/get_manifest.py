import requests
import os
import json


def get_json(url):
    r = requests.get(url)
    return r.json()


url = "https://objects.library.uu.nl/manifest/iiif/v2/1874-389916"
J = get_json(url)
# print(J)

cmds = []

item_id = 0
for sequence in J["sequences"]:
    for canvas in sequence["canvases"]:
        print(canvas["label"], ":", canvas["width"], "×", canvas["height"])
        for image in canvas["images"]:
            resource = image["resource"]
            print(item_id)
            print(resource.keys())
            print("-", resource["width"], "×", resource["height"])
            print("-", resource["service"])
            print("-", resource["service"]["@id"])
            oid = resource["service"]["@id"]
            fileid = oid.replace(
                "https://objects.library.uu.nl/fcgi-bin/iipsrv.fcgi?IIIF=/", ""
            )
            fileid = fileid.replace(".jp2", "")
            fileid = fileid.replace("/", "_")
            print("-", fileid)
            item_id += 1

            out = {
                "@id": resource["service"]["@id"],
                "width": resource["width"],
                "height": resource["height"],
            }

            filename = f"item_{item_id:04d}__{fileid}__info.json"
            with open(
                os.path.join("/scratch/iiif_cache/wsk_uu_ed1/", filename), "w"
            ) as fh:
                json.dump(out, fh)

            cmd = f"mapedge trace -s ./series/wsk/uu/ed1/settings.json /scratch/iiif_cache/wsk_uu_ed1/{filename} {item_id}"
            print(cmd)
            cmds.append(cmd)

with open("/tmp/trace.sh", "w") as fh:
    print("\n".join(cmds), file=fh)
