import csv


def chars_are_all_digits(chars):
    if chars:
        for char in chars:
            if not char.isdigit():
                return False
        return True
    else:
        return False

def chars_contain_digits(chars):
    for char in chars:
        if char.isdigit():
            return True
    return False


def get_iiif_image_endpoint(uuid):
    return "https://dlc.services/iiif-img/7/32/" + uuid


def get_thumbnail_url(uuid):
    return get_iiif_image_endpoint(uuid) + "/full/512,/0/default.jpg"

def parse_sheet_info(image_name):
    image_name = image_name.replace(".jpg", "")
    # print(image_name)
    splitted = image_name.split("-")

    # for val in splitted:
        # print(" -", val, chars_are_all_digits(val))
    if chars_are_all_digits(splitted[0]):
        sheet_id = int(splitted[0])
        remaining = splitted[1:]
    else:
        sheet_id = -1
        remaining = splitted[:]
    # print(sheet_id, remaining)

    sub_sheet_id = -1
    sub_sub_sheet_id = -1
    year = -1
    last = remaining[-1]
    if chars_contain_digits(last):
        if chars_are_all_digits(last):
            
            if int(last) <= 4:
                sub_sheet_id = int(last)
                remaining = remaining[:-1]
            else:
                year = int(last)
                remaining = remaining[:-1]
                if chars_are_all_digits(remaining[-1]):
                    sub_sheet_id = int(remaining[-1])
                    remaining = remaining[:-1]
                else:
                    sub_sheet_id = -1
        else:
            for v in "ab":
                if v in last:
                    sub_sub_sheet_id = v
                    sub_sheet_id = int(last.replace(v, ""))
                    break
            else:
                raise ValueError(f"what is this? {last}")
            

            remaining = remaining[:-1]
            sub_sheet_id = -1
    else:
        sub_sheet_id = -1

    return (sheet_id, sub_sheet_id, sub_sub_sheet_id,  year, " ".join(remaining), image_name)
    # if len(splitted) == 4:
    #     sheet_id, sheet_title, sheet_sub_id, year, = splitted
    # elif len(splitted) == 3:
    #     sheet_id, sheet_title, sheet_sub_id, = splitted
    #     year = None
    # elif len(splitted) == 2:
    #     sheet_id, sheet_title, = splitted
    #     sheet_sub_id = None
    #     year = None
    # else:
    #     raise ValueError("unhandled amount")



def process_url(url):
    splitted = url.split("/")
    
    idx = splitted.index("waterstaatskaart")
    edition_idx_primary = idx + 1
    edition_idx_secondary = idx + 2
    sheet_info_idx = idx + 3

    edition_info = [splitted[get] for get in [edition_idx_primary, edition_idx_secondary]]
    sheet_info = splitted[sheet_info_idx]

    res = [
        tuple(edition_info),
        parse_sheet_info(sheet_info)
    ]
    return res


edition_lut = {
('2e', 'edit-2bis'): '2bis',
('2e', 'tweede-editie'): '2',
('3e', 'derde-editie'): '3',
('5e', 'geogegevens'): '5',
('3e', 'edit-3bis'): '3bis',
('1e', 'eerste-editie'): '1',
('4e', 'geogegevens'): '4',
('1e', 'edit-1bis'): '1bis',
}
# editions = set()
with open("waterstaatskaart-dlcs.csv") as fh:
    records = []
    
    for line_no, line in enumerate(csv.reader(fh)):
        # print(line_no)
        if line_no == 0:
            continue
        uuid, orig_url = line[3], line[4]
        print(uuid, orig_url)
        res = process_url(orig_url)

        # editions.add(res[0])
        # print(edition_lut[res[0]])

        sheet_id, sub_sheet_id, sub_sub_sheet_id, year, sheet_title, image_name, = res[1]

        rec = {
            'uuid': uuid, 
            'thumbnail': get_thumbnail_url(uuid),
            'original_url': orig_url,
            'iiif_endpoint_url': get_iiif_image_endpoint(uuid),
            'edition': edition_lut[res[0]],
            'sheet_id': sheet_id, 
            'sub_sheet_id': sub_sheet_id, 
            'sub_sub_sheet_id': sub_sub_sheet_id, 
            'sheet_title': sheet_title, 
            'year': year,
            'image_name': image_name

        }
        print(rec)
        records.append(rec)
    
import pprint
pprint.pprint(records)

with open("waterstaatskaart-dlcs-annotated.tsv", "w") as fh:
    # print("\t".join([key for key in records[0]]), file=fh)
    print("\t".join([key for key in records[0]]), file=fh)

    for record in records:
        out = "\t".join(str(record[key]) for key in record)
        print(out, file=fh)
        
        
# print(editions)