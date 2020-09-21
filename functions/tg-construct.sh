#!/bin/bash

function construct () {
    local WBND=$1
    local EBND=$2
    local SBND=$3
    local NBND=$4
    tg-construct --ignore-landmass --work-dir=./work --output-dir=./output/Terrain --min-lon=$WBND --max-lon=$EBND --min-lat=$SBND --max-lat=$NBND AirportArea AirportObj Bog DeciduousForest DryCrop EvergreenForest Grassland Greenspace IrrCrop Lake Marsh MixedForest Ocean Parking Road-Motorway Road-Primary Road-Trunk Rock SRTM-3 Sand Scrub SubUrban Town Urban
}
