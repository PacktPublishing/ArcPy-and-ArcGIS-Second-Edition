# Import libraries and define parameters
import arcpy, csv


# Define the variables
busStops = arcpy.GetParameterAsText(0) 
censusBlocks2010 = arcpy.GetParameterAsText(1) 
censusBlockField = arcpy.GetParameterAsText(2) 
csvname = arcpy.GetParameterAsText(3) 
headers = arcpy.GetParameterAsText(4).split(',') 
sql = arcpy.GetParameterAsText(5) 
keyfields = arcpy.GetParameterAsText(6).split(';') 
dataDic = {} 
censusFields = [ 'BLOCKID10',censusBlockField,'SHAPE@'] 
if "SHAPE@" not in keyfields: 
    keyfields.append("SHAPE@") 

# Add message is used instead of print
arcpy.AddMessage(busStops) 
arcpy.AddMessage(censusBlocks2010) 
arcpy.AddMessage(censusBlockField) 
arcpy.AddMessage(csvname) 
arcpy.AddMessage(sql) 
arcpy.AddMessage(keyfields) 
x = 0

# Search the bus stop feature class and create buffers
with arcpy.da.SearchCursor(busStops, keyfields, sql) as cursor: 
    for row in cursor: 
        stopid = x 
        shape = row[-1] 
        dataDic[stopid] = [] 
        dataDic[stopid].append(shape.buffer(400)) 
        dataDic[stopid].extend(row[:-1]) 
        x+=1 

# Find intersecting blocks and buffers          
processedDataDic = {} 
for stopid in dataDic.keys(): 
    values = dataDic[stopid] 
    busStopBuffer = values[0] 
    blocksIntersected = [] 
    with arcpy.da.SearchCursor(censusBlocks2010, censusFields) as cursor: 
        for row in cursor: 
            block = row[-1] 
            population = row[1] 
            blockid = row[0]             
 
            if busStopBuffer.overlaps(block) ==True: 
                interPoly = busStopBuffer.intersect(block,4) 
                data = population,interPoly, block 
                blocksIntersected.append(data) 
    processedDataDic[stopid] = values, blocksIntersected 

# Create an average value for each census block
# The average is proportional to the intersect area  
dataList = [] 
for stopid in processedDataDic.keys(): 
    allValues = processedDataDic[stopid] 
    popValues = [] 
    blocksIntersected = allValues[-1] 
    for blocks in blocksIntersected: 
        pop = blocks[0] 
        totalArea = blocks[-1].area 
        interArea = blocks[-2].area 
        finalPop = pop * (interArea/totalArea) 
        popValues.append(finalPop) 
    averagePop = round(sum(popValues)/len(popValues),2) 
    busStopLine = allValues[0][1] 
    busStopID = stopid 
    finalData = busStopLine, busStopID, averagePop 
    dataList.append(finalData) 

# Create a spreadsheet of the results
def createCSV(data, csvname, mode ='ab'): 
    with open(csvname, mode) as csvfile: 
        csvwriter = csv.writer(csvfile, delimiter=',') 
        csvwriter.writerow(data) 
              

createCSV(headers, csvname, 'wb')      
for data in dataList: 
    createCSV(data, csvname) 
