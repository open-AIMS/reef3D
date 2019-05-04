import Metashape as ps
import sys,os



### SET DATA PATH
doc=Metashape.app.document
docpath=doc.path
c=docpath.split('/projects')[0]

for chunk in doc.chunks:
    print("---Estimating image quality---")
    chunk.estimateImageQuality(chunk.cameras)
    for camera in chunk.cameras:
        if float(camera.meta["Image/Quality"]) < float(sys.argv[1]):
            camera.enabled = False