import requests
from mapedge.lib.trace.vectorops import mul, add
from enum import Enum
import os


def as_linestring(ln):
    c = ", ".join([f"{pt[0]} {pt[1]}" for pt in ln])
    return f"LINESTRING({c})"


def as_polygon(poly):
    rings = []
    for ring in poly:
        c = ", ".join([f"{pt[0]} {pt[1]}" for pt in ring])
        rings.append(c)
    return "POLYGON((" + "".join(rings) + "))"


def as_point(pt):
    c = f"{pt[0]} {pt[1]}"
    return f"POINT({c})"


def as_rect(bl, tr):
    xmin, ymin = bl
    xmax, ymax = tr

    pts = [[[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax], [xmin, ymin]]]

    return pts


url = "https://dlc.services/iiif-resource/7/string1string2string3/waterstaatskaart/3/1"


def as_json(url):
    return requests.get(url).json()


L = []
J = as_json(url)
for sequence in J["sequences"]:
    for canvas in sequence["canvases"]:
        for image in canvas["images"]:
            L.append([canvas["label"], image["resource"]["service"]["@id"]])


class Ordering(Enum):
    ALPHABETICAL = 1
    GEOGRAPHICAL = 2


def make_ordered_sheets(ordering):
    sheets = []
    just_one_sheets = set(
        [4, 8, 9, 13, 18, 20, 23, 24, 29, 36, 46, 47, 53, 55, 60, 61, 62, 63]
    )
    missing = set([35, 56, 59])
    # 1 more for the inset in sheet 29
    for sheet in range(1, 64):
        if sheet in missing:
            continue
        elif sheet in just_one_sheets:
            sheets.append([sheet, None])
        else:
            # produced order of sheets with 2 subs can either be W, O or O, W, dependent on ordering setting
            if ordering is Ordering.GEOGRAPHICAL:
                # UGLY:
                # 15 Lemmer / 15-20 Enkhuizen does not follow the flip of W,O in the manifest :|
                # undo the reversing of O/W...
                if sheet == 15:
                    for side in ["O", "W"]:
                        sheets.append([sheet, side])
                else:
                    for side in ["W", "O"]:
                        sheets.append([sheet, side])
            elif ordering is Ordering.ALPHABETICAL:
                for side in ["O", "W"]:
                    sheets.append([sheet, side])
    return map(tuple, sheets)


custom_mapping = {
    0: [7, 0],
    6: [6, 1],
    14: [5, 2],
    15: [7, 2],
    22: [5, 3],
    31: [5, 4],
    33: [8, 4],
    39: [4, 5],
    49: [3, 6],
    59: [2, 7],
    70: [1, 8],
    79: [0, 9],
    90: [0, 10],
    94: [7, 10],
    98: [9, 11],
    99: [8, 12],
}


# FIXME: To update:
# - [ ] 0b14025b-49d4-4a17-a670-579e28ccf0a8_82/ 3 Uithuizen Oost
#       -- lijkt geen 20km breedte te hebben, maar ietsje smaller te zijn

custom_sizes = {
    41: [20650, 25000],  # sheet 25.O
    69: [20000, 16000],  # sheet 41.O
    94: [26000, 25000],  # sheet 57.W
    97: [15250, 25000],  # sheet 58.O -- FIXME: overlaps a bit with neighbouring sheets
    98: [27000, 25000],  # sheet 60
    100: [15000, 25000],  # sheet 62
    101: [9750, 12100],  # sheet 29 (inset, not part of original manifest)
}

