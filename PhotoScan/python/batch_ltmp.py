###############################################################################
####Title: Bash processing LTMP transects for Structural complexity
####Description: Series of steps within the structure from montion algirthms to reconstruct the 3D structure of the reef substrate within Photoscan. The script asumes that each chuck is a transect within LTMP surveys and that each chuck is labeled with the site and transect number for a given reef. A project contains all transects and sites per reef and it is labeled with the reef name. This script is a batch processing to produce 3D point cloud and mesh from the reconstructions of each transects, which will then be processed in MatLab to derive 3D metrics of structural complexity
####Author: Manuel Gonzalez-Rivero
####Date: 10/06/2018
###############################################################################

import PhotoScan
import os,re,sys

# Set Environment Variables

qual=0.6     # image quality value below which cameras are disabled
ttshld=60   # Threshold for detecting targets
keylim=60000  # key point limit for matching
tielim=6000   # tie point limit for matching
sbar = '/media/pearl/3d_ltmp/reference_scales/scalebars.txt'    # text file with scalebar info. Relative path to root path (network processing)


#Import Environment Variables
	#filename = '/home/sam3d/Documents/AgisoftScannerConfig/Variable_File.txt' 
	#fin=open(filename, 'r')
	#USER =fin.readline()
    # NAME =fin.readline()
    # AA =fin.readline()
    # DPQ =fin.readline()
    # MQ =fin.readline()
    #
    # print("Variables transferred.")
    # print(USER)
    # print(NAME)
    # print(AA)
    # print(DPQ)
    # print(MQ)
    # NAME = NAME[:-1]
    


doc = PhotoScan.app.document


for chunk in doc.chunks:
	################################################################################################
	### Image Quality control  ###
	## 
    # print("---Estimating image quality---")
    # chunk.estimateImageQuality(chunk.cameras)
    # for camera in chunk.cameras:
    #     if float(camera.meta["Image/Quality"]) < qual:
    #         camera.enabled = False
  
    
	################################################################################################
	### Detect Markers ###
	## 
    print("---Detecting Markers---")
    chunk.detectMarkers(PhotoScan.TargetType.CircularTarget12bit, ttshld)
    

    ############### Add ScaleBars and distande from file ###############################
    # print("---Adding ScaleBars---")
    #
    # file = open(sbar, "rt")
    # markers = {}
    # for marker in chunk.markers:
    #         markers[marker.label] = marker
    #
    # eof = False
    # line = file.readline()
    # while not eof:
    #     t1,t2, dist = line.split(',')[0], line.split(',')[1],line.split(',')[2]
    #
    #     if t1 in markers.keys() and t2 in markers.keys():
    #         s=chunk.addScalebar(markers[t1], markers[t2])
    #         s.reference.distance=float(dist)
    #
    #     line = file.readline()        #reading the line in input fil
    #     if not len(line):
    #         eof = True
    #         break
    #
    # file.close()
        
    ############### enabling rolling shutter compensation ################################ 
    print("---Rolling shutter compensation---")
    
    # try:
    #     for sensor in chunk.sensors:
    #         rolling_shutter = True
    # except Exception as e:
    #     print("Error:", e)
    #     raise
    
	############### Align photos. #########################################################
	## Perform image matching for the chunk frame.
	# matchPhotos(accuracy=HighAccuracy, preselection=NoPreselection, filter_mask=False, keypoint_limit=40000, tiepoint_limit=4000[, progress])
	# - Alignment accuracy in [HighestAccuracy, HighAccuracy, MediumAccuracy, LowAccuracy, LowestAccuracy]
	# - Image pair preselection in [ReferencePreselection, GenericPreselection, NoPreselection]
    print("---Aligning photos---")
    chunk.matchPhotos(accuracy=PhotoScan.MediumAccuracy, preselection=PhotoScan.ReferencePreselection, filter_mask=False, keypoint_limit=keylim, tiepoint_limit=tielim)
    chunk.alignCameras()
    
    ############### Add ScaleBars and distande from file###############################
    print("---Aligment optimization---")
    # chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True,
                                                             # fit_b1=True, fit_b2=True, fit_k1=True,
                   #                                           fit_k2=True, fit_k3=True, fit_k4=False,
    #                                                          fit_p1=True, fit_p2=True, fit_p3=False,
    #                                                          fit_p4=False)
    # # doc.save()
                                                           
	################################################################################################
	### build dense cloud ###
	## Generate depth maps for the chunk.
	# buildDenseCloud(quality=MediumQuality, filter=AggressiveFiltering[, cameras], keep_depth=False, reuse_depth=False[, progress])
	# - Dense point cloud quality in [UltraQuality, HighQuality, MediumQuality, LowQuality, LowestQuality]
	# - Depth filtering mode in [AggressiveFiltering, ModerateFiltering, MildFiltering, NoFiltering]
    # print("---Building dense cloud---")
    # chunk.buildDepthMaps(quality=PhotoScan.MediumQuality, filter=PhotoScan.ModerateFiltering)
    # chunk.buildDenseCloud()
    # # doc.save()
    
	################################################################################################
	### build mesh ###
	## Generate model for the chunk frame.
	# buildModel(surface=Arbitrary, interpolation=EnabledInterpolation, face_count=MediumFaceCount[, source ][, classes][, progress])
	# - Surface type in [Arbitrary, HeightField]
	# - Interpolation mode in [EnabledInterpolation, DisabledInterpolation, Extrapolated]
	# - Face count in [HighFaceCount, MediumFaceCount, LowFaceCount]
	# - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
    # print("---Building Mesh model---")
#     chunk.buildModel(surface=PhotoScan.HeightField, interpolation=PhotoScan.EnabledInterpolation, face_count=PhotoScan.HighFaceCount)
#     doc.save()
    
	################################################################################################
	## Export points and mesh
    reefname=os.path.basename(os.path.splitext(doc.path)[0])
    chunk.exportPoints( "pointsPLY/"+reefname+'_'+chunk.label+ ".PLY", 
    binary=True, precision=6, colors=True, format=PhotoScan.PointsFormatPLY)
    # chunk.exportModel( "mesh/"+reefname+'_'+chunk.label+ ".PLY",
#     binary=True, precision=6, colors=F, format=PhotoScan.ModelFormatPLY)
    doc.save()

print("Script finished")
        

