import os
import pandas as pd
from datetime import datetime
import numpy as np

# Define the folders and their corresponding date ranges
folders = {
    "Folder 1": ("24/05 01:00:00", "07/06 01:00:00"),
    "Folder 2": ("01/06 01:00:00", "15/06 01:00:00"),
    "Folder 3": ("07/06 01:00:00", "21/06 01:00:00"),
    "Folder 4": ("18/06 01:00:00", "02/07 01:00:00")
}
# Data_FID = pd.read_csv(r"E:/Emission_Python/toado_grid_corner_filter.csv")

def process_and_convert_to_txt(df, output_file):
    with open(output_file, 'w') as file:
        for index, row in df.iterrows():
            year, month, day, hour, lat, lon, substance, value = row
            file.write(f"{int(year)},{int(month)},{int(day)},{int(hour)},{lat},{lon},{substance},{value}\n")
# df_filtered_1 = pd.DataFrame(columns = [["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]]); df_filtered_2 = pd.DataFrame(columns = [["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]])
df_filtered_1 = pd.DataFrame(columns = []); df_filtered_2 = pd.DataFrame(columns = [])

# Directory containing the txt files
directory = "D:/Code_Result/Result/NASA_TUTORIAL_SPACE/EMISSION6/TXT_FINAL/"
start_date = datetime.strptime(folders["Folder 1"][0], "%d/%m %H:%M:%S")
end_date = datetime.strptime(folders["Folder 1"][1], "%d/%m %H:%M:%S")
substance_data, number = {}, 0
filenames = sorted(os.listdir(directory))
print(filenames)
for filename in filenames:
        if filename.endswith("Month_5.txt"):
            substance = filename[:-12]
            df = pd.read_csv(os.path.join(directory,    filename), header=None)
            df_filtered_1 = df[(df[2] >= start_date.day) & (df[3] >= start_date.hour) & (df[1] >= start_date.month)]
            df_filtered_1.columns = ["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]
            df_filtered_1["Year"] = 2023
            number = number + 1 
        if filename.endswith("Month_6.txt"):
            substance = filename[:-12]
            df = pd.read_csv(os.path.join(directory, filename), header=None)
            df_filtered_2 = df[(df[2] <= end_date.day) & (df[3] <= 24) & (df[1] <= end_date.month)]
            df_filtered_2.columns = ["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]
            df_filtered_2["Year"] = 2023
            number = number + 1
        if (number == 2):
            # print(df_filtered_1)
            # print(df_filtered_2)
            df = pd.concat([df_filtered_1, df_filtered_2], ignore_index=True)
            df.columns = ["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]
            substance_name = filename.split("_")[0]
            process_and_convert_to_txt(df, f"D:/Code_Result/Result/NASA_TUTORIAL_SPACE/EMISSION6/TXT_FINALE/Batch_1/{substance_name}.txt"); number = 0
        
# Directory containing the txt files
directory = "D:/Code_Result/Result/NASA_TUTORIAL_SPACE/EMISSION6/TXT_FINAL/"
start_date = datetime.strptime(folders["Folder 2"][0], "%d/%m %H:%M:%S")
end_date = datetime.strptime(folders["Folder 2"][1], "%d/%m %H:%M:%S")
substance_data = {}
for filename in sorted(os.listdir(directory)):
        if filename.endswith("Month_6.txt"):
            substance = filename[:-12]
            df = pd.read_csv(os.path.join(directory, filename), header=None)
            print(directory, filename)
            df_filtered_1 = df[(df[2] >= start_date.day) & (df[3] >= start_date.hour) & (df[1] >= start_date.month) &
                            (df[2] <= end_date.day) & (df[3] <= 24) & (df[1] <= end_date.month)]
            df = df_filtered_1
            df.columns = ["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]
            df["Year"] = 2023
            print(df)
            substance_name = filename.split("_")[0]
            process_and_convert_to_txt(df, f"D:/Code_Result/Result/NASA_TUTORIAL_SPACE/EMISSION6/TXT_FINALE/Batch_2/{substance_name}.txt")

# Directory containing the txt files
directory = "D:/Code_Result/Result/NASA_TUTORIAL_SPACE/EMISSION6/TXT_FINAL/"
start_date = datetime.strptime(folders["Folder 3"][0], "%d/%m %H:%M:%S")
end_date = datetime.strptime(folders["Folder 3"][1], "%d/%m %H:%M:%S")
substance_data = {}
for filename in sorted(os.listdir(directory)):
        if filename.endswith("Month_6.txt"):
            substance = filename[:-12]
            df = pd.read_csv(os.path.join(directory, filename), header=None)
            df_filtered_1 = df[(df[2] >= start_date.day) & (df[3] >= start_date.hour) & (df[1] >= start_date.month) &
                            (df[2] <= end_date.day) & (df[3] <= 24) & (df[1] <= end_date.month)]
            df = df_filtered_1
            df.columns = ["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]
            df["Year"] = 2023
            substance_name = filename.split("_")[0]
            process_and_convert_to_txt(df, f"D:/Code_Result/Result/NASA_TUTORIAL_SPACE/EMISSION6/TXT_FINALE/Batch_3/{substance_name}.txt")
        
# Directory containing the txt files
directory = "D:/Code_Result/Result/NASA_TUTORIAL_SPACE/EMISSION6/TXT_FINAL/"
start_date = datetime.strptime(folders["Folder 4"][0], "%d/%m %H:%M:%S")
end_date = datetime.strptime(folders["Folder 4"][1], "%d/%m %H:%M:%S")
substance_data, number = {}, 0
filenames = sorted(os.listdir(directory))
print(filenames)
for filename in filenames:
        if filename.endswith("Month_6.txt"):
            substance = filename[:-12]
            df = pd.read_csv(os.path.join(directory, filename), header=None)
            print(df)
            df_filtered_1 = df[(df[2] >= start_date.day) & (df[3] >= start_date.hour) & (df[1] >= start_date.month)]
            df_filtered_1.columns = ["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]
            df_filtered_1["Year"] = 2023
            number = number + 1
        if filename.endswith("Month_7.txt"):
            substance = filename[:-12]
            df = pd.read_csv(os.path.join(directory, filename), header=None)
            print(df)
            df_filtered_2 = df[(df[2] <= end_date.day) & (df[3] <= 24) & (df[1] <= end_date.month)]
            df_filtered_2.columns = ["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]
            df_filtered_2["Year"] = 2023
            # print(df_filtered_2)
            number = number + 1
        if (number == 2):
            # print(filename)
            df = pd.concat([df_filtered_1, df_filtered_2], ignore_index=True)
            df.columns = ["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]
            substance_name = filename.split("_")[0]; number = 0
            process_and_convert_to_txt(df, f"D:/Code_Result/Result/NASA_TUTORIAL_SPACE/EMISSION6/TXT_FINALE/Batch_4/{substance_name}.txt")
