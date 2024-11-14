import os
from mapedge.lib.visualize import make_simple_svg_mask
import json
import csv


import uuid


with open(os.path.join(os.path.dirname(__file__), "uu-ed2.csv")) as csvfile:
    reader = csv.reader(csvfile)
    records = [row for row in reader]

print(records)
### make corners to show full image
output_folder_name = "/tmp/start_annotate"
os.makedirs(output_folder_name, exist_ok=True)
for i, record in enumerate(records, start=1):
    # label, width, height, iiif_url = record
    (
        fid,
        edition,
        sheet_id,
        sub_sheet_id,
        sheet,
        sheet_title,
        remark,
        id,
        iiif_url,
        width,
        height,
    ) = record
    # resource = image["resource"]
    # uuid = resource["service"]["@id"].split("/")[-1]
    # # print(resource.keys())
    # print("-", resource["service"]["width"], "×", resource["service"]["height"])
    # print("-", resource["service"]["@id"])
    # print("-", resource["service"]["@id"] + "/full/!1024,1024/0/default.jpg")

    # w, h = resource["service"]["width"], resource["service"]["height"]
    # the corners of the image, starting bottom left, going ccw
    # with y positive down

    # uuid = i
    image_corners = [(0, height), (width, height), (width, 0), (0, 0)]
    svg_mask = make_simple_svg_mask([width, height], image_corners)

    # write out corners json
    out = {}
    out["corners"] = {
        "pixel_corner_points": image_corners,
        "svg_mask": svg_mask,
    }
    oid = str(uuid.uuid4())
    out["uuid"] = oid
    out["sheet"] = sheet
    out["iiif_end_point"] = iiif_url.replace("/info.json", "")
    print(out["iiif_end_point"])

    with open(os.path.join(output_folder_name, f"out-{i}.json"), "w") as fh:
        json.dump(out, fh)
