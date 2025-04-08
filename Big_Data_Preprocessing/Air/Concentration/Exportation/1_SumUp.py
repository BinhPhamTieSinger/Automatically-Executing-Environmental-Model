import os
from arcpy import *
from arcpy import env
from arcpy.sa import *
import rasterio
import numpy as np
import pandas as pd
from rasterio.transform import from_origin
from rasterio.plot import show
import rioxarray as rio
from PIL import Image
import xarray as xr
import time
import shutil

def generating_PATH(path):
    os.makedirs(path, exist_ok=True)

month_standard_string = "March"; month_string_number = "3"; day_in_month = 31
PROJECT = "Oregon_Project"; MASK_PROVINCE_CITY = "Oregon_Project"
BIG_DATA_PREPROCESSING_PATH = "G:/Big_Data_Preprocessing"
EXPORTATION_PATH = f"{BIG_DATA_PREPROCESSING_PATH}/Air/Concentration/Exportation"
CALIBRATION_PATH = f"{BIG_DATA_PREPROCESSING_PATH}/Air/Concentration/Calibration"

SHAPEFILE_CITY = f"{EXPORTATION_PATH}/Result/0_Initial_Data/Shapefile/OREGON_SHAPEFILES/reprojected_orcntypoly.shp"
SHAPEFILE_PROVINCES = f"{EXPORTATION_PATH}/Result/0_Initial_Data/Shapefile/OREGON_PROVINCES/"
SHAPEFILE_POINT_DETERMINATION = f"{EXPORTATION_PATH}/Result/0_Initial_Data/Shapefile/OREGON_POINTS/Oregon_Point_Actual.shp"
VALUE_IDW = 0.002

# shutil.copy(fr'{CALIBRATION_PATH}/Result/5_GeoTIFF_Calibrated/', fr'{EXPORTATION_PATH}/Result/1_GeoTIFF_Dataset/')

mask_EXTRACT_MASK_POINTS = SHAPEFILE_POINT_DETERMINATION
path_tiff_files_EXTRACT_MASK_POINTS = fr'{EXPORTATION_PATH}/Result/1_GeoTIFF_Dataset/'
output_dir_EXTRACT_MASK_POINTS = fr'{EXPORTATION_PATH}/Result/3_Raster_Dataset/'
output_pnt_EXTRACT_MASK_POINTS = fr'{EXPORTATION_PATH}/Result/2_Point_Dataset/'

path_shape_files_INTERPOLATION = fr'{EXPORTATION_PATH}/Result/2_Point_Dataset/'
path_shape_out_files_INTERPOLATION = fr"{EXPORTATION_PATH}/Result/4_Point_Dataset_3D/"
out_IDW_INTERPOLATION = fr"{EXPORTATION_PATH}/Result/5_IDW_Interpolation"

# mask_EXTRACT_MAP_CITY = f"{MAIN_PATH}/{MASK_PROVINCE_CITY}/{SHAPEFILE_CITY}"
mask_EXTRACT_MAP_CITY = SHAPEFILE_CITY
output_dir_EXTRACT_MAP_CITY = fr'{EXPORTATION_PATH}/Result/6_Extract_Map/'
path_tiff_files_EXTRACT_MAP_CITY = fr'{EXPORTATION_PATH}/Result/5_IDW_Interpolation/'

# masks_EXTRACT_MAP_PROVINCE = f"{MAIN_PATH}/{MASK_PROVINCE_CITY}/{SHAPEFILE_PROVINCES}/"
masks_EXTRACT_MAP_PROVINCE = SHAPEFILE_PROVINCES
output_tiff_file_EXTRACT_MAP_PROVINCE = fr'{EXPORTATION_PATH}/Result/7_Average_Province/Hour/Tiff/'
path_tiff_files_EXTRACT_MAP_PROVINCE = fr'{EXPORTATION_PATH}/Result/5_IDW_Interpolation/'

