import os
import arcpy
from arcpy import env 
from arcpy import * 
from arcpy.sa import *

### IMPORTING SHAPE FILES AFTER CALIBRATE #################################
path_shape_files = r'F:/CMAQ_Model/HaNoi_Project/Point_Dataset/'

raw_name = os.listdir(path_shape_files)
outnames = []
for rname in raw_name:
    if (rname.endswith(".shp")):
        portion = os.path.splitext(rname)
        temp_name = portion[0]
        outnames.append(temp_name)
###########################################################################



### INTERPOLATION THE POINTS AND EXPORT TO TIF FILES ################################
path_shape_out_files = r"F:/CMAQ_Model/HaNoi_Project/Point_Dataset_3D/"
out_IDW = r"F:/CMAQ_Model/HaNoi_Project/IDW_Interpolation"
arcpy.env.outputZFlag = 'Enabled'
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("3D")
for outname in outnames:
    print(outname, os.path.splitext(outname)[0] + '.tif', path_shape_out_files + outname + ".shp") # Watching the progress
    arcpy.ddd.FeatureTo3DByAttribute(path_shape_files + outname + ".shp", path_shape_out_files + outname + ".shp", 'GRID_CODE')
    outIDW = Idw(path_shape_out_files + outname + ".shp", "GRID_CODE", 0.0005, None, RadiusVariable(12, None))
    outname = os.path.join(out_IDW, os.path.splitext(outname)[0] + '.tif')
    outIDW.save(outname)
#####################################################################################
