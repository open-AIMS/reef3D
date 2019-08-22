# Script adds user defined altitude to Source values in the Reference pane.
#
# This is python script for Metashape Pro. Scripts repository: https://github.com/agisoft-llc/metashape-scripts

import Metashape as ps
import sys
# Checking compatibility
compatible_major_version = "1.5"
found_major_version = ".".join(ps.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))

alt=float(sys.argv[1])
doc=ps.app.document
chunk=doc.chunk

def add_altitude(chunk, alt, accXY, accZ):
	"""Adds user-defined altitude for camera instances in the Reference panel"""
	print("Script started...")
	
	for camera in chunk.cameras:
		if camera.reference.location:
			coord = camera.reference.location#
			#camera.reference.location = ps.Vector([NULL, NULL, alt])
			camera.reference.location = None
			camera.reference.location_accuracy=ps.Vector([accXY,accXY,accZ])
			camera.reference.rotation=ps.Vector([0,0,0])
			camera.reference.rotation_accuracy=ps.Vector([360,10,10])
	print("Script finished!")
add_altitude(chunk,alt, 10,0.5)