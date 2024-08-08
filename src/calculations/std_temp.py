import pandas as pd
import os

def calculate_std(df):
    std_values = df.groupby('Year')['temperature'].std()
    return std_values

def main():
    input_directory = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/ghcn_filled'
    output_file = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/temperature_statistics/std_temperature.csv'
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    all_stds = []

    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            input_file = os.path.join(input_directory, filename)
            df = pd.read_csv(input_file)
            std_values = calculate_std(df)
            std_values['Station_ID'] = os.path.splitext(filename)[0]
            all_stds.append(std_values)

    combined_stds = pd.concat(all_stds)
    combined_stds.to_csv(output_file)
    print(f"Standard deviation of temperatures saved to: {output_file}")

if __name__ == "__main__":
    main()
