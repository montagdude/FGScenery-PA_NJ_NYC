#!/bin/bash

OGR=ogr-decode

# Landcover
for file in landcover/shapefiles/NLCD/*.shp; do
    fname=$(basename $file)
    area_type=$(echo $fname | cut -f 1 -d '.')
    $OGR --area-type $area_type work/$area_type $file
done

# Water data from NHD
$OGR --area-type Lake work/Lake landcover/shapefiles/NHD/NHD_Area_River.shp
$OGR --area-type Lake work/Lake landcover/shapefiles/NHD/NHD_Waterbody_Lake.shp
$OGR --area-type Lake work/Lake landcover/shapefiles/NHD/NHD_Waterbody_Reservoir.shp
#$OGR --area-type Ocean work/Ocean landcover/shapefiles/NHD/NHD_Area_Estuary.shp        # Don't have any of these this time
$OGR --area-type Ocean work/Ocean landcover/shapefiles/NHD/NHD_Waterbody_Estuary.shp

# Parking from OSM
$OGR --area-type Road work/Parking landcover/shapefiles/OSM/parking.shp
