################################
# 2. Read_Extract_Calculate.py #
################################

import os
from arcpy import *
from arcpy import env
from arcpy.sa import *
import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import from_origin
from rasterio.plot import show
import rioxarray as rio
from PIL import Image
import xarray as xr
import time

### READING EXCEL FILES USING PANDAS ############################################
    ### Reading multiplier ###
df = pd.read_excel(r"F:\CMAQ_Model\HaNoi_Project\Excel\Calibration_Multiplier.xlsx")
print(df)
    ### Reading longitude and lattitude ###
df_lon = pd.read_excel(r"F:\CMAQ_Model\HaNoi_Project\Excel\COORLON.xlsx")
df_lat = pd.read_excel(r"F:\CMAQ_Model\HaNoi_Project\Excel\COORLAT.xlsx")
print(df_lon)
print(df_lat)
#################################################################################



### CREATING DATAFRAMES MULTIPLIER FOR EACH HOURS ###############################
column_names, column_min_max, column_cell = ['ROW', 'COL', 'LON', 'LAT'], [], ['ROW', 'COL', 'LON', 'LAT']
hours = [str(i).zfill(2) for i in range(24)]
days_months = [f'{str(day).zfill(2)}{str(5).zfill(2)}' for day in range(1, 32)]
column_names.extend(f'{day}-{hour}h' for day in days_months for hour in hours)
column_min_max.extend(f'{day}-{hour}h' for day in days_months for hour in hours)
df_multiplier = pd.DataFrame(columns=column_names)
df_min_max = pd.DataFrame(columns = column_min_max)
df_cell = pd.DataFrame(columns=column_cell)
print(df_min_max)
#################################################################################



### LISTING TIFF FILES ####################################
path_tiff_files = r'F:/CMAQ_Model/HaNoi_Project/Tiff/'
raw_name = os.listdir(path_tiff_files)
outnames = []
for rname in raw_name:
    portion = os.path.splitext(rname)
    temp_name = portion[0] + '.TIFF'
    outnames.append(temp_name)

# for outname in outnames:
#     print(outname)

arcpy.env.overwriteOutput = True
arcpy.env.workspace = path_tiff_files
rasters = arcpy.ListRasters("*", "All")
###########################################################


### FIXING AND SORTING COLUMNS NAME ############
column_names_df = []
for col in df.columns:
    if (len(col[5:]) == 2):
        col = col[:5] + str(col[5:6]).zfill(2)
    column_names_df.append(col)
df.columns = column_names_df
df = df.reindex(sorted(df.columns), axis=1)
#################################################



### READING RASTER USING RASTERIO #####
date_str = np.array(df.columns)
num_day, max_day = 0, date_str.size
########################################

