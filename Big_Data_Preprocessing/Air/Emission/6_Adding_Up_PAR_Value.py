import os
import pandas as pd

# Define the directory containing the PAR files
directory = "D:/Code_Result/Result/NASA_TUTORIAL_SPACE/EMISSION6/TXT_FINALE/Batch_4"

# Filter the PAR files
par_files = [filename for filename in os.listdir(directory) if filename.startswith("PAR")]

# Initialize a DataFrame to store the combined data
combined_data = pd.DataFrame(columns=['Year', 'Month', 'Day', 'Hour', 'Lat', 'Lon', 'Substance', 'Value'])

# Initialize flag and dataframes
number = 0
df_1 = None
df_2 = None

# Read and sum the values from each PAR file
for filename in par_files:
    if filename.startswith("PAR1"):
        file_path = os.path.join(directory, filename)
        df_1 = pd.read_csv(file_path, header=None, dtype=str)  # Assuming comma-separated values and reading as strings
        df_1.columns = ['Year', 'Month', 'Day', 'Hour', 'Lat', 'Lon', 'Substance', 'Value']
        df_1['Value'] = pd.to_numeric(df_1['Value'], errors='coerce')  # Convert 'Value' column to numeric
        number += 1

    if filename.startswith("PAR2"):
        file_path = os.path.join(directory, filename)
        df_2 = pd.read_csv(file_path, header=None, dtype=str)  # Assuming comma-separated values and reading as strings
        df_2.columns = ['Year', 'Month', 'Day', 'Hour', 'Lat', 'Lon', 'Substance', 'Value']
        df_2['Value'] = pd.to_numeric(df_2['Value'], errors='coerce')  # Convert 'Value' column to numeric
        number += 1
    
    print(number)
    if number == 2:
        print(df_1)
        print(df_2)
        # Sum the 'Value' columns
        combined_value = df_1['Value'] + df_2['Value']
        
        # Add data to combined_data DataFrame
        combined_data = pd.concat([df_1.drop(columns=['Value']), pd.DataFrame({'Value': combined_value})], axis=1)
        combined_data["Substance"] = "PAR"
        # Reset flag and dataframes for next iteration
        number = 0
        df_1 = None
        df_2 = None
        break

# Save the combined data to a new text file
combined_data.to_csv(os.path.join(directory, "PAR.txt"), sep=',', index=False, header=False)
