# FGScenery-PA_NJ_NYC

Custom FlightGear scenery for Pennsylvania, New Jersey, and New York City
Data sources:
* Landcover: National landcover database (NLCD):
  https://www.usgs.gov/centers/eros/science/national-land-cover-database
* Elevation: Shuttle Radar Topology Mission 3-arc-second (SRTM-3), void-filled version:
  https://earthexplorer.usgs.gov/
* Rivers and waterbodies: National Hydrography Dataset (NHD):
  https://www.usgs.gov/core-science-systems/ngp/national-hydrography
* Buildings, roads, pylons, other objects: OpenStreetMap using osm2city:
  https://www.openstreetmap.org/
  https://osm2city.readthedocs.io/en/latest/
* Also includes TerraSync objects
* Custom materials: National Agriculture Imagery Program (NAIP):
  https://earthexplorer.usgs.gov/

The git repository includes the scripts used to generate the scenery, but it does not include all the input data. To just download the scenery itself, go to the Releases page and download the zip archives.

Installation and Usage
================================================================================
To install, download Buildings.zip, Objects.zip, Pylons.zip, Roads.zip, and Terrain.zip, and extract them wherever you like, for example, into a directory called PA_NJ_NYC on your computer. Point FlightGear to the directory with the --fg-scenery command line option, the FG_SCENERY environment variable, or add it to Additional Scenery Folders in the GUI. To use the custom materials, download FGData.zip, extract, and copy the contents to the appropriate locations in your FGData directory (aka $FG_ROOT). For example, eastern-us.xml and materials.xml go in $FG_ROOT/Materials/regions, and the textures go in $FG_ROOT/Textures/Terrain.

For the best experience, if your computer can handle it, turn on OSM buildings and detailed roads and pylons under Rendering Options. Note that some areas, especially downtown New York City, will require a powerful video card to get decent framerates with these options on.

Screenshots
================================================================================

![alt tag](https://raw.githubusercontent.com/montagdude/FGScenery-PA_NJ_NYC/master/area_covered.png)
Area covered by this scenery

![alt tag](https://raw.githubusercontent.com/montagdude/FGScenery-PA_NJ_NYC/master/screenshots/c182s-atlantic-city.png)
Atlantic City, NJ

![alt tag](https://raw.githubusercontent.com/montagdude/FGScenery-PA_NJ_NYC/master/screenshots/dr400-philadelphia.png)
Philadelphia, PA

![alt tag](https://raw.githubusercontent.com/montagdude/FGScenery-PA_NJ_NYC/master/screenshots/ec135-manhattan.png)
Manhattan, NYC

![alt tag](https://raw.githubusercontent.com/montagdude/FGScenery-PA_NJ_NYC/master/screenshots/pa28-wilkes-barre.png)
Wilkes-Barre, PA