path_tiff_files_CALCULATING_CITY = fr'{EXPORTATION_PATH}/Result/6_Extract_Map/'
path_tiff_files_CALCULATING_DAY_CITY = f"{EXPORTATION_PATH}/Result/8_Average_City/Tiff_File/Day/"
path_tiff_files_CALCULATING_MONTH_CITY = f"{EXPORTATION_PATH}/Result/8_Average_City/Tiff_File/Month/"
outExcelDir_CALCULATING_CITY = fr"{EXPORTATION_PATH}/Result/8_Average_City/"

# masks_CALCULATING_PROVINCE = f"{MAIN_PATH}/{MASK_PROVINCE_CITY}/{SHAPEFILE_PROVINCES}/"
masks_CALCULATING_PROVINCE = SHAPEFILE_PROVINCES
outExcelDir_CALCULATING_PROVINCE = fr"{EXPORTATION_PATH}/Result/7_Average_Province/"
path_tiff_files_CALCULATING_PROVINCE = fr'{EXPORTATION_PATH}/Result/7_Average_Province/Hour/Tiff/'
path_tiff_files_CALCULATING_DAY_PROVINCE = f"{EXPORTATION_PATH}/Result/7_Average_Province/Day/Tiff/"
path_tiff_files_CALCULATING_HOUR_PROVINCE = f"{EXPORTATION_PATH}/Result/7_Average_Province/Month/Tiff/"

output_dir_MAX_AVERAGE = f"{EXPORTATION_PATH}/Result/8_Average_City/Tiff_File/Max_Average/"
output_tiff_HOUR_1_MAX = f"{EXPORTATION_PATH}/Result/8_Average_City/Tiff_File/Max_Average/{month_standard_string}_Hour_1_Max.tiff"
output_tiff_HOUR_24_MAX = f"{EXPORTATION_PATH}/Result/8_Average_City/Tiff_File/Max_Average/{month_standard_string}_Hour_24_Max.tiff"

generating_PATH(path_tiff_files_EXTRACT_MASK_POINTS)
generating_PATH(output_dir_EXTRACT_MASK_POINTS)
generating_PATH(output_pnt_EXTRACT_MASK_POINTS)
generating_PATH(path_shape_files_INTERPOLATION)
generating_PATH(path_shape_out_files_INTERPOLATION)
generating_PATH(out_IDW_INTERPOLATION)
generating_PATH(output_dir_EXTRACT_MAP_CITY)
generating_PATH(path_tiff_files_EXTRACT_MAP_CITY)
generating_PATH(masks_EXTRACT_MAP_PROVINCE)
generating_PATH(output_tiff_file_EXTRACT_MAP_PROVINCE)
generating_PATH(path_tiff_files_EXTRACT_MAP_PROVINCE)
generating_PATH(path_tiff_files_CALCULATING_CITY)
generating_PATH(path_tiff_files_CALCULATING_DAY_CITY)
generating_PATH(path_tiff_files_CALCULATING_MONTH_CITY)
generating_PATH(outExcelDir_CALCULATING_CITY)
generating_PATH(masks_CALCULATING_PROVINCE)
generating_PATH(outExcelDir_CALCULATING_PROVINCE)
generating_PATH(path_tiff_files_CALCULATING_PROVINCE)
generating_PATH(path_tiff_files_CALCULATING_DAY_PROVINCE)
generating_PATH(path_tiff_files_CALCULATING_HOUR_PROVINCE)
generating_PATH(output_dir_MAX_AVERAGE)



print("1. Extract the points from the raster")
raw_name = os.listdir(path_tiff_files_EXTRACT_MASK_POINTS)
outnames = []
for rname in raw_name:
    portion = os.path.splitext(rname)
    temp_name = portion[0] + '.TIFF'
    outnames.append(temp_name)
