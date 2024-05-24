# * --> Means that you have to check if it is suitable with your condition
import arcpy, os
import xarray as xr

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")

path_Netcdf_Air = "D:/Emission/CAMS_GLOB_AIR_NETCDF/" # Path to your CAMS_GLOB_AIR data (Default: D:/Emission/CAMS_GLOB_AIR_NETCDF)*
path_Netcdf_Ant = "D:/Emission/CAMS_GLOB_ANT_NETCDF/" # Path to your CAMS_GLOB_ANT data (Default: D:/Emission/CAMS_GLOB_ANT_NETCDF)*
path_Netcdf_Bio = "D:/Emission/CAMS_GLOB_BIO_NETCDF/" # Path to your CAMS_GLOB_BIO data (Default: D:/Emission/CAMS_GLOB_BIO_NETCDF)*

create_directory_if_not_exists(path_Netcdf_Air) # Create the path_Netcdf_Air if you don't have one
create_directory_if_not_exists(path_Netcdf_Ant) # Create the path_Netcdf_Ant if you don't have one
create_directory_if_not_exists(path_Netcdf_Bio) # Create the path_Netcdf_Bio if you don't have one

data_Air_acetylene = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_acetylene_v2.1_monthly_2023.nc"
data_Air_alcohols = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_alcohols_v2.1_monthly_2023.nc"
data_Air_bc = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_bc_v2.1_monthly_2023.nc"
data_Air_benzene = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_benzene_v2.1_monthly_2023.nc"
data_Air_co = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_co_v2.1_monthly_2023.nc"
data_Air_co2 = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_co2_v2.1_monthly_2023.nc"
data_Air_ethane = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_ethane_v2.1_monthly_2023.nc"
data_Air_ethene = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_ethene_v2.1_monthly_2023.nc"
data_Air_formaldehyde = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_formaldehyde_v2.1_monthly_2023.nc"
data_Air_hexanes = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_hexanes_v2.1_monthly_2023.nc"
data_Air_ketones = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_ketones_v2.1_monthly_2023.nc"
data_Air_nh3 = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_nh3_v2.1_monthly_2023.nc"
data_Air_nmvocs = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_nmvoc_v2.1_monthly_2023.nc"
data_Air_nox = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_nox_v2.1_monthly_2023.nc"
data_Air_oc = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_oc_v2.1_monthly_2023.nc"
data_Air_other_aldehydes = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_other-aldehydes_v2.1_monthly_2023.nc"
data_Air_other_alkenes_and_alkynes = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_other-alkenes-and-alkynes_v2.1_monthly_2023.nc"
data_Air_other_aromatics = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_other-aromatics_v2.1_monthly_2023.nc"
data_Air_propane = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_propane_v2.1_monthly_2023.nc"
data_Air_propene = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_propene_v2.1_monthly_2023.nc"
data_Air_so2 = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_so2_v2.1_monthly_2023.nc"
data_Air_toluene = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_toluene_v2.1_monthly_2023.nc"
data_Air_xylene = path_Netcdf_Air + "CAMS-GLOB-AIR_Glb_0.5x0.5_anthro_xylene_v2.1_monthly_2023.nc"



