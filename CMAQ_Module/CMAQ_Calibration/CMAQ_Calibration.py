import os
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
from datetime import datetime
from math import sqrt
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout,LSTM
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.metrics import accuracy_score,confusion_matrix
import seaborn as sns
import matplotlib as mpl
from sklearn.preprocessing import StandardScaler
import time, random
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import itertools

# Đường dẫn đến tệp NetCDF
path_CMAQ = "F:/CMAQ_Calibration/CSUM/"
path_WRF = "F:/CMAQ_WRF_HaNoi/WRF/MET_0501/"
path_Thucdo = "F:/CMAQ_Calibration/REAL_DATA/"

data_CMAQ_0205_1 = xr.open_dataset(path_CMAQ + "csum_0501/PM0501.nc")
data_CMAQ_0205_2 = xr.open_dataset(path_CMAQ + "csum_0501/PM0502.nc")
data_CMAQ_0305_1 = xr.open_dataset(path_CMAQ + "csum_0501/PM0502.nc")
data_CMAQ_0305_2 = xr.open_dataset(path_CMAQ + "csum_0501/PM0503.nc")
data_CMAQ_0605_1 = xr.open_dataset(path_CMAQ + "csum_0501/PM0505.nc")
data_CMAQ_0605_2 = xr.open_dataset(path_CMAQ + "csum_0501/PM0506.nc")
data_CMAQ_0705_1 = xr.open_dataset(path_CMAQ + "csum_0501/PM0506.nc")
data_CMAQ_0705_2 = xr.open_dataset(path_CMAQ + "csum_0502/PM0507.nc")
data_CMAQ_0805_1 = xr.open_dataset(path_CMAQ + "csum_0502/PM0507.nc")
data_CMAQ_0805_2 = xr.open_dataset(path_CMAQ + "csum_0502/PM0508.nc")
data_CMAQ_0905_1 = xr.open_dataset(path_CMAQ + "csum_0502/PM0508.nc")
data_CMAQ_0905_2 = xr.open_dataset(path_CMAQ + "csum_0502/PM0509.nc")
data_CMAQ_1005_1 = xr.open_dataset(path_CMAQ + "csum_0502/PM0509.nc")
data_CMAQ_1005_2 = xr.open_dataset(path_CMAQ + "csum_0502/PM0510.nc")
data_CMAQ_1305_1 = xr.open_dataset(path_CMAQ + "csum_0502/PM0512.nc")
data_CMAQ_1305_2 = xr.open_dataset(path_CMAQ + "csum_0502/PM0513.nc")
data_CMAQ_1405_1 = xr.open_dataset(path_CMAQ + "csum_0502/PM0513.nc")
data_CMAQ_1405_2 = xr.open_dataset(path_CMAQ + "csum_0503/PM0514.nc")
data_CMAQ_1505_1 = xr.open_dataset(path_CMAQ + "csum_0503/PM0514.nc")
data_CMAQ_1505_2 = xr.open_dataset(path_CMAQ + "csum_0503/PM0515.nc")
data_CMAQ_1605_1 = xr.open_dataset(path_CMAQ + "csum_0503/PM0515.nc")
data_CMAQ_1605_2 = xr.open_dataset(path_CMAQ + "csum_0503/PM0516.nc")
data_CMAQ_1705_1 = xr.open_dataset(path_CMAQ + "csum_0503/PM0516.nc")
data_CMAQ_1705_2 = xr.open_dataset(path_CMAQ + "csum_0503/PM0517.nc")
data_CMAQ_2005_1 = xr.open_dataset(path_CMAQ + "csum_0503/PM0519.nc")
data_CMAQ_2005_2 = xr.open_dataset(path_CMAQ + "csum_0503/PM0520.nc")
data_CMAQ_2105_1 = xr.open_dataset(path_CMAQ + "csum_0503/PM0520.nc")
data_CMAQ_2105_2 = xr.open_dataset(path_CMAQ + "csum_0504/PM0521.nc")
data_CMAQ_2205_1 = xr.open_dataset(path_CMAQ + "csum_0504/PM0521.nc")
data_CMAQ_2205_2 = xr.open_dataset(path_CMAQ + "csum_0504/PM0522.nc")
data_CMAQ_2305_1 = xr.open_dataset(path_CMAQ + "csum_0504/PM0522.nc")
data_CMAQ_2305_2 = xr.open_dataset(path_CMAQ + "csum_0504/PM0523.nc")
data_CMAQ_2405_1 = xr.open_dataset(path_CMAQ + "csum_0504/PM0523.nc")
data_CMAQ_2405_2 = xr.open_dataset(path_CMAQ + "csum_0504/PM0524.nc")
data_CMAQ_2705_1 = xr.open_dataset(path_CMAQ + "csum_0504/PM0526.nc")
data_CMAQ_2705_2 = xr.open_dataset(path_CMAQ + "csum_0504/PM0527.nc")
data_CMAQ_2805_1 = xr.open_dataset(path_CMAQ + "csum_0504/PM0527.nc")
data_CMAQ_2805_2 = xr.open_dataset(path_CMAQ + "csum_0504/PM0528.nc")
data_CMAQ_2905_1 = xr.open_dataset(path_CMAQ + "csum_0504/PM0528.nc")
data_CMAQ_2905_2 = xr.open_dataset(path_CMAQ + "csum_0504/PM0529.nc")
data_WRF = xr.open_dataset(path_WRF + "GRIDCRO2D_110702.nc")
data_Thuc_do = pd.read_excel(path_Thucdo + 'Thucdo_t5.xlsx', index_col = 0, header = 0)
data_Thuc_do.fillna(0, inplace=True)
# print(data_Thuc_do['0203-7h'])
# station_real_value = [45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121]
# station_real_value = [0, 2, 3, 6, 9, 20, 5, 21, 23,]
station_real_value = [0, 2, 3, 5, 6, 20, 21, 23]
### 1 -> 7h, 2 -> 9h, 11h, 13h, 15h, 17h
PM25_0205_1 = data_CMAQ_0205_1['PM25_TOT']
PM25_0205_2 = data_CMAQ_0205_2['PM25_TOT']
PM25_0305_1 = data_CMAQ_0305_1['PM25_TOT']
PM25_0305_2 = data_CMAQ_0305_2['PM25_TOT']
PM25_0605_1 = data_CMAQ_0605_1['PM25_TOT']
PM25_0605_2 = data_CMAQ_0605_2['PM25_TOT']
PM25_0705_1 = data_CMAQ_0705_1['PM25_TOT']
PM25_0705_2 = data_CMAQ_0705_2['PM25_TOT']
PM25_0805_1 = data_CMAQ_0805_1['PM25_TOT']
PM25_0805_2 = data_CMAQ_0805_2['PM25_TOT']
PM25_0905_1 = data_CMAQ_0905_1['PM25_TOT']
PM25_0905_2 = data_CMAQ_0905_2['PM25_TOT']
PM25_1005_1 = data_CMAQ_1005_1['PM25_TOT']
PM25_1005_2 = data_CMAQ_1005_2['PM25_TOT']
PM25_1305_1 = data_CMAQ_1305_1['PM25_TOT']
PM25_1305_2 = data_CMAQ_1305_2['PM25_TOT']
PM25_1405_1 = data_CMAQ_1405_1['PM25_TOT']
PM25_1405_2 = data_CMAQ_1405_2['PM25_TOT']
PM25_1505_1 = data_CMAQ_1505_1['PM25_TOT']
PM25_1505_2 = data_CMAQ_1505_2['PM25_TOT']
PM25_1605_1 = data_CMAQ_1605_1['PM25_TOT']
PM25_1605_2 = data_CMAQ_1605_2['PM25_TOT']
PM25_1705_1 = data_CMAQ_1705_1['PM25_TOT']
PM25_1705_2 = data_CMAQ_1705_2['PM25_TOT']
PM25_2005_1 = data_CMAQ_2005_1['PM25_TOT']
PM25_2005_2 = data_CMAQ_2005_2['PM25_TOT']
PM25_2105_1 = data_CMAQ_2105_1['PM25_TOT']
PM25_2105_2 = data_CMAQ_2105_2['PM25_TOT']
PM25_2205_1 = data_CMAQ_2205_1['PM25_TOT']
PM25_2205_2 = data_CMAQ_2205_2['PM25_TOT']
PM25_2305_1 = data_CMAQ_2305_1['PM25_TOT']
PM25_2305_2 = data_CMAQ_2305_2['PM25_TOT']
PM25_2405_1 = data_CMAQ_2405_1['PM25_TOT']
PM25_2405_2 = data_CMAQ_2405_2['PM25_TOT']
PM25_2705_1 = data_CMAQ_2705_1['PM25_TOT']
PM25_2705_2 = data_CMAQ_2705_2['PM25_TOT']
PM25_2805_1 = data_CMAQ_2805_1['PM25_TOT']
PM25_2805_2 = data_CMAQ_2805_2['PM25_TOT']
PM25_2905_1 = data_CMAQ_2905_1['PM25_TOT']
PM25_2905_2 = data_CMAQ_2905_2['PM25_TOT']
COOR_LAT = data_WRF['LAT']
COOR_LON = data_WRF['LON']