# for outname in outnames:
#     print(outname)
arcpy.env.overwriteOutput = True
arcpy.env.workspace = path_tiff_files_EXTRACT_MASK_POINTS
rasters_after_calibrate = arcpy.ListRasters("*", "All")
for raster in rasters_after_calibrate:
    outExtractByMask = ExtractByMask(raster, mask_EXTRACT_MASK_POINTS)
    outname = os.path.join(output_dir_EXTRACT_MASK_POINTS, os.path.splitext(raster)[0] + '.tif')
    outExtractByMask.save(outname)
    print(output_pnt_EXTRACT_MASK_POINTS + f"{raster[:-5]}.shp")
    arcpy.RasterToPoint_conversion(outExtractByMask, output_pnt_EXTRACT_MASK_POINTS + f"{raster[:-5]}.shp", "VALUE")



print("2. Interpolation")
raw_name = os.listdir(path_shape_files_INTERPOLATION)
outnames = []
for rname in raw_name:
    if (rname.endswith(".shp")):
        portion = os.path.splitext(rname)
        temp_name = portion[0]
        outnames.append(temp_name)
arcpy.env.outputZFlag = 'Enabled'
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("3D")
for outname in outnames:
    print(outname, os.path.splitext(outname)[0] + '.tif', path_shape_out_files_INTERPOLATION + outname + ".shp") # Watching the progress
    arcpy.ddd.FeatureTo3DByAttribute(path_shape_files_INTERPOLATION + outname + ".shp", path_shape_out_files_INTERPOLATION + outname + ".shp", 'GRID_CODE')
    outIDW = Idw(path_shape_out_files_INTERPOLATION + outname + ".shp", "GRID_CODE", VALUE_IDW, None, RadiusVariable(12, None))
    outname = os.path.join(out_IDW_INTERPOLATION, os.path.splitext(outname)[0] + '.tif')
    outIDW.save(outname)



print("3. Extract the map city from the raster")
raw_name = os.listdir(path_tiff_files_EXTRACT_MAP_CITY)
outnames = []
for rname in raw_name:
    if (rname.endswith('.tif')):
        portion = os.path.splitext(rname)
        temp_name = portion[0] + '.tif'
        outnames.append(temp_name)
# for outname in outnames:
#     print(outname)
arcpy.env.overwriteOutput = True
arcpy.env.workspace = path_tiff_files_EXTRACT_MAP_CITY
rasters_after_interpolation = arcpy.ListRasters("*", "TIF")
for raster in rasters_after_interpolation:
    outExtractByMask = ExtractByMask(raster, mask_EXTRACT_MAP_CITY)
    outname = os.path.join(output_dir_EXTRACT_MAP_CITY, os.path.splitext(raster)[0] + '.tif')
    print(outname)
    outExtractByMask.save(outname)






print("4. Calculate Max Average 24 Hours and 1 Hour")
os.makedirs(output_dir_MAX_AVERAGE, exist_ok=True)
raw_name = os.listdir(output_dir_EXTRACT_MAP_CITY)
outnames = [os.path.splitext(rname)[0] + '.tif' for rname in raw_name]
arcpy.env.overwriteOutput = True
arcpy.env.workspace = output_dir_EXTRACT_MAP_CITY
rasters_after_extract_map = arcpy.ListRasters("*", "ALL")
# for raster in rasters_after_extract_map:
#     print(raster)
def max_elements(*arrays):
    return np.max(np.array(arrays), axis=0)
first_raster_path = os.path.join(output_dir_EXTRACT_MAP_CITY, rasters_after_extract_map[0])
with rasterio.open(first_raster_path) as src:
    metadata = src.meta.copy()
    substance = src.read(1)
    valid_mask = (substance >= 0)
    size_of_array = np.count_nonzero(valid_mask)
    array_daily = np.zeros(size_of_array)
    array_monthly = np.zeros(size_of_array)
    array_day = np.zeros(size_of_array)
    array_month = np.zeros(size_of_array)
