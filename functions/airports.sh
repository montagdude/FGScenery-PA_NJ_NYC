#!/bin/bash

function process_airports () {
    local WBND=$1
    local EBND=$2
    local SBND=$3
    local NBND=$4
    genapts850 --input=apt.dat --work=./work --dem-path=SRTM-3 --min-lon=$WBND --max-lon=$EBND --min-lat=$SBND --max-lat=$NBND 
}
