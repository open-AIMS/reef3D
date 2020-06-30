import processing
from qgis.PyQt.QtCore import QFileInfo
from qgis.core import QgsProject
from qgis.PyQt.QtCore import *


rasterLayer = QgsProject.instance().mapLayersByName('HELIX_test')[0]
pointLayer=QgsProject.instance().mapLayersByName('observers')[0]


alg_params = {
'DEM': rasterLayer,
'OBSERVER_ID': '',
'OBSERVER_POINTS': pointLayer,
'OBS_HEIGHT': 0.1,
'OBS_HEIGHT_FIELD': '',
'RADIUS': QgsExpression('0.1').evaluate(),
'RADIUS_FIELD': '',
'TARGET_HEIGHT': 0,
'TARGET_HEIGHT_FIELD': '',
'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
}

viewpoints = processing.run('visibility:create_viewpoints', alg_params)

i=0

for ft in viewpoints['OUTPUT'].getFeatures():
    results = {}
    #create temporary vector for each observer
    # create layer
    vl = QgsVectorLayer("Point", "observer", "memory")
    pr = vl.dataProvider()
    # Enter editing mode
    vl.startEditing()
    # add fields
    pr.addAttributes(viewpoints['OUTPUT'].fields())
    pr.addFeature(ft)
    vl.commitChanges()
    vl.updateExtents()
#    QgsProject.instance().addMapLayer(vl)
    
    alg_params = {
    'ANALYSIS_TYPE': 0,
    'DEM': rasterLayer,
    'OBSERVER_POINTS': vl,
    'OPERATOR': 1,
    'REFRACTION': 0.13,
    'USE_CURVATURE': False,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    }
    viewshed_raster = processing.run('visibility:Viewshed', alg_params)
#    print(viewshed_raster)
    i = i + 1
#    print(i)
    

#    QgsProject.instance().addMapLayer(viewpoints['OUTPUT'])

##    coordStr = '%f,%f' % (point.x(),point.y())
#    coordArray = coordStr.split(',')
#
#    #extent generation, +- 50,000Metres from point origin(coordStr)
#    xMin = float(coordArray[0]) - 0.1
#    xMax = float(coordArray[0]) + 0.1
#    yMin = float(coordArray[1]) - 0.1
#    yMax = float(coordArray[1]) + 0.1

    #Type juggling to get xmin,xmax,ymin,ymax
#    extcoordStr = str(xMin) + ',' + str(xMax) + ',' + str(yMin) + ',' + str(yMax)
#
#    outputViewshed = 'E:\\3d_ltmp\exports\viewshed_temp\viewshed_%i.tif' % i
#
    #running viewshed with observer and target heights set to 20Metres at max distance of 50Km
# Create viewpoints




##Viewshed analysis        

QgsProject.instance().addMapLayer(viewshed_raster['OUTPUT'])

results= viewshed_raster['OUTPUT']

    
i=0
for ft in pointLayer.getFeatures():
    point = ft.geometry().asPoint()
##    coordStr = '%f,%f' % (point.x(),point.y())
#    coordArray = coordStr.split(',')
#
#    #extent generation, +- 50,000Metres from point origin(coordStr)
#    xMin = float(coordArray[0]) - 0.1
#    xMax = float(coordArray[0]) + 0.1
#    yMin = float(coordArray[1]) - 0.1
#    yMax = float(coordArray[1]) + 0.1

    #Type juggling to get xmin,xmax,ymin,ymax
#    extcoordStr = str(xMin) + ',' + str(xMax) + ',' + str(yMin) + ',' + str(yMax)
#
#    outputViewshed = 'E:\\3d_ltmp\exports\viewshed_temp\viewshed_%i.tif' % i
#
    #running viewshed with observer and target heights set to 20Metres at max distance of 50Km
   
    outputs_0=processing.run('grass:r.viewshed', rasterLayer, coordStr, '0.1', '0', '0.1', 0.14286, 500, False, False, False, False, extcoordStr, 0, outputViewshed)
    i = i + 1