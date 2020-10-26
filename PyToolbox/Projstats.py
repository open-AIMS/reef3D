from glob import glob
import os, sys
sys.path.append('C:\\Users\\mgonzale\\Documents\\gits')
from reef3D.PyToolbox import PSeval as pe


projFolder='E:\\3d_ltmp\\projects'
projList = [y for x in os.walk(projFolder) for y in glob(os.path.join(x[0], '*.psx'))]

