######################################################################
# Note: In this section there is many required:                      #
# - The tutorial about how to transfer from 1 month to another       #
# and the value for each sector and substance: Excel/Tutorial.xls    #
# (If you need Tutorial.xls you can download in the folder)          #
# - The mask (point shapefile) for extracting value to points        #
######################################################################

from arcpy import *
from arcpy import env
from arcpy.sa import *
import pandas as pd
import numpy as np
import os, datetime
from osgeo import ogr
import rasterio
import xarray as xr
from rasterio.transform import from_origin
import subprocess, time
from tqdm import tqdm

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")

### INITIALIZATION ###
value_Substances = pd.read_excel('D:/Emission/Excel/Tutorial.xls', sheet_name = '(3)')
value_Day_Sector = pd.read_excel('D:/Emission/Excel/Tutorial.xls', sheet_name = '(1)')
substance_Air = ["acetylene", "alcohols", "bc", "benzene", "co", "co2", "ethane", "ethene", "formaldehyde",
                 "hexanes", "ketones", "nh3", "nmvocs", "nox", "oc", "other_aldehydes", "other_alkenes_and_alkynes",
                 "other_aromatics", "propane", "propene", "so2", "toluene", "xylene"] # Substances in Air Module
time_Data_excel_Air = ['01012023']; variable_Air = ['avi']; area_Cell = 9000000
### Setting Time Dimension, Variable and Area of Cell
print(value_Substances)
print(value_Day_Sector)

string_Day = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']; coordinate = ['LON', 'LAT']
hour_Day = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23', 'h24']
mask = "D:/Emission/Point_ShapeFile/Point_Determination.shp"
# This mask required for extracting Values from GeoTIFF files to Points
# This mask and the GeoTIFF files have to be in the same coordinate
lat_value, lon_value = [], []
shapefile = ogr.Open(mask)
layer = shapefile.GetLayer()
for feature in layer:
    attributes = feature.items()
    lat_value.append(attributes['lat'])
    lon_value.append(attributes['lon'])
column_value_name = ['Year', 'Month', 'Day', 'Hour', 'Lat', 'Lon', 'Substance', 'Value']
df_Value_Day_1 , value_1  = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_2 , value_2  = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_3 , value_3  = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_4 , value_4  = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_5 , value_5  = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_6 , value_6  = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_7 , value_7  = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_8 , value_8  = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_9 , value_9  = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_10, value_10 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_11, value_11 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_12, value_12 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_13, value_13 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_14, value_14 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_15, value_15 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_16, value_16 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_17, value_17 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_18, value_18 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_19, value_19 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_20, value_20 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_21, value_21 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_22, value_22 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_23, value_23 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_24, value_24 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_25, value_25 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_26, value_26 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_27, value_27 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_28, value_28 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_29, value_29 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_30, value_30 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
df_Value_Day_31, value_31 = pd.DataFrame(columns = coordinate + hour_Day), pd.DataFrame()
Value_Month = pd.DataFrame()
df_Value = pd.DataFrame(columns = coordinate + hour_Day)
list_Value_Substance = {
    'bc': ['PEC', ],
    'oc': ['POC', ],
    'co': ['CO', ],
    'ethane': ['ETHA', ],
    'co2': ['CO2_INV', ],
    'nox': ['NO', 'NO2', 'N2O_INV', ],
    'nmvocs': ['VOC_INV', ],
    'so2': ['SO2', ],
    'nh3': ['NH3', ], 
    'propane': ['PRPA', ],
    'hexanes': ['PAR1 (HEXAN)', ],
    'ethene': ['ETH', ],
    'propene': ['OLE', ],
    'acetylene': ['ETHY', ],
    'other_alkenes_and_alkynes': ['IOLE1 (ALKENES)', ],
    'alcohols': ['MEOH', 'ETOH', ], 
    'formaldehyde': ['FORM', ],
    'other_aldehydes': ['ALDX', ], 
    'ketones': ['KET', ], 
    'benzene': ['BENZ', ], 
    'toluene': ['TOL', ], 
    'xylene': ['XYLMN', ], 
    'other_aromatics': ['XYLMN', ], 
}










