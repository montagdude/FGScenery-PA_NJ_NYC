#!/usr/bin/env python
#
# Generates TerraGear processing scripts
#

import sys
import os
from matplotlib import pyplot as plt

class Block:

    def __init__(self, blockid, blockfile=None):
        self._id = blockid
        self._west = None
        self._east = None
        self._south = None
        self._north = None
        self._areaPlacement = []    # Defines where block lies in overall region area
                                    # (e.g., NORTH, WEST, INTERIOR, etc.)
        if blockfile is not None:
            self.readBlockDefinition(blockfile)

    def readBlockDefinition(self, filename):
        try:
            f = open(filename)
        except IOError:
            sys.stderr.write("Error: unable to open {:s}.\n".format(filename))
            sys.exit(1)

        boundary = f.readline()
        for placement in ["NORTH", "SOUTH", "EAST", "WEST", "INTERIOR"]:
            if boundary.find(placement) != -1:
                self._areaPlacement.append(placement)

        line = f.readline()     # Top left corner
        try:
            self._west = float(line.split()[0])
            self._north = float(line.split()[1])
        except (IndexError, ValueError) as e:
            sys.stderr.write("Error parsing {:f}.\n".format(filename))
            sys.exit(1)
        line = f.readline()
        line = f.readline()     # Bottom right corner
        try:
            self._east = float(line.split()[0])
            self._south = float(line.split()[1])
        except (IndexError, ValueError) as e:
            sys.stderr.write("Error parsing {:f}.\n".format(filename))
            sys.exit(1)
        f.close()

    def plot(self, ax):
        '''Plots block on an axis'''
        x = [self._west, self._west, self._east, self._east, self._west]
        y = [self._north, self._south, self._south, self._north, self._north]
        ax.plot(x, y)
        cen = (0.5*(self._west + self._east), 0.5*(self._south + self._north))
        ax.annotate(self._id, cen, ha='center', va='center')

    def area(self):
        return (self._east - self._west)*(self._north - self._south)


def plot_blocks(blocks):
    fig, ax = plt.subplots()
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Blocks")
    for block in blocks:
        block.plot(ax)
    ax.set_aspect('equal', 'datalim')
    ax.grid()
    plt.show()
    fig.savefig("blocks.png", bbox_inches="tight")


def write_airport_script(blocks):
    '''Writes script to run genapts850 for all blocks'''

    f = open("process_airports.sh", "w")
    f.write("#!/bin/bash\n")
    f.write("#\n")
    f.write(". functions/airports.sh\n\n")
    nblocks = len(blocks)
    for i,block in enumerate(blocks):
        f.write("echo \"Working on block {:d} of {:d}...\"\n".format(i+1,nblocks))
        f.write("process_airports {:f} {:f} {:f} {:f}\n".format(block._west, block._east,
                                                                block._south, block._north))
    f.close()
    os.chmod("process_airports.sh", 0o755)


def write_tgconstruct_script(blocks):
    '''Writes script to run tg-construct for all blocks'''

    f = open("tg-construct.sh", "w")
    f.write("#!/bin/bash\n")
    f.write("#\n")
    f.write(". functions/tg-construct.sh\n\n")
    nblocks = len(blocks)
    for i,block in enumerate(blocks):
        # For north boundary of area, need to subtract 1 tile height from the command
        # to get TerraGear to generate to the intended latitude. Otherwise it goes too
        # far and ends up with "cliffs" at the edge of the shapefiles and a big gap with
        # the default terrain. I don't know why that is, but it is nonetheless.
        north = block._north
        west = block._west
        f.write("echo \"Working on block {:d} of {:d}...\"\n".format(i+1,nblocks))
        if "NORTH" in block._areaPlacement:
            north -= 0.125
        #FIXME: for this scenery only
        if i==0 or i==1:
            print("Warning: West boundary is being adjusted. Please review this in future scripts.")
            west += 0.125       # Because I put the border at -80.625, which I think is actually
                                # halfway between tiles.
        f.write("construct {:f} {:f} {:f} {:f}\n".format(west, block._east,
                                                         block._south, north))
    f.close()
    os.chmod("tg-construct.sh", 0o755)