custom_anchors = {
    # move south 12'500m
    0: [140000, 625000 - 12500],  # 1.W
    7: [140000, 600000 - 12500],  # 5.W
    15: [140000, 575000 - 12500],  # 10.W
    24: [140000, 550000 - 12500],  # 15.O
    #
    14: [100000 + 4500, 575000],  # sheet 9. (texel)   # FIXME:GUESS
    6: [120000 - 4000, 600000],  # sheet 4. (vlieland) # FIXME:GUESS
    1: [160000 + 10500, 625000],  # 1.O (Ameland), move 10'000m east
    39: [81000, 500000],  # sheet 24
    94: [134000, 375000],  # sheet 57.W
    81: [40000, 403250],  # sheet 48.O
    # This move of 7500m north is a guess
    90: [0, 375000 + 7500],  #  sheet 53 # FIXME:GUESS
    91: [20000, 375000 + 7500],  # 54.W  # FIXME:GUESS
    92: [40000, 375000 + 7500],  # 54.O  # FIXME:GUESS
    93: [60000, 375000 + 7500],  # 55    # FIXME:GUESS
    #
    98: [+23000 + 155000, -113000 + 463000],  # sheet 60
    99: [+15000 + 155000, -138000 + 463000],  # sheet 61
    100: [+35000 + 155000, -138000 + 463000],  # sheet 62
    101: [260000, 475000],  # sheet 29, inset (south part below main sheet 29)
}

anchor = [0, 625000]
size = [20000, 25000]

M = []
for index in range(0, 103):  # 1 more than in the manifest (inset in 29)
    if index in custom_mapping:
        [c, r] = custom_mapping[index]
    else:
        c += 1
    # specify special sheets
    # - [x] custom anchor
    # - [x] custom size
    if index in custom_sizes:
        tile_size = custom_sizes[index]
    else:
        tile_size = size
    if index in custom_anchors:
        tl = custom_anchors[index]
    else:
        tl = add(mul(mul([1, -1], [c, r]), size), anchor)

    br = add(tl, mul([1, -1], tile_size))
    xmin, ymax = tl
    xmax, ymin = br
    bl = (xmin, ymin)
    tr = (xmax, ymax)
    rect = as_rect(bl, tr)
    M.append([index, as_polygon(rect)])

# process the manifest into a dictionary, so we can lookup based on sheet id / sub sheet id the iiif url and canvas label
combined = zip(make_ordered_sheets(Ordering.ALPHABETICAL), L)
iiif_lut = dict(combined)
# we store the inset of 29 under sheet 63 (which is a non-existent id in the serie)
iiif_lut[(63, None)] = iiif_lut[(29, None)]

