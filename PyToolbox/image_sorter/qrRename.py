#! python3
from imgTrans import imgTrans
from pyzbar import pyzbar
import argparse
import cv2, os, datetime
import exifread
import pandas as pd, numpy as np
import shutil, tqdm
from time import sleep


def qrRename(rootpath, QRmap_path):
    QRmap=pd.read_csv(QRmap_path)
    qrData=pd.DataFrame(columns=['Code','Folder', 'Camera'])
    cameras=['RC','LC']
    for c in tqdm.trange(2, desc='Detecting QR codes'):
        camera=cameras[c]
        mypath=os.path.join(rootpath,camera)
        gdir = [dI for dI in os.listdir(mypath) if os.path.isdir(os.path.join(mypath,dI))]
        for gx in tqdm.trange(len(gdir), desc='Scanning subdirectories',leave=False):
            g=gdir[gx]
            if os.path.isdir(os.path.join(mypath,g)):
                check=0
                im=0
                while (check <1) & (im in range(20)):
                    if len(os.listdir(os.path.join(mypath,g)))>10:
                        imgname=os.listdir(os.path.join(mypath,g))[im]
                        if imgname.endswith(tuple((".jpg",".JPG"))):
                            i=0
                            check2=0
                            while (check2 < 1) & (i in range(7)):
                                img=imgTrans(os.path.join(mypath,g,imgname), i)
                                barcodes = pyzbar.decode(img,symbols=[pyzbar.ZBarSymbol.QRCODE])
                                # loop over the detected barcodes
                                if len(barcodes) != 0:
                                    for barcode in barcodes:
                                        barcodeData = barcode.data.decode("utf-8")
                                        barcodeType = barcode.type
                                        qrData=qrData.append({'Code': barcodeData,
                                                                  'Folder': g,
                                                                  'Camera':camera}, ignore_index=True)
                                    check2 +=1
                                else:
                                    check2=0
                                i +=1
                    if check2==1:
                        check +=1
                        newname=str(QRmap['Name'].loc[QRmap['Code']==int(barcodeData)].to_list()[0])
                        newname=g+'_'+newname
                        if not os.path.exists(os.path.join(mypath,newname)):
                            os.rename(os.path.join(mypath,g),os.path.join(mypath,newname))
                            
                    im +=1


    print('{} QR codes found in {} transects for the {} camera'.format(len(qrData['Code'].loc[qrData['Camera']=='RC']),
                                                                len(os.listdir(os.path.join(rootpath,'RC'))),
                                                                'RC'))
    print('{} QR codes found in {} transects for the {} camera'.format(len(qrData['Code'].loc[qrData['Camera']=='LC']),
                                                                len(os.listdir(os.path.join(rootpath,'LC'))),
                                                                'LC'))