import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress
import os

# Define the reasonable temperature range
MIN_TEMP = -10
MAX_TEMP = 50

# Load your temperature data
data_folder = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/processed/ghcn_filled/'

# Ensure the plots directory exists
output_dir = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/plots/daily_plots_filtered'
os.makedirs(output_dir, exist_ok=True)

for file_name in os.listdir(data_folder):
    if file_name.endswith('.csv'):
        # Load data
        data_path = os.path.join(data_folder, file_name)
        df = pd.read_csv(data_path)
        
        # Assuming the temperature column exists and filtering out NaN values
        df = df.dropna(subset=['temperature'])

        # Filter out temperature values that are outside the reasonable range
        df = df[(df['temperature'] >= MIN_TEMP) & (df['temperature'] <= MAX_TEMP)]

        # Convert 'Year', 'Month', 'Day' columns to a single datetime column
        df['date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

        # Convert the dates to ordinal format to use in regression
        df['day_of_year'] = df['date'].dt.dayofyear

        # Linear regression
        X = df['day_of_year'].values.reshape(-1, 1)
        y = df['temperature'].values

        # Fit the model
        model = LinearRegression()
        model.fit(X, y)

        # Predict values
        df['predicted_temp'] = model.predict(X)

        # Calculate the slope, intercept, and R^2 value
        slope, intercept, r_value, p_value, std_err = linregress(df['day_of_year'], df['temperature'])

        # Plot the results
        plt.figure(figsize=(10, 6))
        plt.scatter(df['day_of_year'], df['temperature'], color='blue', s=1, label='Observed')
        plt.plot(df['day_of_year'], df['predicted_temp'], color='red', 
                 label=f'Linear fit (slope = {slope:.4f}, R² = {r_value**2:.4f})')
        plt.xlabel('Day of the Year')
        plt.ylabel('Temperature (°C)')
        plt.title(f'Temperature Trend for {df["Year"].iloc[0]}')
        plt.xticks(ticks=np.arange(1, 367, 30), rotation=45)
        plt.legend(loc='upper right')  # Manually set legend location to avoid the "best" calculation
        plt.grid(True)

        # Save the plot
        plot_filename = os.path.join(output_dir, f'temp_trend_{df["Year"].iloc[0]}.png')
        plt.savefig(plot_filename)
        plt.close()
