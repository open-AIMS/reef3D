library(whitebox)
library(raster)
library(sp)
library(rgdal)
library(sf)
library(rgeos)

dem_maker=function(f, outfolder){
  
  # f<-"/your/path/irregular_points.xyz"
  pts <- read.table(f, header=FALSE, col.names=c("x", "y", "z")) # change accordingly - use read.csv for a csv!
  
  # create a SpatialPointsDataFrame
  coordinates(pts) = ~x+y 									   
  
  # create an empty raster object to the extent of the points
  rast <- raster(ext=extent(pts), resolution=c(0.0008023512, 0.0008023451))
  crs(rast)<-CRS('+init=+proj=merc +lon_0=0 +lat_ts=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs +ellps=WGS84 +towgs84=0,0,0')
  
  # rasterize your irregular points 
  rasOut<-rasterize(pts, rast, pts$z, fun = mean) # we use a mean function here to regularly grid the irregular input points
  
  #write it out as a geotiff
  fout="my_raster.tif"
  writeRaster(rasOut, fout, format="GTiff")
}


vshd=function(dem.file,npts,qsize,h, tempfolder){
  #Example:
  # dem.file='E:\\3d_ltmp\\exports\\DEM\\HELIX_test.tif'
  # npts=5
  # qsize=0.05
  # h=0.05
  #tempfolder
  
  ##SET UP WORKSPACE
  dem=raster(dem.file)
  lin <- rasterToContour(is.na(r))
  pol <- as(st_union(st_polygonize(st_as_sf(lin))), 'Spatial') # st_union to dissolve geometries
  pol<-gBuffer(pol,width=-0.2)
  pts <- spsample(pol[1,], npts, type = 'random')
  vshd={}
  
  ##CALCULATE VIEWSHED FROM EACH POINT
  for (p in 1:length(pts)){
    #generate Observer
    tp<-pts[p,]
    tp<- SpatialPointsDataFrame(tp, data.frame(ID=1:length(tp)))
    writeOGR(tp, layer='obs',"E:\\3d_ltmp\\exports\\viewshed_temp",driver="ESRI Shapefile",overwrite_layer = T)
    
    #Crop DEM to limit ViewShed
    crop.p<-gBuffer(tp, width=qsize,quadsegs=1, capStyle="SQUARE")
    dem=crop(r,extent(crop.p))
    writeRaster(dem, "E:\\3d_ltmp\\exports\\viewshed_temp\\dem.tif",overwrite=T)
    
    #Calculate Viewshed raster
    whitebox::wbt_viewshed("E:\\3d_ltmp\\exports\\viewshed_temp\\dem.tif","E:\\3d_ltmp\\exports\\viewshed_temp\\obs.shp", "E:\\3d_ltmp\\exports\\viewshed_temp\\viewshed.tif", height = h, verbose_mode = FALSE)
    
    #Calculate exposed proportion
    v<-raster("E:\\3d_ltmp\\exports\\viewshed_temp\\viewshed.tif")
    vshd<-c(vshd,sum(v[]>0)*100/sum(v[]>=0))
  }
  return(median(vshd))
}



vshd_wrapper=function(folder,npts,qsize,h){
  list.files(folder, pattern = '*.tif')
  
  
}