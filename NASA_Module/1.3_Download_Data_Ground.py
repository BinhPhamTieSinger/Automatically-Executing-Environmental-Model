import pandas as pd
from datetime import datetime
import os

data_path = "F:/Zalo_Receiver/Thang07_2023/"
excel_files = os.listdir(data_path)
output_excel_path = "F:/Zalo_Receiver/Observed_Data_July.xlsx"

data_dict = {}; value_lon = []; value_lat = []; stations = []
for excel_file in excel_files:
    excel_path = data_path + excel_file; print(excel_path)
    data = pd.read_csv(excel_path)
    sheet_name = data['location_name'][0]
    stations.append(sheet_name)
    value_lon.append(data['longitude'][0])
    value_lat.append(data['latitude'][0])
    value_year = []; value_month = []; value_day = []
    value_hour = []; value_pm25 = []
    for index in range(data['location_name'].size):
        if (data['parameter'][index] == "pm25"):
            datetime_str = data['datetimeLocal'][index][:-6]
            dt = datetime.fromisoformat(datetime_str)
            if (dt.month == 7):
                value_year.append(dt.year); value_month.append(dt.month)
                value_day.append(dt.day); value_hour.append(dt.hour)
                value_pm25.append(data['value'][index])

    df = pd.DataFrame(data = {"Year": value_year, "Month": value_month,
                                "Day": value_day, "Hour": value_hour,
                                "PM2.5": value_pm25})
    data_dict[sheet_name] = df
data_coordinate = pd.DataFrame(data = {"Stations": stations, "Lon": value_lon, "Lat": value_lat})
data_coordinate.to_csv("F:/Zalo_Receiver/Coordinate.csv", index=False)

with pd.ExcelWriter(output_excel_path) as writer:  
    for excel_file in excel_files:
        excel_path = data_path + excel_file; print(excel_path)
        data = pd.read_csv(excel_path)
        sheet_name = data['location_name'][0]; print(sheet_name)
        data_dict[sheet_name].to_excel(writer, sheet_name=sheet_name)