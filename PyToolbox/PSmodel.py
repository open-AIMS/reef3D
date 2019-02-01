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

          
def preProcess(doc, chunk, qual,ttshld, scaletxt, calfile):
    '''
    Pre-processing chunks by:
    1) detecting markers
    2) adding scale bars
    3) filtering images by quality
    4) Roller shutter compensation
    5) Add Camera callibration
    
    Inputs:
    * doc: Photoscan document object(e.g., PhotoScan.app.document)
    * scaletxt: name of the file containing the distance between markers and date of measurements (e.g., scalebars.csv)
    * qual: quality threshold used to filter images
    * ttshold:  tolerance threshold for marker detection
    *calfile= calibration parameters in XML format. If no calibration exist type 'NONE'
    '''
    
    ### SET ENVIRONMENTAL VARIABLES 
    docpath=doc.path
    c=docpath.split('/projects')[0]
    print(c)
    sbar = os.path.join(c,'reference_scales', scaletxt)
    print(sbar)
    df=pd.read_csv(sbar,delimiter='\t')
    df['DATE']=pd.to_datetime(df['DATE'],format='%d/%m/%Y')
    
    ############### Enabling rolling shutter compensation ################################ 
    print("---Rolling shutter compensation---")
    
    try:
        for sensor in chunk.sensors:
            sensor.rolling_shutter = True
            #sensor.type = PhotoScan.Sensor.Type.Fisheye         
    except Exception as e:
        print("Error:", e)
        raise
        
    
    ############## Import Camera calibration parameters ###############
    if calfile!='NONE':
        print("---Importing calibration parameters---")
        calib = PhotoScan.Calibration()
        os.path.join(c,'calibration', calfile)
        calib.load(os.path.join(c,'calibration', calfile), format="xml")
        sensor = chunk.sensors[0] #first calibration group in the active chunk

        #sensor.calibration = calib # this will set the Adjusted values according to the XML
        sensor.user_calib = calib #and this will load the XML values to the Initial values

    
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
    img_date=datetime.strptime(camera.photo.meta['Exif/DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
    ref_date=pst.nearest(df['DATE'],img_date)

    markers = {}
    for marker in chunk.markers:
        markers[marker.label] = marker

    with open(sbar, 'r', errors='replace') as f:
        lines = f.readlines()[1:]
    for line in lines:
        #FIXME there is a problem with the date format time data 'A' does not match format '%d/%m/%y' <MGR>
        tdate,t1,t2, dist = datetime.strptime(line.split('\t')[0],'%d/%m/%Y'), line.split('\t')[1],line.split('\t')[2], line.split('\t')[3]
        
        if t1 in markers.keys() and t2 in markers.keys() and ref_date==tdate:
            s=chunk.addScalebar(markers[t1], markers[t2])
            s.reference.distance=float(dist)

        


        
def checkalign(chunk):
    aligned_photos = []   # empty list
    for camera in chunk.cameras:
        if camera.transform:
            aligned_photos.append(camera.label)  # creates list of photos that aligned
    return(aligned_photos)



def photoscanProcess(path, export_path,
scaletxt = "scalebars.csv",proj_path = "projects",
data_path = "data/LTMP",calfile = "callibration_fisheye.xml"):				
    ''''
    path: relative directory path to each transect. Eventually this will come from reefmon
    export_path: folder name where data will be exported to (not built in here yet)
    scaletext: text file containing the scale bar measurements per trip
    proj_path: root folder where projects will be saved
    data_path: root directory where data is stored. This will help using the relative path in "path"
    calfile: califration parameter files from cameras. This should be stored in the calibration folder
    
    '''
    ### Set GPU environment ####
    PhotoScan.app.gpu_mask = 2 ** len(PhotoScan.app.enumGPUDevices()) - 1 #setting GPU mask
    if PhotoScan.app.gpu_mask:
        PhotoScan.app.cpu_enable = False
    else:
        PhotoScan.app.cpu_enable = True
    ## end of set GPU environment
    
    ### processing parameters
    accuracy = PhotoScan.Accuracy.MediumAccuracy  #align photos accuracy
    reference_preselection = False
    generic_preselection = True
    keypoints = 40000 #align photos key point limit
    tiepoints = 4000 #align photos tie point limit
    source = PhotoScan.DataSource.DenseCloudData #build mesh/DEM source
    surface = PhotoScan.SurfaceType.HeightField #build mesh surface type
    quality = PhotoScan.Quality.LowQuality #build dense cloud quality 
    filtering = PhotoScan.FilterMode.AggressiveFiltering #depth filtering
    interpolation = PhotoScan.Interpolation.EnabledInterpolation #build mesh interpolation 
    blending = PhotoScan.BlendingMode.MosaicBlending #blending mode
    face_num = PhotoScan.FaceCount.HighFaceCount #build mesh polygon count
    mapping = PhotoScan.MappingMode.GenericMapping #build texture mapping
    atlas_size = 4096
    TYPES = ["jpg", "jpeg", "tif", "tiff"]
    
	###end of processing parameters definition
    print("Processing " + path)
    ##Create folder structure
    desc=path.split('/')
    ##desc should include campaign[0], reef anme[1] and sitetransect[2]

    if not os.path.exists(os.path.join(proj_path,desc[0],desc[1])):
        os.makedirs(os.path.join(proj_path,desc[0],desc[1]))
        
    #PhotoScan.app.messageBox('hello world! \n')
    PhotoScan.app.console.clear()
    ## construct the document class
    doc = PhotoScan.app.document
    ## save project
    psxfile = os.path.join(proj_path,path + '.psx')
    doc.save( psxfile )
    print ('>> Project saved to: ' + psxfile)
    
    #List images and split them into chuncks
    #imlist=glob.glob(os.path.join(data_path,desc[0],desc[1],desc[2])+'/*.JPG')
    docpath=doc.path
    c=docpath.split('/projects')[0]
    list_files = os.listdir(os.path.join(c,data_path,path))
    imlist = list()
    for entry in list_files: #finding image files
    	file = os.path.join(c,data_path,path, entry)
    	if os.path.isfile(file):
    		if file[-3:].lower() in TYPES:
    			imlist.append(file)
                
    
    if not(len(imlist)):
    	print("No images in " + path)
    	return False
        
    imdate=[]
    for i in imlist:
        d=Image.open(os.path.join(path,i))._getexif()[36867]
        imdate.append(datetime.strptime(d, '%Y:%m:%d %H:%M:%S')) #get image date time
    
    im=pd.DataFrame({'im':imlist,'date':imdate})
    im=im.sort_values('date', ascending=1)
    imlist=im.im
    n=200 #group size
    m=10 #overlap
    imlist=[imlist[i:i+n] for i in range(0, len(imlist), n-m)]
    
    ## create a chunk for every image group and process it
    for i in range(0,len(imlist)):
        chunk = doc.addChunk()
        chunk.label=desc[2]+'_'+str(i)
        chunk.addPhotos(imlist[i])
        preProcess(doc, chunk, 0.5, 80, scaletxt, calfile)

        ### align photos ###
        ## Perform image matching for the chunk frame.
        # matchPhotos(accuracy=HighAccuracy, preselection=NoPreselection, filter_mask=False, keypoint_limit=40000, tiepoint_limit=4000[, progress])
        # - Alignment accuracy in [HighestAccuracy, HighAccuracy, MediumAccuracy, LowAccuracy, LowestAccuracy]
        # - Image pair preselection in [ReferencePreselection, GenericPreselection, NoPreselection]
        chunk.matchPhotos(accuracy = accuracy, 
        generic_preselection = generic_preselection, 
        reference_preselection = reference_preselection, 
        filter_mask = False, 
        keypoint_limit = keypoints, 
        tiepoint_limit = tiepoints)
        chunk.alignCameras()
        chunk.optimizeCameras()
        chunk.resetRegion()
        doc.save()

    	### build dense cloud ###
    	## Generate depth maps for the chunk.
    	# buildDenseCloud(quality=MediumQuality, filter=AggressiveFiltering[, cameras], keep_depth=False, reuse_depth=False[, progress])
    	# - Dense point cloud quality in [UltraQuality, HighQuality, MediumQuality, LowQuality, LowestQuality]
    	# - Depth filtering mode in [AggressiveFiltering, ModerateFiltering, MildFiltering, NoFiltering]

    	### build mesh ###
    	## Generate model for the chunk frame.
        chunk.buildDepthMaps(quality = quality, filter = filtering)
        chunk.buildDenseCloud(point_colors = True, keep_depth = False)
        doc.save()
        # - Surface type in [Arbitrary, HeightField]
        #         - Interpolation mode in [EnabledInterpolation, DisabledInterpolation, Extrapolated]
        #         - Face count in [HighFaceCount, MediumFaceCount, LowFaceCount
        #         - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
    	
        ###building mesh
        chunk.buildModel(surface = surface, source = source, interpolation = interpolation, face_count = face_num)
        doc.save()

    	###build texture
        chunk.buildUV(mapping = mapping, count = 2)
        chunk.buildTexture(blending = blending, size = atlas_size)
        doc.save()

        print("Processed " + chunk.label)



## Merge chunks
# chunk = doc.addChunk()
# chunk.label=desc[2]
# chunk.mergeChunks(doc.chunks, merge_dense_clouds=False, merge_markers=True)

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
### build DEM (before build dem, you need to save the project into psx) ###
## Build elevation model for the chunk.
# buildDem(source=DenseCloudData, interpolation=EnabledInterpolation[, projection ][, region ][, classes][, progress])
# - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
# chunk.buildDem(source=PhotoScan.DenseCloudData, interpolation=PhotoScan.EnabledInterpolation, projection=chunk.crs)
#     doc.save( psxfile )


#
################################################################################################
## auto classify ground points (optional)
#chunk.dense_cloud.classifyGroundPoints()
#chunk.buildDem(source=PhotoScan.DenseCloudData, classes=[2])

################################################################################################
	











