import os
import pandas as pd
import math

def merge_meteo_data(CA_stations_dfs, raw_folder, psv_files, batch_size=500):
    # Get unique station IDs
    unique_stations = CA_stations_dfs['Station_ID'].unique()
    total_files = len(psv_files)
    total_batches = math.ceil(total_files / batch_size)
    print(f"Total files to process: {total_files}, in {total_batches} batches.")

    # Define dtypes for the columns
    dtype_dict = {
        'Station_ID': 'str',
        'Year': 'int64',
        'Month': 'int64',
        'Day': 'int64',
        'Hour': 'int64',
        'wind_speed': 'float64',
        'precipitation': 'float64',
        'relative_humidity': 'float64'
    }
    
    # Define columns to load
    usecols = ['Station_ID', 'Year', 'Month', 'Day', 'Hour', 'wind_speed', 'precipitation', 'relative_humidity']

    # Loop through the files in batches
    for batch_num in range(total_batches):
        # Get the files for the current batch
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_files)
        batch_files = psv_files[start_idx:end_idx]
        
        print(f"Processing batch {batch_num + 1}/{total_batches}, files {start_idx + 1} to {end_idx}.")
        
        for psv_file in batch_files:
            station_id, year = os.path.splitext(psv_file)[0].split('_')
            
            if station_id not in unique_stations:
                continue
            
            file_path = os.path.join(raw_folder, psv_file)
            
            # Load the PSV file
            psv_df = pd.read_csv(file_path, sep='|', dtype=dtype_dict, usecols=usecols)
            
            psv_df['datetime'] = pd.to_datetime(psv_df[['Year', 'Month', 'Day', 'Hour']])
            
            psv_df['Station_ID'] = psv_df['Station_ID'].astype(str)
            CA_stations_dfs['Station_ID'] = CA_stations_dfs['Station_ID'].astype(str)
            
            # Filter the columns
            psv_df_filtered = psv_df[['Station_ID', 'datetime', 'wind_speed', 'precipitation', 'relative_humidity']]
            
            # Merge the data
            CA_stations_dfs['datetime'] = pd.to_datetime(CA_stations_dfs['datetime'])
            CA_stations_dfs = CA_stations_dfs.merge(psv_df_filtered, on=['Station_ID', 'datetime'], how='left', suffixes=('', '_new'))
            
            # Fill missing values
            for col in ['wind_speed', 'precipitation', 'relative_humidity']:
                if f'{col}_new' in CA_stations_dfs.columns:
                    CA_stations_dfs[col].fillna(CA_stations_dfs[f'{col}_new'], inplace=True)
                    CA_stations_dfs.drop(columns=[f'{col}_new'], inplace=True)
        
        # Progress update
        print(f"Completed batch {batch_num + 1}/{total_batches}.")
    
    print("Merging completed.")
    return CA_stations_dfs

def create_csv_meteo(CA_stations_dfs):
    output_folder = '../data/processed/ghcn_meteo'
    os.makedirs(output_folder, exist_ok=True)

    years = CA_stations_dfs['Year'].unique()

    for year in years:
        yearly_data = CA_stations_dfs[CA_stations_dfs['Year'] == year]
        output_file = os.path.join(output_folder, f'CA_{year}_meteo.csv')
        yearly_data.to_csv(output_file, index=False)

    print('New datafrane yearly files saved to ghcn_meteo')

def combine_meteo_to_df(folder):
    ''' combines individual csv files into their own dataframes based on year.
    It then concatenates all dataframes into one and returns it.''' 

    dfs = []
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            full_path = os.path.join(folder, filename)
            
            try:
                df = pd.read_csv(full_path, dtype={'County':'str'}, low_memory=False)
                dfs.append(df) 
                print(f"Processed file: {filename}")
            
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")

    CA_stations = pd.concat(dfs, ignore_index=True) # type: ignore

    return CA_stations