maxhour = 0
value = []
for raster in rasters_after_extract_map:
    with rasterio.open(os.path.join(output_dir_EXTRACT_MAP_CITY, raster)) as src:
        substance = src.read(1)
        valid_values = substance[valid_mask]
        array_day = max_elements(array_day, valid_values)
        array_daily = array_daily + valid_values
    # print(raster)
    parts = raster.split('_')
    value = np.array(value)
    hours = int(raster[5:7])
    days = int(raster[0:2])
    months = int(raster[2:4])
    maxhour += 1
    print(hours, days, months, raster)
    if maxhour == 24:
        array_monthly = max_elements(array_monthly, array_daily/24)
        array_month = max_elements(array_month, array_day)
        maxhour = 0
        array_day.fill(0)
        array_daily.fill(0)
substance[valid_mask] = array_month
metadata.update({
    'dtype': 'float32',
    'count': 1,
    'transform': src.transform
})
with rasterio.open(output_tiff_HOUR_1_MAX, 'w', **metadata) as dst:
    dst.write(substance.astype('float32'), 1)
substance[valid_mask] = array_monthly
metadata.update({
    'dtype': 'float32',
    'count': 1,
    'transform': src.transform
})
with rasterio.open(output_tiff_HOUR_24_MAX, 'w', **metadata) as dst:
    dst.write(substance.astype('float32'), 1)








print("5. Extract the map provinces from the raster")
os.makedirs(output_tiff_file_EXTRACT_MAP_PROVINCE, exist_ok=True)
arcpy.env.workspace = masks_EXTRACT_MAP_PROVINCE
shapefiles = arcpy.ListFeatureClasses()
# for shapefile in shapefiles:
#     print(shapefile)
arcpy.env.overwriteOutput = True
arcpy.env.workspace = path_tiff_files_EXTRACT_MAP_PROVINCE
rasters_after_interpolation = arcpy.ListRasters("*", "TIF")
# for raster in rasters_after_interpolation:
#     print(raster)
for raster in rasters_after_interpolation:
    for mask in shapefiles:
        # print(raster + '_' + os.path.splitext(mask)[0])
        outExtractByMask = ExtractByMask(raster, masks_EXTRACT_MAP_PROVINCE + mask)
        outname = os.path.join(output_tiff_file_EXTRACT_MAP_PROVINCE, raster + '_' +  os.path.splitext(mask)[0] + '.tif')
        print(outname)
        outExtractByMask.save(outname)







print("6. Calculate the average, min, max of substance in city")
os.makedirs(path_tiff_files_CALCULATING_DAY_CITY, exist_ok=True)
os.makedirs(path_tiff_files_CALCULATING_MONTH_CITY, exist_ok=True)
raw_name = os.listdir(path_tiff_files_CALCULATING_CITY)
outnames = []
for rname in raw_name:
    portion = os.path.splitext(rname)
    temp_name = portion[0] + '.tif'
    outnames.append(temp_name)
arcpy.env.overwriteOutput = True
arcpy.env.workspace = path_tiff_files_CALCULATING_CITY
rasters_after_extract_map = arcpy.ListRasters("*", "ALL")
# for raster in rasters_after_extract_map:
#     print(raster)
days, months = [str(day).zfill(2) for day in range(1, day_in_month+1)], [month_string_number]
column_names = [f'{day}{month}' for day in days for month in months]
column_names.append(month_standard_string)
df = pd.DataFrame(columns=column_names)
# print(df)
PM_25 = rasterio.open(os.path.join(path_tiff_files_CALCULATING_CITY, rasters_after_extract_map[0])).read(1)
size_of_array = 0
for i in range(PM_25.shape[0]):
    for j in range(PM_25.shape[1]):
        if (PM_25[i][j] >= 0):
            size_of_array += 1
