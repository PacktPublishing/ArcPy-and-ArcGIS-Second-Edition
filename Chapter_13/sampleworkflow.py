import arcpy, arcrest
from functions.dataquery import getData,bufferGeometry,transformGeometry
from functions.dataquery import extentGeometry,queryLayer,complaintScore,updateEnterpriseFeature

url = "https://sampleserver6.arcgisonline.com/arcgis/rest/services/SF311/FeatureServer/"
layerid = 0
workspace = r"Database Connections\SanFranciscoDB"
feature_class = r"Database Connections\SanFranciscoDB\SanFrancisco\Bus_Stops"
bus_stop_fields = ["SHAPE@", "OID@", "STOPID"]

sql = "NAME = '71 IB' AND BUS_SIGNAG = 'Ferry Plaza'"
bus_data_dic = getData(feature_class,bus_stop_fields, sql)
bus_data_geometries = bus_data_dic['SHAPE@']

bus_data_buffers = bufferGeometry(bus_data_geometries)
bus_data_transforms = transformGeometry(bus_data_buffers)
bus_data_extents = extentGeometry(bus_data_transforms)

datascores = []
for extent in bus_data_extents: 
    query_data = queryLayer(url,layerid,geom=extent)
    score = complaintScore(query_data) 
    datascores.append(score) 

data_dic = {}
for counter,stop in enumerate(bus_data_dic['STOPID']):
    sql = "STOPID = {0}".format(stop) 
    fields = ["complaintScore"] 
    data = [datascores[counter]]  
    data_dic[stop] = sql, data, fields

updateEnterpriseFeature(data_dic, workspace,feature_class) 
print "update process complete"
