import arcpy
from arcpy_token import return_token, submit_request
#make it possible to overwrite an existing feature class
arcpy.env.overwriteOutput = True
#assign the feature class we will be updating to the variable update
update = r"C:\PythonBook\Scripts\SanFrancisco.gdb\Chapter9Results\BusStops_Moved_Update"

user_file = open('username.txt', 'r')
username = user_file.readline().rstrip('\n')
pass_file = open('password.txt', 'r')
password = pass_file.readline().rstrip('\n')
service_url = "https://arcgis.com/sharing"

def update_featureclass_agol(base_URL, update_feature, count):
    #set the variable n to 0 to be used to query objectID
    n = 0
    #template feature class to be used when creating feature class FC
    template = r"C:\PythonBook\Scripts\SanFrancisco.gdb\SanFrancisco\Bus_Stops"
    #create feature class in memory
    FC = arcpy.CreateFeatureclass_management("in_memory", "FC", "POINT", template, "DISABLED", "DISABLED", "", "", "0", "0", "0")
    #generate token
    token = return_token(service_url, username, password)
    #loop over request number of times where count is number of features/1000
    for x in range(count):
        where = "OBJECTID>"+str(n)
        #url parameters
        query = "/query?where={}&returnGeometry=true&outSR=2227&outFields=*&f=json&token={}".format(where, token)
        fs_URL = base_URL + query #build the finla url
        fs = arcpy.FeatureSet()
        fs.load(fs_URL)
        arcpy.Append_management (fs, FC, "NO_TEST")
        
        n+=1000 #add 1000 to n for next query

        print n

    with arcpy.da.SearchCursor(FC, ['OID@', 'SHAPE@XY', "FACILITYID"]) as cursor:
        for row in cursor:
            objectid = row[0]
            #get the x value from 'SHAPE@XY'
            pointx = row[1][0]
            #get the y value from 'SHAPE@XY'
            pointy = row[1][1]
            fid = row[2]

            fid_sql ="FACILITYID = {0}".format(fid)
            with arcpy.da.UpdateCursor(update_feature, ['SHAPE@'], fid_sql) as cursor:
                for urow in cursor:
                    print "FACILITYID updated is ", fid
                    #update the location of point using the x and y values from the FC feature
                    urow[0] = arcpy.Point(pointx, pointy)
                    cursor.updateRow(urow)

#call the main function
def main():
    update_featureclass_agol("https://services7.arcgis.com/LLWzNvydeNCpjeTo/arcgis/rest/services/BusStops/FeatureServer/0", update, 17)

if __name__ == '__main__':
    main()