maxhour, array_day, array_month = 0, np.zeros(size_of_array), np.zeros(size_of_array)
value_min, value_max = [], []
for raster in rasters_after_extract_map:
    raster_tiff = rasterio.open(os.path.join(path_tiff_files_CALCULATING_CITY, raster))
    PM_25 = raster_tiff.read(1)
    row, col, value = [], [], []
    for i in range(PM_25.shape[0]):
        for j in range(PM_25.shape[1]):
            if (PM_25[i][j] >= 0):
                value.append(PM_25[i][j])
                row.append(i)
                col.append(j)
    parts = raster.split('_')
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
        # print(np.min(array_day)/24)
        # print(np.max(array_day)/24)
        value_min.append(np.min(array_day)/24)
        value_max.append(np.max(array_day)/24)
        array_day = np.zeros(size_of_array)
        metadata = raster_tiff.meta
        transform = metadata['transform']
        metadata.update({
            'dtype': PM_25.dtype,
            'count': 1,
            'height': PM_25.shape[0],
            'width': PM_25.shape[1],
            'transform': transform
        })
        output_tiff = path_tiff_files_CALCULATING_DAY_CITY + f"Day_{str(days).zfill(2)}.tiff"
        with rasterio.open(output_tiff, 'w', **metadata) as dst:
            dst.write(PM_25, 1)
maxhour, dem = 0, 0
for i in range(PM_25.shape[0]):
    for j in range(PM_25.shape[1]):
        if (PM_25[i][j] >= 0):
            PM_25[i][j] = array_month[dem]/(24*day_in_month)
            dem = dem + 1
# print(np.min(array_month)/(24*day_in_month))
# print(np.max(array_month)/(24*day_in_month))
value_min.append(np.min(array_month)/(24*day_in_month))
value_max.append(np.max(array_month)/(24*day_in_month))
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
output_tiff = path_tiff_files_CALCULATING_MONTH_CITY + f"{month_standard_string}.tiff"
with rasterio.open(output_tiff, 'w', **metadata) as dst:
    dst.write(PM_25, 1)
df.loc['Min'] = value_min
df.loc['Max'] = value_max
df.to_excel(outExcelDir_CALCULATING_CITY + 'Average.xlsx', index = False)







print("7. Calculate the average, min, max of substance in province")
province = []
arcpy.env.workspace = masks_CALCULATING_PROVINCE
shapefiles = arcpy.ListFeatureClasses()
for shapefile in shapefiles:
    # print(shapefile)
    province.append(shapefile[:-4])
    os.makedirs(path_tiff_files_CALCULATING_DAY_PROVINCE + shapefile[:-4], exist_ok=True)
    os.makedirs(path_tiff_files_CALCULATING_HOUR_PROVINCE + shapefile[:-4], exist_ok=True)
arcpy.env.workspace = masks_CALCULATING_PROVINCE
shapefiles = arcpy.ListFeatureClasses()
# for shapefile in shapefiles:
    # print(shapefile)
raw_name = os.listdir(path_tiff_files_CALCULATING_PROVINCE)
outnames = []
for rname in raw_name:
    portion = os.path.splitext(rname)
    temp_name = portion[0] + '.tif'
    outnames.append(temp_name)
arcpy.env.overwriteOutput = True
arcpy.env.workspace = path_tiff_files_CALCULATING_PROVINCE
rasters_after_extract_map = arcpy.ListRasters("*", "ALL")
# for raster in rasters_after_extract_map:
#     print(raster)
days, months = [str(day).zfill(2) for day in range(1, day_in_month+1)], [month_string_number]
column_names = [f'{day}{month}_{tinh}' for day in days for month in months for tinh in province]
column_names.extend(f"{month_standard_string}_{tinh}" for tinh in province)
df = pd.DataFrame(columns=column_names)
# print(df)
array_day_province = {}
array_month_province = {}
max_hour_province = {}
ok_province = {}
PM_25_province = {}
value_min, value_max, value_average = [], [], []
for tinh in province:
    array_day_province[tinh] = []
    array_month_province[tinh] = []
    max_hour_province[tinh] = 0
    ok_province[tinh] = True
    PM_25_province[tinh] = []
