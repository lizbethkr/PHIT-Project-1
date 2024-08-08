import pandas as pd
import os

def calculate_mean(df):
    mean_values = df.groupby('Year')['temperature'].mean()
    return mean_values

def main():
    input_directory = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/ghcn_filled'
    output_file = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/temperature_statistics/mean_temperature.csv'

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    all_means = []

    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            input_file = os.path.join(input_directory, filename)
            df = pd.read_csv(input_file)
            mean_values = calculate_mean(df)
            mean_values['Station_ID'] = os.path.splitext(filename)[0]
            all_means.append(mean_values)

    combined_means = pd.concat(all_means)
    combined_means.to_csv(output_file)
    print(f"Mean temperatures saved to: {output_file}")

if __name__ == "__main__":
    main()
