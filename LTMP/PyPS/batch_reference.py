## Autoprocessing script for multiple sub-folders in some master folder

#compatibility Agisoft PhotoScan Professional 1.4.2
#use argument to specify the path to the "master folder"

import PhotoScan, os, sys, time

def process(path):

	PhotoScan.app.gpu_mask = 2 ** len(PhotoScan.app.enumGPUDevices()) - 1 #setting GPU mask
	if PhotoScan.app.gpu_mask:
		PhotoScan.app.cpu_enable = False  
	else:
		PhotoScan.app.cpu_enable = True
		
	
	### processing parameters
	accuracy = PhotoScan.Accuracy.HighAccuracy  #align photos accuracy
	reference_preselection = False
	generic_preselection = True
	keypoints = 40000 #align photos key point limit
	tiepoints = 4000 #align photos tie point limit
	source = PhotoScan.DataSource.DenseCloudData #build mesh/DEM source
	surface = PhotoScan.SurfaceType.Arbitrary #build mesh surface type
	quality = PhotoScan.Quality.MediumQuality #build dense cloud quality 
	filtering = PhotoScan.FilterMode.AggressiveFiltering #depth filtering
	interpolation = PhotoScan.Interpolation.EnabledInterpolation #build mesh interpolation 
	blending = PhotoScan.BlendingMode.MosaicBlending #blending mode
	face_num = PhotoScan.FaceCount.HighFaceCount #build mesh polygon count
	mapping = PhotoScan.MappingMode.GenericMapping #build texture mapping
	atlas_size = 4096
	TYPES = ["jpg", "jpeg", "tif", "tiff"]
	###end of processing parameters definition

	print("Processing " + path)
	list_files = os.listdir(path)
	list_photos = list()
	for entry in list_files: #finding image files
		file = path + "/" + entry
		if os.path.isfile(file):
			if file[-3:].lower() in TYPES:
				list_photos.append(file)
	if not(len(list_photos)):
		print("No images in " + path)
		return False
	
	doc = PhotoScan.Document()	
	doc.save(path + "/" + path.rsplit("/", 1)[1] + ".psx")
	chunk = doc.addChunk()
	chunk.label = path.rsplit("/", 1)[1]
	
	###align photos
	chunk.addPhotos(list_photos)
	chunk.matchPhotos(accuracy = accuracy, generic_preselection = generic_preselection, reference_preselection = reference_preselection, filter_mask = False, keypoint_limit = keypoints, tiepoint_limit = tiepoints)
	chunk.alignCameras()
	chunk.optimizeCameras()
	chunk.resetRegion()
	doc.save()	
				
	###building dense cloud
	chunk.buildDepthMaps(quality = quality, filter = filtering)
	chunk.buildDenseCloud(point_colors = True, keep_depth = False)
	doc.save()
	
	###building mesh
	chunk.buildModel(surface = surface, source = source, interpolation = interpolation, face_count = face_num)
	doc.save()

	###build texture
	chunk.buildUV(mapping = mapping, count = 1)
	chunk.buildTexture(blending = blending, size = atlas_size)
	doc.save()
	
	###export model
	chunk. exportModel(path = path + "/" + chunk.label + ".obj", binary=False, texture_format=ImageFormatJPEG, texture=True, normals=False, colors=False, cameras=False, format = PhotoScan.ModelFormatOBJ)

	print("Processed " + chunk.label)
	return True

def main()

	t0 = time.time()
	print("Script started...")

	if len(sys.argv) < 2:
		print("No valid path input. Script aborted.")
		return False
	if os.path.isdir(sys.argv[1]):
		path = sys.argv[1]
	else:
		print("No valid path input. Script aborted.")
		return False	
	
	folders = ["/".join([path,entry]) for entry in os.listdir(path) if os.path.isdir(os.path.join(path,entry))]