### READING ###
path_tiff_files = "D:/Emission_PhuYen/CAMS_GLOB_AIR_TIFF/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = path_tiff_files
rasters = arcpy.ListRasters("*", "ALL")
for raster in rasters:
    print(raster)
output_folder_Air = "D:/Emission_PhuYen/CAMS_GLOB_AIR_EXCEL/RV/"
create_directory_if_not_exists(output_folder_Air)
arcpy.env.workspace = output_folder_Air
for raster in rasters:
    parts = raster.split('_')
    sector = parts[0]
    substance, i = parts[1], 1
    while (parts[i] != 'Air'):
        i += 1
    for j in range(2, i, 1):
        substance = substance + "_" + parts[j]
    date = parts[i+1][0:8]
    raster_tiff = os.path.join(path_tiff_files, raster)
    print(raster_tiff)
    ExtractValuesToPoints(mask, raster_tiff, output_folder_Air + "Extract_Point_Air")
    arcpy.conversion.TableToExcel(output_folder_Air + "Extract_Point_Air.shp", output_folder_Air + f"value_{substance}_{sector}_{date}.xlsx")

df_Air = pd.DataFrame()

for variable in variable_Air:
    for time_df in time_Data_excel_Air:
        for substance in substance_Air:
            df_Excel = pd.read_excel(output_folder_Air + f"value_{substance}_{variable}_{time_df}.xlsx")
            df_Air["LON"], df_Air["LAT"] = df_Excel["lon"], df_Excel["lat"]
            df_Air[f"{variable}_{substance}_{time_df}"] = df_Excel["RASTERVALU"]
df_Air.to_excel(output_folder_Air + "df_Air.xlsx", index = False)
print(df_Air)







