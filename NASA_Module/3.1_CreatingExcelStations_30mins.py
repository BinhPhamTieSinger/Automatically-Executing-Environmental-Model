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

mask = "D:/Code_Result/Result/NASA/Coordinate_Shapefile/Oregon_Stations_Coordinate.shp" ### TO DO: TO FIX
path_Tiff = r"D:/Code_Result/Result/NASA/Waiting_Process/"
path_Value = r"D:/Code_Result/Result/NASA/Value_Data_30minutes/"
os.makedirs(path_Value, exist_ok=True)
arcpy.env.workspace = path_Tiff
arcpy.env.overwriteOutput = True

rasters = arcpy.ListRasters("*", "ALL")
for raster in rasters:
    print(raster)
    raster_tiff = path_Tiff + raster
    parts = raster_tiff.split('_')
    ExtractValuesToPoints(mask, raster_tiff, path_Value + "Extract_Point_PhuYen")
    arcpy.conversion.TableToExcel(path_Value + "Extract_Point_PhuYen.shp", path_Value + f"{raster[:-4]}.xlsx")