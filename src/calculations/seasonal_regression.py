import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from scipy.stats import linregress
import matplotlib.pyplot as plt

# Define the reasonable temperature range
MIN_TEMP = -10
MAX_TEMP = 55

# Define the seasons
SEASONS = {
    'Winter': [12, 1, 2],
    'Spring': [3, 4, 5],
    'Summer': [6, 7, 8],
    'Fall': [9, 10, 11]
}

# Directory containing the cleaned data files
data_folder = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/processed/ghcn_clean/'

# Ensure the plots directory exists
output_dir = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/plots/seasonal_plots_with_season_as_predictor'
os.makedirs(output_dir, exist_ok=True)

# Initialize lists to store year, season, and mean temperatures
years = []
seasons = []
mean_temperatures = []

# Iterate over each CSV file in the data folder
for file_name in os.listdir(data_folder):
    if file_name.endswith('.csv'):
        year = int(file_name.split('_')[1])  # Extract year from filename
        if year == 2023:  # Skip the year 2023
            continue

        # Load the data for the current year
        df = pd.read_csv(os.path.join(data_folder, file_name))

        # Assuming the 'Temperature' column exists and filtering out NaN values
        df = df.dropna(subset=['Temperature'])

        # Filter out temperature values that are outside the reasonable range
        df = df[(df['Temperature'] >= MIN_TEMP) & (df['Temperature'] <= MAX_TEMP)]

        # Add season information based on the month
        df['Season'] = df['Month'].apply(lambda x: next(season for season, months in SEASONS.items() if x in months))

        # Calculate the mean temperature for each season
        for season_name in SEASONS.keys():
            df_season = df[df['Season'] == season_name]
            if not df_season.empty:
                mean_temp = df_season['Temperature'].mean()
                years.append(year)
                seasons.append(season_name)
                mean_temperatures.append(mean_temp)

# Convert lists to a DataFrame
df_mean = pd.DataFrame({'Year': years, 'Season': seasons, 'Mean_Temperature': mean_temperatures})

# Encode the seasons as categorical variables
encoder = OneHotEncoder()
season_encoded = encoder.fit_transform(df_mean[['Season']]).toarray()
season_labels = encoder.categories_[0]

# Prepare the input features
X = np.hstack([df_mean['Year'].values.reshape(-1, 1), season_encoded])
y = df_mean['Mean_Temperature'].values

# Fit the model
model = LinearRegression()
model.fit(X, y)

# Predict values
df_mean['predicted_temp'] = model.predict(X)

# Calculate the slope, intercept, and R^2 value for each season
for season_name in SEASONS.keys():
    df_season = df_mean[df_mean['Season'] == season_name]
    slope, intercept, r_value, p_value, std_err = linregress(df_season['Year'], df_season['Mean_Temperature'])
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.scatter(df_season['Year'], df_season['Mean_Temperature'], color='blue', s=50, label='Observed')
    plt.plot(df_season['Year'], df_season['predicted_temp'], color='red', 
             label=f'Linear fit (slope = {slope:.4f}, R² = {r_value**2:.4f})')
    plt.xlabel('Year')
    plt.ylabel('Mean Temperature (°C)')
    plt.title(f'{season_name} Temperature Trend Over Time')
    plt.xticks(ticks=np.arange(df_season['Year'].min(), df_season['Year'].max() + 1, 1))
    plt.grid(True)
    plt.legend(loc='upper right')

    # Save the plot
    plot_filename = os.path.join(output_dir, f'{season_name.lower()}_temperature_trend_with_season_as_predictor.png')
    plt.savefig(plot_filename)
    plt.close()

    print(f"Plot saved for {season_name} to {plot_filename}")
