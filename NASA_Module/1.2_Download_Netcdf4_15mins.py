import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

month_day = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
for month in range(1, 2, 1):
    for day in range(13, month_day[month]+1, 1):
        month_string = str(month).zfill(2); day_string = str(day).zfill(2)
        url = f"https://portal.nccs.nasa.gov/datashare/gmao/geos-cf/v1/ana/Y2023/M{month_string}/D{day_string}/"
        save_dir = f"D:/Code_Result/Result/NASA/NASA_Data_15minutes/Y23M{month_string}/D{day_string}"
        os.makedirs(save_dir, exist_ok=True)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a")
        filtered_links = [link.get("href") for link in links if link.get("href").startswith("GEOS-CF.v01.rpl.htf_inst_15mn_g1440x721") and link.get("href").endswith("00z.nc4")]
        with tqdm(total=len(filtered_links), desc="Downloading files") as pbar:
            for link in filtered_links:
                file_url = url + link
                file_name = os.path.join(save_dir, link)
                print(f"\n Downloading {file_name}...")
                response = requests.get(file_url)
                with open(file_name, "wb") as f:
                    f.write(response.content)
                print(f"Download_Netcdf4_D01.py downloaded successfully.")
                pbar.update(1)