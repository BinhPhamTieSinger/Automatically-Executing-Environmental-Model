import pandas as pd
import numpy as np
from arcpy import *
from arcpy import env                               
from arcpy.sa import *
import os, datetime
from osgeo import ogr
import rasterio
import xarray as xr
from rasterio.transform import from_origin
import subprocess, time, glob
from natsort import natsorted
from tqdm import tqdm

# Path to the directory containing Excel files
excel_dir_Air = "D:/Emission/CAMS_GLOB_AIR_EXCEL/CAMS_GLOB_AIR_EXCEL/CB/"
excel_dir_Ant = "D:/Emission/CAMS_GLOB_AIR_EXCEL/CAMS_GLOB_ANT_EXCEL/CB/"
excel_dir_Bio = "D:/Emission/CAMS_GLOB_AIR_EXCEL/CAMS_GLOB_BIO_EXCEL/CB/"
column_names = ['Year', 'Month', 'Day', 'Hour', 'Lat', 'Lon', 'Substance', 'Value']
excel_files = []
files_Air = natsorted(glob.glob(excel_dir_Air + "*.xlsx"))
excel_files.extend(files_Air)
files_Ant = glob.glob(excel_dir_Ant + "*.xlsx")
excel_files.extend(files_Ant)
files_Bio = natsorted(glob.glob(excel_dir_Bio + "*.xlsx"))
excel_files.extend(files_Bio)
variable_Air = np.array(['avi'])
variable_Bio = np.array(['emission_bio', 'emiss_bio'])
variable_Ant = np.array(['ene', 'ind', 'tro', 'res', 'agl', 'awb', 'ags', 'swd', 'shp', 'fef', 'slv'])
# Create a dictionary to store DataFrames for each substance
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
substance_encrypt_list = ["ACET", "ALD2", "ALDX", "BENZ", "CH4", "CO", "CO2_INV", "ETH", "ETHA", "ETHY",
                          "ETOH", "FORM", "IOLE1 (ALKENES)", "IOLE2 (ACETYLEN)", "ISOP", "KET", "MEOH",
                          "N2O_INV", "NH3", "NO", "NO2", "OLE", "PAR",
                          "PCA", "PNA", "PAL", "PFE", "PK", "PMN", "PMG", "PTI", "PCL", "PH2O", "PMC", "PMOTHR", "PNH4",
                          "PNO3", "PSO4", "PRPA", "SO2", "TERP", "TOL", "VOC_INV", "XYLMN", "PSI", "PNCOM", "PEC", "POC"]

substance_in_PEC = ["PCA", "PNA", "PAL", "PFE", "PK", "PMN", "PMG", "PTI", "PCL", "PH2O", "PMC", "PMOTHR", "PNH4", "PNO3", "PSO4"]
ratio_in_PEC = [1/6, 1/6, 1/2, 1/2, 1/2, 1/2, 1/2, 1/2, 1/6, 1/12, 220, 11, 0.75, 11/6, 4/3]
ratio_in_PEC = [float(value) for value in ratio_in_PEC]
substance_in_POC = ["PSI", "PNCOM"]
ratio_in_POC = [1/3, 1]
ratio_in_POC = [float(value) for value in ratio_in_POC]


dataframes = {(month, substance): pd.DataFrame(columns=column_names) for month in months for substance in substance_encrypt_list}

def process_dataframe(month, substance_x, df_excel):
    dataframes[(month, substance_x)]["Year"] = df_excel["Year"]
    dataframes[(month, substance_x)]["Month"] = df_excel["Month"]
    dataframes[(month, substance_x)]["Day"] = df_excel["Day"]
    dataframes[(month, substance_x)]["Hour"] = df_excel["Hour"]
    dataframes[(month, substance_x)]["Lat"] = df_excel["Lat"]
    dataframes[(month, substance_x)]["Lon"] = df_excel["Lon"]
    dataframes[(month, substance_x)]["Substance"] = df_excel["Substance"]
    if dataframes[(month, substance_x)]["Value"].isna().any():
        dataframes[(month, substance_x)]["Value"].fillna(df_excel["Value"], inplace=True)
    else:
        dataframes[(month, substance_x)]["Value"] += df_excel["Value"]