### HANDLING ###
total_iterations = len(rasters)  # Total number of iterations
for raster in tqdm(rasters, desc="Processing files", total=total_iterations):
    print("\n")
    parts = raster.split('_')
    date = parts[-1][0:8]
    sector_x = parts[0]
    substance = parts[1]
    i = 2
    while (parts[i] != "Air"):
        substance = substance + "_" + parts[i]
        i += 1
    occupation = parts[i]
    for value_substance in list_Value_Substance[substance]:
        value_substance_x = value_substance
        for times in range(7):
            value_substance = value_substance_x
            day, month, year = int(date[2:4])+times, int(date[0:2]), int(date[4:8])
            value_Temporal_Month = pd.read_excel('D:/Emission/Excel/Temporal-Emission_PhuYens.xlsx', sheet_name = f'fd-{date[0:2]}18-EDGAR')
            day_weekday = string_Day[datetime.date(year, month, day).weekday()]
            sector = "TRO" + '-' + "tro"
            index, value_Sector = 0, []
            try:
                while (value_Day_Sector['Sector (*)'][index] != sector):
                    index += 1
            except:
                print(sector, "Out of index")
            for day_x in string_Day:
                value_Sector.append(value_Day_Sector[day_x][index])
            # print(value_Sector)
            if (day_weekday == 'Thứ 7'):
                sector = sector + '-' + 'Saturday'
            elif (day_weekday == 'Chủ Nhật'):
                sector = sector + '-' + 'Sunday'
            else:
                sector = sector + '-' + 'Weekday'
            index_Value_Substances = 0
            # print(substance, sector, value_substance)
            while (value_Substances['NAME'][index_Value_Substances] != value_substance):
                index_Value_Substances += 1
            value_substance = value_Substances['VALUE'][index_Value_Substances]
            # print(times, sector_x + "_" + substance + "_" + date, day_weekday, sector, substance, value_substance)
            index_Value_Sector_Day, value = 0, []
            while (value_Temporal_Month['Sector'][index_Value_Sector_Day] != sector):
                index_Value_Sector_Day += 1
            for hour in hour_Day:
                value.append(value_Temporal_Month[hour][index_Value_Sector_Day])
            
            value_Layer_Const, value_Hour = [], []
            for index in range(df_Air[sector_x + "_" + substance + "_" + date].size):
                value_Layer_Const.append((df_Air[sector_x + "_" + substance + "_" + date][index]*(10**3)*area_Cell)/value_substance)
            # print(value_Layer_Const)
            for index in range(df_Air[sector_x + "_" + substance + "_" + date].size):
                value_Hour = [df_Air['LON'][index], df_Air['LAT'][index]]
                for hour in range(24):
                    value_Hour.append(value_Layer_Const[index]*value_Sector[datetime.date(year, month, day).weekday()]*value[hour]*7/30)
                globals()[f"df_Value_Day_{day}"].loc[index] = value_Hour
            
        excel_file_path_df = f"D:/Emission_PhuYen/CAMS_GLOB_AIR_EXCEL/DF/{occupation}_{value_substance_x}_{sector_x}_{int(date[0:2])}_{substance}.xlsx"
        excel_file_path_cb = f"D:/Emission_PhuYen/CAMS_GLOB_AIR_EXCEL/CB/{occupation}_{value_substance_x}_{sector_x}_{int(date[0:2])}_{substance}.xlsx"
        # DF --> DataFrames  # CB --> Combines (You can actually delete the DataFrames but do not delete Combines if you haven't run the Sum_Up_Convert_Result.py)
        create_directory_if_not_exists(excel_file_path_df)
        create_directory_if_not_exists(excel_file_path_cb)
      
        # Save the DataFrame to Excel
        for i in range(1, 8, 1):
            print(raster, i)
            value_Value_x, value_Value_hour, value_Value_day = [], [], []
            value_Value_year, value_Value_month, substance_saved = [], [], []
            value_lon, value_lat = [], []
            for hour in hour_Day:
                for index in range(globals()[f"df_Value_Day_{i}"][hour].size):
                    value_Value_x.append(globals()[f"df_Value_Day_{i}"][hour][index])
                    value_Value_month.append(month)
                    value_Value_year.append(2023)
                    substance_saved.append(value_substance_x)
                    value_lon.append(globals()[f"df_Value_Day_{i}"]['LON'][index])
                    value_lat.append(globals()[f"df_Value_Day_{i}"]['LAT'][index])
                    value_Value_hour.append(int(hour[1:]))
            globals()[f"value_{i}"]['Year'] = value_Value_year
            globals()[f"value_{i}"]['Month'] = value_Value_month
            globals()[f"value_{i}"]['Day'] = i
            globals()[f"value_{i}"]['Hour'] = value_Value_hour
            globals()[f"value_{i}"]['Lat'] = value_lat
            globals()[f"value_{i}"]['Lon'] = value_lon
            globals()[f"value_{i}"]['Substance'] = value_substance_x
            globals()[f"value_{i}"]['Value'] = value_Value_x
        for hour in range(8, 32, 1):
            print(raster, hour)
            if (hour % 7 == 0):
                globals()[f"df_Value_Day_{hour}"] = globals()[f"df_Value_Day_7"]
                globals()[f"value_{hour}"] = globals()[f"value_7"]
                globals()[f"value_{hour}"]['Day'] = hour
            else:
                globals()[f"df_Value_Day_{hour}"] = globals()[f"df_Value_Day_{hour%7}"]
                globals()[f"value_{hour}"] = globals()[f"value_{hour%7}"]
                globals()[f"value_{hour}"]['Day'] = hour
            # print(hour, globals()[f"value_{hour}"])
        for index_value_lon_lat in range(globals()[f"df_Value_Day_{i}"]['LON']):
            lon_value = globals()[f"df_Value_Day_{i}"]['LON'][index_value_lon_lat]
            lat_value = globals()[f"df_Value_Day_{i}"]['LAT'][index_value_lon_lat]
            value = 0
            for index in range(1, 32, 1):
                for hour in range(1, 25, 1):
                    value = value + globals()[f"value_{index}"]

        print('-'*75)

print("Successfully Executing Code!!!")
