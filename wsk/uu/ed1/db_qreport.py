import sqlite3


db = sqlite3.connect(
    "/home/martijn/Documents/work/2023-08_synthesis/mapedge/series/wsk/sheet_index/ed1/uu.gpkg"
)
db.enable_load_extension(True)

db.cursor().execute("SELECT load_extension('mod_spatialite')")

# sql = "select count(*) from qreport"
sql = """
select
    round(st_maxx(geom) - st_minx(geom), 0) as dx,
    round(st_maxy(geom) - st_miny(geom), 0) as dy,
    sheets.uuid,
    distance_0,
    distance_5,
    distance_2,
    distance_3,
    abs(distance_0 - distance_5) + abs(distance_2 - distance_3) as total_delta,
    abs(distance_0 - distance_5) as delta_hori,
    abs(distance_2 - distance_3) as delta_vert,
    
    abs(distance_0 - round(round(st_maxx(geom) - st_minx(geom), 0) /1000.0/ 2.54 * 600, 0)) as off_in_x1,
    abs(distance_5 - round(round(st_maxx(geom) - st_minx(geom), 0) /1000.0/ 2.54 * 600, 0)) as off_in_x2,
    abs(distance_2 - round(round(st_maxy(geom) - st_miny(geom), 0) /1000.0/ 2.54 * 600, 0)) as off_in_y1,
    abs(distance_3 - round(round(st_maxy(geom) - st_miny(geom), 0) /1000.0/ 2.54 * 600, 0)) as off_in_y2
from
    wskSheetindexEd1 as sheets, 
    qreport 
where
    sheets.uuid=qreport.uuid
    --and (delta_vert >= 10 or delta_hori >= 10)
order by
    total_delta desc
"""
recordset = db.cursor().execute(sql).fetchall()
for row in recordset:
    print(row)


# )
