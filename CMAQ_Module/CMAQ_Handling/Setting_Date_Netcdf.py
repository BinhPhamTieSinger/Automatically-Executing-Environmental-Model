import os
import subprocess

# Directory containing the .nc files
nc_dir = r'F:\CMAQ_Model\HaNoi_Project\NetCDF'

dem = 0
# Iterate over all .nc files in the directory
for nc_file in os.listdir(nc_dir):
    if nc_file.endswith('.nc'):
        if (dem == 744):
            break
        dem += 1
        print(nc_file)
        # Extract the date and time from the filename
        filename_parts = os.path.splitext(nc_file)[0].split('-')
        date = filename_parts[0]
        time = filename_parts[1]

        # Combine date and time into a single string
        # date_str = f'2020-{date[:2]}-{date[2:]}'
        hour_str = f'{time}:00:00'
        day_str = f'{date[:2]}'
        month_str = f'{date[2:]}'
        year_str = '2023'
        print (hour_str + " " + day_str + " " + month_str + " " + year_str)
        command_1 = f"ncap2 -h -s 'defdim(\"time\",1);time[time]=0.0;time@long_name=\"time\";time@calendar=\"standard\";time@units=\"days since {year_str}-{month_str}-{day_str} {hour_str}\"' -O {os.path.join(nc_dir, nc_file)} tmp.nc"
        subprocess.run(command_1, shell=True)
        command_2 = f'mv tmp.nc {os.path.join(nc_dir, nc_file)}'
        subprocess.run(command_2, shell=True)

print("Date set for all .nc files.")
subprocess.run(['cdo', 'cat', os.path.join(nc_dir, 'F:/CMAQ_Model/HaNoi_Project/NetCDF/*.nc'), os.path.join(nc_dir, 'F:/CMAQ_Model/HaNoi_Project/NetCDF/May.nc')])
