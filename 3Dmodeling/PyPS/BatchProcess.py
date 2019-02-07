#!/usr/bin/env python3

import os
import PhotoScan
import sys
sys.path.append('/Users/uqmgonz1/Documents/GitHub')
from reef3D.PyToolbox import PStools as pt
from reef3D.PyToolbox import PSmodel as pm
import pickle 



def runNetwork(project_path,  argstring, tname='RunScript', PSscript='scripts/reef3D/PyToolbox/PSmodel.py'):
    ''''
    Run a task over the network
    '''

    client = PhotoScan.NetworkClient()

    task1 = PhotoScan.NetworkTask()
    task1.name = tname
    task1.params['path'] = PSscript #path to the script to be executed
    task1.params['args'] = argstring #string of the arguments with space as separator
    client.connect('agisoft-qmgr.aims.gov.au') #server ip
    batch_id = client.createBatch(proj_path, [task1])
    client.resumeBatch(batch_id)
    print("Job started...")

##TODO Tidy and test this function. check filepaths (/ vs \). Reorganise data?. <mgr>
def batchNet(summary_file, camType, proj_dir='projects', export_path='exports'):
    ''''
    Having images registered in ReefMon from the field, the intention is to batch process
    each transect in a campain and export the data products for QAQC and further analysis
    summary_file: CSV file queried from ReefMon DB inidicating the sample id and path to
    images for each transect in a given campain. proj_dir: directory where projects are
    saved
    '''
    with open(os.path.join(rootdir,summary_file), 'r', errors='replace') as f:
        lines = f.readlines()[1:]
    for line in lines:
        MASTER_SAMPLE_ID,CRUISE_CODE,SITE_NO, TRANSECT_NO,VIDEO_FILENAME = line.split(',')[2],
        line.split(',')[3],line.split(',')[6],line.split(',')[7],line.split(',')[8]
        SAMPLE_ID=MASTER_SAMPLE_ID+'sc'+TRANSECT_NO
        
        #### create empty project file
        if not os.path.exists(os.path.join(proj_dir,os.basedir(VIDEO_FILENAME))):
            os.makedirs(os.path.join(proj_dir,os.basedir(VIDEO_FILENAME)))
        
        PhotoScan.app.console.clear()
        doc = PhotoScan.app.document # construct the document class        
        psxfile = os.path.join(proj_dir,VIDEO_FILENAME + '.psx') # save project
        doc.save(psxfile)
        print ('>> Processing file: ' + psxfile)
        
        ##load camera parameters
        ##TODO change this. It is only a placemarker as a reference
        with open('obj/' + name + '.pkl', 'rb') as f:
                camdict=pickle.load(f)
        
        f.close()
        camdict=camdict[camType]
        
        ##TODO create camera dictionay
        ### create task job and distrubute to network
        args=" ".join([SAMPLEID,camdict,path, export_path])
        
        runNetwork(project_path=psxfile, 
        argstring=args, 
        tname='RunScript', 
        PSscript='scripts/reef3D/PyToolbox/PSmodel.py')
    f.close()
 
            
            
    
