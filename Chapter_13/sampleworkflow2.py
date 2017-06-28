import arcpy, arcrest
from functions.dataquery import getData,bufferGeometry,transformGeometry
from functions.dataquery import extentGeometry,queryLayer,complaintScore,updateFeatureClass

url = "https://sampleserver6.arcgisonline.com/arcgis/rest/services/SF311/FeatureServer/"
layerid = 0
feature_class = r"C:\Projects\SanFrancisco.gdb\SanFrancisco\Bus_Stops"
bus_stop_fields = ["SHAPE@", "OID@", "STOPID"]
sql = "NAME = '71 IB' AND BUS_SIGNAG = 'Ferry Plaza' "

bus_data_dic = getData(feature_class,bus_stop_fields, sql)
bus_data_geometries = bus_data_dic['SHAPE@']

print "data retrieved"

bus_data_buffers = bufferGeometry(bus_data_geometries)
bus_data_transforms = transformGeometry(bus_data_buffers)
bus_data_extents = extentGeometry(bus_data_transforms)

datascores = []
for extent in bus_data_extents:
    query_data = queryLayer(url,layerid,'1=1',geom=extent)
    score = complaintScore(query_data) 
    datascores.append(score)
    
print "data received and processed"

data_dic = {}
for counter,stop in enumerate(bus_data_dic['STOPID']):
    sql = "STOPID = {0}".format(stop) 
    fields = ["LATE_EVENI"]  #Add a new field to the dataset or pick an existing one like 'LATE_EVENI'
    data = [datascores[counter]] 
    data_dic[stop] = sql, data, fields
    print sql, data

updateFeatureClass(data_dic, feature_class) 
print 'data updated'
