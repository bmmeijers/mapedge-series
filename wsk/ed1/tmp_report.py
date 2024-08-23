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
import csv


def main(folder_name, out_filename):
    glob_pattern = os.path.join(folder_name, "*.json")
    files = glob.glob(glob_pattern)
    files.sort()

    rows = []

    for filename in files:
        row = {}
        rows.append(row)

        # skip backup files
        if "~" in filename:
            continue
        i = int(filename.split("_")[-1].replace(".json", ""))
        number = f"{i:04}"
        with open(filename) as fp:
            J = json.load(fp)
            # print(J)

        row["number"] = number
        row["uuid"] = f"{J['uuid']}"
        row["iiif_url_overview"] = f"{J['iiif_end_point']}/full/512,/0/default.jpg"

        if "corners" in J:
            for sampling_strategy in ["outer", "outer-inner"]:
                if sampling_strategy == "outer":
                    frames = ["outer"]
                elif sampling_strategy == "outer-inner":
                    frames = ["outer", "inner"]

                for frame in frames:
                    for map_side in ["left", "right", "top", "bottom"]:
                        sampled_pts = J["samples"][sampling_strategy][frame][map_side]
                        indices_inliers = J["corners"]["inliers"][sampling_strategy][
                            frame
                        ][map_side]

                        if indices_inliers:
                            inlier_count = len(indices_inliers)
                        else:
                            inlier_count = 0
                        k = "__".join([map_side, frame, sampling_strategy, "inliers"])
                        row[k] = inlier_count

                        if sampled_pts:
                            sampled_count = len(sampled_pts)
                        else:
                            sampled_count = 0
                        k = "__".join(
                            [map_side, frame, sampling_strategy, "sampled_ct"]
                        )
                        row[k] = sampled_count

        if "corners" in J and "pixel_corner_points" in J["corners"]:
            # create 6 distances (also the diagonals)
            #
            # +-----------+
            # |           |
            # |           |
            # +-----------+

            distances = []
            if len(J["corners"]["pixel_corner_points"]) >= 4:

                for i in range(4):
                    for j in range(i + 1, 4):
                        delta = int(
                            dist(
                                J["corners"]["pixel_corner_points"][i],
                                J["corners"]["pixel_corner_points"][j],
                            )
                        )
                        distances.append(delta)
                for i, d in enumerate(distances):
                    row[f"distance_{i}"] = d

        if "corners" in J and "pixel_corner_points" in J["corners"]:

            if len(J["corners"]["pixel_corner_points"]) >= 4:
                row["tri_eq0__diagonal_calculated"] = int(
                    math.sqrt(distances[0] ** 2 + distances[2] ** 2)
                )
                row["tri_eq0__diagonal_distance"] = distances[4]
                row["tri_eq0__comparison"] = distances[4] - int(
                    math.sqrt(distances[0] ** 2 + distances[2] ** 2)
                )

                row["tri_eq1__diagonal_calculated"] = int(
                    math.sqrt(distances[3] ** 2 + distances[5] ** 2)
                )
                row["tri_eq1__diagonal_distance"] = distances[1]
                row["tri_eq1__comparison"] = distances[1] - int(
                    math.sqrt(distances[3] ** 2 + distances[5] ** 2)
                )

                row["tri_cmp_0plus1"] = abs(
                    (
                        distances[4]
                        - int(math.sqrt(distances[0] ** 2 + distances[2] ** 2))
                    )
                    + (
                        distances[1]
                        - int(math.sqrt(distances[3] ** 2 + distances[5] ** 2))
                    )
                )

                pairs = [(0, 5), (1, 4), (2, 3)]  # x diag y
                diffs = [abs(distances[j] - distances[i]) for i, j in pairs]

                for diff, label in zip(diffs, ["x", "diag", "y"]):
                    row[f"dist_diff_{label}"] = diff

    if rows:
        with open(out_filename, "w", newline="") as f:
            w = csv.DictWriter(f, rows[0].keys())
            w.writeheader()
            w.writerows(rows)
        print(f"Written {out_filename}")
    else:
        print("Empty output, no file written.")


# input_folder = "/tmp/corners_wsk_dlcs_ed1/"
# output_folder = "/tmp/corners_vis_corners2"

input_folder = "/tmp/corners/"
out_filename = "/tmp/report.csv"

main(input_folder, out_filename)
