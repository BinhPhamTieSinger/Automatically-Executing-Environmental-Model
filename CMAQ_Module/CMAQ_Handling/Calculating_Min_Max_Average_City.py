import os
from arcpy import *
import arcpy.management
import subprocess
import pandas as pd
import rasterio
import numpy as np
import sys



### LISTING TIFF FILES AFTER CALIBRATE ###################################
path_tiff_files = r'F:/CMAQ_Model/HaNoi_Project/Extract_Map/'
raw_name = os.listdir(path_tiff_files)
outnames = []
for rname in raw_name:
    portion = os.path.splitext(rname)
    temp_name = portion[0] + '.tif'
    outnames.append(temp_name)

arcpy.env.overwriteOutput = True
arcpy.env.workspace = path_tiff_files
rasters_after_extract_map = arcpy.ListRasters("*", "ALL")
for raster in rasters_after_extract_map:
    print(raster)
###########################################################################

### Creating DataFrame ###
# Generate day and month lists
days, months = [str(day).zfill(2) for day in range(1, 32)], ['05']
# Create column names
column_names = [f'{day}{month}' for day in days for month in months]
column_names.append("May")
# Create an empty DataFrame with the specified column names
df = pd.DataFrame(columns=column_names)
print(df)
##########################

### CALCULATING AVERAGE DAYS AND MONTHS #########################################
PM_25 = rasterio.open(os.path.join(path_tiff_files, rasters_after_extract_map[0])).read(1)
size_of_array = 0
for i in range(PM_25.shape[0]):
    for j in range(PM_25.shape[1]):
        if (PM_25[i][j] >= 0):
            size_of_array += 1
maxhour, array_day, array_month = 0, np.zeros(size_of_array), np.zeros(size_of_array)
value_min, value_max = [], []
for raster in rasters_after_extract_map:
    raster_tiff = rasterio.open(os.path.join(path_tiff_files, raster))
    PM_25 = raster_tiff.read(1)
    row, col, value = [], [], []
    for i in range(PM_25.shape[0]):
        for j in range(PM_25.shape[1]):
            if (PM_25[i][j] >= 0):
                value.append(PM_25[i][j])
                row.append(i) # longitude
                col.append(j) # latitude
                # print(PM_25[i][j])
            # else:
            #     print(PM_25[i][j])
    value = np.array(value)
    hours = int(raster[5:7])
    days = int(raster[0:2])
    months = int(raster[2:4])
    maxhour += 1
    print(PM_25.shape[0], PM_25.shape[1], hours, days, months, raster, array_day.shape, value.shape) # Watching the process
    array_day = array_day + value
    array_month = array_month + value
    array_day = np.array(array_day)
    value = np.array(value)
    if maxhour == 24:
        maxhour, dem = 0, 0
        for i in range(PM_25.shape[0]):
            for j in range(PM_25.shape[1]):
                if (PM_25[i][j] >= 0):
                    PM_25[i][j] = array_day[dem]/24
                    dem = dem + 1
        print(np.min(array_day)/24)
        print(np.max(array_day)/24)
        value_min.append(np.min(array_day)/24)
        value_max.append(np.max(array_day)/24)
        array_day = np.zeros(size_of_array)
        ### Exporting Tiff Files from df after Calibrate ###################################################
        metadata = raster_tiff.meta
        transform = metadata['transform']
        metadata.update({
            'dtype': PM_25.dtype,
            'count': 1,
            'height': PM_25.shape[0],
            'width': PM_25.shape[1],
            'transform': transform
        })
        output_tiff = f"F:\CMAQ_Model\HaNoi_Project\Average_Day_Month\Tiff_File\Day\Day_{str(days).zfill(2)}.tiff"
        with rasterio.open(output_tiff, 'w', **metadata) as dst:
            dst.write(PM_25, 1)
        #######################################################################################################
    ### Exporting Monthly Average ###
maxhour, dem = 0, 0
for i in range(PM_25.shape[0]):
    for j in range(PM_25.shape[1]):
        if (PM_25[i][j] >= 0):
            PM_25[i][j] = array_month[dem]/(24*31)
            dem = dem + 1
print(np.min(array_month)/(24*31))
print(np.max(array_month)/(24*31))
value_min.append(np.min(array_month)/(24*31))
value_max.append(np.max(array_month)/(24*31))
array_month = np.zeros(size_of_array)
metadata = raster_tiff.meta
transform = metadata['transform']
metadata.update({
    'dtype': PM_25.dtype,
    'count': 1,
    'height': PM_25.shape[0],
    'width': PM_25.shape[1],
    'transform': transform
})
output_tiff = f"F:\CMAQ_Model\HaNoi_Project\Average_Day_Month\Tiff_File\Month\May.tiff"
with rasterio.open(output_tiff, 'w', **metadata) as dst:
    dst.write(PM_25, 1)

    ### Importing Values to DataFrame and export it as Excel ###
df.loc['Min'] = value_min
df.loc['Max'] = value_max
outExcelDir = r"F:/CMAQ_Model/HaNoi_Project/Average_Day_Month/"
df.to_excel(outExcelDir + 'Average.xlsx', index = False)
#################################################################################
