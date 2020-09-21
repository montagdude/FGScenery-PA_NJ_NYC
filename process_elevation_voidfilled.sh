#!/bin/bash
#
# Convert to hgt
CWD=$(pwd)
cd elevation_data/SRTM-3_voidfilled
for file in *.tif; do
    base=$(echo $file | cut -f 1 -d '.')
    NORTH=$(echo $base | cut -f 1 -d '_' | cut -f 2 -d 'n')
    WEST=$(echo $base | cut -f 2 -d '_' | cut -f 2 -d 'w')
    gdal_translate -of SRTMHGT $file N${NORTH}W${WEST}.hgt
done

# Now process it
cd $CWD
gdalchop work/SRTM-3 elevation_data/SRTM-3_voidfilled/*.hgt
# http://wiki.flightgear.org/Using_TerraGear#General_comments_from_forum_discussion
terrafit work/SRTM-3 -e 5 -x 20000
rm -f elevation_data/SRTM-3_voidfilled/*.hgt
rm -f elevation_data/SRTM-3_voidfilled/*.aux.xml
