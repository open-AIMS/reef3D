import Metashape as ps

import sys,os

### SET DATA PATH
doc=ps.app.document
docpath=doc.path
c=docpath.split('/projects')[0]
#data_path="/Volumes/3d_ltmp/data/LTMP/RM/201819/OR/11-049/Site1Tran1"


for chunk in doc.chunks:
    ############## Import Camera calibration parameters ###############
    print("---Importing calibration parameters---")
    calib = ps.Calibration()
    calib.load(os.path.join(c,'calibration', str(sys.argv[1])), format="xml")
    
    ############## SET UP CAMERA ######################################
    for sensor in chunk.sensors:
        sensor.rolling_shutter = False
        sensor.focal_length=3.0
        sensor.user_calib = calib #and this will load the XML values to the Initial values
        #sensor.calibration = calib # this will set the Adjusted values according to the XML
        if str(sys.argv[1])=='GoPro4K_OR.xml':
            sensor.type = ps.Sensor.Type.Fisheye
            sensor.pixel_width=0.00173066
            sensor.pixel_height=0.00173066
        else:
            sensor.type = ps.Sensor.Type.Frame
            sensor.pixel_width=0.002281
            sensor.pixel_height=0.002281

                