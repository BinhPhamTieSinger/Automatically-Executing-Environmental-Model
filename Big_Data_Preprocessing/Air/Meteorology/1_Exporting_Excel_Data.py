import matplotlib as mat
import pandas as pd
import numpy as np
import os
from netCDF4 import Dataset
from wrf import getvar, ALL_TIMES # type: ignore

def compute_cell_indices(rows, cols, multiplier):
    x = np.array([], dtype=int)
    for r, c in zip(rows, cols):
        x = np.append(x, r * multiplier + c)
    return x

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


def process_rain_and_rh(row, col, UTC, path_WRF, wrfs, month):
    data_Rain = np.array([])
    data_RH = np.array([])

    day_month = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # wrfs = [wrf_1, wrf_2, wrf_3, wrf_4]
    starting_times, ending_times = compute_time_period(wrfs, month, UTC)
    for i, wrf in enumerate(wrfs):
        starting_time = starting_times[i]
        ending_time = ending_times[i]
        wrfin = Dataset(path_WRF + wrf)
        rh2 = getvar(wrfin, "rh2", ALL_TIMES)
        data_Rain = np.append(data_Rain, wrfin["RAINC"][starting_time:ending_time+1, row+1, col+1])
        data_RH = np.append(data_RH, rh2[starting_time:ending_time+1, row+1, col+1])
        print(f"{wrf} {starting_time} {ending_time} {ending_time - starting_time + 1}")
    print(data_Rain.shape, data_RH.shape)
    
    return data_Rain, data_RH


def process_other_meteorological(row, col, UTC, datasets, wrfs, month):
    data_PBL = np.array([])
    data_Temp = np.array([])
    data_Pres = np.array([])
    data_WSpeed = np.array([])
    data_WDir = np.array([])

    day_month = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # wrfs = [wrf_1, wrf_2, wrf_3, wrf_4]
    starting_times, ending_times = compute_time_period(wrfs, month, UTC)
    for i, wrf in enumerate(wrfs):
        starting_time = starting_times[i]
        ending_time = ending_times[i]
        data_PBL = np.append(data_PBL, datasets[f'data_{i+1}_1']['PBL'][starting_time:ending_time+1, 0, row, col])
        data_Temp = np.append(data_Temp, datasets[f'data_{i+1}_1']['TEMP2'][starting_time:ending_time+1, 0, row, col])
        data_Pres = np.append(data_Pres, datasets[f'data_{i+1}_2']['PRES'][starting_time:ending_time+1, 0, row, col])
        data_WSpeed = np.append(data_WSpeed, datasets[f'data_{i+1}_1']['WSPD10'][starting_time:ending_time+1, 0, row, col])
        data_WDir = np.append(data_WDir, datasets[f'data_{i+1}_1']['WDIR10'][starting_time:ending_time+1, 0, row, col])
    
    return data_PBL, data_Temp, data_Pres, data_WSpeed, data_WDir


def process_cell_data(row, col, cell_index, data_PM25_df, day_month, month_number, UTC, path_WRF, datasets, year, wrfs):
    data_PM25 = data_PM25_df.iloc[cell_index][4:]
    print(f"PM2.5 has been prepared")
    print(data_PM25.shape)
    data_Rain, data_RH = process_rain_and_rh(row, col, UTC, path_WRF, wrfs, month_number)
    print(f"Rain and RH have been prepared")
    data_PBL, data_Temp, data_Pres, data_WSpeed, data_WDir = process_other_meteorological(row, col, UTC, datasets, wrfs, month_number)
    print(f"Other meteorological factors habe been prepared")
    hour = 0
    day = 1
    month = month_number
    column_names = ['Year', 'Month', 'Day', 'Hour', 'PM2.5', 'PBL', 'TEMP', 'PRES', 'WSPEED', 'WDIR', 'RH', 'RAIN']
    df = pd.DataFrame(columns=column_names)
    n_steps = data_PM25.size
    for i in range(n_steps):
        df.loc[i] = [
            year,
            month,
            day,
            hour,
            data_PM25[i],
            data_PBL[i],
            data_Temp[i],
            data_Pres[i] / 100,
            data_WSpeed[i],
            data_WDir[i],
            data_RH[i],
            data_Rain[i]
        ]
        hour += 1
        if hour == 24:
            hour = 0
            day += 1
            if day > day_month[month]:
                day = 1
                month += 1
    return df


def main():
    mat.use("Agg")
    month_number = 3; area = "Oregon"; year = 2023
    path_PM25 = f"G:/Big_Data_Preprocessing/Air/Concentration/Calibration/Result/2_Excel/"
    path_WRF = f"G:/Model_Execution/WRF_Libraries/Thang_{month_number}_{area}/"
    wrfs = []
    for file in os.listdir(path_WRF):
        wrfs.append(file)
    rows = np.array([63, 70, 70, 68, 69])
    cols = np.array([30, 30, 34, 30, 31])
    x = compute_cell_indices(rows, cols, multiplier=85)
    day_month = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
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
    for key in datasets: print(f"Done reading {key}")
    data_PM25_df = pd.read_excel(path_PM25 + "Cell.xlsx")
    print("READING SUCCESSFULLY: PM2.5 data")
    print("Done reading PM2.5 data\n")
    UTC = -7
    for idx in range(rows.size):
        row = rows[idx]
        col = cols[idx]
        cell_index = x[idx]
        print(f"Processing cell at row: {row}, col: {col}, cell_index: {cell_index}")
        df = process_cell_data(row, col, cell_index, data_PM25_df, day_month, month_number, UTC, path_WRF, datasets, year, wrfs)
        output_path = f"G:/Big_Data_Preprocessing/Air/Meteorology/Result/Data/Meteorological_Data_{row}_{col}.xlsx"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_excel(output_path, index=False)
        print(f"Dataframe has been saved to {output_path}")
        print(f"Completed processing for cell ({row}, {col})")
        print('-' * 75)


if __name__ == "__main__":
    main()