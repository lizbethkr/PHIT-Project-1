import pandas as pd
import os

# Directory paths
data_directory = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/ghcn_filled/'
stats_directory = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/temperature_statistics/'
output_file = os.path.join(stats_directory, 'verification_results.txt')

# Open the output file in write mode
with open(output_file, 'w') as output:
    # Get the list of all processed files (one for each year)
    processed_files = os.listdir(data_directory)

    # Verify each year separately
    for file in processed_files:
        # Skip any non-CSV files
        if not file.endswith('.csv'):
            continue

        year = file.split('_')[-1].split('.')[0]  # Extract the year from the filename

        # Load the original data for the specific year
        original_df = pd.read_csv(os.path.join(data_directory, file))

        # Calculate mean, median, and standard deviation manually
        manual_mean = original_df['filled_temperature'].mean()
        manual_median = original_df['filled_temperature'].median()
        manual_stddev = original_df['filled_temperature'].std()

        # Load the corresponding stats file for the year
        mean_df = pd.read_csv(os.path.join(stats_directory, 'mean_temperature.csv'))
        median_df = pd.read_csv(os.path.join(stats_directory, 'median_temperature.csv'))
        std_df = pd.read_csv(os.path.join(stats_directory, 'std_temperature.csv'))

        # Filter the stats dataframe for the specific year
        mean_value = mean_df[mean_df['Year'] == int(year)]['temperature'].values[0]
        median_value = median_df[median_df['Year'] == int(year)]['temperature'].values[0]
        std_value = std_df[std_df['Year'] == int(year)]['temperature'].values[0]

        # Compare the values
        mean_diff = mean_value - manual_mean
        median_diff = median_value - manual_median
        std_diff = std_value - manual_stddev

        # Write the results to the output file
        output.write(f"Year: {year}\n")
        output.write(f"Mean: Calculated = {mean_value}, Manual = {manual_mean}, Difference = {mean_diff}\n")
        output.write(f"Median: Calculated = {median_value}, Manual = {manual_median}, Difference = {median_diff}\n")
        output.write(f"Standard Deviation: Calculated = {std_value}, Manual = {manual_stddev}, Difference = {std_diff}\n")
        output.write("-" * 50 + "\n")

print(f"Verification findings have been saved to {output_file}")
