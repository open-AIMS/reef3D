import Metashape as ps
import sys,os



import pandas as pd 


### Load files
doc=ps.app.document
docpath=doc.path
#df=pd.read_csv(r"C:\Users\mgonzale\Documents\temp\20190527_Rugo\20190527_D1.csv", sep=';')
df=pd.read_csv(str(sys.argv[1]), sep=';')
dirpath=df.fpath[0]
df['fpath'] = df['fname'].apply(lambda x: x.replace(x, os.path.join(dirpath,x)))


##IMPORT IMAGES in CLUSTERS
 

for i in df.cluster_id.unique()[1:-1]:
	chunk=doc.addChunk()
	chunk.label= os.path.splitext(os.path.basename(sys.argv[1]))[0]+'_C'+str(i)
	chunk.addPhotos(df.fpath.loc[df.cluster_id==i].tolist())
	for cam in chunk.cameras:
		
	