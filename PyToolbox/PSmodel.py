#!/usr/bin/python

##################################################################
#### 3D recontruction from monitoring transects in Agisoft Photoscan #####
##################################################################
#Author: M. Gonzalez-Rivero
#Date: February 2019
#Purpose: Given a path to images in a transect, this script will split images into chunks and process the reconstruction to produce:
#   * 

import PhotoScan
import os,re,sys
import pandas as pd
from datetime import datetime
import sys
sys.path.append('/Users/uqmgonz1/Documents/GitHub')
from reef3D.PyToolbox import PStools as pst
import glob
from PIL import Image
import numpy as np
from reef3D.PyToolbox import CamOverlap as co
from reef3D.PyToolbox import PSeval as pe

import csv
import itertools
import random

#############################################
### Find closest camera pair for scaling ####
#############################################
def closest_pair(lcam, rcams):
    rcam = np.asarray(rcams)
    deltas = rcams - lcam
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)

#############################################
### Stereo scaling based on camera pairs  ###
#############################################
def scale_cams(chunk,thd=[0.5,0.7], lstring='_LC', d=0.4):
    '''
    thd: Min and Max overlaping desired to select camera pairs for scalebars
    lstring: unique string that identify the name of the cameras as the ones on the left-hand side
    d: Distance between the centre of the lens from each camera
    '''
    overlap=[]
    camdict={'right':[], 'left':[]}
    chunk.decimateModel(100000) ## this is to minimise memory load

    for cam in chunk.cameras:
        if cam.transform:
            if cam.label.__contains__(lstring):
                camdict['left'].append(np.r_[cam.key,np.asarray(cam.center)])
            else:
                camdict['right'].append(np.r_[cam.key,np.asarray(cam.center)])
    
    if chunk.crs == None:
    	crs = PhotoScan.CoordinateSystem('LOCAL_CS["Local CS",LOCAL_DATUM["Local Datum",0],UNIT["metre",1]]')
    	chunk.crs = crs
    
    #Find the closed camera pair and check that is a camera pair based on overlaping to set the scalebars 
    for l in camdict['left'][5::10]:
        lcam=l[1:]
        lcam_index=np.int(l[0])
        rcams=np.asarray(camdict['right'])
        rcams=rcams[:,1:]
        rcam_index=np.int(camdict['right'][closest_pair(lcam, rcams)][0])
        scalebar = chunk.addScalebar(chunk.cameras[lcam_index], chunk.cameras[rcam_index])
        scalebar.label = chunk.cameras[lcam_index].label + " - " + chunk.cameras[rcam_index].label
        scalebar.reference.distance = d
        PhotoScan.app.update()
        chunk.updateTransform()
        #fine-tune scalebars based on image-pair overlapping. 
        #Remove those scalebars where images are not overlapping enough or too much.
        #This avoid false pairs 
        try:
            thisIOI=co.IOI(lcam_index,rcam_index,chunk)
            overlap=np.r_[overlap,thisIOI]
            if (thisIOI < thd[0] or thisIOI > thd[1]):
                chunk.remove(scalebar)
        except Exception as e:
            overlap=np.r_[overlap,0] #most likely, these are cameras which edge falls outside the
            chunk.remove(scalebar)
            pass
            
    return(overlap)

###################################################################
### Detection of markers, scalebars and image quality checks   ####
###################################################################
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
       

