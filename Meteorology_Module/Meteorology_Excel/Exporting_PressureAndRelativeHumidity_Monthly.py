import matplotlib as mat
import matplotlib.cm as cm
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from math import pi
from windrose import WindroseAxes
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap
from rasterio.transform import from_origin
from netCDF4 import Dataset
import os, rasterio
from wrf import getvar, ALL_TIMES

path_CMAQ = "F:/CMAQ_Calibration/CSUM/"
path_RH = "F:/WRF_Libraries/Thang_5/"
path_PM25 = "F:/CMAQ_Calibration/RESULT/T5/"

path_WRF = "F:/CMAQ_WRF_HaNoi/WRF/"
data_1_1 = Dataset(path_WRF + "MET_0501/METCRO2D_110702.nc")
data_1_2 = Dataset(path_WRF + "MET_0501/METCRO3D_110702.nc")
data_2_1 = Dataset(path_WRF + "MET_0502/METCRO2D_110702.nc")
data_2_2 = Dataset(path_WRF + "MET_0502/METCRO3D_110702.nc")
data_3_1 = Dataset(path_WRF + "MET_0503/METCRO2D_110702.nc")
data_3_2 = Dataset(path_WRF + "MET_0503/METCRO3D_110702.nc")
data_4_1 = Dataset(path_WRF + "MET_0504/METCRO2D_110702.nc")
data_4_2 = Dataset(path_WRF + "MET_0504/METCRO3D_110702.nc")
lon_ds = Dataset(path_WRF + "MET_0501/GRIDCRO2D_110702.nc")
lat_ds = Dataset(path_WRF + "MET_0501/GRIDCRO2D_110702.nc")

columns = ['PRES', 'RH', 'WSPEED', 'WDIR', 'WU', 'WV', 'LON', 'LAT']
df = pd.DataFrame(columns=columns)

def calculate_wind_direction(u, v):
    wind_dir = np.arctan2(u, v) * 180 / np.pi
    wind_dir = (wind_dir + 360) % 360
    return wind_dir

def calculate_wind_vector(ws, wd):
    # Convert wind direction from degrees to radians
    wd_rad = np.radians(wd)
    # Calculate x and y components
    u = ws * np.sin(wd_rad)
    v = ws * np.cos(wd_rad)
    return u, v

