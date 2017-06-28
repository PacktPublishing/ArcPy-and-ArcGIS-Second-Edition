import arcrest, arcpy
arcpy.env.overwriteOutput = True
url = "https://sampleserver6.arcgisonline.com/arcgis/rest/services/SF311/FeatureServer"
fs_object = arcrest.ags.featureservice.FeatureService(url)
layers = fs_object.layers
layer = layers[0]
array = arcpy.Array()
array.extend([arcpy.Point(-122.55,37.70),arcpy.Point(-122.55,37.81),
                          arcpy.Point(-122.35,37.81),arcpy.Point(-122.35,37.70)])
sf_extent = arcpy.Polygon(array)
arcpy.CopyFeatures_management(sf_extent,r'C:\Projects\extent.shp')
extent_filter = arcrest.filters.GeometryFilter(sf_extent)
json_data = layer.query(where='district IS NOT NULL',
                        geometryFilter=extent_filter,
                        returnCountOnly=True)
print json_data

