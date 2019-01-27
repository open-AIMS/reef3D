#!/usr/bin/python

##################################################################
#### 3D recontruction from monitoring transects in Agisoft Photoscan #####
##################################################################
#Author: M. Gonzalez-Rivero
#Date: November 2018
#Purpose:

import PhotoScan
import os,re,sys
import pandas as pd
from datetime import datetime
import sys
sys.path.append('/Users/uqmgonz1/Documents/GitHub')
from reef3D.PyToolbox import PStools as pst
import glob
from PIL import Image

          
def preProcess(doc, chunk, qual=0.7,ttshld=60, scaletxt='scalebars.csv'):
    '''
    Pre-processing chunks by:
    1) detecting markers
    2) adding scale bars
    3) filtering images by quality
    4) Roller shutter compensation
    
    Inputs:
    * doc: Photoscan document object(e.g., PhotoScan.app.document)
    * scaletxt: name of the file containing the distance between markers and date of measurements (e.g., scalebars.csv)
    * qual: quality threshold used to filter images
    * ttshold:  tolerance threshold for marker detection
    '''
    
    ### SET ENVIRONMENTAL VARIABLES 
    docpath=doc.path
    c=docpath.split('/projects')[0]
    print(c)
    sbar = os.path.join(c,'reference_scales', scaletxt)
    print(sbar)
    df=pd.read_csv(sbar,delimiter=',')
    df['DATE']=pd.to_datetime(df['DATE'],format='%d/%m/%y')
    
    ############### Image quality control ###############################
    print("---Estimating image quality---")
    chunk.estimateImageQuality(chunk.cameras)
    for camera in chunk.cameras:
        if float(camera.meta["Image/Quality"]) < qual:
            camera.enabled = False
 
    ############### Marker detection ###############################
    print("---Detecting Markers---")
    chunk.detectMarkers(PhotoScan.TargetType.CircularTarget12bit, ttshld)
    
    ############### Add ScaleBars and distande from file ###############################
    print("---Adding ScaleBars---")
    camera = chunk.cameras[0]
    #TODO modify this to allow multiple camera metadata. A posible to solution is to add the cruise date as an argument
    #img_date=datetime.strptime(camera.photo.meta['Exif/DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
    img_date=datetime.strptime('2018:10:07 10:45:23', '%Y:%m:%d %H:%M:%S')
    ref_date=pst.nearest(df['DATE'],img_date)

    markers = {}
    for marker in chunk.markers:
        markers[marker.label] = marker

    with open(sbar, 'r', errors='replace') as f:
        lines = f.readlines()[1:]
    for line in lines:
        #FIXME there is a problem with the date format time data 'A' does not match format '%d/%m/%y' <MGR>
        tdate,t1,t2, dist = datetime.strptime(line.split(',')[0],'%d/%m/%y'), line.split(',')[1],line.split(',')[2], line.split(',')[3]
        if t1 in markers.keys() and t2 in markers.keys() and ref_date==tdate:
            s=chunk.addScalebar(markers[t1], markers[t2])
            s.reference.distance=float(dist)

        
    ############### Enabling rolling shutter compensation ################################ 
    print("---Rolling shutter compensation---")
    
    try:
        for sensor in chunk.sensors:
            rolling_shutter = True
    except Exception as e:
        print("Error:", e)
        raise
        
def checkalign(chunk):
    aligned_photos = []   # empty list
    for camera in chunk.cameras:
        if camera.transform:
            aligned_photos.append(camera.label)           # creates list of photos that aligned

    return(aligned_photos)

			
