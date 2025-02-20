import csv
import hashlib
from mapedge.lib.trace.vectorops import mul, add
from mapedge.lib.visualize import make_simple_svg_mask
from quads import points_as_quad
from enum import Enum
import uuid
import pyproj
import json


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


class Ordering(Enum):
    ALPHABETICAL = 1
    GEOGRAPHICAL = 2


# ids of sheets
def make_ordered_sheets(ordering):
    sheets = []
    just_one_sheets = set(
        [
            8,
            9,
            13,
            18,
            20,
            23,
            29,
            30,  # 's gravenhage - wider than normal
            42,
            46,
            55,
            61,
            62,
        ]
    )
    missing = set([4, 24, 35, 36, 47, 53, 56, 59])
    # 1 more for the inset in sheet 29
    for sheet in range(1, 63):
        if sheet in missing:
            continue
        elif sheet in just_one_sheets:
            sheets.append([sheet, None])
        else:
            # produced order of sheets with 2 subs can either be W, O or O, W, dependent on ordering setting
            if ordering is Ordering.GEOGRAPHICAL:
                for side in ["W", "O"]:
                    sheets.append([sheet, side])
            elif ordering is Ordering.ALPHABETICAL:
                for side in ["O", "W"]:
                    sheets.append([sheet, side])

    lst = list(map(tuple, sheets))
    oids = []
    for item in lst:
        oid = f"{item[0]}"
        if item[1] is not None:
            oid += f".{item[1]}"
        else:
            oid += "."
        oids.append(oid.lower())
    return oids


# sheet id to [column, row] index in regular grid
custom_mapping = {
    "1.w": [7, 0],
    "5.w": [7, 1],
    "9.": [5, 2],
    "10.w": [7, 2],
    "14.w": [5, 3],
    "19.w": [5, 4],
    "20.": [8, 4],
    "25.w": [5, 5],  # 25.W - Amsterdam has much larger width
    "30.": [3, 6],
    "31.w": [5, 6],
    ## 55 - 43.O Enschede - much wider
    "37.w": [3, 7],
    "42.": [1, 8],  ## 66 - 42 Zierikzee - much wider
    "43.w": [3, 8],
    "48.w": [1, 9],
    "54.w": [1, 10],
    "57.w": [7, 10],
    "60.w": [9, 11],
    "61.": [9, 12],
}


## The global anchor point from where we start
anchor = [0, 625000]
## The default sheet size (w x h)
size = [20000, 25000]

## The following sheets have a different size
custom_sizes = {
    "9.": [126_800 - 105_000, 582_000 - 550_000],
    "14.o": [152_500 - 120_000, 550_000 - 525_000],
    "19.o": [152_500 - 120_000, 525_000 - 500_000],
    "20.": [180_000 - 152_500, 525_000 - 500_000],
    "25.w": [120_000 - 87_500, 500_000 - 475_000],
    "30.": [100_000 - 67_400, 475_000 - 450_000],
    "34.o": [272_400 - 240_000, 475_000 - 450_000],
    "42.": [60_000 - 36_000, 429_000 - 404_000],
    "46.": [208_000 - 180_000, 425_000 - 400_000],
    "48.w": [40_000 - 16_000, 404_000 - 379_000],
    "54.w": [40_000 - 12_000, 382_000 - 357_000],
    "57.w": [160_000 - 132_400, 375_000 - 350_000],
}

# The following sheets have a different anchor (top left)
custom_anchors = {
    "9.": [105_000, 582_000],
    "20.": [152_500, 525_000],
    "25.w": [87_500, 500_000],
    "30.": [67_400, 475_000],
    "42.": [36_000, 429_000],
    "48.w": [16_000, 404_000],
    "48.o": [40_000, 404_000],
    "54.w": [12_000, 382_000],
    "54.o": [40_000, 382_000],
    "43.w": [60_000, 429_000],
    "49.w": [60_000, 404_000],
    "55.": [60_000, 382_000],
    "57.w": [132_400, 375_000],
    "60.w": [170_000, 350_000],
    "60.o": [190_000, 350_000],
    "61.": [170_000, 325_000],
    "62.": [190_000, 325_000],
}

