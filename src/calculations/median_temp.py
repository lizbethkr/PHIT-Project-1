import pandas as pd
import os

def calculate_median(df):
    median_values = df.groupby('Year')['temperature'].median()
    return median_values

def main():
    input_directory = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/ghcn_filled'
    output_file = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/temperature_statistics/median_temperature.csv'
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    all_medians = []

    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            input_file = os.path.join(input_directory, filename)
            df = pd.read_csv(input_file)
            median_values = calculate_median(df)
            median_values = median_values.reset_index()  # Reset index to include 'Year' in output
            median_values['Station_ID'] = os.path.splitext(filename)[0]
            all_medians.append(median_values)

    combined_medians = pd.concat(all_medians, ignore_index=True)
    combined_medians.to_csv(output_file, index=False)
    print(f"Median temperatures saved to: {output_file}")

if __name__ == "__main__":
    main()
