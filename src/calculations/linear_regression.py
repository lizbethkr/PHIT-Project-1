import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress

# Load your temperature data
data_path = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/data/external/temperature_statistics/mean_temperature.csv'
df = pd.read_csv(data_path)

# Ensure the data is sorted by year
df = df.sort_values(by='Year')

# Linear regression
X = df['Year'].values.reshape(-1, 1)
y = df['temperature'].values

# Fit the model
model = LinearRegression()
model.fit(X, y)

# Predict values
df['predicted_temp'] = model.predict(X)

# Calculate the slope, intercept, and R^2 value
slope, intercept, r_value, p_value, std_err = linregress(df['Year'], df['temperature'])

# Plot the results
plt.figure(figsize=(10, 6))
plt.scatter(df['Year'], df['temperature'], color='blue', label='Observed')
plt.plot(df['Year'], df['predicted_temp'], color='red', label=f'Linear fit (slope = {slope:.4f}, R² = {r_value**2:.4f})')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Trend Over Time')
plt.ylim(0, max(df['temperature']) + 1)  # Start y-axis at 0
plt.legend()
plt.grid(True)

# Save the plot to the plots directory
output_path = 'C:/Users/nenao/PHIT-Project-1-New/PHIT-Project-1/plots/linear_regression_plot.png'
plt.savefig(output_path)

plt.show()
