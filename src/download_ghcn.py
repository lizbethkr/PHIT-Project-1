import pandas as pd
import requests
import os
import time


# URL for GHCN hourly data by year
base_url = "https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/access/by-year/{year}/psv/GHCNh_{station}_{year}.psv"


# preparing folder for the hourly data by year and station
base_folder = "data/ghcn_hourly"
raw_folder = os.path.join(base_folder, "ghcn_raw")
processed_folder = os.path.join(base_folder, "ghcn_processed")


if not os.path.exists(processed_folder):
    os.makedirs(processed_folder)


# read through GHCN station list to get CA stations
all_stations = "https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/doc/ghcnh-station-list.txt"


response = requests.get(all_stations)
metadata_lines = response.text.split('\n')


# list to store metadata within each station
station_metadata = []


# parsing metadata
for line in metadata_lines:
    if len(line) > 0:
        # extract specific data from each line (station)
        # -> formatting in GHCN hourly documentation
        station_id = line[:11].strip()
        latitude = float(line[12:20])
        longitude = float(line[21:30])
        elevation = float(line[31:37])
        state = line[38:40].strip()
        name = line[41:71].strip()


        # put into dictionary for filtering
        station_metadata.append({
            'station_id': station_id,
            'latitude': latitude,
            'longitude': longitude,
            'elevation': elevation,
            'state': state,
            'name': name
        })


# filtering for CA stations
ca_stations = [station['station_id'] for station in station_metadata if station['state'] == 'CA']


# how many CA stations found: 391 stations
print(f"Found {len(ca_stations)} California stations.")


def downloading(url, f_path, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            # response successful
            if response.status_code == 200:
                with open(f_path, 'wb') as f:
                    f.write(response.content)
                print(f"Data downloaded for {url}")
                return True
           
            else:
                print(f"Does not exist: {url}, status code: {response.status_code}")
                return False
        # for timeout errors - retries
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5)


    print(f"Failed to download data from {url} after {retries} attempts")
    return False


def first_half(lst):
    length = len(lst)
    middle = length // 2
    first = lst[:middle]
    return first


# columns to keep
keep_columns = ['Station_ID', 'Station_name', 'Year', 'Month', 'Day',
                'Hour', 'Latitude', 'Longitude', 'temperature']


# only grab first half of the stations for now
ca_half = first_half(ca_stations)


# use CA stations found to get data from stations from 2003 - 2023
for year in range(2003, 2024):
    combined_data = []
    for station in ca_half:
        # create file path
        file_path = os.path.join(raw_folder, f"{station}_{year}.psv")
        url = base_url.format(year=year, station=station)  # format for each station's psv file for each year
           
        if not downloading(url, file_path):
            print(f"Skipping station {station} for year {year} due to download issues.")
            continue


        # read psv (pipe-separated values)
        data = pd.read_csv(file_path, sep='|', low_memory=False)


        data = data[keep_columns]
        data.fillna(0, inplace=True)


        # add station data to the specific year data
        combined_data.append(data)


        # comment below to keep raw files
        os.remove(file_path)


    # all stations for the year loaded -> combine into df and csv file
    if combined_data:
        # combine all dataframes for the year
        combined_df = pd.concat(combined_data, ignore_index=True)


        # save year df to csv file
        combined_df.to_csv(os.path.join(processed_folder, f"CA_stations_{year}.csv"), index=False)
        print(f"Processed all CA stations for year {year}")


print("Complete.")
