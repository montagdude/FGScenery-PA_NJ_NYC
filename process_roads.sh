#!/bin/bash

OGR=ogr-decode

# Major roads from OSM (bridges and tunnels have been removed; handled by osm2city)
MOTORWAYWIDTH=12
TRUNKWIDTH=12
PRIMARYWIDTH=10
SECONDARYWIDTH=8
TERTIARYWIDTH=6
UNCLASSIFIEDWIDTH=6
RESIDENTIALWIDTH=5
MAJORLINKWIDTH=6
MINORLINKWIDTH=4

# We'll only do the top three levels to "fill in" where osm2city fails
$OGR --max-segment 500 --line-width $MOTORWAYWIDTH --area-type Road work/Road-Motorway landcover/shapefiles/OSM/highway_motorway.shp
$OGR --max-segment 500 --line-width $TRUNKWIDTH --area-type Road work/Road-Trunk landcover/shapefiles/OSM/highway_trunk.shp
$OGR --max-segment 500 --line-width $PRIMARYWIDTH --area-type Road work/Road-Primary landcover/shapefiles/OSM/highway_primary.shp
