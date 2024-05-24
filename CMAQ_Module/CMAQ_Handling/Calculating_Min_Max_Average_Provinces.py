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

province = []
### Listing Shape Files ###
arcpy.env.workspace = masks
shapefiles = arcpy.ListFeatureClasses()
for shapefile in shapefiles:
    print(shapefile)
    province.append(shapefile[:-4])
    os.makedirs("F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/Day/Tiff/" + shapefile[:-4], exist_ok=True)
    os.makedirs("F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/Day/Map/" + shapefile[:-4], exist_ok=True)
    os.makedirs("F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/Month/Tiff/" + shapefile[:-4], exist_ok=True)
    os.makedirs("F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/Month/Map/" + shapefile[:-4], exist_ok=True)
    
arcpy.env.workspace = masks
shapefiles = arcpy.ListFeatureClasses()
for shapefile in shapefiles:
    print(shapefile)

### LISTING TIFF FILES AFTER CALIBRATE ###
path_tiff_files = r'F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/Hour/Tiff/'
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


### Creating DataFrame ###
# Generate day and month lists
days, months = [str(day).zfill(2) for day in range(1, 32)], ['05']
# tinhCaMau = ["CaiNuoc", "DamDoi", "NamCan", "NgocHien", "PhuTan", "ThoiBinh", "TP_CaMau", "TranVanThoi", "UMinh"]
# Create column names
column_names = [f'{day}{month}_{tinh}' for day in days for month in months for tinh in province]
column_names.extend(f"May_{tinh}" for tinh in province)
# Create an empty DataFrame with the specified column names
df = pd.DataFrame(columns=column_names)
print(df)
##########################

# Create dictionaries to store variables for each province
array_day_province = {}
array_month_province = {}
max_hour_province = {}
ok_province = {}
PM_25_province = {}

### CALCULATING AVERAGE DAYS AND MONTHS ###
value_min, value_max, value_average = [], [], []
for tinh in province:
    array_day_province[tinh] = []
    array_month_province[tinh] = []
    max_hour_province[tinh] = 0
    ok_province[tinh] = True
    PM_25_province[tinh] = []
# PM_25_huyen = [PM_25_CaiNuoc, PM_25_DamDoi, PM_25_NamCan, PM_25_NgocHien, PM_25_PhuTan, PM_25_ThoiBinh, PM_25_TP_CaMau, PM_25_TranVanThoi, PM_25_UMinh]
for raster in rasters_after_extract_map:
    i = 8
    while (raster[i] != '.'):
        i += 1
    tinh = raster[8:i]
    raster_tiff = rasterio.open(os.path.join(path_tiff_files, raster))
    PM_25 = raster_tiff.read(1)
    row, col, value, size = [], [], [], 0
    for i in range(PM_25.shape[0]):
        for j in range(PM_25.shape[1]):
            if (PM_25[i][j] >= 0):
                value.append(PM_25[i][j])
                row.append(i) # longitude
                col.append(j) # latitude
                size += 1
                # print(PM_25[i][j])
    value = np.array(value)
    days = int(raster[0:2])
    print(raster, tinh, days) # Watching the process
    print(value.shape)
    max_hour = max_hour_province[tinh]
    ok = ok_province[tinh]
    array_day = array_day_province[tinh]
    array_month = array_month_province[tinh]
    if max_hour == 0:
        array_day = np.zeros(size)
    if ok:
        array_month = np.zeros(size)
        ok_province[tinh] = False
    print('-'*100)
    array_day += value
    array_month += value
    max_hour += 1
    max_hour_province[tinh] = max_hour
    PM_25_province[tinh] = PM_25
    array_day_province[tinh] = array_day
    array_month_province[tinh] = array_month
    # Kiểm tra nếu đã đủ 24 giờ thì tính trung bình và reset
    if max_hour == 24:
        max_hour, dem = 0, 0
        max_hour_province[tinh] = max_hour
        for i in range(PM_25.shape[0]):
            for j in range(PM_25.shape[1]):
                if PM_25[i][j] >= 0:
                    PM_25[i][j] = array_day[dem] / 24
                    dem += 1
        print(np.min(array_day) / 24)
        print(np.max(array_day) / 24)
        value_min.append(np.min(array_day) / 24)
        value_max.append(np.max(array_day) / 24)
        value_average.append(np.mean(array_day) / 24)
        array_day = np.zeros(PM_25.shape[0] * PM_25.shape[1])
        
        # Xuất Tiff Files từ df sau khi hiệu chỉnh
        metadata = raster_tiff.meta
        transform = metadata['transform']
        metadata.update({
            'dtype': PM_25.dtype,
            'count': 1,
            'height': PM_25.shape[0],
            'width': PM_25.shape[1],
            'transform': transform
        })
        output_tiff = f"F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/Day/Tiff/{tinh}/Day_{str(days).zfill(2)}_{tinh}.tiff"
        with rasterio.open(output_tiff, 'w', **metadata) as dst:
            dst.write(PM_25, 1)

    ### Exporting Monthly Average ###
for tinh in province:
    PM_25 = PM_25_province[tinh]
    array_month = array_month_province[tinh]
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
    value_average.append(np.mean(array_month)/(24*31))
    metadata = raster_tiff.meta
    transform = metadata['transform']
    metadata.update({
        'dtype': PM_25.dtype,
        'count': 1,
        'height': PM_25.shape[0],
        'width': PM_25.shape[1],
        'transform': transform
    })
    output_tiff = f"F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/Month/Tiff/{tinh}/May.tiff"
    with rasterio.open(output_tiff, 'w', **metadata) as dst:
        dst.write(PM_25, 1)

    ### Importing Values to DataFrame and export it as Excel ###
print(df.shape)
value_min = np.array(value_min)
print(value_min)
print(value_min.size)
df.loc['Min'] = value_min
df.loc['Max'] = value_max
df.loc['Average'] = value_average
print(df)
outExcelDir = r"F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/"
df.to_excel(outExcelDir + 'Min_Max_Average.xlsx', index = False)