#########################
### Process images   ####
#########################
def photoscanProcess(sampleid,camdict,path, export_path,scaletxt = "scalebars.csv",proj_path = "projects",data_path = "data/LTMP"):				
    ''''
    path: relative directory path to each transect. Eventually this will come from reefmon
    export_path: folder name where data will be exported to (not built in here yet)
    scaletext: text file containing the scale bar measurements per trip
    proj_path: root folder where projects will be saved
    data_path: root directory where data is stored. This will help using the relative path in "path"
    calfile: califration parameter files from cameras. This should be stored in the calibration folder
    stereo=logical value for acitivating stereo scaling
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
	
    print("Processing " + path)
    ## Load images into chunks
    desc=path.split('/')
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
        imdate.append(datetime.strptime(d, camdict['dateformat'])) #get image date time
    
    im=pd.DataFrame({'im':imlist,'date':imdate})
    im=im.sort_values('date', ascending=1)
    imlist=im.im
    n=camdict['chunk_size'] #group size
    m=camdict['overlap'] #overlap
    imlist=[imlist[i:i+n] for i in range(0, len(imlist), n-m)]
    ## end on image listing 
    
    
    ## Process chunks
    with open(os.path.join(export_path,'reports',sampleid+".csv"), "w") as csvFile:
        fieldnames = ['SAMPLEID', 'NO_IMAGES','ALIGNED','pALIGNED','SCALED',
        'NO_SCALEBARS','SCALE_ERROR','NO_MAKERS', 'MARKER_ERROR']
        writer = csv.Writer(csvFile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0,len(imlist)):
            chunk = doc.addChunk()
            chunk.label=sampleid+'_'+str(i)
            chunk.addPhotos(imlist[i])
            preProcess(doc, chunk, camdict['qual_threshold'], 
            camdict['tol_threshold'], scaletxt, camdict['calfile'])

            ### align photos ###
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
            chunk.buildDepthMaps(quality = quality, filter = filtering)
            chunk.buildDenseCloud(point_colors = True, keep_depth = False)
            doc.save()

            ###building mesh and stereo scaling
            if camdict['stereo']:
                chunk.buildModel(surface = surface, source = source, interpolation = interpolation, face_count = PhotoScan.FaceCount.LowFaceCount)
                doc.save()
                scale_cams(chunk,thd=camdict['overlap_threshold'], lstring=camdict['lstring'], d=camdict['cam_dist'])
                chunk.buildModel(surface = surface, source = source, interpolation = interpolation, face_count = face_num)
            else:
                chunk.buildModel(surface = surface, source = source, interpolation = interpolation, face_count = face_num)

        	###build mesh texture
            chunk.buildUV(mapping = mapping, count = 4)
            chunk.buildTexture(blending = blending, size = atlas_size)
            doc.save()
        
            ##Build orthomosaic
            XYproj=Matrix([[1.0, 0.0, 0.0, 0.0],
           [0.0, 1.0, 0.0, 0.0],
           [0.0, 0.0, 1.0, 0.0],
           [0.0, 0.0, 0.0, 1.0]])
            chunk.buildOrthomosaic(surface=PhotoScan.DataSource.ModelData,
            blending=PhotoScan.BlendingMode.MosaicBlending,
            projection=XYproj)
        
            ### Write report
            noimgs=len(chunk.cameras) #total numbr of images per chunk
            aligned=len(pe.checkalign(chunk))#number of images aligned
            paligned=len(checkalign(chunk))/len(chunk.cameras) #proportion of images aligned
            serror=mean(pe.scale_error(chunk)) # measurement error
            clength=chunk.orthomosaic.height*chunk.orthomosaic.resolution #length of recuntructed chunk
            cwidth=chunk.orthomosaic.width*chunk.orthomosaic.resolution #width of reconstructed chunk
            nomarkers=len(chunk.markers)
            
            if chunk.transform:
                scaled=True
            else:
                scaled=False
            noscalebars=len(chunk.scalebars)
            nmarkers=len(chunk.markers)
            
            if nmarkers >0:
                merror=np.mean(pe.markerProjError(chunk))
            else:
                merror=NULL
            
            csvData = [sampleid,noimgs,aligned,paligned,scaled,noscalebars,serror,
            nmakers,merror]
            writer.writerows(csvData)
            
            ##TODO: 1)export cameras, mosaics, models. 2) include check gate using model evaluation metics. <mgr>


    csvFile.close()
    print("Processed " + chunk.label)

















