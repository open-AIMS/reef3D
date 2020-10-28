#!/usr/bin/python
##########################################################################
#### Summary statistics from error checking from PS models           #####
##########################################################################
#Author: M. Gonzalez-Rivero
#Date: October 2020
# #Purpose: Given a folder containing models, the script will iterate throguh models to get basic statistics that help identifying the quality of reconstructions and output a CSV 
# file in the same folder that contains the summary metrics across the chunks in each project.


from glob import glob
import os, sys, re, csv
import numpy as np

if len(sys.argv)==2:
	sys.path.append('~/gits')
else:
	sys.path.append(sys.argv[2])

from reef3D.PyToolbox import PSeval as pe
import Metashape as ps


projFolder=sys.argv[1]

projList = [y for x in os.walk(projFolder) for y in glob(os.path.join(x[0], '*.psx'))]

with open(os.path.join(projFolder,"project_summary.csv"), "w", newline='', ) as csvFile:
	fieldnames = ['YEAR','CAMPAIGN','REEFNAME', 'SITE', 'TRANSECT', 'NO_IMAGES',
	'STATUS','pALIGNED','SCALED','NO_SCALEBARS','SCALE_ERROR',
	'NO_MAKERS', 'MARKER_ERROR', 'REl_PATH', "EXPORTED", "DISABLED"]
	writer = csv.writer(csvFile, delimiter=',')
	writer.writerow(fieldnames)
	for proj in projList:
		ps.app.document.open(proj)
		doc=ps.app.document
		doc.read_only = False
		base=os.path.basename(proj)
		# reefname=os.path.splitext(base)[0]
		relPath=proj.split("projects")[1]
		meta=relPath.split("/")
		year=meta[2]
		campaign=meta[3]
		for c in doc.chunks:
			noimgs=len(c.cameras) #total numbr of images per chunk
			no_aligned=len(pe.checkalign(c))#number of images aligned			
			# clength=chunk.orthomosaic.height*chunk.orthomosaic.resolution #length of recuntructed chunk
			# cwidth=chunk.orthomosaic.width*chunk.orthomosaic.resolution #width of reconstructed chunk
			nomarkers=len(c.markers)
			if no_aligned > 0:
				serror=np.mean(pe.scale_error(c)) # measurement error
				status=1
			else:
				serror="NULL"
				aligned=0
			
			if noimgs==0:
				paligned="NULL"
			else:
				paligned=no_aligned/noimgs #proportion of images aligned

			if c.transform.scale:
				scaled="YES"
			else:
				scaled="NO"
			
			c.updateTransform()
			nmarkers=len(c.markers)
			nscalebars=len(c.scalebars)

			if nscalebars ==0 or no_aligned==0 or not(c.transform.scale):
				serror="NULL"
			else: 
				serror=np.mean(pe.scale_error(c)) # measurement error
			
			if nmarkers >0 and no_aligned >0 and c.transform.scale:
				merror=np.mean(pe.markerProjError(c))
			else:
				merror="NULL"
			if "_" in c.label:
				chunkname=c.label.split('_')
				reefname=chunkname[0]
				sitetran=chunkname[1]
				exported="yes"
			else:
				sitetran=c.label
				reefname=reefname=os.path.splitext(base)[0]
				exported="maybe not"
				
			sitetran_id=re.findall(r'\d+', sitetran)
			if "Site" in sitetran and len(sitetran_id)==2:
				Site=sitetran_id[0]
				Trans=sitetran_id[1]
			else:
				Site='NULL'
				Trans='NULL'
				exported='maybe not'
			
			DISABLED=str(not(c.enabled))
			if c.dense_cloud is not None:
				status+=1


			csvData = [year,campaign,reefname,Site, Trans, noimgs,status, paligned,scaled,nscalebars,serror,nmarkers,merror, relPath, exported]
			csvData=[str(f) for f in csvData]
			writer.writerows([csvData])
		doc.save()
