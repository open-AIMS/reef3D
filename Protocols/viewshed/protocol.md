#Viewshed protocol 

List of steps to estimate the 

1. Import:
	* DEM
	* Mosaic

2. Smooth DEM using raster calculator:
	`CON(IsNull("raster"),FocalStatistics("raster",NbrRectangle(5,5, "CELL"), "raster")`
	
	> NOTE: raster= full path to the DEM raster. Onlu necessary if NODATA values are found in the DEM. 
	
3. Create new polygon layer for gridding. Make the grid.
4. Create random points (simulated fish). 
	* Under Data Management /Sampling/ Create Random Points. 
	* Contrain by feature class "grid". 
	* Number of points = number of fish with each cell.
	* Minimum allowed distance 0.1 (no overlapping).
5. Define observer attributes for each random point with the following parameters:

 | Observer Parameter | Value | Description |
 |-----|-------|-----|
 | OFFSETA | 0.1| Altitude of the observer from the substrate |
 | OFFSETB | 0.1| Altitude of the targetfrom the substrate |
 | RADIUS1 | 0 | Minimum radius of the target |
 | RADIUS2 | 3| Maximum sight/detection distance|
 |VERT1 & VERT2| [90, -90]| Field of view of the observer| 
 |AZIMUTH1 $ AZIMUTH2| [0, 360] | Angular view in the horizontal plane| 
 
6. Set up and run script to generate multiple raster files for the viewshed of each observer.

`viewshed_multipleobs.py`
> NOTE: Modify the path to ArcGIS and to folders. Run this script outside ArcGIS to avoid overloading the workspace with each fish raster. Once the workspace folder is defined, create the following folders inside: "output" and "summary". Workspace folder = folder where all the viewshed outputs will be saved. Also, within the "summary" folder, create a folder called "results".

7. Run script to compile the viewshed data in one table:


viewshed_compile_results.py
> NOTE: make sure you set up the paths to workspace and sumamry (input and output)

8. Select attributes where value is 1 and create a new table using the following script:

cleanup_viewshed_table.py

> Note: Define the workspace

9. Join this resulting table (ID) to corresponding obs shapefile (FID) using Data Management/Add Join from the toolbox. 

10. Convert count data to area and percentage area. Summary stats are based on cell counts. Using the cell size from the DEM file (Properties), calculate the area of each cell and multiply this by each column (Field Calculator).

11. Join the Observers shapefile to grid using Data Management/Add Join from the toolbox.
12. Export resulting table as text file to manage in Excel. 



		

