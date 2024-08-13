import os
import pandas as pd
import sys

curr_dir = os.path.dirname('src\data_processing')
proj_dir = os.path.dirname(curr_dir)
src_path = os.path.join(proj_dir, 'src', 'notebook_utils')
sys.path.append(src_path)

from preprocessing import read_ca_stations # type: ignore
from preprocessing import read_qrt_stations

# Function to reduce each processed file based on California stations list
def reduce_processed_files(folder, california_stations):
    for filename in os.listdir("data/raw/ghcn_csv"):
        if filename.startswith("CA_stations_") and filename.endswith(".csv"):
            full_path = os.path.join("data/raw/ghcn_csv", filename)
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

def full_processed_files(folder, california_stations):
    for filename in os.listdir("data/raw/ghcn_csv"):
        if filename.startswith("CA_stations_") and filename.endswith(".csv"):
            full_path = os.path.join("data/raw/ghcn_csv", filename)
            year = filename.split("_")[2].split(".")[0]
            
            try:
                df = pd.read_csv(full_path, na_values=-999)

                reduced_filename = f"full_{filename}"
                reduced_path = os.path.join(folder, reduced_filename)
                
                df.to_csv(reduced_path, index=False)
                
                print(f"Full file saved: {reduced_filename}")
            
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")

def get_reduced_ver():
    california_stations = read_qrt_stations()
    reduce_processed_files('data/processed/ghcn_reduced', california_stations)

def get_full_ver():
    california_stations = read_ca_stations()
    reduce_processed_files('data/processed/ghcn_full', california_stations)

if __name__ == '__main__':
    get_full_ver()