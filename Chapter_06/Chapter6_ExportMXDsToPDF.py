# ---------------------------------------------------------------------------
# Chapter6_ExportMXDsToPDF.py
# Created by Silas Toms
# ---------------------------------------------------------------------------


import arcpy, glob, os
mxdFolder = r'C:\Projects\MXDs' #Any path to a folder with MXDs
pdfFolder = r'C:\Projects' #Any output path
mxdPathList = glob.glob(os.path.join(mxdFolder, '*.mxd'))
for mxdPath in mxdPathList:
    print mxdPath
    mxdObject = arcpy.mapping.MapDocument(mxdPath)
    arcpy.mapping.ExportToPDF(mxdObject,os.path.join(pdfFolder,os.path.basename(mxdPath.replace('mxd','pdf'))))
