import arcpy
import pandas as pd
import matplotlib.pyplot as plt

month_standard_string = "March"; month_string_number = "3"; day_in_month = 31; SUBSTANCE = "PM2.5"; year = 2023
PROJECT = "Oregon_Project"; MASK_PROVINCE_CITY = "Oregon_Project"
BIG_DATA_PREPROCESSING_PATH = "G:/Big_Data_Preprocessing"
EXPORTATION_PATH = f"{BIG_DATA_PREPROCESSING_PATH}/Air/Concentration/Exportation"
CALIBRATION_PATH = f"{BIG_DATA_PREPROCESSING_PATH}/Air/Concentration/Calibration"

SHAPEFILE_CITY = f"{EXPORTATION_PATH}/Result/0_Initial_Data/Shapefile/OREGON_SHAPEFILES/reprojected_orcntypoly.shp"
SHAPEFILE_PROVINCES = f"{EXPORTATION_PATH}/Result/0_Initial_Data/Shapefile/OREGON_PROVINCES/"
SHAPEFILE_POINT_DETERMINATION = f"{EXPORTATION_PATH}/Result/0_Initial_Data/Shapefile/OREGON_POINTS/Oregon_Point_Actual.shp"
VALUE_IDW = 0.002

data = pd.read_excel(fr"{EXPORTATION_PATH}/Result/7_Average_Province/Min_Max_Average.xlsx")
data_average = []

masks = SHAPEFILE_PROVINCES

provinces = []
arcpy.env.workspace = masks
shapefiles = arcpy.ListFeatureClasses()
for shapefile in shapefiles:
    print(shapefile)
    provinces.append(shapefile[:-4])

print(len(provinces))
index = 0
for column in data.columns:
    if (column.startswith(month_standard_string)):
        print(index, column)
        data_average.append(data[column][2])

print(data_average)


plt.rcParams['figure.figsize'] = (10, 6)
fig = plt.figure()
plt.bar(provinces, data_average, color='blue')
plt.xlabel('States')
plt.ylabel(f'{SUBSTANCE} Concentration Value')
# plt.xticks(rotation = 90)
plt.title(f'Average {SUBSTANCE} Concentration Value in Oregon in {month_string_number}, {year}')
fig.savefig(f'{EXPORTATION_PATH}/Result/11_Diagram/{SUBSTANCE}_Concentration.png', dpi=1000, format="png")
plt.show()