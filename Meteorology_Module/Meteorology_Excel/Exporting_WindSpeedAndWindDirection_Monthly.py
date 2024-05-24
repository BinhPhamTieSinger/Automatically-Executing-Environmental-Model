import matplotlib as mat
import pandas as pd
import numpy as np
# import geopandas as gpd
from netCDF4 import Dataset

path_CMAQ = "F:/CMAQ_Calibration/CSUM/"
path_RH = "F:/WRF_Libraries/Thang_5/"

path_WRF = "F:/CMAQ_WRF_HaNoi/WRF/"
data_1_1 = Dataset(path_WRF + "MET_0501/METCRO2D_110702.nc"); print('Done reading data_1_1')
data_2_1 = Dataset(path_WRF + "MET_0502/METCRO2D_110702.nc"); print('Done reading data_2_1')
data_3_1 = Dataset(path_WRF + "MET_0503/METCRO2D_110702.nc"); print('Done reading data_3_1')
data_4_1 = Dataset(path_WRF + "MET_0504/METCRO2D_110702.nc"); print('Done reading data_4_1')

column_names = ['ROW', 'COL']
hours = [str(i).zfill(2) for i in range(24)]
days_months = [f'{str(day).zfill(2)}{str(5).zfill(2)}' for day in range(1, 32)]
column_names.extend(f'{day}-{hour}h' for day in days_months for hour in hours)
df_WSPD, df_WDIR = pd.DataFrame(columns=column_names), pd.DataFrame(columns=column_names)
index = 0

mat.use("Agg")
for row in range(data_1_1['WDIR10'].shape[2]):
    for col in range(data_1_1['WDIR10'].shape[3]):
        data_Temp, data_Pres, data_PBL, data_Rain = np.array([]), np.array([]), np.array([]), np.array([])
        data_WSpeed, data_WDir, data_RH, data_PM25 = np.array([]), np.array([]), np.array([]), np.array([])
        hour, day, dem = 0, 1, 0

        ### FOR OTHER METEOROLOGICAL FACTORS
        data_WSpeed = np.append(data_WSpeed, data_1_1['WSPD10'][168-7:337-7, 0, row, col])
        data_WDir = np.append(data_WDir, data_1_1['WDIR10'][168-7:337-7, 0, row, col])

        data_WSpeed = np.append(data_WSpeed, data_2_1['WSPD10'][169-7:337-7, 0, row, col])
        data_WDir = np.append(data_WDir, data_2_1['WDIR10'][169-7:337-7, 0, row, col])

        data_WSpeed = np.append(data_WSpeed, data_3_1['WSPD10'][169-7:337-7, 0, row, col])
        data_WDir = np.append(data_WDir, data_3_1['WDIR10'][169-7:337-7, 0, row, col])

        data_WSpeed = np.append(data_WSpeed, data_4_1['WSPD10'][97-7:336-7, 0, row, col])
        data_WDir = np.append(data_WDir, data_4_1['WDIR10'][97-7:336-7, 0, row, col])
        # column_names = ['Year', 'Month', 'Day', 'Hour', 'WSPEED', 'WDIR']
        # column_names = ['Year', 'Month', 'Day', 'Hour', 'PM2.5']
        print(data_PM25.size, data_PBL.size, data_RH.size, data_Rain.size)
        df_WSPD.loc[index] = [row, col, data_WSpeed]
        df_WDIR.loc[index] = [row, col, data_WDir]
        index = index + 1
        print(row, col); print('-'*75)

# print(f'Dataframe has been saved to F:\Wind_Vector\Excel_Data\Meteorological_Data_{row}_{col}.xlsx')
df_WSPD.to_excel(f"F:\Wind_Vector\Excel_Data\WSPD.xlsx")
df_WDIR.to_excel(f"F:\Wind_Vector\Excel_Data\WDIR.xlsx")
print("SUCCESS")
