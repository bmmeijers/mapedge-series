import json
import csv


with open(
    "/home/martijn/Documents/work/2023-08_synthesis/mapedge/series/wsk/uu/ed1/manifest/out_new.json"
) as fh:
    J = json.load(fp=fh)


rows = []
for seq in J["sequences"]:
    # print(seq.keys())
    for canvas in seq["canvases"]:
        for image in canvas["images"]:
            iiif_url = image["resource"]["service"]["@id"]
            label, uuid = (
                canvas["label"],
                iiif_url[iiif_url.find("IIIF=") + 5 :].split("/")[-1],
            )
            print(label.split(" - "), uuid)
            splitted = label.split(" - ")
            if len(splitted) > 1:
                sheet_id, sub_sheet_id, title, page = splitted
            else:
                sheet_id = None
                sub_sheet_id = None

            print(sheet_id, sub_sheet_id, uuid, iiif_url)
            row = {
                "sheet_id": sheet_id,
                "sub_sheet_id": sub_sheet_id,
                "uuid": uuid,
                "iiif_url": iiif_url,
            }
            rows.append(row)

out_filename = "/home/martijn/Documents/work/2023-08_synthesis/mapedge/series/wsk/uu/ed1/manifest/sheets_ed2.csv"
with open(out_filename, "w", newline="") as f:
    w = csv.DictWriter(f, rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"Written {out_filename}")
