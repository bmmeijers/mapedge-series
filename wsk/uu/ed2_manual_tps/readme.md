loaded iiif image in editor
digitized 6 points on image correctly
digitized 6 artificial points on world
copied annotation to clipboard
made world coordinates in ackermans 1822 with python script as csv
loaded csv into qgis + set custom projection
transformed to geojson (tick rfcXXXX and you get wgs'84)
manually copied real world point coordinates into the initial annotation
added thin-plate-spline property of annotation
visualize in viewer

TODO:

use such an annotation to transform pixel coordinates found as image corners to wgs'84 with allmaps cli
then we can use these world corners inside qgis and measure over there
transform back to bonne and read the 'real' corners of the sheet

Other sheets that would benefit from this approach:
- Schiermonniksoog
- Denekamp 1 / 2
