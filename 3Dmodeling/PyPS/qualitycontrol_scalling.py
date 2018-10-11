### Add ScaleBars and distande from file

import PhotoScan
import os
import sys
from datetime import datetime
##add python 3.5 module paths for HPC
#sys.path.insert(0,"/usr/local/python/3.5.1/lib/python3.5/site-packages/")
import pandas as pd


doc = PhotoScan.app.document
docpath=doc.path
c=docpath.split('/projects')[0]
### SET ENVIRONMENTAL VARIABLES 
sbar = os.path.join(c,'reference_scales/scalebars_test.csv')
print(sbar) #sys.argv[1] #path to scale bar reference document
# sbar= '/Volumes/3d_ltmp/reference_scales/scalebars_test.csv'
qual = float(sys.argv[1]) # quality threshold for filtering images
ttshld = int(sys.argv[2]) # Tolerance threshold for detecting markers

###SET ENVIRONMENT FOR SEARCHING WITHIN SCALE BAR DOCUMENT
def nearest(items, pivot):
    items=items[items<pivot] #toconsider only the dates previous to pivot
    return min(items, key=lambda x: abs(x - pivot))
    
df=pd.read_csv(sbar,delimiter=',')
df['DATE']=pd.to_datetime(df['DATE'],format='%d/%m/%y')

### PROCESS EACH CHUNK WITHIN THE PROJECT 
for chunk in doc.chunks:
    
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
    img_date=datetime.strptime(camera.photo.meta['Exif/DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
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
    


