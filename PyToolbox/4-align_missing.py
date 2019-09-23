import Metashape as ps

import sys,os

### SET DATA PATH
doc=ps.app.document

for chunk in doc.chunks:
	if chunk.enabled:
		aligned = []   # empty list
		notaligned = []   # empty list
		for camera in chunk.cameras:
			if camera.transform:
				aligned.append(camera)  # creates list of photos that aligned
			else:
				notaligned.append(camera)
	
		chunk.alignCameras(notaligned)
