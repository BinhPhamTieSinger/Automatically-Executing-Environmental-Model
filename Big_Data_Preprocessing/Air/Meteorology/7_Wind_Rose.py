import matplotlib as mat
import matplotlib.cm as cm
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from math import pi
from windrose import WindroseAxes
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap
import geopandas as gpd
from netCDF4 import Dataset
import os

os.makedirs("Result/Output", exist_ok=True)

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

def compute_cell_indices(rows, cols, multiplier):
    x = np.array([], dtype=int)
    for r, c in zip(rows, cols):
        x = np.append(x, r * multiplier + c)
    return x

def main():
    mat.use("Agg")
    month_number = 2; area = "Oregon"; year = 2023; UTC = -7
    day_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    path_WRF = f"G:/Model_Execution/WRF_Libraries/Thang_{month_number}_{area}/"
    wrfs = []
    for file in os.listdir(path_WRF):
        wrfs.append(file)
    rows = np.array([63, 70, 70, 68, 69])
    cols = np.array([30, 30, 34, 30, 31])
    path_MCIP = "G:/Model_Execution/MCIP_Libraries/"
    datasets = {
        'data_WindVector_1': xr.open_dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}01/METCRO2D_110702.nc"),
        'data_WindVector_2': xr.open_dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}02/METCRO2D_110702.nc"),
        'data_WindVector_3': xr.open_dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}03/METCRO2D_110702.nc"),
        'data_WindVector_4': xr.open_dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}04/METCRO2D_110702.nc"),
    }
    for key in datasets: print(f"Done reading {key}")
    starting_times, ending_times = compute_time_period(wrfs, month_number, UTC)
    mat.use("Agg")
    for index in range(rows.size):
        row = rows[index]; col = cols[index]
        Wind_Speed, Wind_Direction = np.array([]), np.array([])
        for i, wrf in enumerate(wrfs):
            starting_time = starting_times[i]; ending_time = ending_times[i]
            for j in range(starting_time, ending_time+1):
                Wind_Speed = np.append(Wind_Speed, datasets[f'data_WindVector_{i+1}']['WSPD10'].sel(TSTEP=j, LAY=0, ROW=row, COL=col).values)
                Wind_Direction = np.append(Wind_Direction, datasets[f'data_WindVector_{i+1}']['WDIR10'].sel(TSTEP=j, LAY=0, ROW=row, COL=col).values)
        print(row, col)
        column_names = ['Wind_Direction', 'Wind_Speed', 'Velocidad_x', 'Velocidad_y']
        df = pd.DataFrame(columns = column_names)
        for index in range(Wind_Direction.size):
            value = []; value.append(Wind_Direction[index]); value.append(Wind_Speed[index])
            value.append(Wind_Speed[index] * np.sin(Wind_Direction[index]*pi/180.0))
            value.append(Wind_Speed[index] * np.cos(Wind_Direction[index]*pi/180.0))
            df.loc[index] = value
        colors = ['darkgreen', 'green', 'blue', 'yellow', 'orange', 'red']
        cmap = LinearSegmentedColormap.from_list("Custom", colors)
        ax = WindroseAxes.from_ax()
        ax.bar(df['Wind_Direction'], df['Wind_Speed'], nsector=36, normed=True, blowto=False, opening=0.8, edgecolor='white', cmap=cmap, bins=np.array([0, 0.5, 2.10, 3.60, 5.70, 8.80, 11.10]))
        ax.set_legend()
        plt.savefig(f'G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/Wind_Rose_Blow_From_{row}_{col}.png')
        plt.close('all')
        ax = WindroseAxes.from_ax()
        ax.bar(df['Wind_Direction'], df['Wind_Speed'], nsector=36, normed=True, blowto=True, opening=0.8, edgecolor='white', cmap=cmap, bins=np.array([0, 0.5, 2.10, 3.60, 5.70, 8.80, 11.10]))
        ax.set_legend()
        plt.savefig(f'G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/Wind_Rose_Blow_To_{row}_{col}.png')
        plt.close('all')
        
if __name__ == "__main__":
    main()