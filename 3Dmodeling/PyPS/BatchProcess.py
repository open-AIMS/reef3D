#!/usr/bin/python


##################################################################
#### Batch process monitoring transects in Agisoft Photoscan #####
##################################################################
#Author: M. Gonzalez-Rivero
#Date: Octuber 2018
#Purpose:

import PhotoScan
import os,re,sys
import pandas as pd
from datetime import datetime


def getDict(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    photoList={}
    listreefs=os.listdir(dirName)
    # Iterate over all the reefs
    for reef in listreefs:
        if os.path.isdir(os.path.join(dirName,reef)):
            listtrans=os.listdir(os.path.join(dirName,reef))
            #iterate over all transects in a reef
            for trans in listtrans:
                if os.path.isdir(os.path.join(dirName,reef,trans)):
                    listimg=os.listdir(os.path.join(dirName,reef,trans))
                    #iterate over all the images in a transect
                    imgs=[]
                    for img in listimg:
                        if re.search(pattern,img):
                            imgs.append(os.path.join(dirName, reef, trans,img))
                    photoList[reef]={trans:imgs}
                            
    return photoList
             

def nearest(items, pivot):
    '''
    Search for the closest date in the scalebar file to the date images were collected
    ''' 
    items=items[items<pivot] #to consider only the dates previous to pivot
    return min(items, key=lambda x: abs(x - pivot))
                
                
def preProcess(chunk, scaletxt='scalebars.csv', qual=0.7,ttshld=60):
    '''
    Pre-processing the chunks by:
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
    sbar = os.path.join(c,'reference_scales', scaletxt)

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
    ref_date=nearest(df['DATE'],img_date)
    file = open(sbar, "rt")
    markers = {}
    for marker in chunk.markers:
        markers[marker.label] = marker

    lines = file.readlines()[1:]
    for line in lines:
        #FIXME there is a problem with the date format time data 'A' does not match format '%d/%m/%y' <MGR>
        tdate,t1,t2, dist = datetime.strptime(line.split(',')[0],'%d/%m/%y'), line.split(',')[1],line.split(',')[2], line.split(',')[3]
        if t1 in markers.keys() and t2 in markers.keys() and ref_date==tdate:
            s=chunk.addScalebar(markers[t1], markers[t2])
            s.reference.distance=float(dist)

    file.close()
        
    ############### Enabling rolling shutter compensation ################################ 
    print("---Rolling shutter compensation---")
    
    try:
        for sensor in chunk.sensors:
            rolling_shutter = True
    except Exception as e:
        print("Error:", e)
        raise
        
#TODO move this to a separate script that wraps the prcessing per transect/reef <mgr>
def runNetwork():
    ''''
    Run a task over the network
    '''

    client = PhotoScan.NetworkClient()

    task1 = PhotoScan.NetworkTask()
    task1.name = 'RunScript'
    task1.params['path'] = "processing/script.py" #path to the script to be executed
    task1.params['args'] = "argument1 argument2" #string of the arguments with space as separator

    path = "projects/project.psx" 
    client.connect('agisoft-qmgr.aims.gov.au') #server ip
    batch_id = client.createBatch(path, [task1])
    client.resumeBatch(batch_id)
    print("Job started...")

			
def photoscanProcess(root_path, save_path, export_path, scaletxt):				
	#PhotoScan.app.messageBox('hello world! \n')
	PhotoScan.app.console.clear()

	## construct the document class
	doc = PhotoScan.app.document

	## save project
	#doc.open("M:/Photoscan/practise.psx")
	psxfile = root_path + 'practise.psx'
	doc.save( psxfile )
	print ('>> Saved to: ' + psxfile)

	## point to current chunk
	#chunk = doc.chunk

	## add a new chunk
	chunk = doc.addChunk()

	## set coordinate system
	# - PhotoScan.CoordinateSystem("EPSG::4612") -->  JGD2000
	chunk.crs = PhotoScan.CoordinateSystem("EPSG::4612")

	################################################################################################
	### get photo list ###
	photoList = []
	getPhotoList(root_path, photoList)
	#print (photoList)
	
	################################################################################################
	### add photos ###
	# addPhotos(filenames[, progress])
	# - filenames(list of string) – A list of file paths.
	chunk.addPhotos(photoList)
	
	################################################################################################
	### align photos ###
	## Perform image matching for the chunk frame.
	# matchPhotos(accuracy=HighAccuracy, preselection=NoPreselection, filter_mask=False, keypoint_limit=40000, tiepoint_limit=4000[, progress])
	# - Alignment accuracy in [HighestAccuracy, HighAccuracy, MediumAccuracy, LowAccuracy, LowestAccuracy]
	# - Image pair preselection in [ReferencePreselection, GenericPreselection, NoPreselection]
	chunk.matchPhotos(accuracy=PhotoScan.LowAccuracy, preselection=PhotoScan.ReferencePreselection, filter_mask=False, keypoint_limit=0, tiepoint_limit=0)
	chunk.alignCameras()

	################################################################################################
	### build dense cloud ###
	## Generate depth maps for the chunk.
	# buildDenseCloud(quality=MediumQuality, filter=AggressiveFiltering[, cameras], keep_depth=False, reuse_depth=False[, progress])
	# - Dense point cloud quality in [UltraQuality, HighQuality, MediumQuality, LowQuality, LowestQuality]
	# - Depth filtering mode in [AggressiveFiltering, ModerateFiltering, MildFiltering, NoFiltering]
	chunk.buildDenseCloud(quality=PhotoScan.LowQuality, filter=PhotoScan.AggressiveFiltering)

	################################################################################################
	### build mesh ###
	## Generate model for the chunk frame.
	# buildModel(surface=Arbitrary, interpolation=EnabledInterpolation, face_count=MediumFaceCount[, source ][, classes][, progress])
	# - Surface type in [Arbitrary, HeightField]
	# - Interpolation mode in [EnabledInterpolation, DisabledInterpolation, Extrapolated]
	# - Face count in [HighFaceCount, MediumFaceCount, LowFaceCount]
	# - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
	chunk.buildModel(surface=PhotoScan.HeightField, interpolation=PhotoScan.EnabledInterpolation, face_count=PhotoScan.HighFaceCount)
	
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
	chunk.buildDem(source=PhotoScan.DenseCloudData, interpolation=PhotoScan.EnabledInterpolation, projection=chunk.crs)

	################################################################################################
	## Build orthomosaic for the chunk.
	# buildOrthomosaic(surface=ElevationData, blending=MosaicBlending, color_correction=False[, projection ][, region ][, dx ][, dy ][, progress])
	# - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
	# - Blending mode in [AverageBlending, MosaicBlending, MinBlending, MaxBlending, DisabledBlending]
	chunk.buildOrthomosaic(surface=PhotoScan.ModelData, blending=PhotoScan.MosaicBlending, color_correction=True, projection=chunk.crs)
	
	################################################################################################
	## auto classify ground points (optional)
	#chunk.dense_cloud.classifyGroundPoints()
	#chunk.buildDem(source=PhotoScan.DenseCloudData, classes=[2])
	
	################################################################################################
	doc.save()

# main
qual = float(sys.argv[1]) # quality threshold for filtering images
ttshld = int(sys.argv[2]) # Tolerance threshold for detecting markers

folder = "M:/Photoscan/Photos/"
photoscanProcess(folder)