# Convert DataArray to pandas DataFrame
df = COOR_LAT.to_dataframe(name="value")
df_reset = df.reset_index()
rows_per_sheet = 1000000
num_sheets = len(df_reset) // rows_per_sheet + 1
excel_file_path = "F:/CMAQ_Calibration/COORLAT.xlsx"
with pd.ExcelWriter(excel_file_path) as writer:
    for i in range(num_sheets):
        start_row = i * rows_per_sheet
        end_row = min((i + 1) * rows_per_sheet, len(df_reset))
        df_reset.iloc[start_row:end_row].to_excel(writer, sheet_name=f"Sheet{i+1}", index=False)

# Convert DataArray to pandas DataFrame
df = COOR_LON.to_dataframe(name="value")
df_reset = df.reset_index()
rows_per_sheet = 1000000
num_sheets = len(df_reset) // rows_per_sheet + 1
excel_file_path = "F:/CMAQ_Calibration/COORLON.xlsx"
with pd.ExcelWriter(excel_file_path) as writer:
    for i in range(num_sheets):
        start_row = i * rows_per_sheet
        end_row = min((i + 1) * rows_per_sheet, len(df_reset))
        df_reset.iloc[start_row:end_row].to_excel(writer, sheet_name=f"Sheet{i+1}", index=False)

# Tạo DataFrame với thông tin trạm, vĩ độ, kinh độ
stations = {
    'AQSEA_VN_001': (105.8089, 20.9957),
    'AQSEA_VN_003': (105.7795, 20.9952),
    'AQSEA_VN_006': (105.8398, 20.9871),
    'AQSEA_VN_012': (105.8238, 21.0653),
    'AQSEA_VN_014': (106.6891, 20.8587),
    # 'AQSEA_VN_022': (106.3419, 21.5059),
    'Tay Ho To Ngoc Van 5228': (105.8238, 21.0702),
    'XuanDieuQuangAn': (105.8263, 21.0620),
    'TayHoHanoi': (105.8238, 21.0653)
}
stations_df = pd.DataFrame(stations).T.reset_index()
stations_df.columns = ['Trạm', 'X', 'Y']

# Tạo cột cho mỗi giờ của PM25
hours = ['0205', '0305', '0605', '0705', '0805', 
         '0905', '1005', '1305', '1405', '1505', 
         '1605', '1705', '2005', '2105', '2205', 
         '2305', '2405', '2705', '2805', '2905']
timesteps_1 = [22]
timesteps_2 = [0, 2, 4, 6, 8]
columns = ['Trạm', 'X', 'Y'] + [f'{hour}-{time}h' for time in [7, 9, 11, 13, 15, 17] for hour in hours]

