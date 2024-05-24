#########################
# 1. Converting File.py #
#########################


import xarray as xr
import rioxarray as rio
from rasterio.transform import from_origin
import rasterio

# Đường dẫn đến tệp NetCDF
path_CMAQ = "F:/CMAQ_Calibration/CSUM/"
path_WRF = "F:/CMAQ_WRF_HaNoi/WRF/MET_0501/"
path_Thucdo = "F:/CMAQ_Calibration/REAL_DATA/"

data_CMAQ_3104 = path_CMAQ + "csum_0501/PM0430.nc"
data_CMAQ_0105 = path_CMAQ + "csum_0501/PM0501.nc"
data_CMAQ_0205 = path_CMAQ + "csum_0501/PM0502.nc"
data_CMAQ_0305 = path_CMAQ + "csum_0501/PM0503.nc"
data_CMAQ_0405 = path_CMAQ + "csum_0501/PM0504.nc"
data_CMAQ_0505 = path_CMAQ + "csum_0501/PM0505.nc"
data_CMAQ_0605 = path_CMAQ + "csum_0501/PM0506.nc"
data_CMAQ_0705 = path_CMAQ + "csum_0502/PM0507.nc"
data_CMAQ_0805 = path_CMAQ + "csum_0502/PM0508.nc"
data_CMAQ_0905 = path_CMAQ + "csum_0502/PM0509.nc"
data_CMAQ_1005 = path_CMAQ + "csum_0502/PM0510.nc"
data_CMAQ_1105 = path_CMAQ + "csum_0502/PM0511.nc"
data_CMAQ_1205 = path_CMAQ + "csum_0502/PM0512.nc"
data_CMAQ_1305 = path_CMAQ + "csum_0502/PM0513.nc"
data_CMAQ_1405 = path_CMAQ + "csum_0503/PM0514.nc"
data_CMAQ_1505 = path_CMAQ + "csum_0503/PM0515.nc"
data_CMAQ_1605 = path_CMAQ + "csum_0503/PM0516.nc"
data_CMAQ_1705 = path_CMAQ + "csum_0503/PM0517.nc"
data_CMAQ_1805 = path_CMAQ + "csum_0503/PM0518.nc"
data_CMAQ_1905 = path_CMAQ + "csum_0503/PM0519.nc"
data_CMAQ_2005 = path_CMAQ + "csum_0503/PM0520.nc"
data_CMAQ_2105 = path_CMAQ + "csum_0504/PM0521.nc"
data_CMAQ_2205 = path_CMAQ + "csum_0504/PM0522.nc"
data_CMAQ_2305 = path_CMAQ + "csum_0504/PM0523.nc"
data_CMAQ_2405 = path_CMAQ + "csum_0504/PM0524.nc"
data_CMAQ_2505 = path_CMAQ + "csum_0504/PM0525.nc"
data_CMAQ_2605 = path_CMAQ + "csum_0504/PM0526.nc"
data_CMAQ_2705 = path_CMAQ + "csum_0504/PM0527.nc"
data_CMAQ_2805 = path_CMAQ + "csum_0504/PM0528.nc"
data_CMAQ_2905 = path_CMAQ + "csum_0504/PM0529.nc"
data_CMAQ_3005 = path_CMAQ + "csum_0504/PM0530.nc"
data_CMAQ_3105 = path_CMAQ + "csum_0504/PM0531.nc"
netcdf_files = [
    data_CMAQ_3104, data_CMAQ_0105, data_CMAQ_0205, data_CMAQ_0305, data_CMAQ_0405, 
    data_CMAQ_0505, data_CMAQ_0605, data_CMAQ_0705, data_CMAQ_0805, data_CMAQ_0905, 
    data_CMAQ_1005, data_CMAQ_1105, data_CMAQ_1205, data_CMAQ_1305, data_CMAQ_1405, 
    data_CMAQ_1505, data_CMAQ_1605, data_CMAQ_1705, data_CMAQ_1805, data_CMAQ_1905, 
    data_CMAQ_2005, data_CMAQ_2105, data_CMAQ_2205, data_CMAQ_2305, data_CMAQ_2405, 
    data_CMAQ_2505, data_CMAQ_2605, data_CMAQ_2705, data_CMAQ_2805, data_CMAQ_2905, 
    data_CMAQ_3005, data_CMAQ_3105
]

