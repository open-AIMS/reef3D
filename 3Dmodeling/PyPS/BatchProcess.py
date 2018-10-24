#!/usr/bin/env python3

import os
import PhotoScan
from reef3D.PyToolbox import PStools as pt



def runNetwork(project_path, desc,chunk,  argstring, tname='RunScript', PSscript='scripts/reef3D/PyToolbox/PSmodel.py'):
    ''''
    Run a task over the network
    '''

    client = PhotoScan.NetworkClient()

    task1 = PhotoScan.NetworkTask()
    task1.chunks.append(chunk)
    task1.name = tname
    task1.params['path'] = PSscript #path to the script to be executed
    task1.params['args'] = argstring #string of the arguments with space as separator
    path = os.path.join(proj_path,desc[0],desc[1],desc[2],str(desc[2] + '.psx'))
    client.connect('agisoft-qmgr.aims.gov.au') #server ip
    batch_id = client.createBatch(path, [task1])
    client.resumeBatch(batch_id)
    print("Job started...")


def batchhNet(dirName, pattern='.JPG$'):
    photoList=pt.getDictLTMP(dirname, pattern)
    for reef, transects in photoList:
        for transect in transects:
            desc=os.path.basename(dirName)
            desc.append(reef)
            desc.append(transect)
            imgList=photoList[reef][transect]
            
            runNetwork()
            
            #TODO create log file
            
    
    
