#!/usr/bin/python


import cv2, os, datetime
import exifread
import pandas as pd, numpy as np
import shutil
from time import sleep


def imgTrans(img_path, method):    
    
    #Read image
    img=cv2.imread(img_path)

    #ALTERING IMAGE
    if method == 0:# orginal
        img=img
    elif method==1: # Changing colour to grey
        img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif method == 7: # Chaning luminosity by gamma transformation - Brighter
        gamma_table=[np.power(x/255.0,1.5)*255.0 for x in range(256)]
        gamma_table=np.round(np.array(gamma_table)).astype(np.uint8)
        img=cv2.LUT(img,gamma_table)
    elif method == 3: # Chaning luminosity by gamma transformation -Darker
        gamma_table=[np.power(x/255.0,0.5)*255.0 for x in range(256)]
        gamma_table=np.round(np.array(gamma_table)).astype(np.uint8)
        img=cv2.LUT(img,gamma_table)
    elif method == 4: #Binary Threshold
        img_grey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        t=cv2.mean(img_grey)
        t=tuple(map(lambda x: isinstance(x, float) and int(round(x, 0)) or x, t))
        ret,img=cv2.threshold(img_grey,t[0],255,cv2.THRESH_BINARY)
    elif method == 5: #OTSU Threshold
        img_grey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        t=cv2.mean(img_grey)
        t=tuple(map(lambda x: isinstance(x, float) and int(round(x, 0)) or x, t))
        ret,img=cv2.threshold(img_grey,t[0],255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    elif method == 6: #UTSU Threhsold with a Gaussian Filter
        img_grey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        t=cv2.mean(img_grey)
        t=tuple(map(lambda x: isinstance(x, float) and int(round(x, 0)) or x, t))
        blur = cv2.GaussianBlur(img_grey,(5,5),0)
        ret,img=cv2.threshold(img_grey,t[0],255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    elif method == 2: #Theshold inverted image
        mask = cv2.inRange(img,(0,0,0),(200,200,200))
        thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
        img = 255-thresholded # black-in-white
    
    return img
