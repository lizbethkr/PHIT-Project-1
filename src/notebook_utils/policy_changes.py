import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def trend_analysis(df, start_date, end_date, policy_name):
    # Filter data for the specified period
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

    df_period = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]
    
    # Extract year from the date
    df_period['Year'] = df_period['datetime'].dt.year
    yearly_avg_temp = df_period.groupby('Year')['Temperature'].mean().reset_index()

    # Prepare data for linear regression
    X = sm.add_constant(yearly_avg_temp['Year'])
    y = yearly_avg_temp['Temperature']

    # Fit the linear regression model
    model = sm.OLS(y, X).fit()

    # Plot the trend
    plt.plot(yearly_avg_temp['Year'], yearly_avg_temp['Temperature'], label=f'{policy_name} Trend')
    plt.xlabel('Year')
    plt.ylabel('Avg Temperature')
    plt.title(f'Temperature Trend Analysis: {policy_name}')
    plt.show()

    print(model.summary())

def calc_metrics(df):
    return df.groupby(['Year', 'Station_name']).agg({
        'heat_event_group': 'nunique',
        'Duration': 'mean',
        'Intensity': 'mean'
    }).reset_index().rename(columns={'heat_event_group': 'Frequency'})