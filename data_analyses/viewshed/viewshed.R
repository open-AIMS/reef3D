library(whitebox)
library(raster)
library(sp)
library(rgdal)
library(sf)
library(rgeos)

dem_maker=function(f, outfolder){
  require(readr)
  require(sp)
  require(tidyverse)
  require(raster)
  
  # f<-"/your/path/irregular_points.xyz"
  pts <- readr::read_delim(f, delim = " ", col_names = F, col_types = cols(.default="d"))
  pts<-pts[,c(1:3)]
  names(pts)<-c("x","y","z")
  pts<-pts%>%
    drop_na()
  # create a SpatialPointsDataFrame
  coordinates(pts) = ~x+y 									   
  
  # create an empty raster object to the extent of the points
  rast <- raster(ext=extent(pts), resolution=c(0.0008023512, 0.0008023451))
  crs(rast)<-CRS('+init=EPSG:3395')

  # rasterize your irregular points 
  rasOut<-rasterize(pts, rast, pts$z, fun = mean) # we use a mean function here to regularly grid the irregular input points
  
  #write it out as a geotiff
  fout=file.path(outfolder, paste0(basename(tools::file_path_sans_ext(f)),".tif"))
  writeRaster(rasOut, fout, format="GTiff")
}

CV <- function(v){
  
  (sd(v,na.rm=T)/mean(v,na.rm=T))*100
}

vshd=function(dem.file,npts,qsize,h, tempfolder){
  #Example:
  # dem.file='E:\\3d_ltmp\\exports\\DEM\\HELIX_test.tif'
  # npts=5
  # qsize=0.05
  # h=0.05
  #tempfolder
  
  ##SET UP WORKSPACE
  r=raster(dem.file)
  crs(r)<-CRS('+init=EPSG:3395')
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
    # proj4string(tp)<-CRS('+init=EPSG:3395')
    writeOGR(tp, layer='obs',file.path(tempfolder),driver="ESRI Shapefile",overwrite_layer = T)
    
    #Crop DEM to limit ViewShed
    crop.p<-gBuffer(tp, width=qsize,quadsegs=1, capStyle="SQUARE")
    dem=crop(r,extent(crop.p))
    crs(dem)<-CRS('+init=EPSG:3395')
    writeRaster(dem, file.path(tempfolder,"dem.tif"),overwrite=T)
    
    #Calculate Viewshed raster
    whitebox::wbt_viewshed(file.path(tempfolder,"dem.tif"),file.path(tempfolder,"obs.shp"), file.path(tempfolder,"viewshed.tif"), height = h, verbose_mode = FALSE)
    
    #Calculate exposed proportion
    v<-raster(file.path(tempfolder,"viewshed.tif"))
    crs(v)<-CRS('+init=EPSG:3395')
    vshd<-c(vshd,sum(v[]>0)*100/sum(v[]>=0))
  }
  return(c(median(vshd,na.rm=T), CV(vshd)))
}


folder='E:\\3d_ltmp\\exports\\DEM\\OI\\21550S'
vshd_wrapper=function(folder,npts,qsize,h, tempfolder){
  require(stringr)
  dems=list.files(folder, pattern = '*.tif',full.names = T)
  results=data.frame(CAMP=character(),REEF_NAME=character(),SITE_NO=numeric(),TRANSECT_NO=numeric(),
                     viewshed=numeric(), viewshed.cv=numeric())
  camp=str_match(folder, "DEM\\\\(.*?)\\\\")[2]
  print(sprintf("Processing field campaign: %s", camp))
  i=0
  for (dem.file in dems){
    filename=basename(tools::file_path_sans_ext(dem.file))
    i=i+1
    print(sprintf("Calculating viewshed for: %s (%s / %s)",filename,as.character(i),as.character(length(dems))))
    parts=strsplit(filename,"_")
    rn=parts[[1]][1]
    sitetran=as.character(parts[[1]][2])
    sn=as.numeric(strsplit(sitetran, "\\D+")[[1]][-1])[1]
    tn=as.numeric(strsplit(sitetran, "\\D+")[[1]][-1])[2]
    vshd.m=vshd(dem.file,npts,qsize,h, tempfolder)
    results=rbind(data.frame(CAMP=camp,REEF_NAME=rn,SITE_NO=sn,TRANSECT_NO=tn,viewshed=vshd.m[1],viewshed.cv=vshd.m[2]),results)
  }
  return(results)
}

##Exectute viewshed analysis
mytempfolder="E:\\3d_ltmp/exports/viewshed_temp/"
res=vshd_wrapper('E:\\3d_ltmp\\exports\\DEM\\OI\\21550S',3,0.1,0.05, mytempfolder)
