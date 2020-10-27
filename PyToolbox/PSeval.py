import Metashape as ps
import numpy as np


def scale_error(chunk):
	'''
	Clculate scale error for each scale bar to produce a vector of errors
	'''
	
	for scalebar in chunk.scalebars:
		dist_source = scalebar.reference.distance
		if not dist_source:
			continue #skipping scalebars without source values
		if type(scalebar.point0) == ps.Camera:
			if not (scalebar.point0.center and scalebar.point1.center):
				continue #skipping scalebars with undefined ends
			dist_estimated = (scalebar.point0.center - scalebar.point1.center).norm() * chunk.transform.scale
		else:
			if not (scalebar.point0.position and scalebar.point1.position):
				continue #skipping scalebars with undefined ends
			dist_estimated = (scalebar.point0.position - scalebar.point1.position).norm() * chunk.transform.scale
		dist_error = dist_estimated - dist_source 
	
	e=np.r_[dist_error]
	
	return(e)

#################################################################
### Calculate percentage of images aligned from each chunk	 ####
#################################################################
def checkalign(chunk):
	aligned_photos = []	  # empty list
	for camera in chunk.cameras:
		if camera.transform:
			aligned_photos.append(camera.label)	 # creates list of photos that aligned
	return(aligned_photos)

#################################################################
### Calculate marker error if georeferenced					 ####
#################################################################
def Merror(doc,chunk):
	max_iterations = 10 # Max allowed iterations for one marker
	result = []
	for marker in chunk.markers:
		num_projections = len(marker.projections)

		positions = []
		if num_projections > 2 and marker.type == PhotoScan.Marker.Type.Regular:  # Marker needs more than two projections to evaluate error, and not be a fiducial
			cam_list = [cam for cam in marker.projections.keys() if cam.center]	 # Every aligned camera with projections
			random.shuffle(cam_list)  # Needed if the max_iterations is exceeded
		
			count = 0
			for a, b in itertools.combinations(cam_list, 2):  # Testing pairs of every possible combination

				if a.group and b.group and a.group == b.group and a.group.type == PhotoScan.CameraGroup.Type.Station:  # Skip if the cameras share station group
					continue

				if count >= max_iterations:	 # Break if it reaches the iteration limit
					break
				count += 1

				selected_cameras = [a, b]

				# Note pinned pixel coordinates and if pinned or not (green or blue)
				px_coords = {camera: (marker.projections[camera].coord, marker.projections[camera].pinned) for camera in cam_list}

				# Unpinning the non-selected cameras
				for camera in cam_list:
					if camera not in selected_cameras:
						marker.projections[camera] = None

				# Save the estimated position
				positions.append(list(chunk.crs.project(chunk.transform.matrix.mulp(marker.position))))

				# Revert pinned coordinates
				for camera in cam_list:
					coord, pinned = px_coords[camera]
					marker.projections[camera] = PhotoScan.Marker.Projection(coord)
					marker.projections[camera].pinned = pinned

			iterations = len(positions)	 # Amount of tested positions
			positions = np.array(positions)
			std = np.std(positions, axis=0)	 # Standard deviation
			rms = (np.sqrt(np.mean(std**2)))  # RMS of standard deviation

			result.append((marker.label,) + tuple(std) + (rms, iterations))

		# Write a CSV at desired position
		file_name = PhotoScan.app.getSaveFileName("Save output file", filter="*.csv")
		if file_name:  # If an input was given
			with open(file_name, "w") as file:
				file.write("Label, X, Y, Z, Total, Iterations\n")
				for line in result:

					entry = ""
					for value in line:
						entry += str(value).replace("'", "") + ","

					file.write(entry + "\n")
					
					
					
def markerProjError(chunk):
	merror=[]
	for marker in chunk.markers:
		cerror=[]
		# Every aligned camera with projections
		for cam in marker.projections.keys():
			try:
				projection = marker.projections[cam].coord #2D coordinates on the corresponding image of the marker projection (green/blue flag)
				reprojection = cam.project(marker.position) #2D coordinates on the corresponding image of reprojected marker position
				error = (projection - reprojection).norm() #difference in pixels  
				cerror=np.r_[cerror,error]
			except:
				pass
		
		merror=np.r_[merror,cerror]
	
	return(merror)		   