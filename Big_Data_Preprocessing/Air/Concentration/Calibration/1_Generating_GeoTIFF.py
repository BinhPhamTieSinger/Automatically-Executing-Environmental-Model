import os
import xarray as xr
import rioxarray as rio  # For compatibility if needed
import numpy as np
from rasterio.transform import from_origin
import rasterio

def generate_netcdf_files(month, path_CMAQ, area):
    base_dir = f"{path_CMAQ}/CSUM_{area}_{month}/"
    start_file = ""
    files_list = []
    name_tags = []
    for file in os.listdir(base_dir):
        if file[2:4] == month:
            files_list.append(os.path.join(base_dir, file))
            name_tags.append(f"data_CMAQ_{file[4:6]}{file[2:4]}")
        else:
            start_file = os.path.join(base_dir, file)
    # Append the start file at the end and pad name_tags with 'X'
    return files_list + [start_file], ['X'] + name_tags + ['X']

def compute_tstep(i, tags, dem, offset):
    if i < offset:
        return i + 24-offset, tags[dem]
    else:
        return i - offset, tags[dem + 1]

def write_tiff(PM25, output_path, lon_min, lat_max, pixel_width, pixel_height):
    transform = from_origin(lon_min, lat_max, pixel_width, pixel_height)
    tif_metadata = {
        'count': 1,
        'dtype': 'float32',
        'driver': 'GTiff',
        'height': PM25.shape[0],
        'width': PM25.shape[1],
        'crs': 'EPSG:4326',
        'transform': transform
    }
    with rasterio.open(output_path, 'w', **tif_metadata) as dst:
        dst.write(PM25, 1)
    print(f"Written: {output_path}")

def process_netcdf(netcdf_file, tags, dem, path_MCIP, output_directory, offset):
    ds = xr.open_dataset(netcdf_file)
    wrf_path = os.path.join(path_MCIP, "GRIDCRO2D_110702.nc")
    wrf_ds = xr.open_dataset(wrf_path)
    lon_values = wrf_ds["LON"].values.flatten()
    lat_values = wrf_ds["LAT"].values.flatten()
    
    for i in range(len(ds['TSTEP'])):
        PM25 = ds['PM25_TOT'].sel(LAY=0, TSTEP=i)
        df = PM25.to_dataframe().reset_index()
        n = len(df)
        df["lon"] = lon_values[:n]
        df["lat"] = lat_values[:n]
        new_ds = df.to_xarray()
        lon = new_ds.variables['lon'][:]
        lat = new_ds.variables['lat'][:]
        lon_min, lon_max = lon.min(), lon.max()
        lat_min, lat_max = lat.min(), lat.max()
        pixel_width  = (lon_max - lon_min) / PM25.shape[1]
        pixel_height = (lat_max - lat_min) / PM25.shape[0]
        
        tstep, tag = compute_tstep(i, tags, dem, offset)
        if tag == "X":
            continue
        tstep_str = str(tstep % 24).zfill(2)
        output_filename = f'PM25_{tag[10:14]}_{tstep_str}.tiff'
        output_path = os.path.join(output_directory, output_filename)
        write_tiff(PM25, output_path, lon_min, lat_max, pixel_width, pixel_height)

def main():
    month_number = "03"; offset = 5; area = "Oregon"; UTC = -7
    path_CMAQ = "G:/Model_Execution/CMAQ_Libraries"
    path_MCIP = f"G:/Model_Execution/MCIP_Libraries/MET_{area}_{month_number}01/"
    output_directory = "G:/Big_Data_Preprocessing/Air/Concentration/Calibration/Result/1_GeoTIFF/"
    os.makedirs(output_directory, exist_ok=True)

    netcdf_files, netcdf_tags = generate_netcdf_files(month_number, path_CMAQ, area)
    print("NetCDF files:")
    print(np.array(netcdf_files).reshape(1, -1))
    
    # Process each NetCDF file with its corresponding tags.
    for dem, netcdf_file in enumerate(netcdf_files):
        print(f"Processing file {dem+1}/{len(netcdf_files)}: {netcdf_file}")
        process_netcdf(netcdf_file, netcdf_tags, dem, path_MCIP, output_directory, offset)

if __name__ == "__main__":
    main()
