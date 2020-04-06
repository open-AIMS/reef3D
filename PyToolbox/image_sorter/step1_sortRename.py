#! python3
## STEP 1: Sort images and rename them based on QR codes
from qrRename import  qrRename
from sorter import sorter
import sys

rp=str(sys.argv[1])
ir=str(sys.argv[2])

##Set default values for some arguments that may not change often
if len(sys.argv)==3:
    qrm="C:/Users/mgonzale/Documents/gits/misc_manu/QRmap.csv"
    tg=3
elif len(sys.argv)==4:
    qrm=str(sys.argv[3])
    tg=3
else:
    tg=sys.argv[3]
    
def main(rootpath, img_rename, QRmap_path, time_gap):
    sorter(rootpath, img_rename,time_gap)
    qrRename(rootpath, QRmap_path)
    print('First Step Completed')
    print('[IMPORTANT]: Now, you need to rename transect folders before continue. Use suggestiongs from QR scaner to rename all folders')

if __name__ == "__main__":
    print('Working from: {}. Image prefix: {}'.format(rp,ir))
    main(rp, ir, qrm,tg)