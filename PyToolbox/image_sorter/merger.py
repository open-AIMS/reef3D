#! python3
from pyzbar import pyzbar
import argparse
import cv2, os, datetime
import exifread
import pandas as pd, numpy as np
import shutil, tqdm
from time import sleep

def merger(rootpath):
    cameras=['RC','LC']
    for c in tqdm.trange(len(cameras), desc='Moving camera files'):
        camera=cameras[c]
        mypath=os.path.join(rootpath,camera)
        gdir = [dI for dI in os.listdir(mypath) if os.path.isdir(os.path.join(mypath,dI))]
        for tidx in tqdm.trange(len(gdir), desc='Working within transects', leave=True):
            t=gdir[tidx]
            newfolder= os.path.join(rootpath,t)
            if not os.path.exists(newfolder):
                os.mkdir(newfolder)
            for basename in os.listdir(os.path.join(mypath,t)):
                if basename.endswith(tuple((".jpg",".JPG"))):
                    pathname = os.path.join(os.path.join(mypath,t,basename))
                if os.path.isfile(pathname):
                    shutil.move(pathname, newfolder)
            os.rmdir(os.path.join(mypath,t))