import time
import PhotoScan
import numpy as np
'''
Requires mesh model
'''
##########################################################
### Interception of vector from the camera to the mesh ###
##########################################################
def cross(a, b):
	result = PhotoScan.Vector([a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y *b.x])
	return result

##################################################################
### Calculate the camera footprint (projected polygon on mesh) ###
##################################################################
def cam_poly(cam_index, chunk):
    
    model = chunk.model
    faces = model.faces
    vertices = model.vertices
    camera=chunk.cameras[cam_index]

    sensor = camera.sensor
    steps = [(0, 0), (sensor.width-1, 0), (sensor.width-1, sensor.height-1), (0, sensor.height-1)]

    respoly=np.array([])
    for x,y in steps:
        point = PhotoScan.Vector([x, y]) 
        point = sensor.calibration.unproject(point)
        point = camera.transform.mulv(point) 
        vect = point
        p = PhotoScan.Vector(camera.center)

        for face in faces:
            v = face.vertices
            E1 = PhotoScan.Vector(vertices[v[1]].coord - vertices[v[0]].coord)
            E2 = PhotoScan.Vector(vertices[v[2]].coord - vertices[v[0]].coord)
            D = PhotoScan.Vector(vect)
            T = PhotoScan.Vector(p - vertices[v[0]].coord)
            P = cross(D, E2)
            Q = cross(T, E1)
            result = PhotoScan.Vector([Q * E2, P * T, Q * D]) / (P * E1)
            
            if (0 < result[1]) and (0 < result[2]) and (result[1] + result[2] <= 1):
                t = (1 - result[1] - result[2]) * vertices[v[0]].coord
                u = result[1] * vertices[v[1]].coord
                v_ = result[2] * vertices[v[2]].coord
                res = chunk.transform.matrix.mulp(u + v_ + t)
                res = chunk.crs.project(res)
                thisvert=np.r_[res[0],res[1]] #(x,y) cordimates for a corner (defined in steps)          
                break #finish when the first intersection is found
        
        
        respoly=np.concatenate([thisvert,respoly])
                
    return(respoly)

##################################################################
### Intersection over Union (IoU) from object detectionPython  ###
##################################################################
def IOI(lcam_index,rcam_index,chunk):
    boxA=cam_poly(lcam_index, chunk)
    boxB=cam_poly(rcam_index,chunk)
    
	# convert to positive coordinate system
    minX=min(boxA[0], boxB[0],boxA[2], boxB[2])
    minY=min(boxA[1], boxB[1],boxA[3], boxB[3])
    boxA=[boxA[0]+minX,boxA[1]+minY,boxA[2]+minX,boxA[3]+minY]
    boxB=[boxB[0]+minX,boxB[1]+minY,boxB[2]+minX,boxB[3]+minY]
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

	# compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

	# compute the area of both the prediction and ground-truth
	# rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou