#
# <https://objects.library.uu.nl/reader/index.php?obj=1874-455650&lan=en>

import os
import json
import requests
from mapedge.lib.visualize import make_simple_svg_mask


version = "v3"  # v2 | v3
manifest_url = f"https://objects.library.uu.nl/manifest/iiif/{version}/1874-455650"
J = requests.get(manifest_url).json()

if version == "v3":

    records = []

    for item in J["items"]:
        item_type = item["type"]
        match item_type:
            case "Canvas":
                # print(item.keys())
                canvas = item
                print(canvas)
                for canvas_item in canvas["items"]:
                    # print(canvas_item.keys())
                    canvas_item_type = canvas_item["type"]

                    match canvas_item_type:
                        case "AnnotationPage":
                            for annotation_page in canvas_item["items"]:
                                body = annotation_page["body"]
                                print(annotation_page)
                                width = body["width"]
                                height = body["height"]

                                for service in body["service"]:
                                    print(f"{service=}")
                                    record = (
                                        canvas["label"]["none"][0],
                                        width,
                                        height,
                                        os.path.join(service["id"], "info.json"),
                                    )
                                    #     )
                                    # )
                                    print(service["type"])
                                    print(service["profile"])
                                    records.append(record)
                        case _:
                            raise ValueError(f"unknown type {canvas_item_type}")
            case _:
                raise ValueError("unmatched item_type")

    with open(os.path.join(os.path.dirname(__file__), "trace2.sh"), "w") as fh:
        print(f"# {manifest_url}", file=fh)
        # print("id,iiif_url,width,height", file=fh)
        for i, record in enumerate(records, start=1):
            label, width, height, iiif_url = record
            print(
                f"mapedge trace-new -s ./series/wsk/uu/ed2/settings.json {iiif_url} {i}",
                # f"{label},{iiif_url},{width},{height}",
                file=fh,
            )
