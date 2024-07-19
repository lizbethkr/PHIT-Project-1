import os
import pandas as pd
import numpy as np

# Define your processed folder where the original processed files are stored
processed_folder = "data/ghcn_reduced"

# Function to read California stations from a text file
def read_california_stations(file_path):
    with open(file_path, 'r') as f:
        stations = [line.strip() for line in f.readlines()]
        half_len = len(stations) // 2
        quarter_piece = stations[half_len + (half_len//2):]
        print(len(quarter_piece)) # 99 stations
    return quarter_piece

# Function to reduce each processed file based on California stations list
def reduce_processed_files(folder, california_stations):
    for filename in os.listdir("data/ghcn_processed"):
        if filename.startswith("CA_stations_") and filename.endswith(".csv"):
            full_path = os.path.join("data/ghcn_processed", filename)
            year = filename.split("_")[2].split(".")[0]
            
            try:
                df = pd.read_csv(full_path, na_values=-999)
                
                # Filter dataframe based on California stations list
                df_filtered = df[df['Station_ID'].isin(california_stations)]

                reduced_filename = f"reduced_{filename}"
                reduced_path = os.path.join(folder, reduced_filename)
                
                df_filtered.to_csv(reduced_path, index=False)
                
                print(f"Reduced file saved: {reduced_filename}")
            
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")

california_stations_file = "data/external/ca_stations.txt"
california_stations = read_california_stations(california_stations_file)

reduce_processed_files(processed_folder, california_stations)
