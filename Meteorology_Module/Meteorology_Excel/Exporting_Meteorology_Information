import matplotlib as mat
import pandas as pd
import numpy as np
# import geopandas as gpd
from netCDF4 import Dataset
from wrf import getvar, ALL_TIMES

path_CMAQ = "F:/CMAQ_Calibration/CSUM/"
path_RH = "F:/WRF_Libraries/Thang_5/"
path_PM25 = "F:/CMAQ_Calibration/RESULT/T5/"

data = pd.read_excel(path_PM25 + "Cell_PM25.xlsx")
print('Done reading data')

rows = np.array([35, 34, 30, 53, 37])
cols = np.array([32, 34, 63, 51, 33])
x = np.array([]).astype(int)
for index in range(rows.size):
    x = np.append(x, rows[index]*70 + cols[index]+1)

path_WRF = "F:/CMAQ_WRF_HaNoi/WRF/"
data_1_1 = Dataset(path_WRF + "MET_0501/METCRO2D_110702.nc"); print('Done reading data_1_1')
data_1_2 = Dataset(path_WRF + "MET_0501/METCRO3D_110702.nc"); print('Done reading data_1_2')
data_2_1 = Dataset(path_WRF + "MET_0502/METCRO2D_110702.nc"); print('Done reading data_2_1')
data_2_2 = Dataset(path_WRF + "MET_0502/METCRO3D_110702.nc"); print('Done reading data_2_2')
data_3_1 = Dataset(path_WRF + "MET_0503/METCRO2D_110702.nc"); print('Done reading data_3_1')
data_3_2 = Dataset(path_WRF + "MET_0503/METCRO3D_110702.nc"); print('Done reading data_3_2')
data_4_1 = Dataset(path_WRF + "MET_0504/METCRO2D_110702.nc"); print('Done reading data_4_1')
data_4_2 = Dataset(path_WRF + "MET_0504/METCRO3D_110702.nc"); print('Done reading data_4_2')