# as the UUID was used as primary key, the map with two map fragments messes this up (we don't know how to join the large or small fragment) :|
# solve it with the following dict: the list with ids here is stored in the corner.json files
# if there are more corner.json for a uuid, we take them from left to right in the list
process_order = {
    "0128118b-6593-4124-a403-980702c6b625": [93],
    "08907114-ab47-4681-b67b-1496f243b943": [91],
    "098aee9e-b8a0-4879-8e33-771d2f64c872": [43],
    "0b14025b-49d4-4a17-a670-579e28ccf0a8": [82],
    "0e10f5df-c720-4e36-b63d-971a60b7669c": [100],
    "0e3790f6-5fbe-434d-8d62-95b3017772a0": [26],
    "11131238-3fe7-40aa-bced-19e35043e820": [2],
    "144e7ec3-f7df-409e-8a73-d94686fc8d59": [48],
    "14f6c748-0cdc-46d1-a1da-f746ec72fce6": [10],
    "18ac521e-25ce-4269-b842-b05f61e6c3d6": [51],
    "1c76ebcc-bf80-4a1c-b72f-81f339cb67c0": [17],
    "1ee28e95-4a63-4fb5-84fd-698f1c0c9432": [12],
    "1ff6b839-8af9-42f7-99d2-e0045f64616b": [49],
    "224a148f-8867-4b00-8d9c-8b25ef754968": [32],
    "260f2efc-7a37-4dda-a5f5-132df0ba0af4": [77],
    "296f0051-e9a6-4113-a3ed-d0a0808d23ea": [99],
    "2fbeea4e-d4b5-419a-83bc-e1ac4c945db4": [25],
    "34710795-184c-444d-94e1-33ef56bab73a": [57],
    "347eaabb-177f-4756-9d76-d742970b84cb": [41],
    "41317872-266c-47da-a96c-31a7a9a72634": [33],
    "413a4098-89a3-4b35-9fe4-0238241f74eb": [79],
    "420e3b73-b192-4ac9-a344-1caa2521280a": [78],
    "42860317-0e2b-4507-b093-8b903a80e0c5": [36],
    "441bf962-959a-472c-8e0a-bff25399b42b": [83],
    "44812691-99ab-4ac2-b6b0-26381a20a6d5": [28, 101],
    "46865836-d00b-47ce-a1b4-083ea1704eb8": [88],
    "46c52a8a-17c1-41e7-9fc0-6da05a4c53e8": [35],
    "4a818443-cbcb-4a5a-b3e6-c4f957973efa": [38],
    "4c0aac7c-4323-471c-9b40-ebca5eec2aa1": [75],
    "4d4ad433-0060-4257-ae60-dc29059f1f48": [14],
    "4fe88307-68c1-43d8-a7c4-9afcd877c6fa": [92],
    "50447ac2-fc73-40d5-824f-71876e859532": [94],
    "57aca5c6-7719-4c23-a2aa-7b646dcb0706": [5],
    "586f5e1c-83c1-4a27-902a-9b5170cd431d": [60],
    "5ad8c5e3-4d05-478c-b720-616a34eb5c4b": [45],
    "62454ebd-b494-42e2-82e5-a01828e902ef": [23],
    "625cd690-3876-4b8a-8d49-05d470de6fb7": [73],
    "63bece81-8f52-4569-bb09-706c4c450bc5": [31],
    "64b92ae1-2f84-4900-bb66-5d94fee1b047": [67],
    "6744bbcf-ff3d-43cf-b7b9-ecf69435ded8": [4],
    "67a53423-1b7a-4c9e-8aca-256f32672b6b": [87],
    "6a57ca42-e304-4f6f-9ae5-1821e8bcff4d": [66],
    "6b0511b4-d1a8-44cf-9da7-2295b9a93ed8": [47],
    "6b4562de-aa1c-4fb1-9d12-a761cc1fa17c": [1],
    "6de22dd5-9ab0-4b00-9195-8a1dbbd91b93": [81],
    "717de2cb-6ff8-483d-b6b4-e32aa3669557": [18],
    "7231cf12-fbfd-4368-af01-ff4257fc4e6f": [54],
    "759443fd-635a-45e6-a2ec-ae5dd3a562f0": [6],
    "76580862-ea44-469b-b982-eca554ace713": [64],
    "7cecdaf2-54e0-4f4c-af3c-ded9b739d6b3": [58],
    "80e75e45-0200-4d7e-b280-a1434d53e6cd": [98],
    "827330d9-f0bf-4523-a395-56377dc03506": [85],
    "84b2aa87-6e4b-4df9-b149-a03cf7d2b2b4": [42],
    "8526234c-8595-4e13-87ee-b38559b765bc": [69],
    "87a62767-7099-4786-a3ee-6431dbb59492": [80],
    "8807f9b8-ad7e-4fca-b994-b460fd627f5e": [30],
    "8822d4cf-9b36-4f01-96e4-1fcbe4fd7ea5": [19],
    "8a631a42-74ba-4a75-a22e-ec314d7e641c": [11],
    "8f251532-8c01-4f7f-bfd8-8d48c35c21f4": [46],
    "8f84f0d0-f3ba-4c04-9173-1299b4f4c21e": [21],
    "90515128-a002-4272-9e6c-9568e23bfcd2": [61],
    "90d92b52-c415-41f6-916d-cf2a38d6eeee": [44],
    "934e310f-9619-405c-b2f5-fb90148f54c8": [22],
    "980624ea-96e0-439f-abe4-991004fd1bed": [95],
    "98cb41e5-2877-4498-aa1f-7e6b58340ad4": [40],
    "9904bd27-2bb7-46ef-8a52-3c4c258b4947": [84],
    "9e55eb0e-0ffe-4f4b-a5b8-cc06fa58f2cf": [29],
    "9edc1008-d6e9-47e0-b000-8ccb747b448d": [59],
    "9f0f9f0b-b8b3-4282-91ff-b664337f9315": [16],
    "a0e76aff-d494-4b21-a5f7-566cc8a28319": [3],
    "a9c0eaef-556a-42b1-92cd-36844f21d93c": [97],
    "acc1ccea-2857-459f-9ee4-60c5bd8b8b4d": [71],
    "afc53df4-f230-446f-a4c1-456a456e5d95": [15],
    "b0868f11-eafa-4038-901c-539e84cb1ba4": [50],
    "b0f8048e-79c5-4a4a-8b52-73e0a05c797a": [70],
    "b20482f2-2cb7-4d59-a423-f16a607713dc": [74],
    "bc686606-8230-40e5-9625-4197aa5398ff": [72],
    "bf7aa6c1-6219-42f0-8517-c4331d931e61": [89],
    "c27e1f45-e46d-4075-b7bb-fe00d9978b4d": [52],
    "c544e4c5-9423-4357-bf14-d62f43e5fbc7": [55],
    "c6cabf77-8f58-408c-8e99-f13d0317417d": [27],
    "cc014ff5-8a96-4ec5-a26e-e86a1509f4fa": [53],
    "ce4543b6-c825-4100-8d9c-abd7fcf9c005": [20],
    "d5529e6c-dcd6-49c8-be05-b09a7ddf1a0f": [39],
    "d81a19ae-36a5-462d-9ff1-94c585944132": [86],
    "d8c0e454-392c-4b6a-ad5b-f7a146f8e95f": [90],
    "d96c9189-f2f7-4c4d-ba73-46fcccfcb9d0": [76],
    "d96e4b88-4301-44b2-b5cf-4cf4a8e6107f": [34],
    "d9746bf0-10a4-41fd-b4ee-e5dce6ddc212": [56],
    "dd536914-54f4-468f-abde-437138b3530d": [13],
    "de35d1ed-feae-43d0-95da-3dca97684395": [63],
    "e1db6edb-9017-4945-8b1d-1ad84259625d": [37],
    "e2af8e8e-be6a-4e76-813f-2660e0365014": [65],
    "e3c98935-8d3f-4d00-a04b-6d0262b758ac": [24],
    "e682cd41-f044-4979-8918-bcd84ee90054": [96],
    "ea02c394-e91c-4b05-b344-7d0d027720c4": [7],
    "ee5ae533-ee5b-4f77-a950-ec87f62769f9": [0],
    "ef11a8b4-91d7-4401-9c96-dee281b0703c": [62],
    "f6aaf498-87a5-45e3-b47c-e8b299c2bf94": [8],
    "f7868be0-4c85-4732-bc00-51406bd115e1": [9],
    "fae2eb6f-c6c8-47b4-8a50-d50e61d490ee": [68],
}


