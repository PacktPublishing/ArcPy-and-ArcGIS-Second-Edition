# Import libraries
import arcpy, csv


# Define the variables. Check to make sure that the file paths match your own
busStops = r"C:\Projects\SanFrancisco.gdb\SanFrancisco\Bus_Stops"
censusBlocks2010 = r"C:\Projects\SanFrancisco.gdb\SanFrancisco\CensusBlocks2010"
csvname = r"C:\Projects\StationPopulations.csv"
headers = 'Bus Line Name','Bus Stop ID', 'Population'
sql = "NAME = '71 IB' AND BUS_SIGNAG = 'Ferry Plaza'"

# Search the feature class and buffer the geometry. Add it to a dictionary
dataDic = {}
with arcpy.da.SearchCursor(busStops, ['NAME','STOPID','SHAPE@'], sql) as cursor:
    for row in cursor:
        linename = row[0]
        stopid = row[1]
        shape = row[2]
        dataDic[stopid] = shape.buffer(400), linename

# Intersect census blocks and bus stop buffers        
processedDataDic = {}
for stopid in dataDic.keys():
    values = dataDic[stopid]
    busStopBuffer = values[0]
    linename = values[1]
    blocksIntersected = []
    with arcpy.da.SearchCursor(censusBlocks2010, ['BLOCKID10','POP10','SHAPE@']) as cursor:
        for row in cursor:
            block = row[2]
            population = row[1]
            blockid = row[0]            
            if busStopBuffer.overlaps(block) ==True:
                interPoly = busStopBuffer.intersect(block,4)
                data = row[0],row[1],interPoly, block
                blocksIntersected.append(data)
    processedDataDic[stopid] = values, blocksIntersected


# Create an average population for each bus stop 
dataList = []
for stopid in processedDataDic.keys():
    allValues = processedDataDic[stopid]
    popValues = []
    blocksIntersected = allValues[1]
    for blocks in blocksIntersected:
        pop = blocks[1]
        totalArea = blocks[-1].area
        interArea = blocks[-2].area
        finalPop = pop * (interArea/totalArea)
        popValues.append(finalPop)
    averagePop = round(sum(popValues)/len(popValues),2)
    busStopLine = allValues[0][1]
    busStopID = stopid
    finalData = busStopLine, busStopID, averagePop
    dataList.append(finalData)



# Generate a spreadsheet with the analysis results     
def createCSV(data, csvname, mode ='ab'):
    with open(csvname, mode) as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(data)

# Create the headers row and then add the data using iteration
createCSV(headers, csvname, 'wb')
for data in dataList:
    createCSV(data, csvname)

print 'Data analysis complete'
