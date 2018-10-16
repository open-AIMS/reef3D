#!/usr/bin/env python3

import os,re

def getDict_LTMP(dirName, pattern='.JPG$'):
    '''
    Create a dictorionary for reef, transects and images for a given LTMP campaign
    root_path: path directory to campaign folder. This should contain the data organised per reef and site/transects for each reef
    pattern: file extension for images to import
    '''
    # create a dicto of file and sub directories 
    # names in the given directory 
    photoList={}
    listreefs=os.listdir(dirName)
    # Iterate over all the reefs
    for reef in listreefs:
        if os.path.isdir(os.path.join(dirName,reef)):
            listtrans=os.listdir(os.path.join(dirName,reef))
            photoList.update({reef:{}})
            #iterate over all transects in a reef
            for trans in listtrans:
                if os.path.isdir(os.path.join(dirName,reef,trans)):
                    listimg=os.listdir(os.path.join(dirName,reef,trans))
                    #iterate over all the images in a transect
                    imgs=[]
                    for img in listimg:
                        if re.search(pattern,img):
                            imgs.append(os.path.join(dirName, reef, trans,img))
                    
                    photoList[reef].update({trans:imgs})
                            
    return photoList
             

def nearest(items, pivot):
    '''
    Search for the closest date in the scalebar file to the date images were collected
    ''' 
    items=items[items<pivot] #to consider only the dates previous to pivot
    return min(items, key=lambda x: abs(x - pivot))