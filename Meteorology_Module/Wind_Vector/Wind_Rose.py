import matplotlib as mat
import matplotlib.cm as cm
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from math import pi
from windrose import WindroseAxes
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap

path_WRF = "F:/CMAQ_WRF_HaNoi/WRF/"
data_WindVector_1 = xr.open_dataset(path_WRF + "MET_0401/METCRO2D_110702.nc")
data_WindVector_2 = xr.open_dataset(path_WRF + "MET_0402/METCRO2D_110702.nc")
data_WindVector_3 = xr.open_dataset(path_WRF + "MET_0403/METCRO2D_110702.nc")
data_WindVector_4 = xr.open_dataset(path_WRF + "MET_0404/METCRO2D_110702.nc")
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
    colors = ['darkgreen', 'green', 'blue', 'yellow', 'orange', 'red']
    cmap = LinearSegmentedColormap.from_list("Custom", colors)
    ax = WindroseAxes.from_ax()
    ax.bar(df['Wind_Direction'], df['Wind_Speed'], nsector=36, blowto=False, opening=1.0, edgecolor='white', cmap=cmap, bins=np.array([0, 0.5, 2.10, 3.60, 5.70, 8.80, 11.10]))
    ax.set_legend()
    plt.savefig(f'F:/Wind_Vector/Wind_Blow_From/Wind_Rose_{row}_{col}.png')
    plt.close('all')
    ax = WindroseAxes.from_ax()
    ax.bar(df['Wind_Direction'], df['Wind_Speed'], nsector=36, blowto=True, opening=1.0, edgecolor='white', cmap=cmap, bins=np.array([0, 0.5, 2.10, 3.60, 5.70, 8.80, 11.10]))
    ax.set_legend()
    plt.savefig(f'F:/Wind_Vector/Wind_Blow_To/Wind_Rose_{row}_{col}.png')
    plt.close('all')
