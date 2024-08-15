import pandas as pd
import numpy as np
import os
from scipy.stats import kendalltau

# Define the reasonable temperature range
MIN_TEMP = -10
MAX_TEMP = 55

# Directory containing the yearly data files
data_folder = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/processed/ghcn_filled/'

# Initialize lists to store year and mean temperatures
years = []
mean_temperatures = []

# Iterate over each CSV file in the data folder
for file_name in os.listdir(data_folder):
    if file_name.endswith('.csv'):
        year = int(file_name.split('_')[-1].split('.')[0])  # Extract year from filename
        if year == 2023:  # Skip the year 2023
            continue

        # Load the data for the current year
        df = pd.read_csv(os.path.join(data_folder, file_name))

        # Assuming the temperature column exists and filtering out NaN values
        df = df.dropna(subset=['temperature'])

        # Filter out temperature values that are outside the reasonable range
        df = df[(df['temperature'] >= MIN_TEMP) & (df['temperature'] <= MAX_TEMP)]

        # Calculate the mean temperature for the current year
        mean_temp = df['temperature'].mean()

        # Append the year and mean temperature to the lists
        years.append(year)
        mean_temperatures.append(mean_temp)

# Convert lists to a DataFrame
df_mean = pd.DataFrame({'Year': years, 'Mean_Temperature': mean_temperatures})

# Sort the data by year
df_mean = df_mean.sort_values(by='Year')

# Perform the Kendall Tau test (alternative to Mann-Kendall)
tau, p_value = kendalltau(df_mean['Year'], df_mean['Mean_Temperature'])

# Output the results
result_output = f"Kendall Tau tau: {tau}\nP-value: {p_value}\n"

if p_value < 0.05:
    result_output += "There is a statistically significant trend.\n"
else:
    result_output += "There is no statistically significant trend.\n"

# Save the results to a CSV file
output_dir = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/plots'
result_filename = os.path.join(output_dir, 'kendall_tau_results_filtered_no_2023.csv')

df_results = pd.DataFrame({
    "Kendall Tau tau": [tau],
    "P-value": [p_value],
    "Significant Trend": ["Yes" if p_value < 0.05 else "No"]
})

df_results.to_csv(result_filename, index=False)

print(f"Results saved to: {result_filename}")
