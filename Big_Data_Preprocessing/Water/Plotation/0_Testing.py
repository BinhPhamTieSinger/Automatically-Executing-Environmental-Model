import laspy
import numpy as np
import matplotlib.pyplot as plt

# Replace this with your .laz file path
file_path = 'F:/Download/USGS_LPC_OR_WILLAMETTE_VALLEY_OLC_2008_002155.laz'

# Open the .laz file
las = laspy.read(file_path)

# Extract the point cloud data (X, Y, Z)
x = las.x
y = las.y
z = las.z

# Define the grid resolution (e.g., 10m x 10m grid cells)
resolution = 10

# Determine the grid bounds
min_x, max_x = np.min(x), np.max(x)
min_y, max_y = np.min(y), np.max(y)

# Create a 2D grid of X and Y coordinates
x_bins = np.arange(min_x, max_x, resolution)
y_bins = np.arange(min_y, max_y, resolution)
print(len(x_bins), len(y_bins))

# Create an empty array to hold the average Z values for each grid cell
z_grid = np.full((len(y_bins)-1, len(x_bins)-1), np.nan)

# For each grid cell, calculate the average Z value
for i in range(len(x_bins)-1):
    for j in range(len(y_bins)-1):
        print(i, j)
        # Get the points that lie within the current grid cell
        in_cell = (x >= x_bins[i]) & (x < x_bins[i+1]) & (y >= y_bins[j]) & (y < y_bins[j+1])
        
        if np.sum(in_cell) > 0:  # Only process if there are points in the cell
            avg_z = np.mean(z[in_cell])  # Take the average Z-value
            z_grid[j, i] = avg_z

# Create the plot
fig, ax = plt.subplots(figsize=(10, 8))

# Plot a contour map (topographic map)
c = ax.contourf(x_bins[:-1], y_bins[:-1], z_grid, cmap='viridis')

# Add a color bar to show the elevation values
fig.colorbar(c, ax=ax, label='Elevation (Z)')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Topographic Map (Elevation)')

plt.show()
