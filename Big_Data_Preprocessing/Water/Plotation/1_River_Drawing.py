import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point

# -------------------------
# Helper function to extend a 2-point line
# -------------------------
def extend_line(line, extension=0.2):
    """
    Extend a 2-point LineString by 'extension' (in same units as coordinates)
    in the direction of the line at both ends.
    
    For a line with endpoints p1 and p2, this computes the unit vector
    and then returns a new LineString with:
        new_p1 = p1 - extension * u
        new_p2 = p2 + extension * u
    """
    if not isinstance(line, LineString) or len(line.coords) < 2:
        return line
    p1 = line.coords[0]
    p2 = line.coords[-1]
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = np.hypot(dx, dy)
    if length == 0:
        return line
    ux = dx / length
    uy = dy / length
    new_p1 = (p1[0] - extension * ux, p1[1] - extension * uy)
    new_p2 = (p2[0] + extension * ux, p2[1] + extension * uy)
    return LineString([new_p1, new_p2])

# -------------------------
# 1) Read the river geometry
# -------------------------
river_path = "G:/Big_Data_Preprocessing/Water/Plotation/Data/Long_Tom_River.shp"
gdf_river = gpd.read_file(river_path)
river_geom = gdf_river.geometry.iloc[0]

# -------------------------
# 2) Read cross sections from Excel
# -------------------------
excel_file = "G:/Big_Data_Preprocessing/Water/Cross_Section/Data/Excel/longtomriver.xlsx"
df = pd.read_excel(excel_file)
print(df.loc[20])

# Build a GeoDataFrame of cross-sections as 2-point lines
lines = []
for idx, row in df.iterrows():
    p1 = (row["Long First Point"], row["Lat First Point"])
    p2 = (row["Long Second Point"], row["Lat Second Point"])
    line = LineString([p1, p2])
    lines.append(line)
gdf_xsections = gpd.GeoDataFrame(df, geometry=lines, crs=gdf_river.crs)

# -------------------------
# 3) Extend each cross-section line
# -------------------------
# Here, we extend each cross-section by a fixed amount in both directions.
# Adjust 'extension_value' as needed. (e.g., 0.2 degrees ~ 1/5 degree)
extension_value = 0.002
extended_lines = [extend_line(line, extension=extension_value) for line in gdf_xsections.geometry]
gdf_extended = gpd.GeoDataFrame(df, geometry=extended_lines, crs=gdf_river.crs)

# -------------------------
# 4) Connect consecutive cross sections
#    (Connecting first endpoints and second endpoints separately)
# -------------------------
def first_endpoint(ln):
    return Point(ln.coords[0])
def last_endpoint(ln):
    return Point(ln.coords[-1])

first_points = [first_endpoint(ln) for ln in gdf_extended.geometry]
second_points = [last_endpoint(ln) for ln in gdf_extended.geometry]

line_first = LineString(first_points)
line_second = LineString(second_points)
gdf_connect = gpd.GeoDataFrame(geometry=[line_first, line_second], crs=gdf_river.crs)

# -------------------------
# 5) Plot the results
# -------------------------
fig, ax = plt.subplots(figsize=(10, 8))

# Plot the river with increased thickness
gdf_river.plot(ax=ax, color="blue", linewidth=7, label="River")

# Plot the extended cross-sections
gdf_extended.plot(ax=ax, color="red", linewidth=3, label="Extended Cross-Sections")

# Plot the connection lines
gdf_connect.plot(ax=ax, color="green", linewidth=3, label="Connections")

# Add labels to each cross-section
# for idx, line in enumerate(gdf_extended.geometry):
#     if line.is_empty:
#         continue  # Skip empty geometries

#     midpoint = line.interpolate(0.5, normalized=True)  # Find the midpoint of the line
#     ax.text(midpoint.x, midpoint.y, str(idx), fontsize=8, color="black", ha='center', va='center')

ax.set_title("Extended Cross Sections with Connections (Long Tom River)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
x_min, y_min, x_max, y_max = gdf_river.total_bounds  # Get the bounds of the river geometry
range_x = x_max - x_min
range_y = y_max - y_min
max_range = max(range_x, range_y)

# Make the plot square by setting equal limits for both axes
center_x = (x_min + x_max) / 2
center_y = (y_min + y_max) / 2

# Add some padding to the limits
padding = 0.1 * max_range

ax.set_xlim(center_x - max_range / 2 - padding, center_x + max_range / 2 + padding)
ax.set_ylim(center_y - max_range / 2 - padding, center_y + max_range / 2 + padding)

ax.legend()

# ---- Interactive Zooming and Panning Setup ----
# Global variable to track panning start point
pan_start = None
# Set minimum zoom window (in degrees, adjust as needed)
min_width = 0.05
min_height = 0.05

def zoom_fun(event):
    """Scroll to zoom, centered at the mouse pointer."""
    ax = event.inaxes
    if ax is None or event.xdata is None or event.ydata is None:
        return
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    xdata = event.xdata
    ydata = event.ydata
    # Determine zoom factor based on scroll direction
    if event.button == 'up':
        scale_factor = 0.9   # zoom in
    elif event.button == 'down':
        scale_factor = 1.1   # zoom out
    else:
        scale_factor = 1.0
    new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
    new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
    # Ensure new window is not too small
    if new_width < min_width or new_height < min_height:
        return
    # Compute relative position of the mouse in the current view
    relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
    rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
    ax.set_xlim([xdata - new_width*(1-relx), xdata + new_width*relx])
    ax.set_ylim([ydata - new_height*(1-rely), ydata + new_height*rely])
    ax.figure.canvas.draw_idle()

def on_press(event):
    """Store the starting point for panning (left mouse button)."""
    global pan_start
    if event.inaxes is None:
        return
    if event.button == 1:  # left mouse button
        pan_start = (event.xdata, event.ydata)

def on_release(event):
    """Clear the panning start."""
    global pan_start
    pan_start = None

def on_motion(event):
    """Pan the plot when the left mouse button is pressed and the mouse is moved."""
    global pan_start
    if pan_start is None or event.inaxes is None or event.xdata is None or event.ydata is None:
        return
    dx = pan_start[0] - event.xdata
    dy = pan_start[1] - event.ydata
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    ax.set_xlim(cur_xlim[0] + dx, cur_xlim[1] + dx)
    ax.set_ylim(cur_ylim[0] + dy, cur_ylim[1] + dy)
    pan_start = (event.xdata, event.ydata)
    ax.figure.canvas.draw_idle()

# Connect events: scroll for zoom, press/release/move for pan
fig.canvas.mpl_connect('scroll_event', zoom_fun)
# fig.canvas.mpl_connect('button_press_event', on_press)
# fig.canvas.mpl_connect('button_release_event', on_release)
# fig.canvas.mpl_connect('motion_notify_event', on_motion)

plt.tight_layout()
plt.show()