with open(os.path.join(os.path.dirname(__file__), "wsk_ed3.tsv"), "w") as fh:
    tsv_row = "\t".join(
        map(
            str,
            [
                "sheet_serie_id",
                "sub_id",
                "canvas_label",
                "iiif_url",
                "uuid",
                "list_idx",
                "poly_wkt",
                "sheet_id",
            ],
        )
    )
    print(tsv_row, file=fh)
    # process the sheets into a sheet index with polygons
    combined = zip(make_ordered_sheets(Ordering.GEOGRAPHICAL), M)
    for index, item in enumerate(combined):
        (
            (sheet_id, sub_id),
            (_, poly_wkt),
        ) = item

        # join with the lut
        canvas_label, iiif_url = iiif_lut[(sheet_id, sub_id)]
        uuid = iiif_url.replace("https://dlc.services/iiif-img/7/32/", "")
        order_id = process_order[uuid].pop(0)
        if sub_id is None:
            sub_id = ""
        tsv_row = "\t".join(
            map(
                str,
                [
                    sheet_id,
                    sub_id,
                    canvas_label,
                    iiif_url + "/full/!1024,1024/0/default.jpg",
                    uuid,
                    index,
                    poly_wkt,
                    order_id,  # the column that contains the sheet_id of corners.json
                ],
            )
        )
        print(tsv_row, file=fh)
