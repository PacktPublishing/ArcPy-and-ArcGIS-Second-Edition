import arcrest, arcpy

def queryLayer(url, layerid, conditional="1=1",geom=None): 
    'query a layer using a feature service URL'
    fs_object = arcrest.ags.featureservice.FeatureService(url) 
    layers = fs_object.layers
    layer = layers[layerid]
    featureset = layer.query(where=conditional, geometryFilter=geom)
    return featureset
	
	

def getData(featurepath,fields=['SHAPE@', 'OID@'], sql='',srid=None):   
    'retrieve specific fields' 
    data_dic = {field:list() for field in fields}
    with arcpy.da.SearchCursor(featurepath,fields,sql,srid) as cursor:    
        for row in cursor:    
            for counter,field in enumerate(fields):
                data_dic[field].append(row[counter]) 
    return data_dic
	
	
def bufferGeometry(geometries,distance=400):
    'create a buffer around a geometry at a radius of {distance}'
    buffer_geometries = []
    for geometry in geometries:
            buffer_geom = geometry.buffer(distance)
            buffer_geometries.append(buffer_geom)
    return buffer_geometries
	
def transformGeometry(geometries,srid=None):
    'project geometries into different spatial reference systems'
    transform_geometries = []
    if srid != None:
            srid = arcpy.SpatialReference(srid)
    else:
            srid = arcpy.SpatialReference(4326)
    for geometry in geometries:
            projected = geometry.projectAs(srid)
            transform_geometries.append(projected)
    return  transform_geometries
	
def extentGeometry(geometries):
    'create extent geometry filters'
    extent_geometries = []
    for geometry in geometries:
            extent = geometry.extent
            array = arcpy.Array()
            extent_vertices = [arcpy.Point(extent.XMin, extent.YMin),arcpy.Point(extent.XMin, extent.YMax),
                               arcpy.Point(extent.XMax, extent.YMax),arcpy.Point(extent.XMax, extent.YMin)]
            array.extend(extent_vertices)
            extent_geometry = arcpy.Polygon(array,geometry.spatialReference)
            extent_filter = arcrest.filters.GeometryFilter(extent_geometry)
            extent_geometries.append(extent_filter)
    return extent_geometries
	
def complaintScore(featureset):
    'create a tally based complaint score' 
    complaint_score = len(featureset.features) 
    return complaint_score



def updateEnterpriseFeature(data_dict, workspace, feature_class, srid=None,with_undo=False,multi=True):
    'update specific rows and fields in an enterprise feature class'
    editor = arcpy.da.Editor(workspace) 
    editor.startEditing(with_undo, multi) 
    editor.startOperation() 
    for datakey in data_dict.keys():
        sql, data, fields = data_dict[datakey]
        with arcpy.da.UpdateCursor(feature_class, fields,sql,srid) as upcursor: 
            for row in upcursor:    
                row = data 
                upcursor.updateRow(row) 
    editor.stopOperation() 
    editor.stopEditing(True)


def updateFeatureClass(data_dict, feature_class, srid=None):
    'update a non enterprise feature class'
    for datakey in data_dict.keys():
        sql, data, fields = data_dict[datakey]
        with arcpy.da.UpdateCursor(feature_class, fields,sql,srid) as upcursor: 
            for row in upcursor:
                row= data 
                upcursor.updateRow(row) 
