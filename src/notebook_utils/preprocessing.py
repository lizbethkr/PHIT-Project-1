import os
import pandas as pd
import numpy as np
import requests
import sys

# Functions used for data_preprocessing notebook

# Function to read California stations from a text file
def read_california_stations():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(curr_dir, '..', '..', 'data', 'external', 'ca_stations.txt')
    
    with open(filepath, 'r') as f:
        stations = [line.strip() for line in f.readlines()]
        half_len = len(stations) // 2
        quarter_piece = stations[half_len + (half_len//2):]
        print(len(quarter_piece)) # 99 stations
    return quarter_piece

def combine_files_to_dfs(folder):
    ''' combines individual csv files into their own dataframes based on year.
    It then appends each dataframe to a list called dfs.'''

    dfs = []
    for filename in os.listdir(folder):
        if filename.startswith("reduced_CA_stations_") and filename.endswith(".csv"):
            full_path = os.path.join(folder, filename)
            
            try:
                df = pd.read_csv(full_path)
                dfs.append(df) 
                print(f"Processed file: {filename}")
            
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")
    return dfs

def create_full_df():
    ''' function to create a dataframe with all of the hours from 2003 to 2023. '''
    
    stations = read_california_stations()
    date_range = pd.date_range(start='2003-01-01 00:00', end='2023-12-31 23:00', freq='h')

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

def compare_dfs(ref_df, curr_df):
    '''Compare reference dataframe with the uncleaned dataframe to ensure all 
    rows are present for each hour. Update current df with the missing rows.'''

    curr_df_index = curr_df.set_index(['Station_ID', 'Year', 'Month', 'Day', 'Hour'])
    ref_df_index = ref_df.set_index(['Station_ID', 'Year', 'Month', 'Day', 'Hour'])

    metadata_cols = ['Station_ID', 'Station_name', 'Latitude', 'Longitude']
    station_metadata = curr_df[metadata_cols].drop_duplicates(subset='Station_ID').set_index('Station_ID')

    merged = ref_df_index.join(curr_df_index, how='left', lsuffix='_ref', rsuffix='_current')
    missing_rows = merged[merged['temperature_current'].isna()].reset_index()
    missing_rows = missing_rows.merge(station_metadata, on='Station_ID', how='left')

    cols = ['Station_ID', 'Station_name', 'Year', 'Month', 'Day', 'Hour', 'Latitude', 'Longitude', 'temperature']
    for col in cols:
        if col not in missing_rows.columns:
            missing_rows[col] = np.nan

    missing_name_mask = missing_rows['Station_name'].isna()
    missing_rows.loc[missing_name_mask, 'Station_name'] = missing_rows.loc[missing_name_mask, 'Station_ID'].map(
        curr_df.drop_duplicates('Station_ID').set_index('Station_ID')['Station_name']
    )
    
    # add missing rows to the original dataframe
    updated_data = pd.concat([curr_df, missing_rows[cols]], ignore_index=True)

    # sort the dataframe 
    updated_data.sort_values(by=['Station_ID', 'Year', 'Month', 'Day', 'Hour'], inplace=True)
    
    return updated_data

def process_by_year(ref_df, curr_df):
    ''' Create dataframe by using yearly chunks. Still outputs a dataframe with all 99 stations from 2003-2023.'''

    years = ref_df['Year'].unique()

    for year in years: 
        ref_df= ref_df[ref_df['Year'] == year]
        curr_df = compare_dfs(ref_df, curr_df)

    return curr_df