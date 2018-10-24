import PhotoScan
import sys
sys.path.append('scripts/reef3D')
from reef3D.PyToolbox import PSmodel as psm

doc=PhotoScan.app.document
chunk=doc.chunk

psm.preProcess(doc, chunk)