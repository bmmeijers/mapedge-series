import json
import os

with open(os.path.join(os.path.dirname(__file__), "wsk2-bonne.geojson")) as fh:
    J = json.load(fh)

# print(J)
for key in J:
    print(key)

new = {}
# new["crs"] = (
#     {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
# )
new["name"] = "wskUUEd2SheetIndex"
new["type"] = J["type"]
print(J["type"])
print(J["features"])
new["features"] = []
for feature in J["features"]:
    print()
    print(feature["type"])
    print(feature["properties"])
    print(feature["geometry"])

    origSheetId = feature["properties"]["sheet"]
    if origSheetId == "31.3":
        origSheetId = "31.4"
    sheetId, subSheetId = origSheetId.split(".")
    newgeom = {
        "type": "Polygon",
        "coordinates": [feature["geometry"]["coordinates"]]
        + [feature["geometry"]["coordinates"][0]],
    }
    newf = {
        "type": feature["type"],
        "properties": {
            "sheetId": sheetId,
            "subSheetId": subSheetId,
            "sheet": origSheetId,
        },
        "geometry": newgeom,
    }
    new["features"].append(newf)

with open(
    "/home/martijn/Documents/work/2023-08_synthesis/mapedge/series/wsk/uu/ed2/wsk2-bonne-poly.geojson",
    "w",
) as fh:
    json.dump(new, fh)
