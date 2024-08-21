import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # Add this import statement
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress
import os

# Define the reasonable temperature range
MIN_TEMP = -10
MAX_TEMP = 55

# Directory containing the yearly data files
data_folder = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/processed/ghcn_clean/'

# Initialize lists to store year and mean temperatures
years = []
mean_temperatures = []

# Iterate over each CSV file in the data folder
for file_name in os.listdir(data_folder):
    if file_name.endswith('.csv'):
        year = int(file_name.split('_')[1])  # Extract year from filename

        if year == 2023:  # Skip the year 2023
            continue

        # Load the data for the current year
        df = pd.read_csv(os.path.join(data_folder, file_name))

        # Correct the column name to match your CSV file
        if 'Temperature' not in df.columns:
            print(f"Skipping file due to missing 'Temperature' column: {file_name}")
            continue

        # Drop NaN values in the 'Temperature' column
        df = df.dropna(subset=['Temperature'])

        # Filter out temperature values that are outside the reasonable range
        df = df[(df['Temperature'] >= MIN_TEMP) & (df['Temperature'] <= MAX_TEMP)]

        # Calculate the mean temperature for the current year
        mean_temp = df['Temperature'].mean()

        # Append the year and mean temperature to the lists
        years.append(year)
        mean_temperatures.append(mean_temp)

# Check if there's any valid data to process
if len(years) == 0 or len(mean_temperatures) == 0:
    print("No valid data to process.")
else:
    # Convert lists to a DataFrame
    df_mean = pd.DataFrame({'Year': years, 'Mean_Temperature': mean_temperatures})

    # Ensure the data is sorted by year
    df_mean = df_mean.sort_values(by='Year')

    # Linear regression
    X = df_mean['Year'].values.reshape(-1, 1)
    y = df_mean['Mean_Temperature'].values

    # Fit the model
    model = LinearRegression()
    model.fit(X, y)

    # Predict values
    df_mean['predicted_temp'] = model.predict(X)

    # Calculate the slope, intercept, and R^2 value
    slope, intercept, r_value, p_value, std_err = linregress(df_mean['Year'], df_mean['Mean_Temperature'])

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.scatter(df_mean['Year'], df_mean['Mean_Temperature'], color='blue', s=50, label='Observed')
    plt.plot(df_mean['Year'], df_mean['predicted_temp'], color='red', 
             label=f'Linear fit (slope = {slope:.4f}, R² = {r_value**2:.4f})')

    plt.xlabel('Year')
    plt.ylabel('Mean Temperature (°C)')
    plt.title('Mean Temperature Trend Over Time')
    plt.xticks(ticks=np.arange(df_mean['Year'].min(), df_mean['Year'].max() + 1, 1))
    plt.grid(True)
    plt.legend(loc='upper right')

    # Save the plot
    output_dir = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/plots'
    plot_filename = os.path.join(output_dir, 'mean_temperature_trend_filtered_no_2023.png')
    plt.savefig(plot_filename)
    plt.show()
