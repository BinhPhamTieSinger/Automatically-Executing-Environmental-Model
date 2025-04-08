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
from wrf import getvar, ALL_TIMES # type: ignore

os.makedirs("Result/Output", exist_ok=True)

columns = ['PRES', 'RH', 'WSPEED', 'WDIR', 'WU', 'WV', 'LON', 'LAT']
df = pd.DataFrame(columns=columns)

def calculate_wind_direction(u, v):
    wind_dir = np.arctan2(u, v) * 180 / np.pi
    wind_dir = (wind_dir + 360) % 360
    return wind_dir

def calculate_wind_vector(ws, wd):
    wd_rad = np.radians(wd)
    u = ws * np.sin(wd_rad)
    v = ws * np.cos(wd_rad)
    return u, v

def compute_time_period(wrfs, month, UTC):
    day_month = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    current = 0
    starting_times = []; ending_times = []
    for wrf in wrfs:
        starting_time = 0; ending_time = 0
        starting_date = int(wrf.split('_')[-1].split('-')[-1])
        starting_month = int(wrf.split('_')[-1].split('-')[1])
        if (starting_month < month):
            ending_date = day_month[starting_month]+1
            starting_time = (ending_date - starting_date)*24
            ending_time = 13*24-1
            current = starting_date+13-day_month[starting_month]
        else:
            starting_time = (current - starting_date)*24
            if (starting_date + 13 > day_month[starting_month]):
                ending_time = (day_month[starting_month]+1-starting_date)*24-1
            else:
                ending_time = 13*24-1
                current = starting_date+13

        starting_time -= UTC; ending_time -= UTC
        starting_times.append(starting_time)
        ending_times.append(ending_time)
    return starting_times, ending_times

def main():
    mat.use("Agg")
    month_number = 3; area = "Oregon"; year = 2023; UTC = -7
    path_WRF = f"G:/Model_Execution/WRF_Libraries/Thang_{month_number}_{area}/"
    wrfs = []
    for file in os.listdir(path_WRF):
        wrfs.append(file)
    path_MCIP = "G:/Model_Execution/MCIP_Libraries/"
    datasets = {
        'data_1_1': Dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}01/METCRO2D_110702.nc"),
        'data_1_2': Dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}01/METCRO3D_110702.nc"),
        'data_2_1': Dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}02/METCRO2D_110702.nc"),
        'data_2_2': Dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}02/METCRO3D_110702.nc"),
        'data_3_1': Dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}03/METCRO2D_110702.nc"),
        'data_3_2': Dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}03/METCRO3D_110702.nc"),
        'data_4_1': Dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}04/METCRO2D_110702.nc"),
        'data_4_2': Dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}04/METCRO3D_110702.nc")
    }
    lon_ds = Dataset(path_MCIP + f"MET_OREGON_{str(month_number).zfill(2)}04/GRIDCRO2D_110702.nc")
    lat_ds = Dataset(path_MCIP + f"MET_OREGON_{str(month_number).zfill(2)}04/GRIDCRO2D_110702.nc")
    for key in datasets:
        print(f"Done reading {key}")
    

    x = 0
    starting_times, ending_times = compute_time_period(wrfs, month_number, UTC)
    for row in range(datasets['data_1_2']['PRES'].shape[2]):
        for col in range(datasets['data_1_2']['PRES'].shape[3]):
            hour, day, dem = 0, 1, 0

            data_Pres = np.array([])
            data_WSpeed = np.array([])
            data_WDir = np.array([])
            data_Rain = np.array([])
            data_RH = np.array([])
            for i, wrf in enumerate(wrfs):
                starting_time = starting_times[i]
                ending_time = ending_times[i]
                wrfin = Dataset(path_WRF + wrf)
                rh2 = getvar(wrfin, "rh2", ALL_TIMES)
                data_Rain = np.append(data_Rain, wrfin["RAINC"][starting_time:ending_time+1, row+1, col+1])
                data_RH = np.append(data_RH, rh2[starting_time:ending_time+1, row+1, col+1])
                data_Pres = np.append(data_Pres, datasets[f'data_{i+1}_2']['PRES'][starting_time:ending_time+1, 0, row, col])
                data_WSpeed = np.append(data_WSpeed, datasets[f'data_{i+1}_1']['WSPD10'][starting_time:ending_time+1, 0, row, col])
                data_WDir = np.append(data_WDir, datasets[f'data_{i+1}_1']['WDIR10'][starting_time:ending_time+1, 0, row, col])
                print(f"{wrf} {starting_time} {ending_time} {ending_time - starting_time + 1}")
            # print(data_Rain.shape, data_RH.shape, data_Pres.shape, data_WSpeed.shape, data_WDir.shape)

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
    df["WDIR"] = calculate_wind_direction(df["WU"], df["WV"])
    print(df.head())

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

    df_PRES.to_excel('G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/PRES.xlsx')
    df_RH.to_excel('G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/RH.xlsx')

    ds_PRES = xr.Dataset.from_dataframe(df_PRES)
    ds_RH = xr.Dataset.from_dataframe(df_RH)
    ds_PRES.to_netcdf('G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/PRES.nc')
    ds_RH.to_netcdf('G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/RH.nc')



if __name__ == "__main__":
    main()