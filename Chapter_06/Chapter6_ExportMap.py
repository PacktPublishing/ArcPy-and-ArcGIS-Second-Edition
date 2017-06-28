# ---------------------------------------------------------------------------
# Chapter6_ExportMap.py
# Created by Silas Toms
# 2017 04 23
# ---------------------------------------------------------------------------

#Import modules
import arcpy, os

#Assign local variables
mxdPath = r'C:\Projects\MXDs\MapDocument1.mxd'   #Make sure that this matches the MXD's path
outpathTemplate = r'C:\Projects\Map_{0}.pdf'
bufferDist = 400
whereCondition = "NAME = '71 IB' AND BUS_SIGNAG = 'Ferry Plaza'"
queryTemplate = "OBJECTID IN ({0})"

#Create the connection to the MXD
mxdObject = arcpy.mapping.MapDocument(mxdPath)

#Assign the data frame called "Layers" to a variable. As it is in a list, we must pass an index value ([0]) as a parameter
dataFrame = arcpy.mapping.ListDataFrames(mxdObject, "Layers")[0]

#Assign the data frame called "Inset" to a variable.
insetFrame = arcpy.mapping.ListDataFrames(mxdObject, "Inset")[0]


#Get MXD layers from the Layers data frame
layersList = arcpy.mapping.ListLayers(mxdObject,"",dataFrame)
layerStops = layersList[0]
layerBlocks = layersList[3] 


#Get MXD layers from the Inset data frame
layersList = arcpy.mapping.ListLayers(mxdObject,"",insetFrame)
layerStopsInset = layersList[0]

#Add a definition query to the inset bus stop layer to only show the stops of interest
layerStopsInset.definitionQuery = whereCondition

#Assign the list of MXD elements to a variable
elements = arcpy.mapping.ListLayoutElements(mxdObject)

#Loop through the MXD elements
for el in elements:
    if el.type =="TEXT_ELEMENT":
        if el.text == 'Title Element':
            titleElement = el
        elif el.text == 'Subtitle Element':
            subTitleElement = el
        elif el.text == 'Total Population Nearby:':
            populationElement = el
            populationtext = populationElement.text

#Count the number of stops to get a page total 
totalpagecount =0 
with arcpy.da.SearchCursor(layerStops,['OID@' ],whereCondition) as cursor:
    for row in cursor:
        totalpagecount = totalpagecount + 1

pagecounter = 0
with arcpy.da.SearchCursor(layerStops,['SHAPE@','STOPID','NAME','BUS_SIGNAG' ],whereCondition) as cursor:
    for row in cursor:
        print row[1]
        pagecounter += 1
        
        #Get the bus stop geometry and buffer it to create a polygon area around the bus stop, to use for intersection with the census blocks
        stopPointGeometry = row[0]
        stopBuffer = stopPointGeometry.buffer(bufferDist)

        #Select the census blocks surrounding the bus stop using an intersect with the buffer around the bus stop. 
        arcpy.SelectLayerByLocation_management(layerBlocks, 'intersect', stopBuffer, "", "NEW_SELECTION")

        #Use a Search Cursor to iterate through the selected blocks and add their IDs to the collector list.
        #Use the buffer as a base geometry and add block geometries using the union method to create a new geometry that will form the extent of the map data frame         
        collector = []
        unionGeometry = stopBuffer
        population = 0
        with arcpy.da.SearchCursor(layerBlocks,["OID@", "SHAPE@", "POP10"]) as bcursor:
            for brow in bcursor:
                collector.append(brow[0])
                unionGeometry = unionGeometry.union(brow[1])       #Union the geometries, growing it with each row iterated
                population = population + brow[2]

        #Clear the layer selection
        arcpy.SelectLayerByAttribute_management(layerBlocks,  "CLEAR_SELECTION")
        
        #Conditional to see if the bus stop buffer intersected with any blocks
        if len(collector)  > 0:
            
            #Iterator with a counter to create a string from the objectids
            counter = 0
            oidstring = ""
            for oid in collector:
                if counter < len(collector)-1:
                    oidstring = oidstring + str(oid) + ","
                else:
                    oidstring = oidstring + str(oid)
                counter = counter + 1

            #Add the oidstring to the query template to create a definition query for the census block layer 
            defQuery = queryTemplate.format(oidstring)
            layerBlocks.definitionQuery = defQuery

            #Add a definition query to the bus stop layer to only show the stop of interest
            layerStops.definitionQuery = "STOPID = " + str(row[1])

            #Define the extent of the map by assigning the data frame extent to the extent of the unioned census blocks, then zoom out a bit by multiplying the scale
            dataFrame.extent = unionGeometry.extent
            dataFrame.scale = dataFrame.scale * 1.1

            
            #Assign a value to the population text element to add a total population value of the selected census blocks to the map
            populationElement.text = populationtext + "\n" + str(population)

            #Create a dynamic title for each individual page and a subtitle with a page count
            titleElement.text = "Analysis: ("+row[2]+ ")"
            subTitleElement.text= "Page " + str(pagecounter) + " of " + str(totalpagecount)

            #Refresh the Active View of the map
            arcpy.RefreshActiveView()

            #Create the dynamic output PDF file path
            outpath = outpathTemplate.format(str(row[1]))
            print outpath
            
            #Export the PDF
            arcpy.mapping.ExportToPDF(mxdObject,outpath)

            
            #Clean up for the next iteration
            layerStops.definitionQuery = ""
            layerBlocks.definitionQuery = ""