value_min, value_max, value_average, value_cell = [], [], [], []
for raster in rasters:
    raster_tiff = rasterio.open(os.path.join(path_tiff_files, raster))
    ### Check the number of bands in the raster file ###
    # print(raster)
    PM_25 = raster_tiff.read(1)
    ### Show Tiff File ###
    # print(PM_25[0].size)  ### Show Values
    # show(PM_25)           ### Show Image 
    row, col, value = [], [], []
    for i in range(PM_25.shape[0]):
        for j in range(PM_25.shape[1]):
            value.append(PM_25[i][j])
            row.append(i) # longitude
            col.append(j) # latitude
    ####################################################
    ### Doing with Raster Calculation Part 1 #############################################
            
        ### Formula Multiplier ###
        # If X == Y or Y < X (X is the smallest multiplier)
        # or Y > X (X is the largest multilier) -> M(X) == M(Y)
        # Else if X < Y < Z -> M(Y) = (M(X)*(Y-X) + M(Z)*(Z-Y))/(Z-X)
    # print(num_day)
    # print(date_str[num_day])
    months_standard = int(date_str[num_day][2:4])  # Extract the months
    days_standard = int(date_str[num_day][:2])  # Extract the days
    check = 5
    while (check < len(date_str[num_day]) and date_str[num_day][check] != 'h'):
        check += 1
    hours_standard = int(date_str[num_day][5:check])  # Extract the hours
    # print(months_standard)
    # print(days_standard)
    # print(hours_standard)
    parts = raster.split("_")
    hours = int(parts[2][0:2])
    days = int(parts[1][0:2])
    months = int(parts[1][2:4])
    date_raster = parts[1][0:2] + parts[1][2:4] + '-' + parts[2][0:2] + 'h'
    print(date_raster, hours, days, months, num_day) # Watch the progress during running the code
    # print('-'*100)
    df_multiplier['ROW'], df_multiplier['COL'] = row, col
    df_cell['ROW'], df_cell['COL'] = row, col
    df_multiplier[date_raster], df_cell[date_raster] = value, value
    df_cell['LON'], df_cell['LAT'] = df_lon["value"].values, df_lat["value"].values
    df_multiplier['LON'], df_multiplier['LAT'] = df_lon["value"].values, df_lat["value"].values
        ### Extract hours, days, and month ###
    if (hours_standard == 17 and days_standard == 29):
        df_multiplier[date_raster] = df_multiplier[date_raster] * df[date_str[num_day]][2]
    else:
        if (hours == hours_standard and days == days_standard):
            df_multiplier[date_raster] = df_multiplier[date_raster] * df[date_str[num_day]][2]
            num_day = num_day + 1
        elif (hours_standard == 7 and days_standard == 2):
            df_multiplier[date_raster] = df_multiplier[date_raster] * df[date_str[num_day]][2]
        elif (days == days_standard and hours < hours_standard):
            MX, MZ = df[date_str[num_day-1]][2], df[date_str[num_day]][2]
            Y, X, Z = hours+24, int(date_str[num_day-1][5:6]), int(date_str[num_day][5:6])+24
            MY = (MX*(Y-X) + MZ*(Z-Y))/(Z-X)
            df_multiplier[date_raster] = df_multiplier[date_raster] * MY
        elif (days < days_standard):
            MX, MZ = df[date_str[num_day-1]][2], df[date_str[num_day]][2]
            Y, X, Z = hours, int(date_str[num_day-1][5:6]), int(date_str[num_day][5:6])+24
            MY = (MX*(Y-X) + MZ*(Z-Y))/(Z-X)
            df_multiplier[date_raster] = df_multiplier[date_raster] * MY
    ##############################################################################################
    
    ### Raster Calculation Part 2 ###################################################################
        ### Applying the function y = ax^b ###
    a, b = 1.1644, 0.9633 # Define a, b of the function
    print(date_raster) # Watching the progress it makes during runnng the code
    df_multiplier[date_raster] = a * (df_multiplier[date_raster] ** b)
    df_cell[date_raster] = df_multiplier[date_raster]
    #################################################################################################

    ### Changing Result of Tiff Files ###
    dem = 0
    for i in range(PM_25.shape[0]):
        for j in range(PM_25.shape[1]):
            PM_25[i][j] = df_multiplier[date_raster][dem]
            dem = dem + 1
    # show(PM_25)
    print(np.min(PM_25))
    print(np.max(PM_25))
    value_min.append(np.min(PM_25))
    value_max.append(np.max(PM_25))
    value_average.append(np.mean(PM_25))
    #####################################

    ### Approach 2:
    metadata = raster_tiff.meta
    transform = metadata['transform']
    metadata.update({
        'dtype': PM_25.dtype,
        'count': 1,
        'height': PM_25.shape[0],
        'width': PM_25.shape[1],
        'transform': transform
    })
    output_tiff = f"F:\CMAQ_Model\HaNoi_Project\Tiff_after_Calibrate\{date_raster}.tiff"
    with rasterio.open(output_tiff, 'w', **metadata) as dst:
        dst.write(PM_25, 1)
    #######################################################################################################

    print('-'*50)
    ### Delay Time ###
    # time.sleep(0.1)
    ##################

### Check if the df after applying multiplier is correct?
print(df_cell)
print(df_min_max.shape)
value_min = np.array(value_min)
print(value_min.shape)
df_min_max.loc['Min'] = value_min
df_min_max.loc['Max'] = value_max
df_min_max.loc['Average'] = value_average

### Saving df_multiplier into the folder #############################
outExcelDir = "F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/"
out_Min_Max = "F:/CMAQ_Model/HaNoi_Project/Average_Day_Month/"
outCellDir = "F:/CMAQ_Model/HaNoi_Project/Average_Province_Cell/"
df_cell.to_excel(outCellDir + 'Cell_PM25.xlsx', index = False)
df_min_max.to_excel(out_Min_Max + 'Hourly_Average.xlsx', index = False)
df_multiplier.to_excel(outExcelDir + 'Multiplier.xlsx', index = False)
######################################################################
