import pandas as pd
import numpy as np

def verify_filled(file_path):
    df = pd.read_csv(file_path)
    errors = []
    
    for i in range(1, len(df) - 1):
        if not pd.isna(df.iloc[i]['temperature']):
            if pd.isna(df.iloc[i - 1]['temperature']) or pd.isna(df.iloc[i + 1]['temperature']):
                errors.append(f"Error: Filled value at index {i} which is not sandwiched between non-NaN values.")
            else:
                print(f"Correctly filled NaN value at index {i} sandwiched between non-NaN values.")
    
    for error in errors:
        print(error)

if __name__ == "__main__":
    file_path = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/ghcn_filled/filled_CA_stations_2003_revised.csv'
    verify_filled(file_path)
