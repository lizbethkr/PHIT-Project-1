import os
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline

# Functions used for data_preprocessing notebook

# Function to read California stations from a text file
def read_qrt_stations():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(curr_dir, '..', '..', 'data', 'external', 'ca_stations.txt')
    
    with open(filepath, 'r') as f:
        stations = [line.strip() for line in f.readlines()]
        half_len = len(stations) // 2
        quarter_piece = stations[half_len + (half_len//2):]
        print(len(quarter_piece)) # 99 stations
    return quarter_piece

def read_ca_stations():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(curr_dir, '..', '..', 'data', 'external', 'ca_stations.txt')
    
    with open(filepath, 'r') as f:
        stations = [line.strip() for line in f.readlines()]
        print(len(stations)) # 99 stations
    return stations 

def combine_files_to_dfs(folder):
    ''' combines individual csv files into their own dataframes based on year.
    It then concatenates all dataframes into one and returns it.''' 

    dfs = []
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            full_path = os.path.join(folder, filename)
            
            try:
                df = pd.read_csv(full_path)
                dfs.append(df) 
                print(f"Processed file: {filename}")
            
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")

    CA_stations = pd.concat(dfs, ignore_index=True) # type: ignore

    return CA_stations


def create_full_df():
    ''' function to create a dataframe with all of the hours from 2003 to 2023. '''
    
    stations = read_ca_stations()
    date_range = pd.date_range(start='2003-01-01 00:00', end='2023-05-31 23:00', freq='h')

    # dataframe for the date_range
    full_df = pd.DataFrame(date_range, columns=['datetime'])

    # Extract the needed columns: Year, Month, Day and Hour from the datetime
    full_df['Year'] = full_df['datetime'].dt.year
    full_df['Month'] = full_df['datetime'].dt.month
    full_df['Day'] = full_df['datetime'].dt.day
    full_df['Hour'] = full_df['datetime'].dt.hour

    # dataframe with all combinations of station_ID and datetime
    stations_df = pd.DataFrame({'Station_ID': stations})
    all_combos = pd.merge(stations_df.assign(key=1), full_df.assign(key=1), on='key').drop('key', axis=1)

    # add latitude and longitude and temperature
    all_combos['Latitude'] = np.nan
    all_combos['Longitude'] = np.nan
    all_combos['temperature'] = np.nan

    return all_combos


def cubic_spline_interpolate(data, gap_hours=24):
    '''Cubic spline interpolation on the data where there is more than a day's worth of missing temperature values.'''

    data = data.copy()
    data['temperature'] = pd.to_numeric(data['temperature'], errors='coerce')
    
    data['Datetime'] = pd.to_datetime(data[['Year', 'Month', 'Day', 'Hour']])
    data.set_index('Datetime', inplace=True)
    data.sort_index(inplace=True)
    
    hourly_data = data['temperature'].resample('h').mean()
    
    is_missing = hourly_data.isna()
    
    missing_indices = np.where(is_missing)[0]
    
    gaps = np.split(missing_indices, np.where(np.diff(missing_indices) != 1)[0] + 1)
    
    interpolated_data = hourly_data.copy()
    
    for gap in gaps:
        if len(gap) >= gap_hours:
            start_index = max(gap[0] - 1, 0)
            end_index = min(gap[-1] + 1, len(hourly_data) - 1)
            
            x = np.arange(start_index, end_index + 1)
            y = hourly_data.iloc[start_index:end_index + 1].values
            mask = ~np.isnan(y)
            
            if np.sum(mask) > 1:  
                # Apply cubic spline interpolation
                cs = CubicSpline(x[mask], y[mask])
                interpolated_data.iloc[gap] = cs(gap)

    data['temperature'] = data['temperature'].combine_first(interpolated_data)
    data['temperature'] = data['temperature'].round(1)
    data.reset_index(drop=True, inplace=True)
    data.sort_values(by=['Station_ID', 'Year', 'Month', 'Day', 'Hour'], inplace=True)

    return data


def check_station_rows(df):
    ''' Ensure each station has the expected number of rows for each year.'''

    year_hours = 8760
    leap_year_hours = 8784

    def is_leap(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    row_count = df.groupby(['Station_ID', 'Year']).size().reset_index(name='Row_Count')

    def expected_rows(year):
        if year == 2023:
            return 3924
        elif is_leap(year):
            return leap_year_hours
        else:
            return year_hours
        
    row_count['Expected_Row_Count'] = row_count['Year'].apply(expected_rows)
    
    # Identify discrepancies
    discrepancies = row_count[row_count['Row_Count'] != row_count['Expected_Row_Count']]
    
    return discrepancies


def find_missing_rows(complete_df, curr_df):
    '''Find rows present in the complete DataFrame but missing from the current DataFrame.'''
    # Merge to find missing rows
    merged = complete_df.merge(curr_df, on=['Station_ID', 'Year', 'Month', 'Day', 'Hour'], how='left', indicator=True)
    missing_rows = merged[merged['_merge'] == 'left_only'].drop('_merge', axis=1)
    
    return missing_rows


def add_missing_rows(curr_df, missing_rows):
    '''Add missing rows to the current DataFrame.'''
    updated_df = pd.concat([curr_df, missing_rows], ignore_index=True)
    updated_df.sort_values(by=['Station_ID', 'Year', 'Month', 'Day', 'Hour'], inplace=True)
    
    # fill missing Station_name, Latitude, and Longitude
    metadata = curr_df[['Station_ID', 'Station_name', 'Latitude', 'Longitude']].drop_duplicates().set_index('Station_ID')
    updated_df['Station_name'] = updated_df['Station_name'].fillna(updated_df['Station_ID'].map(metadata['Station_name']))
    updated_df['Latitude'] = updated_df['Latitude'].fillna(updated_df['Station_ID'].map(metadata['Latitude']))
    updated_df['Longitude'] = updated_df['Longitude'].fillna(updated_df['Station_ID'].map(metadata['Longitude']))
    
    # keep certain columns
    columns_to_keep = ['Station_ID', 'Station_name', 'Year', 'Month', 'Day', 'Hour', 'Latitude', 'Longitude', 'temperature']
    updated_df_cleaned = updated_df[columns_to_keep]

    return updated_df_cleaned


def fill_gaps(data):
    ''' Using forward/backward fill, fill missing gaps.'''
    
    def within_station(station):
        return station.ffill().bfill()
    
    filled_df = data.groupby('Station_ID', group_keys=False).apply(lambda station: within_station(station[['temperature']]))

    data['temperature'] = filled_df['temperature']
    data['temperature'] = data['temperature'].round(1)
    data.sort_values(by=['Station_ID', 'Year', 'Month', 'Day', 'Hour'], inplace=True)

    return data


# Filling short gaps in temperature
def fill_if_sandwiched(series):
    series_filled = series.copy()
    changes = []
    for i in range(1, len(series) - 1):
        if pd.isna(series.iloc[i]):
            if not pd.isna(series.iloc[i - 1]) and not pd.isna(series.iloc[i + 1]):
                series_filled.iloc[i] = (series.iloc[i - 1] + series.iloc[i + 1]) / 2
                changes.append(series.index[i])  # Use the original index
    return series_filled, changes


def fill_nan_sandwiched(input_file, output_file, txt_output_file):
    print(f"Processing file: {input_file}")
    
    df = pd.read_csv(input_file)
    
    filled_temperatures = []
    changes_log = []

    for name, group in df.groupby('Station_ID'):
        filled_group, changes = fill_if_sandwiched(group['temperature'])
        filled_temperatures.extend(filled_group)
        for change in changes:
            changes_log.append((name, change, group.loc[change, 'temperature'], filled_group.loc[change]))

    df['filled_temperature'] = filled_temperatures

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    os.makedirs(os.path.dirname(txt_output_file), exist_ok=True)
    
    # Save the filled dataframe to the output directory
    df.to_csv(output_file, index=False)
    
    # Log changes
    with open(txt_output_file, 'w') as log_file:
        log_file.write('Station_ID,Index,Original_Temperature,Filled_Temperature\n')
        for log in changes_log:
            log_file.write(f"{log[0]},{log[1]},{log[2]},{log[3]}\n")
    
    print(f"Filled data saved to: {output_file}")
    print(f"Changes log saved to: {txt_output_file}")

def get_reduced_df():
    # create a combined dataframe for all reduced csv files
    dfs = combine_files_to_dfs("../data/processed/ghcn_reduced")
    return dfs

def get_full_df(csv_folder, chunksize=500000):
    # initialize empty list to store chunks
    dfs = []

    # read csv file in chunks
    for filename in os.listdir(csv_folder):
        if filename.endswith(".csv"):
            full_path = os.path.join(csv_folder, filename)
            
            # Read the CSV file in chunks
            df_chunk = pd.read_csv(full_path, chunksize=chunksize)
            
            for chunk in df_chunk:
                # Optionally process each chunk if needed
                dfs.append(chunk)

    # Combine all chunks using the original combine_files_to_dfs function
    combined_df = combine_files_to_dfs(csv_folder)

    return combined_df

def optimize_col_types(df):
    
    for col in ['Year', 'Month', 'Day', 'Hour']:
        df[col] = pd.to_numeric(df[col], downcast='integer')

    for col in ['Latitude', 'Longitude', 'temperature']:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df

