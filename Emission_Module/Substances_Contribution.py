from arcpy import *
from arcpy import env
from arcpy.sa import *
import pandas as pd
import numpy as np
import os, datetime
from osgeo import ogr
import rasterio
import xarray as xr
from rasterio.transform import from_origin
import subprocess, time
from tqdm import tqdm

data_dict = {}; lon = []; lat = []
path_excel = r"F:/Emission/CAMS_GLOB_ANT_EXCEL/CB/"
excel_files = os.listdir(path_excel)
df = pd.read_excel(path_excel + excel_files[0], header=None)
df.columns = ["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]
df = pd.DataFrame(df.groupby(['Lat', 'Lon'])["Value"].sum().reset_index(), columns=['Lat', 'Lon', 'Value'])
for index in range(df['Lat'].size):
    data_dict[(df['Lat'][index], df['Lon'][index])] = 0
    lon.append(df['Lon'][index]); lat.append(df['Lat'][index])

for excel_file in excel_files:
    print(excel_file)
    for day in range(30):
        # print(excel_file)
        path_excel_file = path_excel + excel_file
        df = pd.read_excel(path_excel_file, header=None, sheet_name = f"Day_{day+1}")
        df.columns = ["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]
        df = pd.DataFrame(df.groupby(['Lat', 'Lon'])["Value"].sum().reset_index(), columns=['Lat', 'Lon', 'Value'])
        for index in range(df['Lat'].size):
            data_dict[(df['Lat'][index], df['Lon'][index])] = data_dict[(df['Lat'][index], df['Lon'][index])] + df['Value'][index]

# Open the shapefile
driver = ogr.GetDriverByName('ESRI Shapefile')
dataSource = driver.Open(r"F:\ShapefileCopying\grid03_Project.shp", 1)  # 1 is read/write

# Get the layer
layer = dataSource.GetLayer()

# Check if 'BC' field exists and delete it if it does
layer_defn = layer.GetLayerDefn()
field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]

if 'NOx' in field_names:
    layer.DeleteField(layer_defn.GetFieldIndex('NOx'))

# Define the new field
fldDef = ogr.FieldDefn('NOx', ogr.OFTReal)
layer.CreateField(fldDef)
# Update the new field with values from the DataFrame
for i, feature in enumerate(layer):
    feature.SetField('NOx', float(data_dict[(lat[i], lon[i])])*2592.0)
    layer.SetFeature(feature)  # Save the changes to the feature
# Save and close the data source
dataSource = None
print("Field 'NOx' added and populated with values from DataFrame.")

# projectDir = r"F:/ProjectInGeneral/MyProject/MyProject.aprx"
# projectSaveDir = r"F:/ProjectInGeneralCopy/ProjectInGeneral.aprx"
# env.overwriteOutput = True
# env.workspace = projectDir


# # Open the ArcGIS Pro project
# p = mp.ArcGISProject(projectDir)
# m = p.listMaps('Map')[0]
# l = m.listLayers()[0]

# # Check if the layer has joins and remove them
# join_table_names = [join.name for join in l.getDefinition('joins')]

# if join_table_names:
#     for join_name in join_table_names:
#         arcpy.RemoveJoin_management(l, join_name)

# # Update symbology
# sym = l.symbology
# if hasattr(sym, 'renderer'):
#     if sym.renderer.type == 'SimpleRenderer':
#         sym.updateRenderer('GraduatedColorsRenderer')
#         sym.renderer.colorRamp = p.listColorRamps('Oranges (Continuous)')[0]
#         sym.renderer.classificationField = 'CO'
#         sym.renderer.breakCount = 5
#         l.symbology = sym

# # Save the project copy
# p.saveACopy(projectSaveDir)

# print("Field 'BC' added and populated with values from DataFrame.")
# print("Project saved with updated symbology after handling joins.")
