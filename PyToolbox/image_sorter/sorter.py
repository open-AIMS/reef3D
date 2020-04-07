#! python3
import sys
import argparse
import cv2, os, datetime
import exifread
import pandas as pd, numpy as np
import shutil
import tqdm
from time import sleep

def sorter(rootpath, img_rename,time_gap):
    cameras=['RC','LC']
    for c in tqdm.trange(2, desc='Sorting images per camera'):
        camera=cameras[c]
        mypath=os.path.join(rootpath,camera)
        imdf=pd.DataFrame({'filename':[],'DateTime':[]})
        count=0
        for imgname in os.listdir(mypath):
            if imgname.endswith(".JPG"):
                ##Organise images by time
                count=count+1
                fh=open(os.path.join(mypath,imgname), 'rb')
                tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
                iminfo=pd.DataFrame({'filename':[os.path.join(mypath,imgname)], 
                                     'DateTime': [datetime.datetime.strptime(str(tags["EXIF DateTimeOriginal"]),
                                                                             '%Y:%m:%d %H:%M:%S')]})
                imdf=imdf.append(iminfo)
        # Move image cluster into subfolders
        imdf = imdf.sort_values("DateTime")
        cluster = (imdf["DateTime"].diff() > pd.Timedelta(minutes=time_gap)).cumsum()
        dfs = [v for k,v in imdf.groupby(cluster)]
        i=0
        prefix=img_rename+'_'+camera+'_'
        for clust_idx in tqdm.trange(len(dfs),desc='Creating transects', leave=False):
            clust=dfs[clust_idx]
            #ignore clusters where there is only a couple of images
            if len(clust)>5:
                i=i+1
                dest=os.path.join(mypath,str(i))
                if not os.path.exists(dest):
                    os.mkdir(dest)
                clust.apply(lambda row: shutil.copy(row['filename'], os.path.join(dest,
                                                                                  prefix+os.path.basename(row['filename']))), 
                            axis=1)