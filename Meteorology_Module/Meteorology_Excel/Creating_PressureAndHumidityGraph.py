import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from shapely.ops import unary_union

# Read PRES and RH data
df_PRES = pd.read_excel('F:/Bao_Cao/17_Pressure_WSPEED_WDIR_Distribution/PRES.xlsx')
df_RH = pd.read_excel('F:/Bao_Cao/18_RH_WSPEED_WDIR_Distribution/RH.xlsx')
# Load the shapefile
shapefile_path = "F:/CMAQ_Model/HaNoi_Project/24.Shp/HaNoi_shp/HaNoi.shp"
gdf = gpd.read_file(shapefile_path)
# Extract the bounds of the shapefile
minx, miny, maxx, maxy = gdf.total_bounds
expansion_distance = 0.005  # degrees
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
# Define the extent of Northern Vietnam based on LON and LAT values
lon_min = 105.2
lon_max = 106.3
lat_min = 20.3
lat_max = 21.6

# Create Basemap instance for the map of Northern Vietnam for PRES
fig_pres = plt.figure(figsize=(8, 6))
m_pres = Basemap(projection='mill', llcrnrlon=lon_min, llcrnrlat=lat_min, urcrnrlon=lon_max, urcrnrlat=lat_max, resolution='i')
m_pres.drawcoastlines()
m_pres.drawcountries()
m_pres.drawparallels(np.arange(lat_min, lat_max, 0.5), labels=[1, 0, 0, 0])
m_pres.drawmeridians(np.arange(lon_min, lon_max, 0.5), labels=[0, 0, 0, 1], linewidth=0.1, rotation=90)


# Plot PRES data on the map of Northern Vietnam
x_pres, y_pres = m_pres(df_PRES_LON, df_PRES_LAT)
m_pres.scatter(x_pres, y_pres, c=df_PRES_VAL, cmap='viridis', marker='s', s=100, zorder=10, alpha=0.8)

# Add color bar for PRES
pres_colorbar = plt.colorbar(label='Pressure (PRES)')

# Set title for PRES diagram
plt.title('HaNoi Pressure & Wind Vector (April)')

# Add wind vectors for PRES data
u_pres = df_PRES_WSPEED * np.sin(np.radians(df_PRES_WDIR))
v_pres = df_PRES_WSPEED * np.cos(np.radians(df_PRES_WDIR))
m_pres.quiver(x_pres, y_pres, u_pres, v_pres, scale=100, color='black', width=0.005, zorder=30)

# Plot shapefile of Hanoi on top
m_pres.readshapefile('F:/CMAQ_Model/HaNoi_Project/24.Shp/HaNoi_shp/HaNoi', 'HaNoi', color='red', linewidth=2, zorder=20)

# Show PRES plot
plt.show()

# Create Basemap instance for the map of Northern Vietnam for RH
fig_rh = plt.figure(figsize=(8, 6))
m_rh = Basemap(projection='mill', llcrnrlon=lon_min, llcrnrlat=lat_min, urcrnrlon=lon_max, urcrnrlat=lat_max, resolution='i')
m_rh.drawcoastlines()
m_rh.drawcountries()
m_rh.drawparallels(np.arange(lat_min, lat_max, 0.5), labels=[1, 0, 0, 0])
m_rh.drawmeridians(np.arange(lon_min, lon_max, 0.5), labels=[0, 0, 0, 1], linewidth=0.1, rotation=90)

# Plot RH data on the map of Northern Vietnam
x_rh, y_rh = m_rh(df_PRES_LON, df_PRES_LAT)
m_rh.scatter(x_rh, y_rh, c=df_RH_VAL, cmap='viridis', marker='s', s=100, zorder=10, alpha=0.8)

# Add color bar for RH
rh_colorbar = plt.colorbar(label='Relative Humidity (RH)')

# Set title for RH diagram
plt.title('HaNoi Relative Humidity & Wind Vector (April)')

# Add wind vectors for RH data
u_rh = df_RH_WSPEED * np.sin(np.radians(df_RH_WDIR))
v_rh = df_RH_WSPEED * np.cos(np.radians(df_RH_WDIR))
m_rh.quiver(x_rh, y_rh, u_rh, v_rh, scale=100, color='black', width=0.005, zorder=30)

# Plot shapefile of Hanoi on top
m_rh.readshapefile('F:/CMAQ_Model/HaNoi_Project/24.Shp/HaNoi_shp/HaNoi', 'HaNoi', color='red', linewidth=2, zorder=20)

# Show RH plot
plt.show()