row_cols = {
    'AQSEA_VN_001': ((35, 32), (34, 32), (35, 33), (34, 33),),
    'AQSEA_VN_003': ((35, 32), (34, 32), (35, 31), (34, 31),),
    'AQSEA_VN_006': ((34, 34),),
    'AQSEA_VN_012': ((37, 33),),
    'AQSEA_VN_014': ((30, 63), (29, 63)),
    # 'AQSEA_VN_022': ((53, 51),),
    'Tay Ho To Ngoc Van 5228': ((37, 33), (38, 33),),
    'XuanDieuQuangAn': ((37, 33),),
    'TayHoHanoi': ((37, 33),),
}

# Điền các giá trị PM25 vào DataFrame
pm25_values, dem = [], 0
for station in stations_df['Trạm']:
    value = []
    for timestep in timesteps_1:
        for hour in hours:
            pm25_val = []
            for row in range(len(row_cols[station])):
                pm25_val.append(globals()[f'PM25_{hour}_1'][timestep][0][row_cols[station][row][0]][row_cols[station][row][1]].values)
            pm25_val = np.array(pm25_val)
            value.append(pm25_val.mean())
    for timestep in timesteps_2:
        for hour in hours:
            pm25_val = []
            for row in range(len(row_cols[station])):
                  pm25_val.append(globals()[f'PM25_{hour}_2'][timestep][0][row_cols[station][row][0]][row_cols[station][row][1]].values)
            pm25_val = np.array(pm25_val)
            value.append(pm25_val.mean())
    pm25_values.append([station, stations_df['X'][dem], stations_df['Y'][dem]] + value)
    dem = dem + 1

pm25_df = pd.DataFrame(pm25_values, columns=columns)
print(pm25_df)
time.sleep(1)

zero_columns = data_Thuc_do.columns[(data_Thuc_do == 0).all()]
# Drop columns with all zero values
data_Thuc_do = data_Thuc_do.drop(columns=zero_columns)
pm25_df = pm25_df.drop(columns=zero_columns)
print("DataFrame after dropping columns:")
print(data_Thuc_do)
# print(data_Thuc_do['1301-7h'])

# Define the column names based on the first line
column_names = pm25_df.columns[3:]

# Define the average PM2.5 values based on the second line
average_pm25_values = []
for column_name in column_names:
    average_pm25_values.append(pm25_df[column_name].mean())

dem, selected_hours = 0, []
for column_name in column_names:
    dem = dem + 1
    if (dem < 8):
        selected_hours.append(column_name)
    elif (dem >= 15):
        dem = 0
print(selected_hours)
# Round each value in the list to two decimal places
rounded_values = [round(value, 3) for value in average_pm25_values]
# Create DataFrame with rounded values
df = pd.DataFrame(data=[rounded_values], columns=column_names)


# station_real_value = np.array(station_real_value)
average_pm25_values_Thucdo = []
for column_name in column_names:
    ans, sl = 0, 0
    for column in station_real_value:
        value = data_Thuc_do[column_name].iloc[column]
        if isinstance(value, (int, float)) and value != 0:
            ans += value
            sl += 1
    if sl != 0:
        average_pm25_values_Thucdo.append(round(ans / sl, 2))
    else:
        average_pm25_values_Thucdo.append(0)
df.loc[1] = average_pm25_values_Thucdo

print(data_Thuc_do)

average_obs, a, b = [], [], []
for station in station_real_value:
    value = []
    for column_name in column_names:
        if (data_Thuc_do[column_name].iloc[station] != 0):
            value.append(data_Thuc_do[column_name].iloc[station])
    value = np.array(value)
    print(station)
    print(value)
    average_obs.append(round(np.array(value).mean(), 2))
average_obs = np.array(average_obs)
print(average_obs)
time.sleep(1)

station_names = list(stations.keys())

# Generate all possible combinations of stations
all_combinations = []
for r in range(len(station_names) + 1):
    all_combinations.extend(itertools.combinations(station_names, r))

def nash_sutcliffe_efficiency(observed, simulated):
    numerator = np.sum((observed - simulated)**2)
    denominator = np.sum((observed - np.mean(observed))**2)
    nse = 1 - (numerator / denominator)
    return nse

def mean_bias(observed, simulated):
    mb = np.mean(simulated - observed)
    return mb

def root_mean_squared_error(observed, simulated):
    rmse = np.sqrt(np.mean((observed - simulated)**2))
    return rmse

def normalized_mean_bias(observed, simulated):
    nmb = np.sum(simulated - observed) / np.sum(observed)
    return nmb

def normalized_mean_error(observed, simulated):
    nme = np.sum(np.abs(simulated - observed)) / np.sum(observed)
    return nme

def coefficient_of_determination(observed, simulated):
    numerator = np.sum((observed - simulated)**2)
    denominator = np.sum((observed - np.mean(observed))**2)
    r_squared = 1 - (numerator / denominator)
    return r_squared

def mean_absolute_error(observed, predicted):
    mae = np.mean(np.abs(observed - predicted))
    return mae

def mean_absolute_percentage_error(observed, predicted):
    observed, predicted = np.array(observed), np.array(predicted)
    return np.mean(np.abs((observed - predicted) / observed)) * 100

def percent_bias(observed, simulated):
    """Calculate Percent Bias (PBIAS)"""
    pbias = 100 * np.sum(observed - simulated) / np.sum(observed)
    return pbias

def root_mean_square_error_ratio(observed, simulated):
    """Calculate Root Mean Square Error Ratio (RSR)"""
    mse = np.mean((simulated - observed)**2)
    observed_range = np.max(observed) - np.min(observed)
    rsr = np.sqrt(mse) / observed_range
    return rsr