L = make_ordered_sheets(Ordering.GEOGRAPHICAL)

M = {}
# for sheet_name in range(0, len(L)):  # 1 more than in the manifest (inset in 29)
for sheet_name in L:
    # sheet_name = None
    if sheet_name in custom_mapping:
        [c, r] = custom_mapping[sheet_name]
    else:
        c += 1

    if sheet_name in custom_sizes:
        tile_size = custom_sizes[sheet_name]
    else:
        tile_size = size

    if sheet_name in custom_anchors:
        tl = custom_anchors[sheet_name]
    else:
        tl = add(mul(mul([1, -1], [c, r]), size), anchor)

    br = add(tl, mul([1, -1], tile_size))
    xmin, ymax = tl
    xmax, ymin = br
    bl = (xmin, ymin)
    tr = (xmax, ymax)
    rect = as_rect(bl, tr)
    M[sheet_name] = rect  #  as_polygon(rect)
    # M.append(as_polygon(rect))

WHICH = "front"  # "hwp", "wve", "back"


def make_annotation_feature(px, py, wx, wy):
    """
    Ties Pixel coordinate to World coordinate

    Pixel coordinate system is image coordinate, top left = (0,0), y down = +, x right = +
    World coordinate system is WGS'84 (unspecified realization)
    """

    # FIXME:
    # the spec speaks about 'resourceCoords' instead of 'pixelCoords'
    # https://iiif.io/api/extension/georef/#35-the-resourcecoords-property
    # but allmaps parser does not like that

    return {
        "type": "Feature",
        "properties": {"pixelCoords": [int(px), int(py)]},
        "geometry": {
            "type": "Point",
            "coordinates": [round(wx, 7), round(wy, 7)],
        },
        # lat, lon for world
        # 7 decimals should be sufficient for WGS'84
    }


# Define the RD (EPSG:28992) and ETRS89 (EPSG:4258) projections
# rd_proj = pyproj.Proj(init="epsg:28992")
# etrs89_proj = pyproj.Proj(init="epsg:4258")


# Create a transformer object to convert from RD (EPSG:28992) to ETRS89 (EPSG:4258)
transformer = pyproj.Transformer.from_crs("epsg:28992", "epsg:4258")


def make_annotation_item(uuid, iiif_end_point, iiif_full_url, svg_mask, features):
    """Return a Georeference Annotation (JSON encoded) document

    <https://iiif.io/api/extension/georef/>
    """
    return {
        "id": f"{uuid}",
        "type": "Annotation",
        "@context": [
            "http://www.w3.org/ns/anno.jsonld",
            "http://geojson.org/geojson-ld/geojson-context.jsonld",
            "http://iiif.io/api/presentation/3/context.json",
        ],
        "motivation": "georeferencing",
        "target": {
            "type": "Image",
            "source": f"{iiif_full_url}",
            "service": [
                {"@id": f"{iiif_end_point}", "type": "ImageService2"}
            ],  # FIXME: type can be ImageService3 !
            "selector": {"type": "SvgSelector", "value": f"{svg_mask}"},
        },
        "body": {
            "type": "FeatureCollection",
            "purpose": "gcp-georeferencing",
            "transformation": {
                # "type": "polynomial",
                # "order": 0
                "type": "thinPlateSpline"
            },
            "features": features,
        },
    }


def make_page(items):
    return {
        "type": "AnnotationPage",
        "@context": ["http://www.w3.org/ns/anno.jsonld"],
        "items": items,
    }


# %%
# Make geojson
geojson = {"type": "FeatureCollection", "features": []}


def add_feature(geojson_collection, feature_type, coordinates, properties):
    new_feature = {
        "type": "Feature",
        "geometry": {"type": feature_type, "coordinates": coordinates},
        "properties": properties,
    }
    geojson_collection["features"].append(new_feature)


for sheet_name in L:
    exterior = M[sheet_name][0]
    pts = []
    for pt in exterior:
        lat, lon = transformer.transform(*pt)
        pts.append([lon, lat])
    # etrs89_exterior = [pts]
    props = {"sheet_id": sheet_name}
    add_feature(geojson, "Polygon", [pts], props)
    # break


