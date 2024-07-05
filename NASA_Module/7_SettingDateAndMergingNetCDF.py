import os
import subprocess

SUBSTANCE = "PM25"; month_standard_string = "March"; month_string_number = "03"; day_in_month = 31
PROJECT = "NASA_Project"; MASK_PROVINCE_CITY = "HaNoi_Project"

# Directory containing the .nc files
nc_dir = fr'F:/Test/{PROJECT}/{SUBSTANCE}/NetCDF/'

# Iterate over all .nc files in the directory
for nc_file in os.listdir(nc_dir):
    if nc_file.endswith('.nc'):
        # Extract the date and time from the filename
        filename_parts = os.path.splitext(nc_file)[0].split('_')

        # Construct the date and time strings
        day_str, month_str = filename_parts[2], filename_parts[1]
        hour_str, year_str = f'{filename_parts[3]}:00:00', filename_parts[0]

        print(f'Setting date and time for {nc_file} to {day_str}/{month_str}/{year_str} {hour_str}')
        
        # Command to set the time attribute in the NetCDF file
        command_1 = (
            f'ncap2 -h -s '
            f'\'defdim("time",1);'
            f'time[time]=0.0;'
            f'time@long_name="time";'
            f'time@calendar="standard";'
            f'time@units="days since {year_str}-{month_str}-{day_str} {hour_str}"\' '
            f'-O {os.path.join(nc_dir, nc_file)} {os.path.join(nc_dir, "tmp.nc")}'
        )
        subprocess.run(command_1, shell=True)
        
        # Command to move the temporary file back to the original file
        command_2 = f'mv {os.path.join(nc_dir, "tmp.nc")} {os.path.join(nc_dir, nc_file)}'
        subprocess.run(command_2, shell=True)

print("Date set for all .nc files.")

# Command to concatenate all .nc files into April.nc
concatenate_command = (
    f'cdo cat {os.path.join(nc_dir, "*.nc")} '
    f'{os.path.join(nc_dir, "March.nc")}'
)
subprocess.run(concatenate_command, shell=True)
