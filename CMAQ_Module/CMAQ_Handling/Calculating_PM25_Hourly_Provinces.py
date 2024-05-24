import os
from arcpy import *
from arcpy import env 
from arcpy import * 
from arcpy.sa import *
import subprocess
import pandas as pd
import rasterio
import numpy as np
import sys

masks = "F:/CMAQ_Model/HaNoi_Project/24.Shp/HaNoi_qh/"
output_tiff_file = r'F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/Hour/Tiff/'
# output_map_file = r'F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/Hour/Map/'

### Listing Shape Files ###
arcpy.env.workspace = masks
shapefiles = arcpy.ListFeatureClasses()
for shapefile in shapefiles:
    print(shapefile)

### Listing Raster Files ###
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
for raster in rasters_after_interpolation:
    print(raster)

### Extract by Mask Raster ###
for raster in rasters_after_interpolation:
    for mask in shapefiles:
        print(os.path.splitext(raster)[0] + '_' + os.path.splitext(mask)[0])
        outExtractByMask = ExtractByMask(raster, masks + mask)
        outname = os.path.join(output_tiff_file, os.path.splitext(raster)[0] + '_' +  os.path.splitext(mask)[0] + '.tif')
        print(outname) # Watching the progress
        outExtractByMask.save(outname)
