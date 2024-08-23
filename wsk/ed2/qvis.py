import math
from mapedge.lib.fit.line2 import Line2
from mapedge.lib.visualize.svg_visualizer import SVGVisualizer
import glob
import os
import json
import numpy as np

import os

from mapedge.lib.trace.vectorops import add, dist, mul
from itertools import chain


def main(folder_name, output_folder_name):

    # folder_name = "/scratch/iiif_inspect/north_korea/"
    # folder_name = "/scratch/iiif_inspect/tmk_hires/"  # point_sample_0008.json"
    # output_folder_name = "/tmp/tmk"

    # make sure we can write into output_folder_name
    os.makedirs(output_folder_name, exist_ok=True)
    glob_pattern = os.path.join(folder_name, "*.json")
    files = glob.glob(glob_pattern)
    files.sort()

    # size = (256, 256)
    size = (512, 512)
    vis = SVGVisualizer(size)
    vis.add_crop_mark(mul(size, (0.5, 0.5)))
    svg_file = "cropmark.svg"
    out_filename = os.path.join(output_folder_name, svg_file)
    with open(out_filename, "w") as fh:
        print(vis.show(), file=fh)

    out_id = 0
    html = """<!doctype html><html><head>
<style>
.parent {
  position: relative;
  top: 0;
  left: 0;
}
.image1 {
  position: relative;
  top: 0;
  left: 0;
  border: 1px red solid;
}
.image2 {
  position: absolute;
  top: 0px;
  left: 0px;
  border: 1px green solid;
}
</style>

<link rel="stylesheet" href="https://cdn.datatables.net/2.0.7/css/dataTables.dataTables.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
<script src="https://cdn.datatables.net/2.0.7/js/dataTables.min.js"></script>
<script>
document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM fully loaded and parsed");
    let table = new DataTable('#reportTable');

});
</script>

</head>
<body>
<table id="reportTable">
"""
    html += "<thead><tr><th>number</th><th>uuid</th><th>thumbnail</th><th>top left</th><th>top right</th><th>bottom left</th><th>bottom right</th></tr></thead>"

    html += "<tbody>"
    for filename in files:
        html += "<tr>"
        # skip backup files
        if "~" in filename:
            continue
        i = int(filename.split("_")[-1].replace(".json", ""))
        number = f"{i:04}"
        with open(filename) as fp:
            J = json.load(fp)
            # print(J)
        html += f"<td>{number}</td><td>{J['uuid']} </td>"

        if "corners" in J and "pixel_corner_points" in J["corners"]:
            tsize = size[0]
            iiif_url_overview = f"{J['iiif_end_point']}/full/,{tsize}/0/default.jpg"

            html += f'<td><img loading="lazy" src="{iiif_url_overview}" height="{tsize}"></td>'

            if len(J["corners"]["pixel_corner_points"]) >= 4:
                # print(J["corners"]["pixel_corner_points"])
                for pt in chain(
                    [J["corners"]["pixel_corner_points"][3]],
                    [J["corners"]["pixel_corner_points"][2]],
                    J["corners"]["pixel_corner_points"][:2],
                ):
                    # vis = SVGVisualizer(size)
                    # cx, cy = pt[0], pt[1]

                    # make a centered rectangle

                    to_add = mul(size, (-0.5, -0.5))
                    tl = tuple(map(int, add(pt, to_add)))

                    corner_url = f"{J['iiif_end_point']}/{tl[0]},{tl[1]},{size[0]},{size[1]}/{size[0]},{size[1]}/0/default.jpg"
                    # print(corner_url)
                    # vis.add_xlink_image(corner_url)
                    # vis.add_crop_mark(mul(size, (0.5, 0.5)))
                    # svg_file = f"corner_{out_id}.svg"
                    # out_filename = os.path.join(output_folder_name, svg_file)
                    # with open(out_filename, "w") as fh:
                    #     print(vis.show(), file=fh)

                    out_id += 1
                    html += "<td>"
                    html += '<div class="parent" style="margin:1em; display: inline-block;">'
                    img_tag = f'<img class="image1" src="{corner_url}" width="{size[0]}" height="{size[1]}" loading="lazy">'
                    html += img_tag
                    img_tag = f'<img class="image2" src="cropmark.svg" width="{size[0]}" height="{size[1]}" loading="lazy">'
                    html += img_tag
                    html += "</div>"
                    html += "</td>"
        html += "</tr>"
    html += "</tbody>"
    html += """</table></body></html>"""

    out_filename = os.path.join(output_folder_name, "index.html")
    with open(out_filename, "w") as fh:
        fh.write(html)

    print(f"Written {out_filename}")
    # os.system(f"xdg-open {out_filename}")


# input_folder = "/tmp/corners_wsk_dlcs_ed1/"
# output_folder = "/tmp/corners_vis_corners2"

input_folder = "/tmp/corners-wsk-ed2/"
output_folder = "/tmp/out-wsk-ed2/"

# input_folder = "/tmp/corners-wsk/"
# output_folder = "/tmp/out-wsk-uu/"
# input_folder = "/tmp/corners/"
# output_folder = "/tmp/out-tmk/"
main(input_folder, output_folder)