def photoscanProcess(desc, export_path, scaletxt, photoList,proj_path='projects',data_path='data/LTMP'):				
    ''''
    desc: string vector containing: campaign[0], reefname[1], transectid[2]
    
    '''
    ##Create folder structure
    if not os.path.exists(os.path.join(proj_path,desc[0],desc[1],desc[2])):
        os.makedirs(os.path.join(proj_path,desc[0],desc[1],desc[2]))
    #PhotoScan.app.messageBox('hello world! \n')
    PhotoScan.app.console.clear()
    ## construct the document class
    doc = PhotoScan.app.document
    ## save project
    psxfile = os.path.join(proj_path,str(desc[0]),str(desc[1]),str(desc[2]),str(desc[2] + '.psx'))
    doc.save( psxfile )
    print ('>> Project saved to: ' + psxfile)
    
    #List images and split them into chuncks
    imlist=glob.glob(os.path.join(data_path,desc[0],desc[1],desc[2])+'/*.JPG')
    imdate=[]
    for i in imlist:
        d=Image.open(i)._getexif()[36867]
        imdate.append(datetime.strptime(d, '%Y:%m:%d %H:%M:%S')) #get image date time
    
    im=pd.DataFrame({'im':imlist,'date':imdate})
    im=im.sort_values('date', ascending=1)
    imlist=im.im
    n=200 #group size
    m=20 #overlap
    imlist=[imlist[i:i+n] for i in range(0, len(imlist), n-m)]
    
    ## create a chunk for every image group
    for i in range(0,len(imlist)):
        chunk = doc.addChunk()
        chunk.label=desc[2]+'_'+str(i)
        chunk.addPhotos(imlist[i])
    
    ################################################################################################
    
    for c in doc.chunks:
        #Detect markers and filter bad images
        preProcess(doc, c, scaletxt='scalebars.csv', qual=0.5,ttshld=80)
        ################################################################################################
        ### align photos ###
        ## Perform image matching for the chunk frame.
        # matchPhotos(accuracy=HighAccuracy, preselection=NoPreselection, filter_mask=False, keypoint_limit=40000, tiepoint_limit=4000[, progress])
        # - Alignment accuracy in [HighestAccuracy, HighAccuracy, MediumAccuracy, LowAccuracy, LowestAccuracy]
        # - Image pair preselection in [ReferencePreselection, GenericPreselection, NoPreselection]
        chunk.matchPhotos(accuracy=PhotoScan.LowAccuracy, 
        preselection=PhotoScan.GenericPreselection, 
        filter_mask=False, keypoint_limit=0, 
        tiepoint_limit=50000)
        chunk.alignCameras()
        doc.save( psxfile )
    	################################################################################################
    	### build dense cloud ###
    	## Generate depth maps for the chunk.
    	# buildDenseCloud(quality=MediumQuality, filter=AggressiveFiltering[, cameras], keep_depth=False, reuse_depth=False[, progress])
    	# - Dense point cloud quality in [UltraQuality, HighQuality, MediumQuality, LowQuality, LowestQuality]
    	# - Depth filtering mode in [AggressiveFiltering, ModerateFiltering, MildFiltering, NoFiltering]
        chunk.buildDenseCloud(quality=PhotoScan.LowQuality, filter=PhotoScan.AggressiveFiltering)
        doc.save( psxfile )

        ################################################################################################
    	### build mesh ###
    	## Generate model for the chunk frame.
    	# buildModel(surface=Arbitrary, interpolation=EnabledInterpolation, face_count=MediumFaceCount[, source ][, classes][, progress])
    	# - Surface type in [Arbitrary, HeightField]
    	# - Interpolation mode in [EnabledInterpolation, DisabledInterpolation, Extrapolated]
    	# - Face count in [HighFaceCount, MediumFaceCount, LowFaceCount]
    	# - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
    	# chunk.buildModel(surface=PhotoScan.HeightField, interpolation=PhotoScan.EnabledInterpolation, face_count=PhotoScan.HighFaceCount)
        #     doc.save( psxfile )

	## Merge chunks
    chunk = doc.addChunk()
    chunk.label=desc[2]
    chunk.mergeChunks(doc.chunks, merge_dense_clouds=False, merge_markers=True)
    
    ## Produce Report
    #TODO extract and export camera pose <MGR>
    #check this: chunk.transform.matrix
	################################################################################################
	### build texture (optional) ###
	## Generate uv mapping for the model.
	# buildUV(mapping=GenericMapping, count=1[, camera ][, progress])
	# - UV mapping mode in [GenericMapping, OrthophotoMapping, AdaptiveOrthophotoMapping, SphericalMapping, CameraMapping]
	#chunk.buildUV(mapping=PhotoScan.AdaptiveOrthophotoMapping)
	## Generate texture for the chunk.
	# buildTexture(blending=MosaicBlending, color_correction=False, size=2048[, cameras][, progress])
	# - Blending mode in [AverageBlending, MosaicBlending, MinBlending, MaxBlending, DisabledBlending]
	#chunk.buildTexture(blending=PhotoScan.MosaicBlending, color_correction=True, size=30000)

	################################################################################################
	## save the project before build the DEM and Ortho images
    doc.save()

	################################################################################################
	### build DEM (before build dem, you need to save the project into psx) ###
	## Build elevation model for the chunk.
	# buildDem(source=DenseCloudData, interpolation=EnabledInterpolation[, projection ][, region ][, classes][, progress])
	# - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
	# chunk.buildDem(source=PhotoScan.DenseCloudData, interpolation=PhotoScan.EnabledInterpolation, projection=chunk.crs)
#     doc.save( psxfile )

	################################################################################################
	## Build orthomosaic for the chunk.
	# buildOrthomosaic(surface=ElevationData, blending=MosaicBlending, color_correction=False[, projection ][, region ][, dx ][, dy ][, progress])
	# - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
	# - Blending mode in [AverageBlending, MosaicBlending, MinBlending, MaxBlending, DisabledBlending]
	# chunk.buildOrthomosaic(surface=PhotoScan.ModelData, blending=PhotoScan.MosaicBlending, color_correction=True, projection=chunk.crs)
#     doc.save( psxfile )
#
	################################################################################################
	## auto classify ground points (optional)
	#chunk.dense_cloud.classifyGroundPoints()
	#chunk.buildDem(source=PhotoScan.DenseCloudData, classes=[2])
	
	################################################################################################
	# doc.save()











