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

path_WRF = "F:/CMAQ_WRF_HaNoi/WRF/"
data_WindVector_1 = xr.open_dataset(path_WRF + "MET_0501/METCRO2D_110702.nc")
data_WindVector_2 = xr.open_dataset(path_WRF + "MET_0502/METCRO2D_110702.nc")
data_WindVector_3 = xr.open_dataset(path_WRF + "MET_0503/METCRO2D_110702.nc")
data_WindVector_4 = xr.open_dataset(path_WRF + "MET_0504/METCRO2D_110702.nc")
rows = np.array([35, 34, 30, 53, 37])
cols = np.array([32, 34, 63, 51, 33])
mat.use("Agg")
for index in range(rows.size):
    row = rows[index]; col = cols[index]
    Wind_Speed, Wind_Direction = np.array([]), np.array([])
    for i in range(168-7, 337-7, 1):
        Wind_Speed = np.append(Wind_Speed, data_WindVector_1['WSPD10'].sel(TSTEP=i, LAY=0, ROW=row, COL=col).values)
        Wind_Direction = np.append(Wind_Direction, data_WindVector_1['WDIR10'].sel(TSTEP=i, LAY=0, ROW=row, COL=col).values)
        # print(i)
    for i in range(169-7, 337-7, 1):
        Wind_Speed = np.append(Wind_Speed, data_WindVector_2['WSPD10'].sel(TSTEP=i, LAY=0, ROW=row, COL=col).values)
        Wind_Direction = np.append(Wind_Direction, data_WindVector_2['WDIR10'].sel(TSTEP=i, LAY=0, ROW=row, COL=col).values)
        # print(i)
    for i in range(169-7, 337-7, 1):
        Wind_Speed = np.append(Wind_Speed, data_WindVector_3['WSPD10'].sel(TSTEP=i, LAY=0, ROW=row, COL=col).values)
        Wind_Direction = np.append(Wind_Direction, data_WindVector_3['WDIR10'].sel(TSTEP=i, LAY=0, ROW=row, COL=col).values)
        # print(i)
    for i in range(97-7, 336-7, 1):
        Wind_Speed = np.append(Wind_Speed, data_WindVector_4['WSPD10'].sel(TSTEP=i, LAY=0, ROW=row, COL=col).values)
        Wind_Direction = np.append(Wind_Direction, data_WindVector_4['WDIR10'].sel(TSTEP=i, LAY=0, ROW=row, COL=col).values)
        # print(i)
    print(row, col)
    column_names = ['Wind_Direction', 'Wind_Speed', 'Velocidad_x', 'Velocidad_y']
    df = pd.DataFrame(columns = column_names)
    for index in range(Wind_Direction.size):
        value = []; value.append(Wind_Direction[index]); value.append(Wind_Speed[index])
        value.append(Wind_Speed[index] * np.sin(Wind_Direction[index]*pi/180.0))
        value.append(Wind_Speed[index] * np.cos(Wind_Direction[index]*pi/180.0))
        df.loc[index] = value
    hist, bin_edges = np.histogram(Wind_Speed, bins='auto')
    bin_widths = np.diff(bin_edges)
    total_samples = len(Wind_Speed)
    percentages = hist / total_samples * 100
    labels = [f"{low:.1f}-{high:.1f}" for low, high in zip(bin_edges[:-1], bin_edges[1:])]
    plt.bar(labels, percentages, width=bin_widths, color='blue')
    plt.xlabel('Wind Speed Range (m/s)')
    plt.ylabel('Percentage (%)')
    plt.title('Wind Speed Class Frequency Distribution')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'F:/Wind_Vector/Wind_Class/Wind_Class_{row}_{col}.png')
    plt.close('all')
