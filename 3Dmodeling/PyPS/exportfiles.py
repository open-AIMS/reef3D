### Export files for 3D metrics

import PhotoScan
import os
import sys
import csv



doc = PhotoScan.app.document
docpath=doc.path
c=docpath.split('/projects')[0]
camp=docpath.split('/projects/')[1][:2]

outpath_cam=os.path.join(c,'exports/cameras/', camp)
outpath_points=os.path.join(c,'exports/pointsXYZ/', camp)
outpath_mesh=os.path.join(c,'exports/mesh/', camp)

if not os.path.exists(outpath_cam):
    os.makedirs(outpath_cam)

if not os.path.exists(outpath_points):
    os.makedirs(outpath_points)

if not os.path.exists(outpath_mesh):
    os.makedirs(outpath_mesh)
    

for chunk in doc.chunks:
    #Export camera pose 
    fname=os.path.join(outpath_cam, str(chunk.label+'.csv'))
    with open(fname,'w', newline='') as csv_file:
        writer=csv.writer(csv_file,delimiter=',')
        writer.writerow(['camera','x','y','z'])
        for camera in chunk.cameras:
            if camera.transform:
                line=[camera.label, camera.transform.row(0)[3],camera.transform.row(1)[3],camera.transform.row(2)[3]]
                writer.writerow(line)
            
            
        
