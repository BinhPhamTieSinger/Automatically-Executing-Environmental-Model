import netCDF4
from netCDF4 import Dataset
import os
import datetime as dt
import numpy as np
import arcpy
import xarray as xr
import pandas as pd


SUBSTANCE = "PM25"; month_number = 3; month_name = "March"; year = 2023
day_month = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Data path
BIG_DATA_PREPROCESSING_PATH = "G:/Big_Data_Preprocessing"
EXPORTATION_PATH = f"{BIG_DATA_PREPROCESSING_PATH}/Air/Concentration/Exportation"
CALIBRATION_PATH = f"{BIG_DATA_PREPROCESSING_PATH}/Air/Concentration/Calibration"
data_path = fr'{EXPORTATION_PATH}/Result/9_NetCDF_Dataset'
path_MCIP = f"G:/Model_Execution/MCIP_Libraries/MET_Oregon_{str(month_number).zfill(2)}01/"
path_PM25 = f"G:/Big_Data_Preprocessing/Air/Concentration/Calibration/Result/2_Excel/Cell.xlsx"
path_WDIR = "G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/WSPD.xlsx"
path_WSPD = "G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/WDIR.xlsx"

data = pd.read_excel(path_PM25)
data_WSPD = pd.read_excel(path_WSPD)
data_WDIR = pd.read_excel(path_WDIR)

# Create NetCDF File
output_nc = os.path.join(data_path, 'EMC_Report_26th.nc')
nc = netCDF4.Dataset(output_nc, 'w')

data_WRF = Dataset(path_MCIP + "METCRO2D_110702.nc")

nc.title = 'EMC-Report-26th'
nc.summary = ('PM25 + Wind Vector')
nc.keywords = 'PM25, Wind Vector, Time Step'
nc.license = ('Free License 4.0')
nc.references = ('No reference here!!!')
nc.history = '{0} creation of EMC Report 26th netcdf file.'.format(
              dt.datetime.now().strftime("%Y-%m-%d"))
print(data_WRF)
for variable in data_WRF.variables:
    print(variable)
xorig = data_WRF.getncattr('XORIG')
xcell = data_WRF.getncattr('XCELL')
yorig = data_WRF.getncattr('YORIG')
ycell = data_WRF.getncattr('YCELL')

x_dim_size = data_WRF.dimensions['COL'].size
y_dim_size = data_WRF.dimensions['ROW'].size

print(x_dim_size, y_dim_size)

x = xorig + xcell/2 + xcell * np.arange(x_dim_size)
y = yorig + ycell/2 + ycell * np.arange(y_dim_size)

print("x:", x)
print("y:", y)

# Create dimensions
nc.createDimension('COL', x_dim_size)
nc.createDimension('ROW', y_dim_size)
lon_dim = nc.createDimension('longitude', x_dim_size)
lat_dim = nc.createDimension('latitude', y_dim_size)
tim_dim = nc.createDimension('time', day_month[month_number]*24)

time_var = nc.createVariable('time', np.int32, ('time'))
time_var.standard_name = 'time'
time_var.calendar = 'gregorian'
time_var.time_step = 'Monthly'
time_var.units = f'Hour since {year}-{str(month_number).zfill(2)}-01 00:00:00'
time_var.axis = 'T'

# print(data_WRF['WSPD10'].grid_mapping)

lat_var = nc.createVariable('latitude', np.float64, ('time', 'ROW', 'COL'))
lat_var.units = 'degrees_north'
lat_var.standard_name = 'latitude'
lat_var.axis = 'Y'

lon_var = nc.createVariable('longitude', np.float64, ('time', 'ROW', 'COL'))
lon_var.units = 'degrees_east'
lon_var.standard_name = 'longitude'
lon_var.axis = 'X'

pm25_var = nc.createVariable('PM25', np.float64, ('time', 'ROW', 'COL'))
pm25_var.units = '\u03BCg/m\u00b3'
pm25_var.long_name = 'PM25'
pm25_var.short_name = 'PM25'

wdir_var = nc.createVariable('WDIR', np.float64, ('time', 'ROW', 'COL'))
wdir_var.units = '\u03BCg/m\u00b3'
wdir_var.long_name = 'WDIR'
wdir_var.short_name = 'WDIR'

wspd_var = nc.createVariable('WSPEED', np.float64, ('time', 'ROW', 'COL'))
wspd_var.units = '\u03BCg/m\u00b3'
wspd_var.long_name = 'WSPEED'
wspd_var.short_name = 'WSPEED'

month_norm = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
month_spec = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
date = np.array([])

for day in range(1, month_norm[month_number]+1):
    for hour in range(24):
        date_current = str(dt.datetime(year=year,month=month_number,day=1,hour=0))
        date = np.append(date, date_current)
time_var[:] = np.arange(0, month_norm[month_number]*24, 1)
for day in range(1, month_norm[month_number]+1):
    for hour in range(24):
        day_current = str(day).zfill(2)
        hour_current = str(hour).zfill(2)
        month_current = str(month_number).zfill(2)
        date_time = day_current+month_current+'-'+hour_current+'h'
        index_current = (day-1)*24+hour
        print(date_time, index_current)
        pm25_var[index_current, :, :] = data[date_time].values
        wdir_var[index_current, :, :] = data_WSPD[date_time].values
        wspd_var[index_current, :, :] = data_WDIR[date_time].values
        lat_var[index_current, :, :] = data_WSPD['LAT'].values
        lon_var[index_current, :, :] = data_WSPD['LON'].values

nc.close()