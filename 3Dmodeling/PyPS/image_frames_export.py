#compatibility - PhotoScan Professional v 1.0.4

import time
import PhotoScan

def cross(a, b):
	result = PhotoScan.Vector([a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y *b.x])
	return result

print("Script started")

cam_index = PhotoScan.app.getInt("Input camera index (starting from zero): ")
save_path = PhotoScan.app.getSaveFileName("Specify output file:")

t0 = time.time()
file = open(save_path, "wt")

doc = PhotoScan.app.document
chunk = doc.activeChunk
model = chunk.model
faces = model.faces
vertices = model.vertices

camera = chunk.photos[cam_index]
print(camera) #camera label

step = 100 #bigger value - faster processing.
steps = list(zip(list(range(0, camera.width - 1, step)), [0]*((camera.width - 1)// step)))
steps.extend( list(zip([camera.width - 1]*((camera.height - 1) // step), list(range(0, camera.height - 1, step)))) )
steps.extend( list(zip(list(range((camera.width - 1), 0, -step)), [camera.height - 1]*((camera.width - 1)// step))))
steps.extend( list(zip([0]*((camera.height - 1) // step), list(range(camera.height - 1, 0, -step)))) )

for x,y in steps:
	
	point = PhotoScan.Vector([x, y])
	point = camera.calibration.unproject(point)
	point = camera.transform.mulv(point)
	vect = point
	p = PhotoScan.Vector(camera.center)

	for face in faces:

		v = face.vertices
	
		E1 = PhotoScan.Vector(vertices[v[1]].coord - vertices[v[0]].coord)
		E2 = PhotoScan.Vector(vertices[v[2]].coord - vertices[v[0]].coord)
		D = PhotoScan.Vector(vect)
		T = PhotoScan.Vector(p - vertices[v[0]].coord)
		P = cross(D, E2)
		Q = cross(T, E1)
	
		result = PhotoScan.Vector([Q * E2, P * T, Q * D]) / (P * E1)
	
		if (0 < result[1]) and (0 < result[2]) and (result[1] + result[2] <= 1):
			t = (1 - result[1] - result[2]) * vertices[v[0]].coord
			u = result[1] * vertices[v[1]].coord
			v_ = result[2] * vertices[v[2]].coord
			
			res = chunk.transform.mulp(u + v_ + t)
			res = chunk.crs.project(res)
		
			file.write("{:>04d}".format(x + 1) + "\t" + "{:04d}".format(y + 1) + "\t" + "{:.4f}".format(res[0]) + "\t" + "{:.4f}".format(res[1]) + "\t" + "{:.4f}".format(res[2]) + "\n")
			#face.selected = True
			break #finish when the first intersection is found
				
				
file.close()
t1 = time.time()
t1 -= t0
t1 = float(t1)
print("Script finished in " + "{:.2f}".format(t1) + " seconds.")