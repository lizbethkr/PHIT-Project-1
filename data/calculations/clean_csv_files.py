import pandas as pd

# Function to clean a single CSV file
def clean_csv(file_path):
    df = pd.read_csv(file_path)

    # Assuming the Year column should only contain numeric years, filter out any non-numeric rows
    df = df[pd.to_numeric(df['Year'], errors='coerce').notnull()]

    # Remove any extra columns that are not needed
    if 'Station_ID' in df.columns:
        df = df[['Year', 'temperature']]  # Keep only the 'Year' and 'temperature' columns

    # Save the cleaned DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

    print(f"Cleaned {file_path}")

# Path to the median_temperature.csv file
median_file_path = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/temperature_statistics/median_temperature.csv'

# Clean the median_temperature.csv file
clean_csv(median_file_path)

print("median_temperature.csv file has been cleaned.")
