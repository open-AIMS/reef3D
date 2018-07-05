### Add ScaleBars and distande from file

import PhotoScan

doc = PhotoScan.app.document


for chunk in doc.chunks:
    print("Adding ScaleBars...")

    path = '/Volumes/3d_ltmp/reference_scales/scalebars.txt'
    file = open(path, "rt")

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
        