mat.use("Agg")
for index in range(rows.size):
    row = rows[index]; col = cols[index]
    data_Temp, data_Pres, data_PBL, data_Rain = np.array([]), np.array([]), np.array([]), np.array([])
    data_WSpeed, data_WDir, data_RH, data_PM25 = np.array([]), np.array([]), np.array([]), np.array([])
    hour, day, dem = 0, 1, 0
    ### FOR PM25
    data_PM25 = data.iloc[x[index]][4:]; print(data_PM25)

    ### FOR RH2 ADN RAINC
    wrfin_1 = Dataset(path_RH + "wrfout_d03_2023-04-24")
    data_Rain = np.append(data_Rain, wrfin_1["RAINC"][168-7:337-7, row+1, col+1])
    rh2 = getvar(wrfin_1, "rh2", ALL_TIMES)
    print(row+1, col+1, rh2.shape)
    data_RH = np.append(data_RH, rh2[168-7:337-7, row+1, col+1])
    
    wrfin_2 = Dataset(path_RH + "wrfout_d03_2023-05-01")
    data_Rain = np.append(data_Rain, wrfin_2["RAINC"][169-7:337-7, row+1, col+1])
    rh2 = getvar(wrfin_2, "rh2", ALL_TIMES)
    print(row+1, col+1, rh2.shape)
    data_RH = np.append(data_RH, rh2[169-7:337-7, row+1, col+1])
    
    wrfin_3 = Dataset(path_RH + "wrfout_d03_2023-05-08")
    data_Rain = np.append(data_Rain, wrfin_3["RAINC"][169-7:337-7, row+1, col+1])
    rh2 = getvar(wrfin_3, "rh2", ALL_TIMES)
    print(row+1, col+1, rh2.shape)
    data_RH = np.append(data_RH, rh2[169-7:337-7, row+1, col+1])
    
    wrfin_4 = Dataset(path_RH + "wrfout_d03_2023-05-18")
    data_Rain = np.append(data_Rain, wrfin_4["RAINC"][97-7:336-7, row+1, col+1])
    rh2 = getvar(wrfin_4, "rh2", ALL_TIMES)
    print(row+1, col+1, rh2.shape)
    data_RH = np.append(data_RH, rh2[97-7:336-7, row+1, col+1])


    ### FOR OTHER METEOROLOGICAL FACTORS
    data_PBL = np.append(data_PBL, data_1_1['PBL'][168-7:337-7, 0, row, col])
    data_Temp = np.append(data_Temp, data_1_1['TEMP2'][168-7:337-7, 0, row, col])
    data_Pres = np.append(data_Pres, data_1_2['PRES'][168-7:337-7, 0, row, col])
    data_WSpeed = np.append(data_WSpeed, data_1_1['WSPD10'][168-7:337-7, 0, row, col])
    data_WDir = np.append(data_WDir, data_1_1['WDIR10'][168-7:337-7, 0, row, col])

    data_PBL = np.append(data_PBL, data_2_1['PBL'][169-7:337-7, 0, row, col])
    data_Temp = np.append(data_Temp, data_2_1['TEMP2'][169-7:337-7, 0, row, col])
    data_Pres = np.append(data_Pres, data_2_2['PRES'][169-7:337-7, 0, row, col])
    data_WSpeed = np.append(data_WSpeed, data_2_1['WSPD10'][169-7:337-7, 0, row, col])
    data_WDir = np.append(data_WDir, data_2_1['WDIR10'][169-7:337-7, 0, row, col])

    data_PBL = np.append(data_PBL, data_3_1['PBL'][169-7:337-7, 0, row, col])
    data_Temp = np.append(data_Temp, data_3_1['TEMP2'][169-7:337-7, 0, row, col])
    data_Pres = np.append(data_Pres, data_3_2['PRES'][169-7:337-7, 0, row, col])
    data_WSpeed = np.append(data_WSpeed, data_3_1['WSPD10'][169-7:337-7, 0, row, col])
    data_WDir = np.append(data_WDir, data_3_1['WDIR10'][169-7:337-7, 0, row, col])

    data_PBL = np.append(data_PBL, data_4_1['PBL'][97-7:336-7, 0, row, col])
    data_Temp = np.append(data_Temp, data_4_1['TEMP2'][97-7:336-7, 0, row, col])
    data_Pres = np.append(data_Pres, data_4_2['PRES'][97-7:336-7, 0, row, col])
    data_WSpeed = np.append(data_WSpeed, data_4_1['WSPD10'][97-7:336-7, 0, row, col])
    data_WDir = np.append(data_WDir, data_4_1['WDIR10'][97-7:336-7, 0, row, col])
    column_names = ['Year', 'Month', 'Day', 'Hour', 'PM2.5', 'PBL', 'TEMP', 'PRES', 'WSPEED', 'WDIR', 'RH', 'RAIN']
    # column_names = ['Year', 'Month', 'Day', 'Hour', 'PM2.5']
    df = pd.DataFrame(columns = column_names)
    print(data_PM25.size, data_PBL.size, data_RH.size, data_Rain.size)
    for index in range(data_PM25.size):
        df.loc[index] = [
            2023, 5, day, hour,
            data_PM25[index],
            data_PBL[index],
            data_Temp[index],
            data_Pres[index]/100,
            data_WSpeed[index],
            data_WDir[index],
            data_RH[index],
            data_Rain[index],
        ]; hour = hour + 1
        if (hour == 24):
            hour = 0; day = day + 1
    df['Year'].astype(int); df['Month'].astype(int)
    df['Day'].astype(int); df['Hour'].astype(int)
    print(f'Dataframe has been saved to F:\Wind_Vector\Excel_Data\Meteorological_Data_{row}_{col}.xlsx')
    df.to_excel(f"F:\Wind_Vector\Excel_Data\Meteorological_Data_{row}_{col}.xlsx")
    print(row, col); print('-'*75)
        
