import requests
import os
import json

from mapedge.lib.visualize import make_simple_svg_mask

output_folder_name = "/tmp/start_annotate"
os.makedirs(output_folder_name, exist_ok=True)


def as_wkt_poly(xmin, ymin, xmax, ymax):
    wkt = f"POLYGON(({xmin} {ymin}, {xmax} {ymin}, {xmax} {ymax}, {xmin} {ymax}, {xmin} {ymin}))"
    return wkt


def make_index():
    from mapedge.lib.trace.vectorops import add, mul, sub

    # sheet_count = [14, 13]
    # sheet_size = [20_000, 25_000]  # 20km x25km
    # sheet_anchor = "top-left"  # could be enum with top-left, top-right, bottom-left, bottom-right, center

    sheet_count = [30, 13]
    sheet_size = [20_000, 25_000]  # 20km x25km

    pos_neg = [1, -1]

    # anchor, size to polygon
    def rd_new_2_rd_old(c):
        shift = [155_000, 463_000]
        return sub(c, shift)

    top_right = (280_000, 625_000)  # meter, RD new
    bottom_left = sub(top_right, mul(sheet_count, sheet_size))
    # print(top_right, rd_new_2_rd_old(top_right))
    # print(bottom_left, rd_new_2_rd_old(bottom_left))
    top_left = [bottom_left[0], top_right[1]]
    # print(top_left)

    top_left = [0, 625_000]

    def tl_br_xymin_xymax(tl, br):
        xmin, ymax = tl[0], tl[1]
        xmax, ymin = br[0], br[1]
        return xmin, ymin, xmax, ymax

    sheet_geometry = {}
    # with open("/home/martijn/Documents/tmp/wsk_sheets_ed3.csv", "w") as fh:
    #     print("x;y;wkt", file=fh)
    for y in range(sheet_count[1]):
        for x in range(-1, sheet_count[0]):
            sheet_idx = [x, y]
            where = add(mul(sheet_idx, mul(sheet_size, pos_neg)), top_left)
            tl, br = (where, add(where, mul(sheet_size, pos_neg)))
            # print(tl, br, tl_br_xymin_xymax(tl, br))
            row = ";".join(map(str, (x, y, as_wkt_poly(*tl_br_xymin_xymax(tl, br)))))
            sheet_geometry[(x, y)] = tl_br_xymin_xymax(tl, br)
            # print(row, file=fh)

    # override = {
    #     4: {"titles": ["Vlieland"], "names": ["oost"], "start": 2},
    #     1: {"titles": ["Ameland", "Terschelling"]},
    # }

    # for sheet_id in range(1, 63):
    #     default_names = ["west", "oost"]

    #     default_start = 1
    #     for sub_id, sub_name in enumerate(default_names, start=default_start):
    #         print(
    #             f"""update "waterstaatskaart-dlcs-annotated" set sub_sheet_id = {sub_id} where sheet_id = {sheet_id} and sheet_title like '%{sub_name}' and edition = '3';"""
    #         )  # sheet_id, sub_id, sub_name)

    row_starts = {
        (1, 1): [7, 0],
        (4, 1): [5, 1],
        (9, 1): [5, 2],
        (14, 1): [5, 3],
        (19, 1): [5, 4],
        (24, 1): [3, 5],
        (30, 1): [3, 6],
        (36, 1): [2, 7],
        (42, 1): [1, 8],
        (47, 1): [-1, 9],
        (53, 1): [-1, 10],
        # (57, 1): [15, 10],
        (59, 1): [7, 11],
        (61, 1): [7, 12],
    }

    sub_names = {
        1: "west",
        2: "oost",
    }

    # fh = open("/home/martijn/Documents/tmp/wsk_sheets_ed3__geom.csv", "w")
    # print("sheet_id;sub_sheet_id;sub_sheet_name;wkt", file=fh)
    sheet_dict = {}
    for sheet_id in range(1, 63):
        for sub_sheet_id in range(1, 3):
            if (sheet_id, sub_sheet_id) in row_starts:
                col, row = row_starts[(sheet_id, sub_sheet_id)]
            else:
                col += 1
            print(
                (sheet_id, sub_sheet_id, sub_names[sub_sheet_id]),
                "->",
                col,
                row,
                sheet_geometry[(col, row)],
                as_wkt_poly(*sheet_geometry[(col, row)]),
            )
            # print(
            #     f"{sheet_id};{sub_sheet_id};{sub_names[sub_sheet_id]};{as_wkt_poly(*sheet_geometry[(col, row)])}",
            #     file=fh,
            # )
            sheet_dict[(sheet_id, sub_sheet_id)] = sheet_geometry[(col, row)]
            # print(sheet_id, sub_sheet_id)
    return sheet_dict