data_Ant_acetylene = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_acetylene_v5.3_monthly_2023.nc"
data_Ant_alcohols = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_alcohols_v5.3_monthly_2023.nc"
data_Ant_bc = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_bc_v5.3_monthly_2023.nc"
data_Ant_benzene = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_benzene_v5.3_monthly_2023.nc"
data_Ant_butanes = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_butanes_v5.3_monthly_2023.nc"
data_Ant_ch4 = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_ch4_v5.3_monthly_2023.nc"
data_Ant_co = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_co_v5.3_monthly_2023.nc"
data_Ant_co2_excl_short_cycle_org_C = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_co2_excl_short-cycle_org_C_v5.3_monthly_2023.nc"
data_Ant_co2_short_cycle_org_C = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_co2_short-cycle_org_C_v5.3_monthly_2023.nc"
data_Ant_ethene = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_ethene_v5.3_monthly_2023.nc"
data_Ant_ethane = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_ethane_v5.3_monthly_2023.nc"
data_Ant_formaldehyde = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_formaldehyde_v5.3_monthly_2023.nc"
data_Ant_hexanes = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_hexanes_v5.3_monthly_2023.nc"
data_Ant_isoprene = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_isoprene_v5.3_monthly_2023.nc"
data_Ant_monoterpenes = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_monoterpenes_v5.3_monthly_2023.nc"
data_Ant_n2o = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_n2o_v5.3_monthly_2023.nc"
data_Ant_nh3 = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_nh3_v5.3_monthly_2023.nc"
data_Ant_nmvocs = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_nmvocs_v5.3_monthly_2023.nc"
data_Ant_nox = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_nox_v5.3_monthly_2023.nc"
data_Ant_oc = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_oc_v5.3_monthly_2023.nc"
data_Ant_other_aldehydes = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_other-aldehydes_v5.3_monthly_2023.nc"
data_Ant_other_alkenes_and_alkynes = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_other-alkenes-and-alkynes_v5.3_monthly_2023.nc"
data_Ant_other_aromatics = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_other-aromatics_v5.3_monthly_2023.nc"
data_Ant_other_vocs = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_other-vocs_v5.3_monthly_2023.nc"
data_Ant_propane = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_propane_v5.3_monthly_2023.nc"
data_Ant_propene = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_propene_v5.3_monthly_2023.nc"
data_Ant_so2 = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_so2_v5.3_monthly_2023.nc"
data_Ant_toluene = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_toluene_v5.3_monthly_2023.nc"
data_Ant_total_ketones = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_total-ketones_v5.3_monthly_2023.nc"
data_Ant_xylene = path_Netcdf_Ant + "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_xylene_v5.3_monthly_2023.nc"



data_Bio_acetaldehyde = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_acetaldehyde_v3.1_monthly_2022.nc"
data_Bio_acetone = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_acetone_v3.1_monthly_2022.nc"
data_Bio_butanes_and_higher_alkanes = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_butanes-and-higher-alkanes_v3.1_monthly_2022.nc"
data_Bio_butenes_and_higher_alkenes = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_butenes-and-higher-alkenes_v3.1_monthly_2022.nc"
data_Bio_ch4 = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_CH4_v3.1_monthly_2022.nc"
data_Bio_co = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_CO_v3.1_monthly_2022.nc"
data_Bio_ethane = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_ethane_v3.1_monthly_2022.nc"
data_Bio_ethanol = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_ethanol_v3.1_monthly_2022.nc"
data_Bio_ethene = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_ethene_v3.1_monthly_2022.nc"
data_Bio_formaldehyde = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_formaldehyde_v3.1_monthly_2022.nc"
data_Bio_isoprene = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_isoprene_v3.1_monthly_2022.nc"
data_Bio_methanol = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_methanol_v3.1_monthly_2022.nc"
data_Bio_other_aldehydes = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_other-aldehydes_v3.1_monthly_2022.nc"
data_Bio_other_ketones = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_other-ketones_v3.1_monthly_2022.nc"
data_Bio_other_monoterpenes = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_other-monoterpenes_v3.1_monthly_2022.nc"
data_Bio_propane = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_propane_v3.1_monthly_2022.nc"
data_Bio_propene = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_propene_v3.1_monthly_2022.nc"
data_Bio_toluene = path_Netcdf_Bio + "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_toluene_v3.1_monthly_2022.nc"

#############################################################################################################################################

arcpy.env.overwriteOutput = True

substance_Air = ["acetylene", "alcohols", "bc", "benzene", "co", "co2", "ethane", "ethene", "formaldehyde",
                 "hexanes", "ketones", "nh3", "nmvocs", "nox", "oc", "other_aldehydes", "other_alkenes_and_alkynes",
                 "other_aromatics", "propane", "propene", "so2", "toluene", "xylene"] # Listing Substances of Air*
substance_Ant = ["acetylene", "alcohols", "bc", "benzene", "butanes", "co", "co2_short_cycle_org_C", "ch4" "ethane", "ethene", "formaldehyde", 
                 "hexanes", "isoprene", "monoterpenes", "nh3", "nmvocs", "nox", "oc", "other_aldehydes", "xylene", "other_alkenes_and_alkynes", 
                 "other_aromatics", "other_vocs", "propane", "propene", "so2", "toluene", "total_ketones"] # Listing Substance of Ant*
