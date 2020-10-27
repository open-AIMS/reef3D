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
	fieldnames = ['YEAR','CAMPAIGN','REEFNAME', 'SITE', 'TRANSECT', 'NO_IMAGES','ALIGNED','pALIGNED','SCALED','NO_SCALEBARS','SCALE_ERROR','NO_MAKERS', 'MARKER_ERROR', 'REl_PATH']
	writer = csv.writer(csvFile, delimiter=',')
	writer.writerow(fieldnames)
	for proj in projList:
		ps.app.document.open(proj)
		doc=ps.app.document
		base=os.path.basename(proj)
		# reefname=os.path.splitext(base)[0]
		relPath=proj.split("projects")[1]
		meta=relPath.split("\\")
		year=meta[2]
		campaign=meta[3]
		for c in doc.chunks:
			noimgs=len(c.cameras) #total numbr of images per chunk
			aligned=len(pe.checkalign(c))#number of images aligned
			paligned=aligned/noimgs #proportion of images aligned
			# clength=chunk.orthomosaic.height*chunk.orthomosaic.resolution #length of recuntructed chunk
			# cwidth=chunk.orthomosaic.width*chunk.orthomosaic.resolution #width of reconstructed chunk
			nomarkers=len(c.markers)
			if aligned > 0:
				serror=np.mean(pe.scale_error(c)) # measurement error
			else:
				serror="NULL"

			if c.transform:
				scaled="YES"
			else:
				scaled="NO"

			nmarkers=len(c.markers)
			nscalebars=len(c.scalebars)

			if nscalebars <=1 or aligned==0:
				serror="NULL"
			else: 
				serror=np.mean(pe.scale_error(c)) # measurement error

			if nmarkers >0 and aligned >0:
				merror=np.mean(pe.markerProjError(c))
			else:
				merror="NULL"
			[reefname, sitetran]=c.label.split('_')
			[Site, Trans]=re.findall(r'\d+', sitetran)

			csvData = [year,campaign,reefname,Site, Trans, noimgs,aligned,paligned,scaled,nscalebars,serror,nmarkers,merror, relPath]
			csvData=[str(f) for f in csvData]
			writer.writerows([csvData])