# print(dataframes)
total_iterations = len(excel_files)  # Total number of iterations
# variables = {f"value_{substance}": None for substance in substance_encrypt_list}
for file_path in tqdm(excel_files, desc="Processing files", total=total_iterations):
    print("\nReading Excel file:", file_path)
    file_name = file_path.split("\\")[-1]
    parts = np.array(file_name.split("_"))
    group, substance, sector = parts[0], parts[1], ""
    index, month = 2, 0
    if (group == "Air"):
        if (parts[index] != "avi"):
            substance = substance + "_" + parts[index]
            index = index + 1
        month, sector = int(parts[index+1]), parts[index] ### Air
    elif (group == "Bio"):
        if (parts[index] != "emiss"):
            substance = substance + "_" + parts[index]
            index = index + 1
        month, sector = int(parts[index+2]), parts[index] + "_" + parts[index+1] ### Bio
    else:
        for index in range(0, variable_Ant.size, 1):
            j = 2
            while (j < parts.size and parts[j] != variable_Ant[index]):
                j = j + 1
            if (j != parts.size):
                month, sector = int(parts[j+1]), parts[j] ### Ant
                for i in range(2, j, 1):
                    substance = substance + "_" + parts[i]
                break
    # excel_data = pd.read_excel(file_path, sheet_name=None, header=None)
    df_excel = pd.DataFrame(columns = column_names)
    print(file_name, substance, group, sector, month)
    if (substance == "POC"):
        index = 0
        for substance_x in substance_in_POC:
            for sheet_name in range(1, days_in_month[month]+1, 1):
                df = pd.read_excel(file_path, header=None, names = column_names, sheet_name=f"Day_{sheet_name}")
                df["Value"] = df["Value"]*ratio_in_POC[index]
                df_excel = pd.concat([df_excel, df], ignore_index=True)
                df_excel["Substance"] = substance_x
            print(df_excel)
            process_dataframe(month, substance_x, df_excel)
            index += 1
        print('-'*100)
    elif (substance == "PEC"):
        index = 0
        for substance_x in substance_in_PEC:
            for sheet_name in range(1, days_in_month[month]+1, 1):
                df = pd.read_excel(file_path, header=None, names = column_names, sheet_name=f"Day_{sheet_name}")
                df["Value"] = df["Value"]*ratio_in_PEC[index]
                df_excel = pd.concat([df_excel, df], ignore_index=True)
                df_excel["Substance"] = substance_x
            print(df_excel)
            process_dataframe(month, substance_x, df_excel)
            index += 1
        print('-'*100)
    for sheet_name in range(1, days_in_month[month]+1, 1):
        # print(f"Day_{sheet_name}")
        df = pd.read_excel(file_path, header=None, names = column_names, sheet_name=f"Day_{sheet_name}")
        df_excel = pd.concat([df_excel, df], ignore_index=True)
    print(df_excel)
    process_dataframe(month, substance, df_excel)
    print('-'*100)





txt_dir = "D:/Code_Result/Result/Emission_PhuYen_thang04/TXT_FILE/"
for key, df in dataframes.items():
    month, substance = key
    file_name = f"{substance}_Month_{month}"
    # full_file_path = os.path.join(file_path, file_name)

    if not df.empty:
        df.columns = column_names

        # Create a text file name based on the Excel file name
        output_file = file_name + ".txt"
                
        # Process the DataFrame and write the data to a text file
        with open(os.path.join(txt_dir, output_file), 'w') as file:
            for index, row in df.iterrows():
                year, month, day, hour, lat, lon, substance, value = row
                file.write(f"{int(year)},{int(month)},{int(day)},{int(hour)},{lat},{lon},{substance},{value}\n")

        # df.to_excel(full_file_path, index=False, header = False)
        print(f"DataFrame for substance {substance} in month {month} saved as {file_name}")
    
print("Successfully Executing Code!!!")