substance_Bio = ["acetaldehyde", "acetone", "butanes_and_higher_alkanes", "butenes_and_higher_alkenes", "ch4", 
                 "co", "ethane", "ethanol", "ethene", "formaldehyde", "isoprene", "methanol", "other_aldehydes", 
                 "other_ketones", "other_monoterpenes", "propane", "propene", "toluene"] # Listing Substance of Bio*

variable_Ant = ['ene', 'ind', 'tro', 'res', 'agl', 'awb', 'ags', 'swd', 'shp', 'fef', 'slv'] # Sectors of Ant*
variable_Bio = ['emission_bio', 'emiss_bio'] # Sectors of Bio*
variable_Air = ['avi'] # Sectors of Air*

time_Data_Air = ["01/01/2023 12:00:00 AM"] # Time Dimension for extracting to GeoTIFF File*
time_Data_Ant = ["01/01/2023 12:00:00 AM"] # Time Dimension for extracting to GeoTIFF File*
time_Data_Bio = ["01/01/2022 12:00:00 AM"] # Time Dimension for extracting to GeoTIFF File*


output_folder_Air = "F:/Emission/CAMS_GLOB_AIR_TIFF/"
create_directory_if_not_exists(output_folder_Air)
for substance in substance_Air:
    for time in time_Data_Air:
        ds_Air = xr.open_dataset(globals().get(f"data_Air_{substance}", 0))
        for variable in variable_Air:
            if variable in ds_Air.variables:
                print(f"data_Air_{substance}", time)
                out_raster_layer = f"{variable}_{substance}_Air_{time[:10].replace('/', '').replace(':', '').replace(' ', '')}"
                out_raster_path = output_folder_Air + out_raster_layer + ".tif"
                arcpy.MakeNetCDFRasterLayer_md(globals().get(f"data_Air_{substance}", 0), variable,
                                                "lon", "lat", out_raster_layer, dimension_values=[("time", time)])
                arcpy.CopyRaster_management(out_raster_layer, out_raster_path)

output_folder_Ant = "F:/Emission/CAMS_GLOB_ANT_TIFF/"
create_directory_if_not_exists(output_folder_Ant)
for substance in substance_Ant:
    for time in time_Data_Ant:
        ds_Ant = xr.open_dataset(globals().get(f"data_Ant_{substance}", 0))
        for variable in variable_Ant:
            if variable in ds_Ant.variables:
                print(f"data_Ant_{substance}", time)
                out_raster_layer = f"{variable}_{substance}_Ant_{time[:10].replace('/', '').replace(':', '').replace(' ', '')}"
                out_raster_path = output_folder_Ant + out_raster_layer + ".tif"
                arcpy.MakeNetCDFRasterLayer_md(globals().get(f"data_Ant_{substance}", 0), variable,
                                                "lon", "lat", out_raster_layer, dimension_values=[("time", time)])
                arcpy.CopyRaster_management(out_raster_layer, out_raster_path)
        
output_folder_Bio = "F:/Emission/CAMS_GLOB_BIO_TIFF/"
create_directory_if_not_exists(output_folder_Bio)
for substance in substance_Bio:
    for time in time_Data_Bio:
        ds_Bio = xr.open_dataset(globals().get(f"data_Bio_{substance}", 0))
        for variable in variable_Bio:
            if variable in ds_Bio.variables:
                print(f"data_Bio_{substance}", time)
                out_raster_layer = f"{variable}_{substance}_Bio_{time[:10].replace('/', '').replace(':', '').replace(' ', '')}"
                out_raster_path = output_folder_Bio + out_raster_layer + ".tif"
                arcpy.MakeNetCDFRasterLayer_md(globals().get(f"data_Bio_{substance}", 0), variable,
                                                "lon", "lat", out_raster_layer, dimension_values=[("time", time)])
                arcpy.CopyRaster_management(out_raster_layer, out_raster_path)

print("Successfully Executing Code!!!")

