from arcpy import *
from arcpy import env
from arcpy.sa import *
import os
import time

path_Netcdf_NASA = r"D:/Code_Result/Result/NASA/NASA_Data_30minutes/"
path_Tiff = r"D:/Code_Result/Result/NASA/Tiff_Data_30minutes/"
arcpy.env.workspace = path_Netcdf_NASA
os.makedirs(path_Netcdf_NASA, exist_ok=True)
os.makedirs(path_Tiff, exist_ok=True)
arcpy.env.overwriteOutput = True
variables = ['PM25_RH35_GCC']

month_day = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
for month in range(8, 9, 1):
    # for day in range(1, month_day[month]+1, 1):
    for day in range(1, 7, 1):
        path_Netcdf = path_Netcdf_NASA + f"Y23M{str(month).zfill(2)}/" + f"D{str(day).zfill(2)}/"
        files_Netcdf = os.listdir(path_Netcdf); print(path_Netcdf)
        for file_Netcdf in files_Netcdf:
            for variable in variables:
                parts_Netcdf = file_Netcdf.split('.')
                year = parts_Netcdf[4][0:4]
                month = parts_Netcdf[4][4:6]
                day = parts_Netcdf[4][6:8]
                hour = parts_Netcdf[4][9:11]
                tiff_file = year + "_" + month+ "_" + day + "_" + hour + "_" + variable
                netcdf_file = path_Netcdf + file_Netcdf
                print(tiff_file)
                arcpy.MakeNetCDFRasterLayer_md(netcdf_file, variable, 
                                            'lon', 'lat', tiff_file, "", "", "", "")
                arcpy.CopyRaster_management(tiff_file, path_Tiff + tiff_file + '.tif')
    
print("Success Fully Executing Code")