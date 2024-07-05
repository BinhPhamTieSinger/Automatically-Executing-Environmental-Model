import arcpy
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel(r"F:/Test/NASA_Project/PM25/Average_Province/Min_Max_Average.xlsx")
data_average = []

masks = "F:/CMAQ_Model/HaNoi_Project/24.Shp/HaNoi_qh/"

provinces = []
### Listing Shape Files ###
arcpy.env.workspace = masks
shapefiles = arcpy.ListFeatureClasses()
for shapefile in shapefiles:
    print(shapefile)
    provinces.append(shapefile[:-4])

print(len(provinces))
index = 0
for column in data.columns:
    if (column.startswith("March")):
        print(index, column)
        data_average.append(data[column][2])

print(data_average)


plt.rcParams['figure.figsize'] = (12, 8)
# Vẽ đồ thị cột
plt.bar(provinces, data_average, color='blue')
plt.xlabel('Huyện')
plt.ylabel('Giá trị PM2.5')
plt.xticks(rotation = 45)
plt.title('Nồng độ PM2.5 trung bình Hà Nôi tháng 3 năm 2024 (Dữ liệu hiệu chỉnh NASA)')
plt.show()