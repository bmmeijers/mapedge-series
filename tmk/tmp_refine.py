import glob
import json

from matplotlib import pyplot as plt

from mapedge.lib.trace.centered_rect import CenteredRectangle
from mapedge.lib.trace.detect_frame import apply_pipeline
from mapedge.lib.trace.detect_rim import center_coordinates, search_rim
from mapedge.lib.trace.iiif_image_load import iiif_image_from_url

from mapedge.lib.visualize.svg_visualizer import SVGVisualizer
from mapedge.lib.trace.vectorops import add, mul

import os

os.makedirs("/tmp/corner-test", exist_ok=True)

for i, filename in enumerate(sorted(glob.glob("/tmp/corners/ransac__*.json"))):

    with open(filename) as fh:
        J = json.load(fh)
    url = J["iiif_end_point"]
    iiif_url_overview = f"{J['iiif_end_point']}/full/full/0/default.jpg"

    vis = SVGVisualizer(J["image_size"])
    vis.add_xlink_image(iiif_url_overview)

    print(J["corners"]["pixel_corner_points"])

    w, h = 800, 40
    sizes = [(w, h), (h, w)]  # make horizontal and vertical rectangle
    pairs = []
    for size in sizes:
        for c in J["corners"]["pixel_corner_points"]:
            pairs.append([c, size])
    print(len(pairs))

    MAG = 0.5

    def up(size):
        ret = mul(size, [0, -MAG])
        print(f"up {size} {ret}")
        return ret

    def down(size):
        ret = mul(size, [0, +MAG])
        print(f"down {size} {ret}")
        return ret

    def left(size):
        # print(f"left {size}")
        # return size
        ret = mul(size, [-MAG, 0])
        print(f"left {size} {ret}")
        return ret

    def right(size):
        # print(f"right {size}")
        # return size
        ret = mul(size, [+MAG, 0])
        print(f"right {size} {ret}")
        return ret

    # functions to apply to the 8 rectangles
    displace = [up, up, down, down, right, left, left, right]
    axes = [0, 0, 0, 0, 1, 1, 1, 1]

    coords = []
    for pair, d_fn, ax in zip(pairs, displace, axes):
        center, size = pair
        dir_vec = d_fn(size)
        new_center = add(center, dir_vec)
        to_add = mul(size, (-0.5, -0.5))
        print(new_center)
        tl = tuple(map(int, add(new_center, to_add)))
        #         dir_vec = mul(size, (-0.5, 0))
        #         dir_vec = mul(dir_vec, (1, -0.5))
        #         displaced_center = add(c, dir_vec)
        #         print(c)
        #         # calculate the rectangle location around it, and visualize as SVG
        #         to_add = mul(size, (-0.5, -0.5))
        #         tl = tuple(map(int, add(displaced_center, to_add)))
        # vis.add_rect(topleft=tl, size=size, attributes='stroke="blue" fill="none"')

        rect = CenteredRectangle(center=new_center, half_size=mul(size, (+0.5, +0.5)))
        x, y, w, h = rect.svg_region()
        print(x, y, w, h, url)
        if True:
            region_image = iiif_image_from_url(url, x, y, w, h)

            pipeline = "gray|threshold(178)"
            bw = apply_pipeline(region_image, pipeline, inspect=False)

            # fig = plt.figure(layout="constrained")
            # axis_dict = fig.subplot_mosaic(mosaic="AAABBC;AAABBC")
            # axis_dict = fig.subplot_mosaic(mosaic="BBBC;BBBC")
            # axis_dict = fig.subplot_mosaic(
            #     mosaic="A",
            #     # sharex=True,
            #     # sharex=bool(rim_side & RimSide.LEFT or rim_side & RimSide.RIGHT),
            #     # sharey=bool(rim_side & RimSide.BOTTOM or rim_side & RimSide.TOP),
            #     # sharey=True,
            # )
            # axA = axis_dict["A"]
            # axB = axis_dict["B"]
            axA = None

            settings = {"rim_fraction_filled": 0.5}
            figaxis = None
            pixel_value = 0  # white = 255, black = 0

            res = search_rim(bw, pixel_value, ax, settings, axA)
            print(res[0])

            local_center = center_coordinates(bw)
            expected_location = local_center[ax]

            points = []
            for start, end in res[0]:
                width = end - start
                half_width = width * 0.5

                c = start + half_width
                print(c, half_width)

                to_adapt = local_center[:]

                off = expected_location - c

                to_adapt[ax] = c
                to_adapt = tuple(to_adapt)

                print(off, to_adapt)

                global_pt = add(rect.tl(), to_adapt)

                points.append((off, global_pt))
            # sort on distance from center (which should be the expected location)
            points.sort(key=lambda x: abs(x[0]))
            if points:
                # vis.add_crop_mark(points[0][1])
                coords.append(points[0][1][ax])
            else:
                coords.append(None)

        print(coords)
        # fig.show()
        # fig.clear()

    # if we have found ordinates,
    # then the first 4 are x's, the last 4 are y's
    # going from bl to br to tr to tl (ccw)
    X = coords[:4]
    Y = coords[4:]
    new_corners = []
    for x, y in zip(X, Y):
        if x and y:
            pt = [x, y]
            vis.add_crop_mark(pt)
            new_corners.append(pt)
        else:
            new_corners.append(None)
    content = vis.show()
    with open(f"/tmp/{i}.svg", "w") as fh:
        fh.write(content)
    with open(f"/tmp/corner-test/{i}.json", "w") as fh:
        J["corners"]["refined_pixel_corner_points"] = new_corners
        json.dump(J, fh)
