# Stanford Japan

## Origin
<https://earthworks.stanford.edu/catalog/stanford-ph028ym3863>


https://geowebservices.stanford.edu/geoserver/wfs
druid:ph028ym3863


sheet index was produced by adding a virtual field to the geojson file downloaded from stanford
the virtual field `uuid` was filled with `concat("druid", '_00_0001')`, so the uuid of the image is then there
the file is saved from qgis as geojson with the additional field


## Sheets

- [ ] zc857my1503_00_0001 = folded top left
- [ ] fg106xz0738 = broken sheet 


## Missing from wget

fd867ny9894_00_0001
mb450gb7296_00_0001
zz473nh9056_00_0001


should have been?

fd867ny9894_0001
mb450gb7296_0001
 
- [x] fd867ny9894_0001
- [x] mb450gb7296_0001
- [x] zz473nh9056_0001



## Indexing 

CREATE INDEX idx__report__uuid ON report (uuid);
CREATE INDEX idx__sheet_index__uuid ON sheet_index (uuid);

## Virtual layer

Click `import` after having loaded report and sheet_index into the QGIS TOC

```
select * from sheet_index s, report r where s.uuid=r.uuid
```


## Select failing sheets

### We did not obtain so many points as inliers

select * from sheet_index s, report r where s.uuid=r.uuid
where min("left__outer__outer-inner__inliers", min("right__outer__outer-inner__inliers", min("top__outer__outer-inner__inliers" , bottom__outer__outer-inner__inliers"))) < 5

### The distances at both sides deviate from each other

select (1 - (cast(min(distance_2, distance_3) as float) / cast(max(distance_2, distance_3) as float))) * 100.0 from report

select (1 - (cast(min(distance_0, distance_5) as float) / cast(max(distance_0, distance_5) as float))) * 100.0 from report


select uuid from report

where

(1 - (cast(min(distance_2, distance_3) as float) / cast(max(distance_2, distance_3) as float))) * 100.0 > 0.25 
or
(1 - (cast(min(distance_0, distance_5) as float) / cast(max(distance_0, distance_5) as float))) * 100.0 > 0.25
or
(1 - (cast(min(distance_1, distance_4) as float) / cast(max(distance_1, distance_4) as float))) * 100.0 > 0.25


###
Distance calculation for the sheets

select round(greatcirclelength(makeline(st_pointn(st_exteriorring(geom), 1),st_pointn(st_exteriorring(geom), 2))),0) as d1, round(greatcirclelength(makeline(st_pointn(st_exteriorring(geom), 2),st_pointn(st_exteriorring(geom), 3))),0) as d2, uuid from sheet_index order by d1;

Sheet most North
- 19485m
Sheet most South
- 25395m

Height of sheets, constant
- 18533m

most northern:
https://stacks.stanford.edu/image/iiif/cx422vn9780/cx422vn9780_00_0001/full/1024,/0/default.jpg
most southern:
https://stacks.stanford.edu/image/iiif/ph299bg5284/ph299bg5284_00_0001/full/1024,/0/default.jpg
(difference in horizontal size)