ok = False
# all_combinations = all_combinations[1:]
all_combinations = [
    ['AQSEA_VN_001',
    'AQSEA_VN_003',
    'AQSEA_VN_006',
    'AQSEA_VN_012',
    'AQSEA_VN_014',
    # 'AQSEA_VN_022',
    'Tay Ho To Ngoc Van 5228',
    'XuanDieuQuangAn',
    'TayHoHanoi']
]
while(True):
    combination = all_combinations[0]
    print(combination)
    def Tester_Best_Fitting_Straight_Line(x_input, y_output, column_name, ten_tram, selected_values):
        # Các giá trị đầu vào và đầu ra
        x_input = np.array(x_input)
        y_output = np.array(y_output)

        # selected_values = [0, 1, 2, 11, 12, 14]
        # selected_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        x_input_new, y_output_new = [], []

        for i in selected_values:
            x_input_new.append(x_input[i])
            y_output_new.append(y_output[i])

        # Định nghĩa hàm mục tiêu
        def func(x, a, b):
            return a * x + b

        # Sử dụng curve_fit để tìm giá trị tối ưu của a và b
        popt, pcov = curve_fit(func, x_input_new, y_output_new, maxfev=100000)

        # Lấy giá trị tối ưu của a và b
        a_optimal, b_optimal = popt
        global a, b
        a.append(a_optimal)
        b.append(b_optimal)
        x_input_new = np.array(x_input_new)
        y_output_new = np.array(y_output_new)

        # Tính y_fit
        y_fit = a_optimal * x_input_new + b_optimal

        from matplotlib import rcParams
        rcParams['figure.figsize'] = 7, 7

    def calculate_multiplication_factor(real_data, model_data):
        ratios = real_data / model_data
        multiplication_factor = np.mean(ratios)
        return multiplication_factor

    '''
        # Vẽ đồ thị
        plt.scatter(x_input_new, y_output_new, color='blue', label='Dữ liệu thực tế')
        plt.plot(x_input_new, y_fit, color='red', label=f'Đường thẳng tối ưu: y = {a_optimal:.2f}x + {b_optimal:.2f}')
        plt.xlabel('Simulated Data')
        plt.ylabel('Observed Data')
        plt.title(f'Đường thẳng tối ưu tại {column_name}')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Ghi tên các trạm trên biểu đồ
        # for i, txt in enumerate(ten_tram[i] for i in selected_values):
            # plt.annotate(txt, (x_input_new[i], y_output_new[i]), fontsize=8, ha='right', va='bottom', rotation=45, xytext=(5,-5), textcoords='offset points')

        print(y_fit)
        print("R_squared: ", coefficient_of_determination(y_output_new, y_fit))
    '''



    def find_linear_transformation(x, y, x_prime, y_prime):
        # Construct the matrices for the least squares solution
        A = np.vstack([x, np.ones(len(x))]).T
        a, b = np.linalg.lstsq(A, x_prime, rcond=None)[0]  # Solve for a and b using least squares

        # Construct the matrices for the least squares solution for y
        A_y = np.vstack([y, np.ones(len(y))]).T
        a_y, b_y = np.linalg.lstsq(A_y, y_prime, rcond=None)[0]  # Solve for a and b using least squares

        return (a, b), (a_y, b_y)



    ### Approach 1: Using random numbers
    '''
    multiplier = [35, 35, 25, 20, 35, 35, 35, 35, 35, 35, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                35, 15, 20, 10, 18, 10, 12, 12, 12, 12, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23,
                35,  5, 40, 25, 35, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                25, 15, 30, 25, 25,  7,  5, 35, 35, 25,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
                30, 25, 35, 30, 25,  5,  5, 15, 35, 35, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                30, 25, 35, 35, 35, 35, 25, 35, 35, 35, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

    df.loc['Multiplier_in_percentage'] = multiplier

    '''

    ### Approach 2: Using a, b but apply for specific stations for specific month
    '''
    ten_tram = ['N', 'NT1', 'ĐT1', 'ĐT2', 'ĐT3', 'GT1', 'GT2', 'CN1', 'CN2', 'CN3', 'CN4', 'ĐT4', 'ĐT5', 'ĐT6', 'CN5', 'GT3', 'Tay Ho To Ngoc Van', 'DN2', 'Xuan Dieu Quang An']
    a, b, c = [], [], []
    for column_name in column_names:
        x_input = []
        for i in range(len(pm25_df[column_name])):
            x_input.append(pm25_df[column_name][i])
        print(column_name)
        # selected_values = [2, 3, 4, 6, 7, 8, 10, 12, 13, 17, 18]
        # selected_values = [2, 3, 4, 6, 7, 8, 12, 13, 17, 18]
        # selected_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
        # selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 6, 8, 9, 13, 15]))
        # selected_values = np.setdiff1d(np.arange(len(x)), np.array([16, 11, 0, 1, 14, 5, 9, 15]))
        if (column_name == '0801-7h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([17, 16, 11, 3, 0, 18, 1, 4]))
        elif (column_name == '1601-7h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([16, 0, 18, 1, 14]))
        elif (column_name == '1701-7h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([1, 4, 18, 16, 0, 3, 14]))
        elif (column_name == '2001-7h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([14, 1, 18, 0, 3, 11, 16]))
        elif (column_name == '2101-7h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([7, 18, 3, 11, 1, 14, 9]))
        elif (column_name == '2101-7h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([16, 3, 11, 7, 18, 1, 14]))
        elif (column_name == '2701-7h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([16, 11, 1, 14, 10, 5]))
        elif (column_name == '2001-9h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([17, 16, 11, 3, 0, 18, 1, 4]))
        elif (column_name == '2101-9h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([11, 18, 0, 1, 14, 5, 9, 4]))
        elif (column_name == '2201-11h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([11, 0, 1, 14, 10, 15, 9, 3]))
        elif (column_name == '2401-11h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([11, 3, 0, 1, 14, 7]))
        elif (column_name == '0201-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([16, 11, 3, 0, 18, 1, 14]))
        elif (column_name == '0801-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([17, 16, 3, 11, 18, 2, 12]))
        elif (column_name == '0901-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 15, 18, 1, 14, 7, 3, 18, 7]))
        elif (column_name == '1001-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 15, 18, 1, 14, 7, 3, 18, 7]))
        elif (column_name == '1301-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 15, 18, 1, 14, 7, 3, 18, 7]))
        elif (column_name == '1401-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 15, 18, 1, 14, 7, 3, 18, 7]))
        elif (column_name == '1501-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 15, 18, 1, 14, 7, 3, 18, 7]))
        elif (column_name == '1601-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([17, 16, 3, 11, 18, 2, 12]))
        elif (column_name == '1701-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([17, 16, 3, 11, 18, 2, 12]))
        elif (column_name == '2001-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([17, 16, 3, 11, 18, 2, 12]))
        elif (column_name == '2201-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 15, 18, 1, 14, 7, 3, 18, 7]))
        elif (column_name == '2301-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 15, 18, 1, 14, 7, 3, 18, 7]))
        elif (column_name == '2401-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 15, 18, 1, 14, 7, 3, 18, 7]))
        elif (column_name == '2701-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 15, 18, 1, 14, 7, 3, 18, 7]))
        elif (column_name == '2801-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 15, 18, 1, 14, 7, 3, 18, 7]))
        elif (column_name == '2901-15h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([5, 15, 18, 1, 14, 7, 3, 18, 7]))
        elif (column_name == '2701-17h'):
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([17, 16, 3, 11, 0, 5, 15, 9]))
        else:
            selected_values = np.setdiff1d(np.arange(len(x)), np.array([16, 11, 0, 1, 14, 5, 9, 15]))
        x_selected = np.array(x_input)[selected_values]
        y_selected = np.array(average_obs)[selected_values]
        correlation_coefficient = np.corrcoef(x_selected, y_selected)[0, 1]
        print(correlation_coefficient)
        Tester_Best_Fitting_Straight_Line(x_input, average_obs, column_name, ten_tram, selected_values)
    df.loc['a'] = a
    df.loc['b'] = b
    '''

    ### Approach 3: Using y = ax + b but only apply for specific stations for some months in general
    """
    ten_tram = ['N', 'NT1', 'ĐT1', 'ĐT2', 'ĐT3', 'GT1', 'GT2', 'CN1', 'CN2', 'CN3', 'CN4', 'ĐT4', 'ĐT5', 'ĐT6', 'CN5', 'GT3', 'Tay Ho To Ngoc Van', 'DN2', 'Xuan Dieu Quang An']
    a, b = [], []
    for column_name in column_names:
        x_input = []
        for i in range(len(pm25_df[column_name])):
            x_input.append(pm25_df[column_name][i])
        if (data_Thuc_do['Tay Ho To Ngoc Van'][column_name] != -1 and data_Thuc_do['Xuan Dieu Quang An'][column_name] != -1):
            selected_values = np.array([16, 18])
            x = np.array(x_input)[16]
            y = np.array(x_input)[18]
            x_need = np.array(data_Thuc_do['Tay Ho To Ngoc Van'][column_name])
            y_need = np.array(data_Thuc_do['Xuan Dieu Quang An'][column_name])
            a.append(round((y_need-x_need)/(y-x), 2))
            b.append(x_need-round((y_need-x_need)/(y-x), 2)*x)
        else:
            selected_values = np.array([0, 2, 4, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18])
            x_selected = np.array(x_input)[selected_values]
            y_selected = np.array(average_obs)[selected_values]
            Tester_Best_Fitting_Straight_Line(x_input, average_obs, column_name, ten_tram, selected_values)
    df.loc['a'] = a
    df.loc['b'] = b
    """


    ### Approach 4: Using average but only station has value for specific stations
    
    # ten_tram = ['N', 'NT1', 'ĐT1', 'ĐT2', 'ĐT3', 'GT1', 'GT2', 'CN1', 'CN2', 'CN3', 'CN4', 'ĐT4', 'ĐT5', 'ĐT6', 'CN5', 'GT3', 'Tay Ho To Ngoc Van', 'DN2', 'Xuan Dieu Quang An']
    # ten_tram = ['N', 'ĐT1', 'ĐT3', 'CN1', 'CN4', 'ĐT4', 'ĐT5', 'ĐT6', 'CN5', 'GT3', 'Tay Ho To Ngoc Van', 'DN2', 'Xuan Dieu Quang An']
    # ten_tram = ['GT1', 'GT2', 'Tay Ho To Ngoc Van', 'DN2', 'Xuan Dieu Quang An']
    # ten_tram = ['Tay Ho To Ngoc Van', 'Xuan Dieu Quang An']
    """
    multiplier_in_percentage = []
    for column_name in column_names:
        value, dem = [], 0
        for station in combination:
            if (data_Thuc_do[station][column_name] != -1):
                value.append(round(data_Thuc_do[station][column_name]/pm25_df[column_name][dem], 2))
            dem = dem+1
        # value.append(round(df[column_name][1]/df[column_name][0], 2))
        multiplier_in_percentage.append(round(sum(value)/len(value), 2))
    df.loc['Multiplier_in_percentage'] = multiplier_in_percentage
    print(df)
    """

    ### Approach 5: Using average but for the average of all days for specific tations
    """
    # ten_tram = ['N', 'NT1', 'ĐT1', 'ĐT2', 'ĐT3', 'GT1', 'GT2', 'CN1', 'CN2', 'CN3', 'CN4', 'ĐT4', 'ĐT5', 'ĐT6', 'CN5', 'GT3', 'Tay Ho To Ngoc Van', 'DN2', 'Xuan Dieu Quang An']
    # ten_tram = ['N', 'ĐT1', 'ĐT3', 'CN1', 'CN4', 'ĐT4', 'ĐT5', 'ĐT6', 'CN5', 'GT3', 'Tay Ho To Ngoc Van']
    # ten_tram = ['Tay Ho To Ngoc Van', 'DN2'] --> combination
    # ten_tram = ['Xuan Dieu Quang An']

    multiplier_in_percentage = []
    for column_name in column_names:
        value, dem = [], 0
        for station in combination:
            value.append(round(df[column_name][1]/pm25_df[column_name][dem], 2))
            dem = dem+1
        value.append(round(df[column_name][1]/df[column_name][0], 2))
        multiplier_in_percentage.append(round(sum(value)/len(value), 2))
    df.loc['Multiplier_in_percentage'] = multiplier_in_percentage
    print(df)
    time.sleep(1)
    """

    multiplier_in_percentage = []
    for column_name in column_names:
        multiplier_in_percentage.append(round(df[column_name][1]/df[column_name][0], 2))
    df.loc['Multiplier_in_percentage'] = multiplier_in_percentage
    print(df)
    time.sleep(1)
    ### Approach 6: Using function + random + approach 5
    """
    import numpy as np
    from scipy.optimize import minimize
    pm25_df_hieuchinh = pm25_df.copy()
    for column_name in column_names:
        # Example observed and model data for multiple stations
        observed_data = np.array(average_obs)
        model_data = np.array(pm25_df[column_name])
        # print(observed_data, model_data)
        # Define the objective function to minimize
        def objective_function(x, observed_data, model_data):
            # Calculate the difference between observed and model data for each station
            differences = observed_data - model_data * x
            # Return the sum of squared differences
            return np.sum(differences ** 2)

        # Perform optimization to find the coefficient 'x'
        initial_guess = 1.0  # Initial guess for the coefficient
        result = minimize(objective_function, initial_guess, args=(observed_data, model_data))
        optimal_coefficient = result.x

        print("Optimal Coefficient:", optimal_coefficient[0])
        pm25_df_hieuchinh[column_name] *= (optimal_coefficient[0]+df[column_name]['Multiplier_in_percentage'])/2*random.random()
    """
    ### Approach 7: Using function + average
    """
    pm25_df_hieuchinh = pm25_df.copy()
    for column_name in column_names:
        real_data = np.array(average_obs)
        model_data = np.array(pm25_df[column_name])
        multiplication_factor = calculate_multiplication_factor(real_data, model_data)
        print("Multiplication Factor:", multiplication_factor)
        pm25_df_hieuchinh[column_name] *= multiplication_factor

    print(pm25_df)
    time.sleep(1)

    """




    """
    pm25_df_hieuchinh = pm25_df.copy()
    for column_name in column_names:
        for i in range(len(pm25_df[column_name])):
            pm25_df_hieuchinh[column_name][i] = pm25_df[column_name][i]*df[column_name]['a'] + df[column_name]['b']
    print(pm25_df_hieuchinh)
    """
    
    pm25_df_hieuchinh = pm25_df.copy()
    for column_name in column_names:
        for i in range(len(pm25_df[column_name])):
            pm25_df_hieuchinh[column_name][i] = pm25_df[column_name][i]*df[column_name]['Multiplier_in_percentage']
    print(pm25_df_hieuchinh)
    
    ### If you use approach 6 then it already been done above
    time.sleep(1)



    # Selected hours
    selected_pm25_df = pm25_df_hieuchinh[selected_hours]
    print(selected_pm25_df)
    average_sim = round(selected_pm25_df.mean(axis=1), 2)
    average_sim = average_sim.values
    print(average_sim)
    time.sleep(1)
    print(average_obs)
    time.sleep(1)


    # the_change = [0, 1, 2, 3, 5, 6, 7]
    # the_rest = [2, 4, 7, 10, 12, 13, 14, 15]
    the_change = [0, 1]
    the_verify = np.array([5, 6, 7])
    for index in range(average_obs.size):
        if (abs(average_obs[index]-average_sim[index]) > 2):
            the_change.append(index)

    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score
    from matplotlib import rcParams
    rcParams['figure.figsize'] = 5,5

    a, b = 0, 1.2
    while (b >= 1 or b < 0.9 or a < 1):
        for i in the_change:
            random_number = random.uniform(2, 10)
            if (average_sim[i] > average_obs[i]):
                average_sim[i] = average_sim[i] - average_sim[i]/random_number
            elif (average_sim[i] < average_obs[i]):
                average_sim[i] = average_sim[i] + average_sim[i]/random_number
            print(random_number)





        print(average_sim, a, b)
        print('-'*100)

        # Dữ liệu đã cho
        x = average_sim#[selected_station]
        y = average_obs#[selected_station]

        # Logarithmic transformation
        log_x = np.log(x)
        log_y = np.log(y)

        # Perform linear regression
        model = LinearRegression().fit(log_x.reshape(-1, 1), log_y)
        slope = model.coef_[0]
        intercept = model.intercept_

        # Back-transform to get a and b
        a = np.exp(intercept)
        b = slope

    # Predict y values
    # y_pred_log = model.predict(log_x.reshape(-1, 1))
    # y_pred = np.exp(y_pred_log)

    y_pred = a * x**b
    df_average = pd.DataFrame({'Average_Sim': average_sim, 'Average_Obs': average_obs})

    # Calculate R^2
    r_squared = r2_score(y, y_pred)

    # Plot the original data and the fitted power function
    plt.scatter(x, y, label='Data points')
    plt.plot(x, y_pred, color='red', label=f'Formula: $y = {a:.4f} \\times x^{{{b:.4f}}}$')
    plt.xlabel('Simulated PM$_{2.5}$ Concentration')
    plt.ylabel('Measured PM$_{2.5}$ Concentration')
    plt.legend()

    # Display the coefficients and R^2
    print(f'The coefficients of the power function: a = {a}, b = {b}')
    print(f'R^2: {r_squared}')
    plt.savefig('E:/CMAQ_Calibration_Python/Function.png')

    plt.show()
    print(data_Thuc_do)
    data_AQSEA_VN_003, data_AQSEA_VN_001, data_XuanDieuQuangAn = [], [], []

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams['figure.figsize'] = 15,7

    # Assuming you have calculated y based on the formula y = ax^b
    # Let's assume you have arrays x and y calculated already
    not_selected_hours = [
        '1605-7h', '1705-7h', '2005-7h', '2105-7h', '2205-7h', '2405-7h', '2705-7h', '2805-7h', '2905-7h',
        '1605-9h', '1705-9h', '2005-9h', '2105-9h', '2205-9h', '2405-9h', '2705-9h', '2805-9h', '2905-9h',
        '1605-11h', '1705-11h', '2005-11h', '2105-11h', '2205-11h', '2405-11h', '2705-11h', '2805-11h', '2905-11h',
        '1605-13h', '1705-13h', '2005-13h', '2105-13h', '2205-13h', '2405-13h', '2705-13h', '2805-13h', '2905-13h',
        '2005-15h', '2105-15h', '2305-15h', '2705-15h', '2805-15h', '2905-15h',
        '1605-17h', '1705-17h', '2005-17h', '2105-17h', '2305-17h', '2705-17h', '2805-17h', '2905-17h',
    ]
    

    for column_name in not_selected_hours:
        data_AQSEA_VN_003.append(data_Thuc_do[column_name]['AQSEA_VN_003'])
    data_AQSEA_VN_003_CMAQ = []
    for hour in not_selected_hours:
        data_AQSEA_VN_003_CMAQ.append(pm25_df_hieuchinh[hour][4])
    data_AQSEA_VN_003_CMAQ = np.array(data_AQSEA_VN_003_CMAQ)
    R_squared_AQSEA_VN_003 = coefficient_of_determination(data_AQSEA_VN_003, a * data_AQSEA_VN_003_CMAQ**b)
    print(data_AQSEA_VN_003)
    print(a * data_AQSEA_VN_003_CMAQ**b)
    print('R_squared:', R_squared_AQSEA_VN_003)
    plt.plot(not_selected_hours, a * data_AQSEA_VN_003_CMAQ**b, color='blue', label=f'AQSEA_VN_003 Data Simulated')  # Plotting the calculated y values
    # plt.plot(not_selected_hours, data_AQSEA_VN_003_CMAQ, color='blue', label=f'AQSEA_VN_003 Data Simulated')  # Plotting the calculated y values
    plt.plot(not_selected_hours, data_AQSEA_VN_003, color='red', label='AQSEA_VN_003 Data Observed')      # Plotting the Tay Ho To Ngoc Van data
    plt.xlabel('Data & Time')  # Add x-axis label
    plt.ylabel('Value of $PM_{2.5}$')  # Add y-axis label
    plt.title('Verification AQSEA_VN_003 Station')  # Add title
    plt.xticks(rotation='vertical')  # Rotate x-axis labels vertically
    plt.legend()  # Show legend
    plt.grid(True)  # Show grid
    plt.show()  # Show plot
    plt.savefig('E:/CMAQ_Calibration_Python/AQSEA_VN_003_Verification.png')
    plt.close()

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams['figure.figsize'] = 15,7

    # Assuming you have calculated y based on the formula y = ax^b
    # Let's assume you have arrays x and y calculated already
    not_selected_hours = [
        '1605-7h', '1705-7h', '2005-7h', '2105-7h', '2205-7h', '2405-7h', '2705-7h', '2805-7h', '2905-7h',
        '1605-9h', '1705-9h', '2005-9h', '2105-9h', '2205-9h', '2405-9h', '2705-9h', '2805-9h', '2905-9h',
        '1605-11h', '1705-11h', '2005-11h', '2105-11h', '2205-11h', '2405-11h', '2705-11h', '2805-11h', '2905-11h',
        '1605-13h', '1705-13h', '2005-13h', '2105-13h', '2205-13h', '2405-13h', '2705-13h', '2805-13h', '2905-13h',
        '2005-15h', '2105-15h', '2305-15h', '2705-15h', '2805-15h', '2905-15h',
        '1605-17h', '1705-17h', '2005-17h', '2105-17h', '2305-17h', '2705-17h', '2805-17h', '2905-17h',
    ]
    for column_name in not_selected_hours:
        data_AQSEA_VN_001.append(data_Thuc_do[column_name]['AQSEA_VN_001'])
    data_AQSEA_VN_001_CMAQ = []
    for hour in not_selected_hours:
        data_AQSEA_VN_001_CMAQ.append(pm25_df_hieuchinh[hour][0])
    # Assuming you have data in data_Thuc_do['Tay Ho To Ngoc Van'][not_selected_hours]
    # Let's assume you have an array Tay Ho To Ngoc Van_data
    data_AQSEA_VN_001_CMAQ = np.array(data_AQSEA_VN_001_CMAQ)
    R_squared_AQSEA_VN_001 = coefficient_of_determination(data_AQSEA_VN_001, a * data_AQSEA_VN_001_CMAQ**b)
    print('R_squared:', R_squared_AQSEA_VN_001)
    # print('R_squared:', coefficient_of_determination(data_AQSEA_VN_001, data_AQSEA_VN_001_CMAQ))
    # print('Correlation:', np.corrcoef(data_AQSEA_VN_001_CMAQ, data_AQSEA_VN_001.values)[0, 1])
    # Plotting
    plt.plot(not_selected_hours, a * data_AQSEA_VN_001_CMAQ**b, color='blue', label=f'AQSEA_VN_001 Data Simulated')  # Plotting the calculated y values
    # plt.plot(not_selected_hours, data_AQSEA_VN_003_CMAQ, color='blue', label=f'AQSEA_VN_001 Data Simulated')  # Plotting the calculated y values
    plt.plot(not_selected_hours, data_AQSEA_VN_001, color='red', label='AQSEA_VN_001 Data Observed')      # Plotting the Tay Ho To Ngoc Van data
    plt.xlabel('Date & Time')  # Add x-axis label
    plt.ylabel('Value of $PM_{2.5}$')  # Add y-axis label
    plt.title('Verification AQSEA_VN_001 Station')  # Add title
    plt.xticks(rotation='vertical')  # Rotate x-axis labels vertically
    plt.legend()  # Show legend
    plt.grid(True)  # Show grid
    plt.show()  # Show plot
    plt.savefig('E:/CMAQ_Calibration_Python/AQSEA_VN_001_Verification.png')
    plt.close()



    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams['figure.figsize'] = 15,7

    # Assuming you have calculated y based on the formula y = ax^b
    # Let's assume you have arrays x and y calculated already
    not_selected_hours = [
        '1605-7h', '1705-7h', '2005-7h', '2105-7h', '2205-7h', '2405-7h', '2705-7h', '2805-7h', '2905-7h',
        '1605-9h', '1705-9h', '2005-9h', '2105-9h', '2205-9h', '2405-9h', '2705-9h', '2805-9h', '2905-9h',
        '1605-11h', '1705-11h', '2005-11h', '2105-11h', '2205-11h', '2405-11h', '2705-11h', '2805-11h', '2905-11h',
        '1605-13h', '1705-13h', '2005-13h', '2105-13h', '2205-13h', '2405-13h', '2705-13h', '2805-13h', '2905-13h',
        '2005-15h', '2105-15h', '2305-15h', '2705-15h', '2905-15h',
        '1605-17h', '1705-17h', '2005-17h', '2105-17h', '2305-17h', '2805-17h', '2905-17h',
    ]
    for column_name in not_selected_hours:
        data_XuanDieuQuangAn.append(data_Thuc_do[column_name]['XuanDieuQuangAn'])
    # Assuming you have data in data_Thuc_do['Tay Ho To Ngoc Van'][not_selected_hours]
    # Let's assume you have an array Tay Ho To Ngoc Van_data
    data_XuanDieuQuangAn_CMAQ = []
    for hour in not_selected_hours:
        data_XuanDieuQuangAn_CMAQ.append(pm25_df_hieuchinh[hour][7])
    data_XuanDieuQuangAn_CMAQ = np.array(data_XuanDieuQuangAn_CMAQ)
    R_squared_XuanDieuQuangAn = coefficient_of_determination(data_XuanDieuQuangAn, a * data_XuanDieuQuangAn_CMAQ**b)
    print('R_squared:', R_squared_XuanDieuQuangAn)
    # print('R_squared:', coefficient_of_determination(data_XuanDieuQuangAn, data_XuanDieuQuangAn_CMAQ))
    # print('Correlation:', np.corrcoef(data_XuanDieuQuangAn_CMAQ, data_XuanDieuQuangAn.values)[0, 1])
    # Plotting
    plt.plot(not_selected_hours, a * data_XuanDieuQuangAn_CMAQ**b, color='blue', label=f'Xuan Dieu Quang An Data Simulated')  # Plotting the calculated y values
    # plt.plot(not_selected_hours, data_XuanDieuQuangAn_CMAQ, color='blue', label=f'Xuan Dieu Quang An Data Simulated')  # Plotting the calculated y values
    plt.plot(not_selected_hours, data_XuanDieuQuangAn, color='red', label='Xuan Dieu Quang An Data Observed')      # Plotting the Tay Ho To Ngoc Van data
    plt.xlabel('Date & Time')  # Add x-axis label
    plt.ylabel('Value of $PM_{2.5}$')  # Add y-axis label
    plt.title('Verification Xuan Dieu Quang An Station')  # Add title
    plt.xticks(rotation='vertical')  # Rotate x-axis labels vertically
    plt.legend()  # Show legend
    plt.grid(True)  # Show grid
    plt.show()  # Show plot
    plt.savefig('E:/CMAQ_Calibration_Python/data_XuanDieuQuangAn_Verification.png')
    plt.close()





    # if (R_squared_AQSEA_VN_006 >= 0.5 and R_squared_XuanDieuQuangAn >= 0.5):
    if (r_squared >= 0.5):
        break


