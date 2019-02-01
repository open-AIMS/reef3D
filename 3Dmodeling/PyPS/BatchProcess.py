#!/usr/bin/env python3

import os
import PhotoScan
import sys
sys.path.append('/Users/uqmgonz1/Documents/GitHub')
from reef3D.PyToolbox import PStools as pt
from reef3D.PyToolbox import PSmodel as pm



def runNetwork(project_path, desc,chunk,  argstring, tname='RunScript', PSscript='scripts/reef3D/PyToolbox/PSmodel.py'):
    ''''
    Run a task over the network
    '''

    client = PhotoScan.NetworkClient()

    task1 = PhotoScan.NetworkTask()
    task1.chunks.append(chunk.key)
    task1.name = tname
    task1.params['path'] = PSscript #path to the script to be executed
    task1.params['args'] = argstring #string of the arguments with space as separator
    path = os.path.join(proj_path,desc[0],desc[1],desc[2],str(desc[2] + '.psx'))
    client.connect('agisoft-qmgr.aims.gov.au') #server ip
    batch_id = client.createBatch(path, [task1])
    client.resumeBatch(batch_id)
    print("Job started...")


def batchhNet(rootdir, summary_file, proj_dir):
    with open(os.path.join(rootdir,summary_file), 'r', errors='replace') as f:
        lines = f.readlines()[1:]
    for line in lines:
        MASTER_SAMPLE_ID,CRUISE_CODE,SITE_NO, TRANSECT_NO,VIDEO_FILENAME = line.split(',')[2],
        line.split(',')[3],line.split(',')[6],line.split(',')[7],line.split(',')[8]
        SAMPLE_ID=MASTER_SAMPLE_ID+'sc'+TRANSECT_NO
        
        #### create empty project file
        if not os.path.exists(os.path.join(proj_dir,os.basedir(VIDEO_FILENAME)):
            os.makedirs(os.path.join(proj_dir,os.basedir(VIDEO_FILENAME))
        
        PhotoScan.app.console.clear()
        ## construct the document class
        doc = PhotoScan.app.document
        ## save project
        psxfile = os.path.join(proj_path,VIDEO_FILENAME + '.psx')
        doc.save(psxfile)
        print ('>> Processing file: ' + psxfile)
        
        ### create task job
        runNetwork
        
        
            pm.photoscanProcess(path, export_path,
scaletxt = "scalebars.csv",proj_path = "projects",
data_path = "data/LTMP",calfile = "callibration_fisheye.xml")
            
            runNetwork()
            
            #TODO create log file
            
    
