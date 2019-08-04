import Metashape as ps
import sys,os



### SET DATA PATH
doc=Metashape.app.document
docpath=doc.path
c=docpath.split('/projects')[0]
#data_path="/Volumes/3d_ltmp/data/LTMP/RM/201819/OR/11-049/Site1Tran1"
data_path=str(sys.argv[1])


##LIST IMAGES
TYPES = ["jpg", "jpeg", "tif", "tiff"]
list_files = os.listdir(os.path.join(c,'data',data_path))
imlist = list()
for entry in list_files: #finding image files
	file = os.path.join(c,'data',data_path, entry)
	if os.path.isfile(file):
		if file[-3:].lower() in TYPES:
			imlist.append(file)
            
if not(len(imlist)):
	print("No images in " + data_path)
else:
    ##SPLIT IMAGES INTO GROUPS
    n=int(sys.argv[2]) #group size
    m=int(sys.argv[3]) #number of images overlapping between groups
    imlist.sort()
    imlist=[imlist[i:i+n] for i in range(0,len(imlist),n-m)]

    
    sec=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    for i in range(0,len(imlist)):
        chunk=doc.addChunk()
        chunk.label=data_path.split('/')[4]+'_'+data_path.split('/')[5]+'_'+sec[i]
        chunk.addPhotos(imlist[i])
    
    