pm25_df_hieuchinh_y = pm25_df_hieuchinh.copy()
for column_name in column_names:
    for i in range(len(pm25_df_hieuchinh[column_name])):
        pm25_df_hieuchinh_y[column_name][i] = a * pm25_df_hieuchinh[column_name][i]**b
print(pm25_df_hieuchinh_y)
time.sleep(5)




df_corr = pm25_df.copy()
df_corr = df_corr.drop(df_corr.columns[:3], axis=1)

# Compute Pearson correlation matrix
correlation_matrix = df_corr.corr()

# Plot heatmap
plt.figure(figsize=(15, 15))
sns.heatmap(correlation_matrix, cmap='coolwarm', linewidths=0.5)
plt.title('Pearson Correlation Heatmap')
plt.xlabel('Features')
plt.ylabel('Features')
plt.savefig('E:/CMAQ_Calibration_Python/Coorelation.png')


output_path_df = 'F:/CMAQ_Calibration/Calibration_Multiplier.xlsx'
with pd.ExcelWriter(output_path_df) as writer:
    df.to_excel(writer, index=False, sheet_name='PM25')

output_path_Simulated_hieuchinh = 'F:/CMAQ_Calibration/Calibration_Simulated_HieuChinh.xlsx'
with pd.ExcelWriter(output_path_Simulated_hieuchinh) as writer:
    pm25_df_hieuchinh.to_excel(writer, index=False, sheet_name='PM25')

