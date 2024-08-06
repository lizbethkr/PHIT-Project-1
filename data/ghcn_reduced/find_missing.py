import pandas as pd
import os

def fill_missing_values(file_path, output_directory):
    print(f"Processing file: {os.path.basename(file_path)}")
    df = pd.read_csv(file_path)

    # Fill missing values using forward fill method only for NaNs in between non-NaNs
    df['temperature'] = df['temperature'].fillna(method='ffill').fillna(method='bfill')

    # Check if there are any remaining NaN values
    nan_count = df['temperature'].isna().sum()
    print(f"Remaining NaN values in 'temperature' column after filling: {nan_count}")

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Save the filled dataframe back to a new CSV file in the output directory
    output_file_path = os.path.join(output_directory, os.path.basename(file_path).replace('reduced_CA_stations_', 'filled_CA_stations_'))
    df.to_csv(output_file_path, index=False)
    print(f"Filled data saved to: {output_file_path}")

def main():
    input_directory = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/ghcn_reduced'  # Adjust this path as necessary
    output_directory = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/ghcn_filled'  # Adjust this path as necessary
    print(f"Checking directory: {input_directory}")
    
    if not os.path.exists(input_directory):
        print(f"Input directory does not exist: {input_directory}")
        return
    
    all_files = os.listdir(input_directory)
    print(f"All files in directory: {all_files}")
    
    # Update pattern to match reduced_CA_stations_*.csv
    files = [f for f in all_files if f.endswith('.csv') and f.startswith('reduced_CA_stations_')]
    print(f"Found {len(files)} files to process.")
    
    if not files:
        print(f"No files found in directory: {input_directory}")
        return

    for file in files:
        file_path = os.path.join(input_directory, file)
        fill_missing_values(file_path, output_directory)

if __name__ == "__main__":
    main()