with open(
    "/home/martijn/Documents/work/2023-08_synthesis/mapedge/series/wsk/ed5/sheet-index-ed5.geojson",
    "w",
) as fh:
    json.dump(geojson, fh)

# Also make georeference available in CSV
with open("/tmp/sheet-index-ed5.csv", "w") as fh:
    writer = csv.writer(fh)
    heading = ["sheet_id", "geo_epsg_4258", "geo_epsg_28992"]
    writer.writerow(heading)
    for sheet_name in L:
        exterior = M[sheet_name][0]

        if sheet_name[-1] == ".":
            sheet_name = sheet_name[:-1]
        pts = []
        for pt in exterior:
            lat, lon = transformer.transform(*pt)
            pts.append([lon, lat])
        rec = [sheet_name, pts, exterior]
        print(rec)
        writer.writerow(rec)

# %%
# Make georeference annotations

for WHICH in "front", "hwp", "wve", "back":
    with open(
        "/home/martijn/Documents/work/2023-08_synthesis/mapedge/series/wsk/ed5/sheets_oid.csv"
    ) as fh:
        reader = csv.reader(fh)
        header = next(reader)  # skip header
        print(header)
        # lines = [" ".join((line[5], line[6], line[7])).lower() for line in reader]
        LUT = {"OOST": "o", "WEST": "w", "": ""}
        no_idx = header.index("sheet_number")
        dir_idx = header.index("sheet_direction")
        tp_idx = header.index("sheet_type")
        lines = [
            [".".join([line[no_idx], LUT[line[dir_idx]]]), line]
            for line in reader
            if line[tp_idx] == WHICH
        ]

        iiif_url_idx = header.index("iiif_url")
        width_idx = header.index("width")
        height_idx = header.index("height")

    items = []
    for line in lines:
        key, l = line
        # print(key)
        if key in M:
            # print(M[key], l)
            # ...
            iiif_end_point = l[iiif_url_idx].replace("/info.json", "")
            iiif_full_url = iiif_end_point
            iiif_full_url += "/full/full/0/default.jpg"
            # uuid = iiif_end_point.split("/")[-1]
            # oid = str(uuid.uuid4())

            # seeding the md5 algorithm with a 'stable' string
            # leads to the same uuid being generated
            m = hashlib.md5()
            m.update(str(l).encode("utf-8"))
            oid = uuid.UUID(m.hexdigest())

            w = int(l[width_idx])
            h = int(l[height_idx])

            image_corners = [(0, h), (w, h), (w, 0), (0, 0)]
            svg_mask = make_simple_svg_mask([w, h], image_corners)

            def flipy(pt):
                return int(pt[0]), -int(pt[1])

            # make y-up
            image_corners = list(map(flipy, image_corners))
            # sort
            image_corners = points_as_quad(image_corners)
            # make y-down
            image_corners = list(map(flipy, image_corners))

            exterior = M[key][0]  # exterior ring of the polygon
            # print(points_as_quad(exterior[:-1]))
            # print(image_corners)
            # print(M[key], iiif_end_point, w, h, oid)

            features = []
            for wcoord, pcoord in zip(points_as_quad(exterior[:-1]), image_corners):
                wx, wy = wcoord
                px, py = pcoord

                # Sample coordinates in RD (x, y)
                # rd_x, rd_y = 155000, 463000

                # Transform RD to ETRS89
                etrs89_lat, etrs89_lon = transformer.transform(wx, wy)
                # print(f"ETRS89 coordinates: ({etrs89_lat}, {etrs89_lon})")
                feature = make_annotation_feature(px, py, etrs89_lon, etrs89_lat)
                features.append(feature)
            # print(features)
            georef_annotation_item = make_annotation_item(
                oid, iiif_end_point, iiif_full_url, svg_mask, features
            )
            items.append(georef_annotation_item)

    # write the combined annotation page to file
    annotation_page = make_page(items)
    with open(f"{WHICH}.json", "w") as fh:
        json.dump(annotation_page, fh)

    # with open("/home/martijn/tmp/ed5.wkt", "w") as fh:
    #     for i, (sheet, wkt) in enumerate(zip(L, M)):
    #         print(";".join(map(str, [i, sheet, wkt])), file=fh)
