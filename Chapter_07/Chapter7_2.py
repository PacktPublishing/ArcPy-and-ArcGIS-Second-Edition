# Import libraries
import arcpy

# uncomment the next line to overwrite existing files with output
#arcpy.env.overwriteOutput = True 

# Check out the extension
arcpy.CheckOutExtension("Network")

# Define the variables. Check to make sure that the file paths match your own
busStops = r'C:\Projects\SanFrancisco.gdb\SanFrancisco\Bus_Stops'
networkDataset = r'C:\Projects\SanFrancisco.gdb\Chapter7Results\street_network'
networkLayer = "streetRoute"
impedance = "Length"
routeLayerFile = "C:\Projects\{0}_2.lyr".format(networkLayer)


# Make a route layer
arcpy.arcpy.na.MakeRouteLayer(networkDataset, networkLayer, impedance)
print 'layer created'

# Search the bus stops feature class and add the geometry to the layer
sql = "NAME = '71 IB' AND BUS_SIGNAG = 'Ferry Plaza'"
with arcpy.da.SearchCursor(busStops,['SHAPE@', 'STOPID'],sql) as cursor:
    for row in cursor:
        stopShape = row[0]
        print row[1]
        arcpy.na.AddLocations(networkLayer,'Stops', stopShape, "", "")

# Solve the network layer
arcpy.na.Solve(networkLayer,"SKIP")

# Save the layer to file
arcpy.management.SaveToLayerFile(networkLayer,routeLayerFile,"RELATIVE")

print 'finished'