def get_json(url):
    r = requests.get(url)
    return r.json()


url = "https://dlc.services/iiif-resource/7/string1string2string3/waterstaatskaart/3/1"
J = get_json(url)
print(J)

skip = set(  # sheet id / subsheet id (1=west, 2=oost)
    [
        (4, 1),
        (8, 2),
        (9, 2),
        (13, 2),
        (18, 2),
        (20, 1),
        (23, 2),
        (24, 1),
        (29, 2),
        (35, 1),  # Both sheets of #35 are missing ??
        (35, 2),
        (36, 1),
        (46, 2),
        # (47, 1),
        # (53, 1),
        (55, 2),
        (56, 1),  # Both sheets 56 are missing
        (56, 2),
        (59, 1),
        (59, 2),
    ]
)
all_sheets = []
for sheet_id in range(1, 63):
    for sub_sheet_id in range(2, 0, -1):
        oid = (sheet_id, sub_sheet_id)
        if oid in skip:
            continue
        all_sheets.append(oid)

sub_names = {
    1: "west",
    2: "oost",
}

item_id = 0

sheet_geoms = make_index()

records = []
# in dit manifest zijn de bladen alfabetisch geordend, dus oost komt voor west
# geografisch springt dit dus heen en weer over de x-as (eerst rechts, dan links, dan over rechts, etc)
for sequence in J["sequences"]:
    for canvas in sequence["canvases"]:
        for image in canvas["images"]:
            resource = image["resource"]
            (
                sheet_id,
                sub_sheet_id,
            ) = all_sheets[item_id]
            print()
            print(
                item_id + 1,
                "--",
                all_sheets[item_id],
                sub_names[sub_sheet_id],
                "--",
                all_sheets[item_id][0],
                sub_names[sub_sheet_id],
            )
            uuid = resource["service"]["@id"].split("/")[-1]
            row = list(
                map(
                    str,
                    [
                        sheet_id,
                        sub_sheet_id,
                        sub_names[sub_sheet_id],
                        as_wkt_poly(*sheet_geoms[all_sheets[item_id]]),
                        resource["service"]["@id"],
                        resource["service"]["@id"] + "/full/!1024,1024/0/default.jpg",
                        uuid,
                    ],
                )
            )
            records.append(row)

            # print(resource.keys())
            print("-", resource["width"], "×", resource["height"])
            print("-", resource["service"]["@id"])
            print("-", resource["service"]["@id"] + "/full/!1024,1024/0/default.jpg")
            print(row)
            item_id += 1

            w, h = resource["width"], resource["height"]
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
            out["iiif_end_point"] = resource["service"]["@id"]

            with open(os.path.join(output_folder_name, f"out-{uuid}.json"), "w") as fh:
                json.dump(out, fh)


with open("/home/martijn/Documents/tmp/wsk_sheets_ed3__manifest.csv", "w") as fh:
    header = "sheet_id;sub_sheet_id;sub_sheet_name;wkt;iiif_endpoint;iiif_sample;uuid"
    print(header, file=fh)
    for row in records:
        print(";".join(row), file=fh)
