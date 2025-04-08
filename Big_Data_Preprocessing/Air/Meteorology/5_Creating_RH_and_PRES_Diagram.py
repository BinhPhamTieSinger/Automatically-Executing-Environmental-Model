import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from shapely.ops import unary_union
import os

os.makedirs("Result/Output", exist_ok=True)

year = 2023; month_number = 3; month_name = "March"
df_PRES = pd.read_excel('G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/PRES.xlsx')
df_RH = pd.read_excel('G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/RH.xlsx')
BIG_DATA_PREPROCESSING_PATH = "G:/Big_Data_Preprocessing"
EXPORTATION_PATH = f"{BIG_DATA_PREPROCESSING_PATH}/Air/Concentration/Exportation"
shapefile_path = f"{EXPORTATION_PATH}/Result/0_Initial_Data/Shapefile/OREGON_SHAPEFILES/reprojected_orcntypoly.shp"
gdf = gpd.read_file(shapefile_path)
lon_min = -124.85
lon_max = -116.4
lat_min = 41.9
lat_max = 46.3

minx, miny, maxx, maxy = gdf.total_bounds
expansion_distance = 0.01
expanded_geometries = []
for geom in gdf.geometry:
    buffered_geom = geom.buffer(expansion_distance)
    expanded_geometries.append(buffered_geom)
expanded_boundary = unary_union(expanded_geometries)

df_PRES_LON = []; df_PRES_LAT = []; df_PRES_VAL = []
df_PRES_WSPEED = []; df_PRES_WDIR = []
df_RH_LON = []; df_RH_LAT = []; df_RH_VAL = []
df_RH_WSPEED = []; df_RH_WDIR = []
for index in range(df_PRES['LON'].size):
    test_point = Point(df_PRES['LON'][index], df_PRES['LAT'][index])
    is_within = expanded_boundary.contains(test_point)
    if is_within:
        df_PRES_LON.append(df_PRES['LON'][index])
        df_PRES_LAT.append(df_PRES['LAT'][index])
        df_PRES_VAL.append(df_PRES['PRES'][index])
        df_PRES_WSPEED.append(df_PRES['WSPEED'][index])
        df_PRES_WDIR.append(df_PRES['WDIR'][index])
        df_RH_LON.append(df_RH['LON'][index])
        df_RH_LAT.append(df_RH['LAT'][index])
        df_RH_VAL.append(df_RH['RH'][index])
        df_RH_WSPEED.append(df_RH['WSPEED'][index])
        df_RH_WDIR.append(df_RH['WDIR'][index])

fig_pres = plt.figure(figsize=(8, 6))
m_pres = Basemap(projection='mill', llcrnrlon=lon_min, llcrnrlat=lat_min, urcrnrlon=lon_max, urcrnrlat=lat_max, resolution='i')
m_pres.drawparallels(np.arange(lat_min, lat_max, 0.5), labels=[1, 0, 0, 0])
m_pres.drawmeridians(np.arange(lon_min, lon_max, 0.5), labels=[0, 0, 0, 1], linewidth=0.1, rotation=90)
x_pres, y_pres = m_pres(df_PRES_LON, df_PRES_LAT)
m_pres.scatter(x_pres, y_pres, c=df_PRES_VAL, cmap='viridis', marker='s', s=300, zorder=10, alpha=0.8)
pres_colorbar = plt.colorbar(label='Pressure (PRES)')
plt.title(f'Oregon Pressure & Wind Vector ({month_name} {year})')
u_pres = df_PRES_WSPEED * np.sin(np.radians(df_PRES_WDIR))
v_pres = df_PRES_WSPEED * np.cos(np.radians(df_PRES_WDIR))
m_pres.quiver(x_pres, y_pres, u_pres, v_pres, scale=100, color='black', width=0.005, zorder=30)
m_pres.readshapefile(shapefile_path[:-4], shapefile_path.split('/')[-1][:-4], color='red', linewidth=2, zorder=20)
plt.show()
fig_pres.savefig('G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/PRESSURE_WVECTOR_January.jpg', format='jpg', dpi=1000)
fig_rh = plt.figure(figsize=(8, 6))
m_rh = Basemap(projection='mill', llcrnrlon=lon_min, llcrnrlat=lat_min, urcrnrlon=lon_max, urcrnrlat=lat_max, resolution='i')
m_rh.drawcoastlines()
m_rh.drawcountries()
m_rh.drawparallels(np.arange(lat_min, lat_max, 0.5), labels=[1, 0, 0, 0])
m_rh.drawmeridians(np.arange(lon_min, lon_max, 0.5), labels=[0, 0, 0, 1], linewidth=0.1, rotation=90)
x_rh, y_rh = m_rh(df_PRES_LON, df_PRES_LAT)
m_rh.scatter(x_rh, y_rh, c=df_RH_VAL, cmap='viridis', marker='s', s=300, zorder=10, alpha=0.8)
rh_colorbar = plt.colorbar(label='Relative Humidity (RH)')
plt.title(f'Oregon Relative Humidity & Wind Vector ({month_name} {year})')
u_rh = df_RH_WSPEED * np.sin(np.radians(df_RH_WDIR))
v_rh = df_RH_WSPEED * np.cos(np.radians(df_RH_WDIR))
m_rh.quiver(x_rh, y_rh, u_rh, v_rh, scale=100, color='black', width=0.005, zorder=30)
m_rh.readshapefile(shapefile_path[:-4], shapefile_path.split('/')[-1][:-4], color='red', linewidth=2, zorder=20)
plt.show()
fig_rh.savefig('G:/Big_Data_Preprocessing/Air/Meteorology/Result/Output/RELATIVE_HUMIDITY_WVECTOR_January.jpg', format='jpg', dpi=1000)