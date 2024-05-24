import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
from matplotlib.animation import FuncAnimation
from mpl_toolkits.basemap import Basemap
import geopandas as gpd
from shapely.ops import unary_union
from shapely.geometry import Point

# Open the NetCDF file
file_path = 'F:/EMC_Report_26th/EMC_Report_26th.nc'
ds = nc.Dataset(file_path, 'r')

# Extract the necessary variables
lat = ds.variables['latitude'][0, :, :]  # Select the first time step for initialization
lon = ds.variables['longitude'][0, :, :]  # Select the first time step for initialization
pm25 = ds.variables['PM25'][:]
wdir = ds.variables['WDIR'][:]
wspd = ds.variables['WSPEED'][:]
time = ds.variables['time'][:]

# Load the shapefile and create the expanded boundary
shapefile_path = "F:/CMAQ_Model/HaNoi_Project/24.Shp/HaNoi_shp/HaNoi.shp"
gdf = gpd.read_file(shapefile_path)
minx, miny, maxx, maxy = gdf.total_bounds
expansion_distance = 0.005  # degrees
expanded_geometries = [geom.buffer(expansion_distance) for geom in gdf.geometry]
expanded_boundary = unary_union(expanded_geometries)

mask = np.zeros(lat.shape, dtype=bool)
for i in range(lat.shape[0]):
    for j in range(lat.shape[1]):
        test_point = Point(lon[i, j], lat[i, j])
        if expanded_boundary.contains(test_point):
            mask[i, j] = True

# Initialize new arrays for the filtered data
filtered_pm25 = np.full(pm25.shape, np.nan)
filtered_wdir = np.full(wdir.shape, np.nan)
filtered_wspd = np.full(wspd.shape, np.nan)

# Apply the mask to all time steps
for t in range(pm25.shape[0]):
    filtered_pm25[t, mask] = pm25[t, mask]
    filtered_wdir[t, mask] = wdir[t, mask]
    filtered_wspd[t, mask] = wspd[t, mask]


# Time metadata (optional, for proper timestamp formatting)
time_units = ds.variables['time'].units
time_calendar = ds.variables['time'].calendar

# Convert netCDF4 time variable to datetime objects
time_format = nc.num2date(time, units=time_units, calendar=time_calendar)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 14))

# Set up the Basemap
lon_min = 105.2
lon_max = 106.2
lat_min = 20.5
lat_max = 21.5
m = Basemap(projection='merc', llcrnrlon=lon_min, urcrnrlon=lon_max,
            llcrnrlat=lat_min, urcrnrlat=lat_max, resolution='i', ax=ax)
# m.drawcoastlines()
# m.drawcountries()
# m.drawmapboundary()
m.drawparallels(np.arange(lat_min, lat_max, 0.2), labels=[1,0,0,0])
m.drawmeridians(np.arange(lon_min, lon_max, 0.2), labels=[0,0,0,1])

# Convert lat/lon to Basemap projection coordinates
lon_proj, lat_proj = m(lon, lat)

# Define the plot elements that will be updated in the animation
pm25_plot = m.scatter(lon_proj, lat_proj, c=filtered_pm25[0, :, :], cmap='RdYlGn_r', 
                      marker='s', s=260, zorder=10, alpha=0.8, vmin=0, vmax = 80)
quiver = m.quiver(lon_proj, lat_proj, filtered_wspd[0, :, :] * np.cos(filtered_wdir[0, :, :]),
                  filtered_wspd[0, :, :] * np.sin(filtered_wdir[0, :, :]), color='black', zorder=30)
# Add a colorbar at the bottom
cbar = plt.colorbar(pm25_plot, ax=ax, orientation='horizontal', pad=0.05)
cbar.set_label('PM25 Concentration Value')

# Add text annotations for min and max values
# min_text = ax.text(0.02, -0.2, f'Data Min = {np.nanmin(filtered_pm25[0, :, :])}', transform=ax.transAxes)
# max_text = ax.text(0.7, -0.2, f'Data Max = {np.nanmax(filtered_pm25[0, :, :])}', transform=ax.transAxes)

# Set the title and subtitle
# title = ax.set_title('')
fig.suptitle(f'PM25 Concentration Ha Noi Project', y = 0.895)
title = plt.title(f'Time: {time_format[0]}')

m.readshapefile('F:/CMAQ_Model/HaNoi_Project/24.Shp/HaNoi_shp/HaNoi', 'HaNoi', color='red', linewidth=2, zorder=20)

plt.show()



def update(frame):
    # Update the PM25 plot
    pm25_plot.set_array(filtered_pm25[frame, :, :].flatten())

    # Update the quiver plot
    quiver.set_UVC(filtered_wspd[frame, :, :] * np.sin(filtered_wdir[frame, :, :]),
                   filtered_wspd[frame, :, :] * np.cos(filtered_wdir[frame, :, :]))

    # Update the title with the new time
    title.set_text(f'Time: {time_format[frame]}')

    # min_text.set_text(f'Data Min = {np.nanmin(filtered_pm25[frame, :, :])}')
    # max_text.set_text(f'Data Max = {np.nanmax(filtered_pm25[frame, :, :])}')
    ### This not working

    return pm25_plot, quiver, title

# Create the animation
ani = FuncAnimation(fig, update, frames=len(time_format), blit=False)

# Save the animation
ani.save('F:/EMC_Report_26th/pm25_wind_animation.mp4', writer='ffmpeg', fps=10)

# Optionally, show the plot window
plt.show()