netcdf_files_name = [
    'data_CMAQ_3104', 'data_CMAQ_0105', 'data_CMAQ_0205', 'data_CMAQ_0305', 'data_CMAQ_0405', 
    'data_CMAQ_0505', 'data_CMAQ_0605', 'data_CMAQ_0705', 'data_CMAQ_0805', 'data_CMAQ_0905', 
    'data_CMAQ_1005', 'data_CMAQ_1105', 'data_CMAQ_1205', 'data_CMAQ_1305', 'data_CMAQ_1405', 
    'data_CMAQ_1505', 'data_CMAQ_1605', 'data_CMAQ_1705', 'data_CMAQ_1805', 'data_CMAQ_1905', 
    'data_CMAQ_2005', 'data_CMAQ_2105', 'data_CMAQ_2205', 'data_CMAQ_2305', 'data_CMAQ_2405', 
    'data_CMAQ_2505', 'data_CMAQ_2605', 'data_CMAQ_2705', 'data_CMAQ_2805', 'data_CMAQ_2905', 
    'data_CMAQ_3005', 'data_CMAQ_3105', 'data_CMAQ_0106'
]
data_WRF = xr.open_dataset(path_WRF + "GRIDCRO2D_110702.nc")
COOR_LAT = data_WRF['LAT']
COOR_LON = data_WRF['LON']
file_tiff = []

# Define the output directory
output_directory = "F:/CMAQ_Model/HaNoi_Project/Tiff/"
dem = 0
# Iterate over each NetCDF file
for netcdf_file in netcdf_files:
    # Open the NetCDF file
    ds = xr.open_dataset(netcdf_file)
    # Iterate over each TSTEP
    for i in range(len(ds['TSTEP'])):
        # Select PM25_TOT variable and set LAY = 0 for the current TSTEP
        PM25_TOT = ds['PM25_TOT'].sel(LAY=0, TSTEP=i)

        # Convert PM25_TOT to a DataFrame
        df = PM25_TOT.to_dataframe()

        # Add 'lon' and 'lat' columns
        # Assuming you have separate files for lon and lat
        lon_ds = xr.open_dataset(path_WRF + "GRIDCRO2D_110702.nc")
        lat_ds = xr.open_dataset(path_WRF + "GRIDCRO2D_110702.nc")
        lon_values = lon_ds["LON"].values.flatten()  # Flatten the array
        lat_values = lat_ds["LAT"].values.flatten()  # Flatten the array
        # Assuming lon and lat have the same dimensions as df, otherwise you need to align them
        # You may need to interpolate or reshape lon and lat values to match the dimensions of df
        lon_values = lon_values[:len(df)]  # Slice lon values to match the length of df
        lat_values = lat_values[:len(df)]  # Slice lat values to match the length of df
        df["lon"] = lon_values
        df["lat"] = lat_values

        # Convert DataFrame back to .nc file
        new_ds = df.to_xarray()

        lon = new_ds.variables['lon'][:]
        lat = new_ds.variables['lat'][:]
        lon_min, lon_max = lon.min(), lon.max()
        lat_min, lat_max = lat.min(), lat.max()
        pixel_width = (lon_max - lon_min) / PM25_TOT.shape[1]
        pixel_height = (lat_max - lat_min) / PM25_TOT.shape[0]

        # Construct output file name

        if (i < 15):
            tstep = i + 9  # Add 3 to TSTEP
            tstep_str = str(tstep % 24).zfill(2)
            print(tstep, tstep_str)
            if (netcdf_files_name[dem][10:14] == "3104"):
                continue
            output_filename = f'PM25_{netcdf_files_name[dem][10:14]}_{tstep_str}.tiff'  # Assuming file name format is data_CMAQ_0101.nc
            output_path = output_directory + output_filename
            file_tiff.append(f'PM25_{netcdf_files_name[dem][10:14]}_{tstep_str}.tiff')
        else:
            tstep = i - 15  # Add 3 to TSTEP
            tstep_str = str(tstep % 24).zfill(2)
            print(tstep, tstep_str)
            if (netcdf_files_name[dem+1][10:14] == "0106"):
                continue
            output_filename = f'PM25_{netcdf_files_name[dem+1][10:14]}_{tstep_str}.tiff'  # Assuming file name format is data_CMAQ_0101.nc
            output_path = output_directory + output_filename
            file_tiff.append(f'PM25_{netcdf_files_name[dem+1][10:14]}_{tstep_str}.tiff')
        print(i, output_path)
        transform = from_origin(lon_min, lat_max, pixel_width, pixel_height)
        tif_metadata = {
            'count': 1,
            'dtype': 'float32',
            'driver': 'GTiff',
            'height': PM25_TOT.shape[0],
            'width': PM25_TOT.shape[1],
            'crs': 'EPSG:4326',
            'transform': transform
        }
        # Write TIFF file
        with rasterio.open(output_path, 'w', **tif_metadata) as dst:
            dst.write(PM25_TOT, 1)
    dem = dem + 1
