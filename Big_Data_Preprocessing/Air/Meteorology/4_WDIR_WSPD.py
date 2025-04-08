import matplotlib as mat
import pandas as pd
import numpy as np
# import geopandas as gpd
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

def main():
    mat.use("Agg")
    month_number = 2; area = "Oregon"; year = 2023; UTC = -7
    day_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
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
    data_LON_LAT = Dataset(path_MCIP + f"MET_Oregon_{str(month_number).zfill(2)}01/GRIDCRO2D_110702.nc")
    for key in datasets:
        print(f"Done reading {key}")

    column_names = ['ROW', 'COL', 'LON', 'LAT']
    hours = [str(i).zfill(2) for i in range(24)]
    days_months = [f'{str(day).zfill(2)}{str(month_number).zfill(2)}' for day in range(1, day_month[month_number]+1)]
    column_names.extend(f'{day}-{hour}h' for day in days_months for hour in hours)
    df_WSPD, df_WDIR = pd.DataFrame(columns=column_names), pd.DataFrame(columns=column_names)
    index = 0

    starting_times, ending_times = compute_time_period(wrfs, month_number, UTC)
    for row in range(datasets['data_1_2']['PRES'].shape[2]):
        for col in range(datasets['data_1_2']['PRES'].shape[3]):
            data_WSpeed = np.array([row, col, data_LON_LAT['LON'][0, 0, row, col], data_LON_LAT['LAT'][0, 0, row, col]])
            data_WDir = np.array([row, col, data_LON_LAT['LON'][0, 0, row, col], data_LON_LAT['LAT'][0, 0, row, col]])
            for i, wrf in enumerate(wrfs):
                starting_time = starting_times[i]
                ending_time = ending_times[i]
                data_WSpeed = np.append(data_WSpeed, datasets[f'data_{i+1}_1']['WSPD10'][starting_time:ending_time+1, 0, row, col])
                data_WDir = np.append(data_WDir, datasets[f'data_{i+1}_1']['WDIR10'][starting_time:ending_time+1, 0, row, col])
                print(f"{wrf} {starting_time} {ending_time} {ending_time - starting_time + 1}")
            print(data_WSpeed.size, data_WDir.size, df_WSPD.columns.size)
            df_WSPD.loc[index] = data_WSpeed
            df_WDIR.loc[index] = data_WDir
            index = index + 1
            # print(data_Rain.shape, data_RH.shape, data_Pres.shape, data_WSpeed.shape, data_WDir.shape)
            print(row, col); print('-'*75)
    df_WSPD.to_excel(f"G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/WSPD.xlsx")
    df_WDIR.to_excel(f"G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/WDIR.xlsx")



if __name__ == "__main__":
    main()