for raster in rasters_after_extract_map:
    i = 13
    while (raster[i] != '.'):
        i += 1
    tinh = raster[13:i]
    raster_tiff = rasterio.open(os.path.join(path_tiff_files_CALCULATING_PROVINCE, raster))
    PM_25 = raster_tiff.read(1)
    row, col, value, size = [], [], [], 0
    for i in range(PM_25.shape[0]):
        for j in range(PM_25.shape[1]):
            if (PM_25[i][j] >= 0):
                value.append(PM_25[i][j])
                row.append(i)
                col.append(j)
                size += 1
    value = np.array(value)
    days = int(raster[0:2])
    # print(raster, tinh, days)
    # print(value.shape)
    max_hour = max_hour_province[tinh]
    ok = ok_province[tinh]
    array_day = array_day_province[tinh]
    array_month = array_month_province[tinh]
    if max_hour == 0:
        array_day = np.zeros(size)
    if ok:
        array_month = np.zeros(size)
        ok_province[tinh] = False
    array_day += value
    array_month += value
    max_hour += 1
    max_hour_province[tinh] = max_hour
    PM_25_province[tinh] = PM_25
    array_day_province[tinh] = array_day
    array_month_province[tinh] = array_month
    if max_hour == 24:
        max_hour, dem = 0, 0
        max_hour_province[tinh] = max_hour
        for i in range(PM_25.shape[0]):
            for j in range(PM_25.shape[1]):
                if PM_25[i][j] >= 0:
                    PM_25[i][j] = array_day[dem] / 24
                    dem += 1
        # print(np.min(array_day) / 24)
        # print(np.max(array_day) / 24)
        value_min.append(np.min(array_day) / 24)
        value_max.append(np.max(array_day) / 24)
        value_average.append(np.mean(array_day) / 24)
        array_day = np.zeros(PM_25.shape[0] * PM_25.shape[1])
        metadata = raster_tiff.meta
        transform = metadata['transform']
        metadata.update({
            'dtype': PM_25.dtype,
            'count': 1,
            'height': PM_25.shape[0],
            'width': PM_25.shape[1],
            'transform': transform
        })
        output_tiff = path_tiff_files_CALCULATING_DAY_PROVINCE + f"{tinh}/Day_{str(days).zfill(2)}_{tinh}.tiff"
        with rasterio.open(output_tiff, 'w', **metadata) as dst:
            dst.write(PM_25, 1)
for tinh in province:
    PM_25 = PM_25_province[tinh]
    array_month = array_month_province[tinh]
    maxhour, dem = 0, 0
    for i in range(PM_25.shape[0]):
        for j in range(PM_25.shape[1]):
            if (PM_25[i][j] >= 0):
                PM_25[i][j] = array_month[dem]/(24*day_in_month)
                dem = dem + 1
    # print(np.min(array_month)/(24*day_in_month))
    # print(np.max(array_month)/(24*day_in_month))
    value_min.append(np.min(array_month)/(24*day_in_month))
    value_max.append(np.max(array_month)/(24*day_in_month))
    value_average.append(np.mean(array_month)/(24*day_in_month))
    metadata = raster_tiff.meta
    transform = metadata['transform']
    metadata.update({
        'dtype': PM_25.dtype,
        'count': 1,
        'height': PM_25.shape[0],
        'width': PM_25.shape[1],
        'transform': transform
    })
    output_tiff = path_tiff_files_CALCULATING_HOUR_PROVINCE + f"{tinh}/{month_standard_string}.tiff"
    with rasterio.open(output_tiff, 'w', **metadata) as dst:
        dst.write(PM_25, 1)
# print(df.shape)
value_min = np.array(value_min)
# print(value_min)
# print(value_min.size)
df.loc['Min'] = value_min
df.loc['Max'] = value_max
df.loc['Average'] = value_average
# print(df)
df.to_excel(outExcelDir_CALCULATING_PROVINCE + 'Min_Max_Average.xlsx', index = False)