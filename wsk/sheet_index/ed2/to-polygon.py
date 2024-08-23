import json
import os

with open(
    os.path.join(os.path.dirname(__file__), "wsk2-bonne.geojson")
) as fh:
    J = json.load(fh)

# print(J)
# for key in J:
#     print(key)

new = {}
# new["crs"] = (
#     {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
# )
new["name"] = "wskBonneEd2SheetIndex"
new["type"] = J["type"]
# print(J["type"])
# print(J["features"])
new["features"] = []
for feature in J["features"]:
    # print()
    # print(feature["type"])
    # print(feature["properties"])
    # print(feature["geometry"])

    print(len(feature["properties"]["images"]))

    origSheetId = feature["properties"]["sheet"]
    sheetId, subSheetId = origSheetId.split(".")
    newgeom = {
        "type": "Polygon",
        "coordinates": [feature["geometry"]["coordinates"]]
        + [feature["geometry"]["coordinates"][0]],
    }
    newf = {
        "type": feature["type"],
        "properties": {"sheetId": sheetId, "subSheetId": subSheetId},
        "geometry": newgeom,
    }
    new["features"].append(newf)

with open(
    "waterstaatskaart-ed2-poly.geojson",
    "w",
) as fh:
    json.dump(new, fh)
