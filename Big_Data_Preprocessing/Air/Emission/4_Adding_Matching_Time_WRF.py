import os
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore')

# Directory containing the txt files
directory = "D:/Code_Result/Result/NASA_TUTORIAL_SPACE/EMISSION6/TXT_FILE/"
directory_out = "D:/Code_Result/Result/NASA_TUTORIAL_SPACE/EMISSION6/TXT_FINAL/"
os.makedirs(directory_out, exist_ok=True)

# Iterate over all files in the directory
for filename in os.listdir(directory):
    # Check if the filename ends with "Month_4.txt"
    if filename.endswith("Month_6.txt"):
        # if (filename != 'PAR2 (BUTANES)_Month_3.txt'): continue
        print(filename)
        # Read the txt file into a pandas DataFrame
        data_month_10 = pd.read_csv(os.path.join(directory, filename), header=None)
        # Set column names
        data_month_10.columns = ["Year", "Month", "Day", "Hour", "Lat", "Lon", "Substance", "Value"]
        print(data_month_10)
        # data_day_31 = data_month_10[(data_month_10["Day"] >= 24) & (data_month_10["Day"] <= 30)]
        # data_day_32 = data_month_10[(data_month_10["Day"] == 30)]
        # data_day_32["Day"][data_day_32["Day"] == 30] = 31
        # data_day_31 = pd.concat([data_day_31, data_day_32])

        # data_day_31 = data_month_10[(data_month_10["Day"] >= 30)]
        # data_day_31["Day"][data_day_31["Day"] == 30] = 1
        # data_day_31["Day"][data_day_31["Day"] == 31] = 2
        # data_day_31["Month"] = 5

        data_day_31 = data_month_10[(data_month_10["Day"] >= 29)]
        data_day_31["Day"][data_day_31["Day"] == 29] = 1
        data_day_31["Day"][data_day_31["Day"] == 30] = 2
        data_day_31["Month"] = 7

        new_filename = filename.replace("Month_6.txt", "Month_7.txt")
        # new_filename = filename
        data_day_31.to_csv(os.path.join(directory_out, new_filename), index=False, header=False)

