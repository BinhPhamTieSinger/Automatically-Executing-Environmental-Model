import os
import arcpy
from arcpy import env 
from arcpy import * 
from arcpy.sa import *


mask = "F:/CMAQ_Model/HaNoi_Project/24.Shp/HaNoi_shp/HaNoi.shp"
output_dir = r'F:/CMAQ_Model/HaNoi_Project/Extract_Map/'

### LISTING TIFF FILES AFTER CALIBRATE ###################################
path_tiff_files = r'F:/CMAQ_Model/HaNoi_Project/IDW_Interpolation/'
raw_name = os.listdir(path_tiff_files)
outnames = []
for rname in raw_name:
    if (rname.endswith('.tif')):
        portion = os.path.splitext(rname)
        temp_name = portion[0] + '.tif'
        outnames.append(temp_name)

for outname in outnames:
    print(outname)

arcpy.env.overwriteOutput = True
arcpy.env.workspace = path_tiff_files
rasters_after_interpolation = arcpy.ListRasters("*", "TIF")
# print(rasters_after_interpolation)
###########################################################################



### Extract by Mask Raster #####################################################
for raster in rasters_after_interpolation:
    outExtractByMask = ExtractByMask(raster, mask)
    outname = os.path.join(output_dir, os.path.splitext(raster)[0] + '.tif')
    print(outname) # Watching the progress
    outExtractByMask.save(outname)
################################################################################