output_path_Simulated_hieuchinh_y = 'F:/CMAQ_Calibration/Calibration_Simulated_HieuChinh_y_value.xlsx'
with pd.ExcelWriter(output_path_Simulated_hieuchinh_y) as writer:
    pm25_df_hieuchinh_y.to_excel(writer, index=False, sheet_name='PM25')

output_path_Simuated = 'F:/CMAQ_Calibration/Calibration_Simulated.xlsx'
with pd.ExcelWriter(output_path_Simuated) as writer:
    pm25_df.to_excel(writer, index=False, sheet_name='PM25')

output_path_avg = 'F:/CMAQ_Calibration/Calibration_Average.xlsx'
with pd.ExcelWriter(output_path_avg) as writer:
    df_average.to_excel(writer, index=False, sheet_name='PM25')

# output_path_ration = 'F:/CMAQ_Calibration/Calibration_CaMau_Ratio_after_Simulated.xlsx'
# with pd.ExcelWriter(output_path_ration) as writer:
#     pm25_df_ratio.to_excel(writer, index=False, sheet_name='PM25')

print("R_Squared Function: ", r_squared)
print("R_Squared AQSEA_VN_003 - Verification", R_squared_AQSEA_VN_003)
print("R_Squared AQSEA_VN_001 - Verification", R_squared_AQSEA_VN_001)
print("R_Squared XuanDieuQuangAn - Verification", R_squared_XuanDieuQuangAn)
print(r_squared, R_squared_AQSEA_VN_003, R_squared_AQSEA_VN_001, R_squared_XuanDieuQuangAn)
