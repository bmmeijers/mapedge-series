#
# The files this script generates can be used to generate an annotation file
# thus all the original IIIF images (with their full size) are then layed out according to the sheet index
#
# For example, using uuid as column and ...uuid.geojson as sheet index
# the jsons geneated by this script generated in /tmp/start_annotate
# can be placed inside an annotation as follows:
# ```
# mapedge annotate -s uuid /home/martijn/Documents/work/2023-08_synthesis/mapedge/series/wsk/ed2/waterstaatskaart-ed2-poly_uuid.geojson /tmp/start_annotate/*.json /tmp/multiple_page.json
# ```


import glob
import os
import json
from mapedge.lib.visualize import make_simple_svg_mask

# the original info.json's from the image server
dirname = "/scratch/iiif_cache/waterstaatskaart_edition_2/"

# the folder where to place the jsons with corner point and mask information

output_folder_name = "/tmp/start_annotate"
os.makedirs(output_folder_name, exist_ok=True)

for filename in sorted(glob.glob(os.path.join(dirname, "*.json"))):
    J = json.load(open(filename))
    uuid = J["@id"].split("/")[-1]

    w, h = J["width"], J["height"]
    # the corners of the image, starting bottom left, going ccw
    # with y positive down
    image_corners = [(0, h), (w, h), (w, 0), (0, 0)]
    svg_mask = make_simple_svg_mask([w, h], image_corners)

    out = {}
    out["corners"] = {
        "pixel_corner_points": image_corners,
        "svg_mask": svg_mask,
    }
    out["uuid"] = uuid
    out["iiif_end_point"] = J["@id"]

    with open(os.path.join(output_folder_name, f"out-{uuid}.json"), "w") as fh:
        json.dump(out, fh)
