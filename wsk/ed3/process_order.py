import glob
import json

d = {}
for filename in sorted(glob.glob("/tmp/corners-wsk-ed3/*.json")):
    with open(filename) as fh:
        J = json.load(fh)
        order_id, uuid = [J["sheet_id"], J["uuid"]]
        if uuid not in d:
            d[uuid] = [order_id]
        else:
            d[uuid].append(order_id)

## as I have processed the sheets in a different order than in the manifest
## the sheet_id key in the corner.json files does not reflect the order of the manifest
##
## hence, we make this lookup, where per UUID, we store a list of process ids (order number in which the sheets were processed)
##
## in the sheet index maker, we copy this {UUID -> [orderid, ...]} dict
##
## the problem actually exists, because uuid's are not unique in this serie (as sheet 29 contains two map fragments on same IIIF image and we did not cope with this appropriately, yet :| )
import pprint

pprint.pprint(d)
