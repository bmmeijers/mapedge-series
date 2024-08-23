import os
import json
import requests
from mapedge.lib.visualize import make_simple_svg_mask

# make corner.json files as a start
# this puts the full image into the rectangle allocated in the sheet index (if run through annotate)


def get_json(url):
    r = requests.get(url)
    return r.json()


output_folder_name = "/tmp/start_annotate"
os.makedirs(output_folder_name, exist_ok=True)

url = "https://dlc.services/iiif-resource/7/string1string2string3/waterstaatskaart/3/1"
J = get_json(url)
print(J)

records = []
# in dit manifest zijn de bladen alfabetisch geordend, dus oost komt voor west
# geografisch springt dit dus heen en weer over de x-as (eerst rechts, dan links, dan over rechts, etc)
for sequence in J["sequences"]:
    for canvas in sequence["canvases"]:
        for image in canvas["images"]:
            resource = image["resource"]
            uuid = resource["service"]["@id"].split("/")[-1]
            # print(resource.keys())
            print("-", resource["service"]["width"], "×", resource["service"]["height"])
            print("-", resource["service"]["@id"])
            print("-", resource["service"]["@id"] + "/full/!1024,1024/0/default.jpg")

            w, h = resource["service"]["width"], resource["service"]["height"]
            # the corners of the image, starting bottom left, going ccw
            # with y positive down
            image_corners = [(0, h), (w, h), (w, 0), (0, 0)]
            svg_mask = make_simple_svg_mask([w, h], image_corners)

            # write out corners json
            out = {}
            out["corners"] = {
                "pixel_corner_points": image_corners,
                "svg_mask": svg_mask,
            }
            out["uuid"] = uuid
            out["iiif_end_point"] = resource["service"]["@id"].replace(
                "https://dlc.services/iiif-img/7/32",
                "https://dlc.services/iiif-img/v3/7/32",
            )

            with open(os.path.join(output_folder_name, f"out-{uuid}.json"), "w") as fh:
                json.dump(out, fh)
