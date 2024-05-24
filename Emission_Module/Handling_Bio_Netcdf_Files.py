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

variable_Bio = ['emission_bio', 'emiss_bio']
substance_Bio = ["acetaldehyde", "acetone", "butanes_and_higher_alkanes", "butenes_and_higher_alkenes", "ch4", "co",
                 "ethane", "ethanol", "ethene", "formaldehyde", "isoprene", "methanol", "other_aldehydes", "other_ketones",
                 "other_monoterpenes", "propane", "propene", "toluene"]
time_Data_excel_Bio = ['01012022']; area_Cell = 9000000
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
df_Value = pd.DataFrame(columns = coordinate + hour_Day)
list_Value_Substance = {
    'co': ['CO', ],
    'ethane': ['ETHA', ],
    'propane': ['PRPA', ],
    'ethene': ['ETH', ],
    'propene': ['OLE', ],
    'formaldehyde': ['FORM', ],
    'other_aldehydes': ['ALDX', ], 
    'other_ketones': ['KET', ], 
    'toluene': ['TOL', ], 
    'ch4': ['CH4', ],
    'butanes_and_higher_alkanes': ['PAR2 (BUTANES)', ],
    'butenes_and_higher_alkenes': ['IOLE1 (ALKENES)', ],
    'methanol': ['MEOH', ],
    'ethanol': ['ETOH', ],
    'acetaldehyde': ['ALD2', ], 
    'acetone': ['ACET', ],
    'isoprene': ['ISOP', ],
    'other_monoterpenes': ['TERP', ],
}











### READING ###

path_tiff_files = "D:/Emission/CAMS_GLOB_BIO_TIFF/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = path_tiff_files
rasters = arcpy.ListRasters("*", "ALL")
for raster in rasters:
    print(raster)

output_folder_Bio = "D:/Emission/CAMS_GLOB_BIO_EXCEL/RV/"
create_directory_if_not_exists(output_folder_Bio)
arcpy.env.workspace = output_folder_Bio
for raster in rasters:
    parts = raster.split('_')
    sector = parts[0] + "_" + parts[1]
    substance, i = parts[2], 2
    while (parts[i] != 'Bio'):
        i += 1
    for j in range(3, i, 1):
        substance = substance + "_" + parts[j]
    date = parts[i+1][0:8]
    raster_tiff = os.path.join(path_tiff_files, raster)
    print(raster_tiff)
    ExtractValuesToPoints(mask, raster_tiff, output_folder_Bio + "Extract_Point_Bio")
    arcpy.conversion.TableToExcel(output_folder_Bio + "Extract_Point_Bio.shp", output_folder_Bio + f"value_{substance}_{sector}_{date}.xlsx")


df_Bio = pd.DataFrame()
for variable in variable_Bio:
    for time_df in time_Data_excel_Bio:
        ds_Bio = xr.open_dataset(globals().get(f"data_Bio_{substance}", 0))
        if variable in ds_Bio.variables:
            for substance in substance_Bio:
                df_Excel = pd.read_excel(output_folder_Bio + f"value_{substance}_{variable}_{time_df}.xlsx")
                df_Bio["LON"], df_Bio["LAT"] = df_Excel["lon"], df_Excel["lat"]
                df_Bio[f"{variable}_{substance}_{time_df}"] = df_Excel["RASTERVALU"]
df_Bio.to_excel(output_folder_Bio + "df_Bio.xlsx", index = False)
print(df_Bio)











### HANDLING ###
total_iterations = len(rasters)  # Total number of iterations
for raster in tqdm(rasters, desc="Processing files", total=total_iterations):
    print("\n")
    parts = raster.split('_')
    date = parts[-1][0:8]
    sector_x = parts[0] + "_" + parts[1]
    substance = parts[2]
    i = 3
    while (parts[i] != "Bio"):
        substance = substance + "_" + parts[i]
        i += 1
    occupation = parts[i]
    for value_substance in list_Value_Substance[substance]:
        value_substance_x = value_substance
        for times in range(7):
            value_substance = value_substance_x
            day, month, year = int(date[2:4])+times, int(date[0:2]), int(date[4:8])
            value_Temporal_Month = pd.read_excel('D:/Emission/Excel/Temporal-Emissions.xlsx', sheet_name = f'fd-{date[0:2]}18-EDGAR')
            day_weekday = string_Day[datetime.date(year, month, day).weekday()]
            sector = "AGS" + '-' + "ags"
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
            # print(value)
            # globals()[f"df_Value_Day_{month}"] = value
            # print(globals().get(f"df_Value_Day_{month}"))
            # raster_tiff = rasterio.open(os.path.join(path_tiff_files, raster))
            value_Layer_Const, value_Hour = [], []
            for index in range(df_Bio[sector_x + "_" + substance + "_" + date].size):
                value_Layer_Const.append((df_Bio[sector_x + "_" + substance + "_" + date][index]*(10**3)*area_Cell)/value_substance)
            # print(value_Layer_Const)
            for index in range(df_Bio[sector_x + "_" + substance + "_" + date].size):
                value_Hour = [df_Bio['LON'][index], df_Bio['LAT'][index]]
                for hour in range(24):
                    value_Hour.append(value_Layer_Const[index]*value_Sector[datetime.date(year, month, day).weekday()]*value[hour]*7/30)
                globals()[f"df_Value_Day_{day}"].loc[index] = value_Hour
            
        excel_file_path_df = f"D:/Emission/CAMS_GLOB_BIO_EXCEL/DF/{occupation}_{value_substance_x}_{sector_x}_{int(date[0:2])}_{substance}.xlsx"
        excel_file_path_cb = f"D:/Emission/CAMS_GLOB_BIO_EXCEL/CB/{occupation}_{value_substance_x}_{sector_x}_{int(date[0:2])}_{substance}.xlsx"
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
            globals()[f'value_{i}']['Substance'] = value_substance_x
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
        with pd.ExcelWriter(excel_file_path_df) as excel_writer:
            for hour in range(1, 32, 1):
                globals()[f"df_Value_Day_{hour}"].to_excel(excel_writer, sheet_name = f"Day_{hour}", index=False)
            
        with pd.ExcelWriter(excel_file_path_cb) as excel_writer:
            for hour in range(1, 32, 1):
                print(hour)
                globals()[f"value_{hour}"]['Day'] = hour
                print(hour, globals()[f"value_{hour}"])
                globals()[f"value_{hour}"].to_excel(excel_writer, sheet_name = f"Day_{hour}", index=False, header=False)
        print("DataFrame saved to Excel file:", excel_file_path_df)
        print("Combining Hour saved to Excel file:", excel_file_path_cb)
        print('-'*75)

print("Successfully Executing Code!!!")
