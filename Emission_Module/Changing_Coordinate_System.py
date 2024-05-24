import arcpy
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
from pyproj import Transformer

arcpy.env.overwriteOutput = True; rasters = np.array([])

### This will project all the GeoTIFF files to GCS_WGS_1984
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("GCS_WGS_1984")
sr = arcpy.SpatialReference("GCS_WGS_1984")
path_tiff_files = "F:/Emission/CAMS_GLOB_AIR_TIFF/"
arcpy.env.workspace = path_tiff_files
rasters_Air = arcpy.ListRasters("*", "ALL")
for raster in rasters_Air:
    arcpy.DefineProjection_management(raster, sr)
    print(raster)

path_tiff_files = "F:/Emission/CAMS_GLOB_ANT_TIFF/"
arcpy.env.workspace = path_tiff_files
rasters_Ant = arcpy.ListRasters("*", "ALL")
for raster in rasters_Ant:
    arcpy.DefineProjection_management(raster, sr)
    print(raster)

path_tiff_files = "F:/Emission/CAMS_GLOB_BIO_TIFF/"
arcpy.env.workspace = path_tiff_files
rasters_Bio = arcpy.ListRasters("*", "ALL")
for raster in rasters_Bio:
    arcpy.DefineProjection_management(raster, sr)
    print(raster)

###########################################################

### This will project the mask of 
in_mask = "D:/Emission/Point_ShapeFile/Point_Determination.shp"
out_mask = "D:/Emission/Point_ShapeFile/Point_Determination_Project.shp"
out_coordinate_system = arcpy.SpatialReference("GCS_WGS_1984")
arcpy.Project_management(in_mask, out_mask, out_coordinate_system)
