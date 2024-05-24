###################################
# 9. Converting_Tiff_To_Netcdf.py #
###################################

import rasterio
from arcpy import *
from arcpy import conversion
from netCDF4 import Dataset
import subprocess
from cdo import *

path_tiff_files = r'F:/CMAQ_Model/HaNoi_Project/Extract_Map/'
output_folder = r'F:/CMAQ_Model/HaNoi_Project/NetCDF/'

# List TIFF files
raw_names = os.listdir(path_tiff_files)
# tif_files = [os.path.join(path_tiff_files, file) for file in raw_names if file.endswith('.tif')]
for raw_name in raw_names:
    if raw_name.endswith(".tif"):
        print(raw_name)
        # Convert TIF to NetCDF
        i = 0
        while (raw_name[i] != '.'):
            i += 1
        tif_input = path_tiff_files + raw_name[0:i] + '.tif'
        nc_output = output_folder + raw_name[0:i] + ".nc"
        subprocess.run(["gdal_translate", "-of", "netCDF", "-co", "FORMAT=NC4", tif_input, nc_output], check=True)


# Then open the cygwin and run the cdo cat *.nc output.nc to merge these files
