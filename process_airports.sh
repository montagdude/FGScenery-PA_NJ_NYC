#!/bin/bash
#
. functions/airports.sh

echo "Working on block 1 of 11..."
process_airports -80.625000 -79.500000 40.900000 42.375000
echo "Working on block 2 of 11..."
process_airports -80.625000 -79.500000 39.625000 40.900000
echo "Working on block 3 of 11..."
process_airports -79.500000 -77.250000 39.625000 40.900000
echo "Working on block 4 of 11..."
process_airports -79.500000 -77.250000 40.900000 42.125000
echo "Working on block 5 of 11..."
process_airports -77.250000 -75.750000 39.625000 40.900000
echo "Working on block 6 of 11..."
process_airports -77.250000 -75.000000 40.900000 42.125000
echo "Working on block 7 of 11..."
process_airports -75.750000 -74.500000 39.625000 40.900000
echo "Working on block 8 of 11..."
process_airports -75.625000 -74.000000 38.875000 39.625000
echo "Working on block 9 of 11..."
process_airports -74.500000 -73.625000 39.625000 40.900000
echo "Working on block 10 of 11..."
process_airports -75.000000 -73.625000 40.900000 41.625000
echo "Working on block 11 of 11..."
process_airports -73.625000 -71.750000 40.500000 41.250000