x = 0
for row in range(data_1_2['PRES'].shape[2]):
    for col in range(data_1_2['PRES'].shape[3]):
        data_Pres, data_RH = np.array([]), np.array([])
        data_WSpeed, data_WDir = np.array([]), np.array([])
        hour, day, dem = 0, 1, 0
        ### FOR RH2 ADN RAINC
        wrfin_1 = Dataset(path_RH + "wrfout_d03_2023-04-24")
        rh2 = getvar(wrfin_1, "rh2", ALL_TIMES)
        print(row+1, col+1, rh2.shape)
        data_RH = np.append(data_RH, rh2[168-7:337-7, row+1, col+1])
        
        wrfin_2 = Dataset(path_RH + "wrfout_d03_2023-05-01")
        rh2 = getvar(wrfin_2, "rh2", ALL_TIMES)
        print(row+1, col+1, rh2.shape)
        data_RH = np.append(data_RH, rh2[169-7:337-7, row+1, col+1])
        
        wrfin_3 = Dataset(path_RH + "wrfout_d03_2023-05-08")
        rh2 = getvar(wrfin_3, "rh2", ALL_TIMES)
        print(row+1, col+1, rh2.shape)
        data_RH = np.append(data_RH, rh2[169-7:337-7, row+1, col+1])
        
        wrfin_4 = Dataset(path_RH + "wrfout_d03_2023-05-18")
        rh2 = getvar(wrfin_4, "rh2", ALL_TIMES)
        print(row+1, col+1, rh2.shape)
        data_RH = np.append(data_RH, rh2[97-7:336-7, row+1, col+1])

        ### FOR OTHER METEOROLOGICAL FACTORS
        data_Pres = np.append(data_Pres, data_1_2['PRES'][168-7:337-7, 0, row, col])
        data_Pres = np.append(data_Pres, data_2_2['PRES'][169-7:337-7, 0, row, col])
        data_Pres = np.append(data_Pres, data_3_2['PRES'][169-7:337-7, 0, row, col])
        data_Pres = np.append(data_Pres, data_4_2['PRES'][97-7:336-7, 0, row, col])

        data_WDir = np.append(data_WDir, data_1_1['WDIR10'][168-7:337-7, 0, row, col])
        data_WDir = np.append(data_WDir, data_2_1['WDIR10'][169-7:337-7, 0, row, col])
        data_WDir = np.append(data_WDir, data_3_1['WDIR10'][169-7:337-7, 0, row, col])
        data_WDir = np.append(data_WDir, data_4_1['WDIR10'][97-7:336-7, 0, row, col])

        data_WSpeed = np.append(data_WSpeed, data_1_1['WSPD10'][168-7:337-7, 0, row, col])
        data_WSpeed = np.append(data_WSpeed, data_2_1['WSPD10'][169-7:337-7, 0, row, col])
        data_WSpeed = np.append(data_WSpeed, data_3_1['WSPD10'][169-7:337-7, 0, row, col])
        data_WSpeed = np.append(data_WSpeed, data_4_1['WSPD10'][97-7:336-7, 0, row, col])

        data_U = data_WSpeed;  data_V = data_WSpeed
        data_U = data_U * np.sin(data_WDir*pi/180.0)
        data_V = data_V * np.cos(data_WDir*pi/180.0)

        data_Lon = lon_ds["LON"][0, 0, row, col]
        data_Lat = lat_ds["LAT"][0, 0, row, col]
        data_Pres = data_Pres/100

        print(data_Pres.size, data_RH.size, data_WDir.size, data_WSpeed.size)
        df.loc[x] = [data_Pres.mean(), data_RH.mean(), data_WSpeed.mean(), data_WDir.mean(), 
                     data_U.mean(), data_V.mean(), data_Lon, data_Lat]
        x = x + 1
        print(row, col); print('-'*75)

print(df)
print(df["WV"].values)
print(df["WU"].values)
df["WDIR"] = calculate_wind_direction(df["WU"], df["WV"])
print(df)

PRES = df['PRES']; RH = df['RH']
WSPEED = df['WSPEED']; WDIR = df['WDIR']
lon_values = lon_ds["LON"][0, 0, :, :].flatten(); lon_values = lon_values[:len(df)]
lat_values = lat_ds["LAT"][0, 0, :, :].flatten(); lat_values = lat_values[:len(df)]
df_PRES = pd.DataFrame(columns = ["PRES", "WSPEED", "WDIR", "LON", "LAT"])
df_RH = pd.DataFrame(columns = ["RH", "WSPEED", "WDIR", "LON", "LAT"])
df_PRES["PRES"] = PRES; df_RH["RH"] = RH
df_PRES["WSPEED"] = WSPEED; df_RH["WSPEED"] = WSPEED
df_PRES["WDIR"] = WDIR; df_RH["WDIR"] = WDIR
df_PRES["LON"] = lon_values; df_RH["LON"] = lon_values
df_PRES["LAT"] = lat_values; df_RH["LAT"] = lat_values

df_PRES.to_excel('F:/Bao_Cao/17_Pressure_WSPEED_WDIR_Distribution/PRES.xlsx')
df_RH.to_excel('F:/Bao_Cao/18_RH_WSPEED_WDIR_Distribution/RH.xlsx')

ds_PRES = xr.Dataset.from_dataframe(df_PRES)
ds_RH = xr.Dataset.from_dataframe(df_RH)
ds_PRES.to_netcdf('F:/Bao_Cao/17_Pressure_WSPEED_WDIR_Distribution/PRES.nc')
ds_RH.to_netcdf('F:/Bao_Cao/18_RH_WSPEED_WDIR_Distribution/RH.nc')
