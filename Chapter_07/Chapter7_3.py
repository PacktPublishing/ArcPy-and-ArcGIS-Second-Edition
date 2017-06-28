# Import libraries
import arcpy

# uncomment the next line to overwrite existing files with output
#arcpy.env.overwriteOutput = True 

# Check out the extension
arcpy.CheckOutExtension("Spatial")

# Define the variables. Check to make sure that the file paths match your own
busStops = r'C:\Projects\SanFrancisco.gdb\SanFrancisco\Bus_Stops'
sanFranciscoHoods = r'C:\Projects\SanFrancisco.gdb\SanFrancisco\SFFind_Neighborhoods'
sfElevation = r'C:\Projects\SanFrancisco.gdb\sf_elevation'

# Get the vertices of the SOMA neighborhood polygon using the explode to points parameter
# Convert the vertices to Point objects
somaGeometry = []
sql = "name = 'South of Market'"
with arcpy.da.SearchCursor(sanFranciscoHoods,['SHAPE@XY'],sql,None, True) as cursor:
    for row in cursor:
        X = row[0][0]
        Y = row[0][1]
        somaGeometry.append(arcpy.Point(X,Y))

# Extract raster areas by vertices using the someGeometry Point objects list to define an area
somaElev = arcpy.sa.ExtractByPolygon(sfElevation, somaGeometry, "INSIDE")

# Create an output file path form the SOMA neighborhood raster
somaOutput = sfElevation.replace('sf_elevation','SOMA_elev')

# Save the output raster as clipped by the neighborhood geometry
somaElev.save(somaOutput)
print 'extraction finished'


# Create an output file path for a new raster with feet elevation values
somaOutFeet = sfElevation.replace('sf_elevation','SOMA_feet')

# Convert the elevation values from meters to feet
outTimes = arcpy.sa.Times(somaOutput, 3.28084)
outTimes.save(somaOutFeet)
print 'conversion complete'

# Get the polygon geometry of the SOMA neighborhood
with arcpy.da.SearchCursor(sanFranciscoHoods,['SHAPE@'],sql) as cursor:
    for row in cursor:
        somaPoly = row[0]

# Make the Bus Stops into a feature layer
arcpy.MakeFeatureLayer_management(busStops, 'soma_stops')

# Select the bus stops that intersect wtih the SOMA neighborhood polygon
arcpy.SelectLayerByLocation_management("soma_stops", "INTERSECT", somaPoly)

# Save the bus stops with a new elevation value field.
outStops = r'C:\Projects\SanFrancisco.gdb\Chapter7Results\SoMaStops'
arcpy.sa.ExtractValuesToPoints("soma_stops", somaOutFeet,
                      outStops,"INTERPOLATE",
                      "VALUE_ONLY")
print 'points generated'
