import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress
import matplotlib.pyplot as plt

# Define the reasonable temperature range
MIN_TEMP = -10
MAX_TEMP = 55

# Directory containing the cleaned data files
data_folder = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/processed/ghcn_clean/'

# Ensure the new plots directory exists
output_dir = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/plots/city_temperature_trends'
os.makedirs(output_dir, exist_ok=True)

# Map of latitude and longitude to city names (example mapping)
coordinates_to_city = {
    (38.9547, -121.0819): 'Auburn',
    (34.0522, -118.2437): 'Los Angeles',
    (37.7749, -122.4194): 'San Francisco',
    # Add more mappings as needed
}

# Initialize lists to store year, latitude, longitude, and mean temperatures
years = []
cities = []
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

        # Group data by station (latitude and longitude)
        for (latitude, longitude), group in df.groupby(['Latitude', 'Longitude']):
            mean_temp = group['Temperature'].mean()
            city = coordinates_to_city.get((latitude, longitude), None)

            if city is None:
                # Handle unknown coordinates by using "Unknown" as the city name
                city = f'Unknown_Lat_{latitude}_Long_{longitude}'
            else:
                city = city.replace(":", "-")  # Replace any invalid characters
            
            cities.append(city)
            years.append(year)
            mean_temperatures.append(mean_temp)

# Convert lists to a DataFrame
df_mean = pd.DataFrame({
    'Year': years,
    'City': cities,
    'Mean_Temperature': mean_temperatures
})

# Prepare the input features
X = pd.get_dummies(df_mean[['Year', 'City']], drop_first=True).values
y = df_mean['Mean_Temperature'].values

# Fit the model
model = LinearRegression()
model.fit(X, y)

# Predict values
df_mean['predicted_temp'] = model.predict(X)

# Plot the results (one plot per city)
for city, group in df_mean.groupby('City'):
    slope, intercept, r_value, p_value, std_err = linregress(group['Year'], group['Mean_Temperature'])

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.scatter(group['Year'], group['Mean_Temperature'], color='blue', s=50, label='Observed')
    plt.plot(group['Year'], group['predicted_temp'], color='red', 
             label=f'Linear fit (slope = {slope:.4f}, R² = {r_value**2:.4f})')
    plt.xlabel('Year')
    plt.ylabel('Mean Temperature (°C)')
    plt.title(f'Temperature Trend for {city}')
    plt.xticks(ticks=np.arange(group['Year'].min(), group['Year'].max() + 1, 1))
    plt.grid(True)
    plt.legend(loc='upper right')

    # Save the plot
    plot_filename = os.path.join(output_dir, f'temp_trend_{city}.png')
    plt.savefig(plot_filename)
    plt.close()

    print(f"Plot saved for {city} to {plot_filename}")