def write_osm2city_script(block):
    '''Writes osm2city script and other files for a block'''

    # Parameters file
    f = open(os.path.join("osm2city", "block{:d}_params.ini".format(block._id)), "w")
    f.write("PREFIX = \"block{:d}\"\n".format(block._id))
    f.write("PATH_TO_SCENERY = \"/home/dello/Projects/FGScenery_development/PA_NJ_NYC/output\"\n")
    f.write("PATH_TO_OUTPUT = \"/home/dello/Projects/FGScenery_development/PA_NJ_NYC/output\"\n")
    f.write("PATH_TO_OSM2CITY_DATA = \"/home/dello/Projects/FGScenery_tools/osm2city-data\"\n\n")

    f.write("NO_ELEV = False\n")
    f.write("FG_ELEV = \"/usr/bin/fgelev\"\n")
    f.write("PROBE_FOR_WATER = True\n")
    f.write("OWBB_USE_BTG_LANDUSE = False\n")
    f.write("BUILDING_FORCE_EUROPEAN_INNER_CITY_STYLE = False\n")
    f.write("POINTS_ON_LINE_DISTANCE_MAX = 100\n")
    f.write("MAX_SLOPE_ROAD = 0.15\n")
    f.write("MAX_SLOPE_MOTORWAY = 0.15\n")
    f.write("MIN_ABOVE_GROUND_LEVEL = 0.25\n")
    f.write("HIGHWAY_TYPE_MIN = 5\n\n")
    
    f.write("DB_HOST = \"localhost\"\n")
    f.write("DB_PORT = 5432\n")
    f.write("DB_NAME = \"block{:d}\"\n".format(block._id))
    f.write("DB_USER = \"postgres\"\n")
    f.write("DB_USER_PASSWORD = \"Time4ADatabase!\"\n")
    f.close()

    # osm2city script
    scriptfile = os.path.join("osm2city", "block{:d}_osm2city.sh".format(block._id))
    f = open(scriptfile, "w")
    f.write("#!/bin/bash\n\n")

    f.write("set -e\n")
    f.write("export PYTHONPATH=/home/dello/Projects/FGScenery_tools/osm2city:$PYTHONPATH\n")
    f.write("export FG_ROOT=/home/dello/SlackBuilds/games/FlightGear-data/fgdata\n")
    f.write("export JAVACMD_OPTIONS=-Djava.io.tmpdir=/home/dello/Desktop\n")
    f.write("echo \"Please enter your user's password for sudo and then the DB password\"\n")
    f.write("sudo -u postgres createdb --encoding=UTF8 --owner=postgres block{:d}\n"\
            .format(block._id))
    f.write("psql --username=postgres --dbname=block{:d} -c \"CREATE EXTENSION postgis;\"\n"\
            .format(block._id))
    f.write("psql --username=postgres --dbname=block{:d} -c \"CREATE EXTENSION hstore;\"\n"\
            .format(block._id))
    f.write("psql --username=postgres --dbname=block{:d} -f ".format(block._id) +
            "/home/dello/Projects/FGScenery_tools/osmosis-latest/script/pgsnapshot_schema_0.6.sql\n")
    f.write("psql --username=postgres --dbname=block{:d} -f ".format(block._id) +
            "/home/dello/Projects/FGScenery_tools/osmosis-latest/script/pgsnapshot_schema_0.6_bbox.sql\n")
    f.write("/home/dello/Projects/FGScenery_tools/osmosis-latest/bin/osmosis --read-pbf " +
            "file=../pa_nj_nyc.osm.pbf --bounding-box completeWays=yes " +
            "top={:.4f} left={:.4f} bottom={:.4f} right={:.4f} "\
            .format(block._north, block._west, block._south, block._east) +
            "--write-pbf file=block{:d}.osm.pbf\n".format(block._id))
    f.write("/home/dello/Projects/FGScenery_tools/osmosis-latest/bin/osmosis --read-pbf " +
            "file=block{:d}.osm.pbf ".format(block._id) +
            "--log-progress --write-pgsql database=block{:d} ".format(block._id) +
            "host=localhost:5432 user=postgres password=Time4ADatabase!\n")
    f.write("psql --username=postgres --dbname=block{:d} -c ".format(block._id) +
            "\"CREATE INDEX idx_nodes_tags ON nodes using gist(tags);\"\n")
    f.write("psql --username=postgres --dbname=block{:d} -c ".format(block._id) +
            "\"CREATE INDEX idx_ways_tags ON ways using gist(tags);\"\n")
    f.write("psql --username=postgres --dbname=block{:d} -c ".format(block._id) +
            "\"CREATE INDEX idx_relations_tags ON relations using gist(tags);\"\n")
    f.write("python3 /home/dello/Projects/FGScenery_tools/osm2city/build_tiles.py " +
            "--logtofile -f block{:d}_params.ini -b ".format(block._id) +
            "*{:.3f}_{:.3f}_{:.3f}_{:.3f} -p 4\n".format(block._west, block._south,
            block._east, block._north))
    os.chmod(scriptfile, 0o755)
    f.close()


if __name__ == "__main__":

    nblocks = 11
    osm2city_block = None
    if len(sys.argv) < 2:
        print("No osm2city script generated. To do that, invoke this script like this:")
        print("{:s} osm2city_blockid".format(sys.argv[0]))
    else:
        osm2city_block = int(sys.argv[1])
        if osm2city_block > nblocks:
            sys.stderr.write("Max block id is {:d}.\n".format(nblocks))
            sys.exit(1)

    blocks = [Block(i, "block{:d}.txt".format(i)) for i in range(1,nblocks+1)]
    area = 0.
    for block in blocks:
        area += block.area()
    print("Area: {:.2f} sq deg".format(area))
    plot_blocks(blocks)
    write_airport_script(blocks)
    write_tgconstruct_script(blocks)
    if osm2city_block is not None:
        write_osm2city_script(blocks[osm2city_block-1])
