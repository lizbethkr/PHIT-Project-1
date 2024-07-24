import pandas as pd
import os

def verify_filled_values(file_path):
    print(f"Verifying file: {os.path.basename(file_path)}")
    df = pd.read_csv(file_path)
    nan_count = df['temperature'].isna().sum()
    print(f"Remaining NaN values in 'temperature' column: {nan_count}")

    if nan_count > 0:
        nan_rows = df[df['temperature'].isna()]
        print("Remaining NaN rows:")
        print(nan_rows)

def main():
    directory = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/ghcn_reduced'  # Adjust this path as necessary
    print(f"Checking directory: {directory}")
    
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return
    
    all_files = os.listdir(directory)
    print(f"All files in directory: {all_files}")
    
    # Update pattern to match reduced_CA_stations_*.csv
    files = [f for f in all_files if f.endswith('.csv') and f.startswith('reduced_CA_stations_')]
    print(f"Found {len(files)} files to check.")
    
    if not files:
        print(f"No files found in directory: {directory}")
        return

    for file in files:
        file_path = os.path.join(directory, file)
        print(f"Processing file: {file_path}")
        verify_filled_values(file_path)

if __name__ == "__main__":
    main()
