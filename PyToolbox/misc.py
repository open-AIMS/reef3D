### Miscellaneous functions
# Set of helper functions for processing images for PhotoScan

from pyexiftool import exiftool
import os.path as osp

def getDate(cams):
    with exiftool.ExifTool() as et:
        DateTime = et.get_tag_batch('DateTimeOriginal',files)
        return(DateTime)

def timeDiff(camA, camB):
    times=getDate([camA,camB])
    tDiff=times[0]-times[1]
    returb(tDiff)

def first_substring(df, variable, substring, contains):
    if contains:
        m = df[variable].str.contains(substring)
        out = m.idxmax() if m.any() else 'no match'
    else:
        m = df[~df[variable].str.contains(substring)]
        out = m.index[0]
    
    return(out)
    
