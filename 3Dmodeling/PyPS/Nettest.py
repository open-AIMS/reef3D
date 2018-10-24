import PhotoScan
import sys
import os

doc=PhotoScan.app.document
chunk=doc.chunk
dp=doc.path
sys.path.append(os.path.join(dp.split('testCamp')[0],'scripts/'))
from reef3D.PyToolbox import PSmodel as psm


psm.preProcess(doc, chunk)