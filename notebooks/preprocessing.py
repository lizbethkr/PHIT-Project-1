import os
import pandas as pd

def combine_files_to_dfs(folder):
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