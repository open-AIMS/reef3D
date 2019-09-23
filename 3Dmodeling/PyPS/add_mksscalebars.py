### Add ScaleBars and distande from file

import Metashape as ps
import sys 
import os

doc = ps.app.document
docpath=doc.path
c=docpath.split('/projects')[0]
scale_file = str(sys.argv[1])

for chunk in doc.chunks:
    print("Adding ScaleBars...")
    file = open(os.path.join(c,'reference_scales', scale_file), "rt")

    markers = {}
    for marker in chunk.markers:
	    markers[marker.label] = marker

    eof = False
    line = file.readline()

    while not eof:
        t1,t2, dist = line.split(',')[0], line.split(',')[1],line.split(',')[2]
    
        if t1 in markers.keys() and t2 in markers.keys():
            s=chunk.addScalebar(markers[t1], markers[t2])
            s.reference.distance=float(dist)
    
        line = file.readline()		#reading the line in input fil
        if not len(line):
            eof = True
            break

    file.close()


print("Script finished")
        

