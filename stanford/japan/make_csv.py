import json
import os
import requests

with open(
    os.path.join(os.path.dirname(__file__), "stanford-ph028ym3863-geojson.json")
) as fp:
    J = json.load(fp)

tpl = "https://stacks.stanford.edu/image/iiif/{oid}/{oid}_00_0001/info.json"

with open(os.path.join(os.path.dirname(__file__), "wget.sh"), "w") as fh:
    # print(";".join(["oid", "purl", "iiif"]), file=fh)
    for feature in J["features"]:

        oid = feature["properties"]["purl"].replace("http://purl.stanford.edu/", "")

        # print(
        #     ";".join([oid, feature["properties"]["purl"], tpl.format(oid=oid)]), file=fh
        # )
        print(f"wget -O {oid}.json { tpl.format(oid=oid)}", file=fh)

    # c = requests.get(os.path.join(feature["properties"]["purl"], "iiif/manifest"))
    # K = c.json()
    # for seq in K["sequences"]:
    #     for canvas in seq["canvases"]:
    #         for image in canvas["images"]:
    #             print(
    #                 feature["properties"]["purl"],
    #                 ";",
    #                 image["resource"]["service"]["@id"],
    #             )
