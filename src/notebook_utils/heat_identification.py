import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
from scipy import stats
import sys
import os


def calc_rolling_percentile(series, window_size=15, percentile=95):
    return series.rolling(window=window_size, center=False).quantile(percentile / 100)


def identify_heat_groups(daily_temp):
    # Create a temp column to identify new heat event groups
    daily_temp['heat_event_change'] = daily_temp['heat_event'].shift(1, fill_value=False) != daily_temp['heat_event']

    # Assign a unique group number to each heat event group
    daily_temp['heat_event_group'] = (daily_temp['heat_event_change'] & daily_temp['heat_event']).cumsum()

    # Fill forward the group number for days within a heat event and drop rows where heat_event_groip is NaN
    daily_temp['heat_event_group'] = daily_temp['heat_event_group'].where(daily_temp['heat_event'], np.nan).ffill()
    daily_temp.dropna(subset=['heat_event_group'], inplace=True)
    daily_temp.drop(columns=['heat_event_change'], inplace=True)

    # filter out groups with less than 3 days of heat events
    valid_groups = daily_temp.groupby('heat_event_group').filter(lambda x: x['heat_event'].sum() >= 2)
    valid_groups.reset_index(drop=True, inplace=True)
    filtered_df = valid_groups[valid_groups['heat_event']].copy()

    # Renumber the groups
    group_mapping = {old_group: new_group for new_group, old_group in enumerate(filtered_df['heat_event_group'].unique(), start=1)}
    filtered_df['heat_event_group'] = filtered_df['heat_event_group'].map(group_mapping)
    filtered_df.reset_index(drop=True, inplace=True)
    
    return filtered_df


def calc_heat_event_metrics(heat_groups_df):
    # Create a Year Column
    heat_groups_df['Date'] = pd.to_datetime(heat_groups_df['Date'])
    heat_groups_df['Year'] = heat_groups_df['Date'].dt.year

    # Calculate the duration and intensity of each heat event group per station per year
    heat_event_metrics = heat_groups_df.groupby(['Station_name', 'heat_event_group', 'Year']).agg(
        Start_date = ('Date', 'first'),
        End_date = ('Date', 'last'),
        Duration = ('Date', 'count'),
        Intensity = ('Tmax', lambda x: (x.max() - heat_groups_df.loc[x.idxmax(), 'CTX95pct'])),
    ).reset_index()

    # Calculte Station_year_frequency
    station_year_frequency = heat_event_metrics.groupby(['Station_name', 'Year']).agg(
        Frequency = ('heat_event_group', 'count')
    ).reset_index()

    # Merge the heat event metrics with the station year frequency
    heat_event_metrics = heat_event_metrics.merge(station_year_frequency, on=['Station_name', 'Year'])

    # Reorder and rename columns
    heat_event_metrics = heat_event_metrics[['Station_name', 'Year', 'heat_event_group', 'Start_date', 'End_date', 'Duration', 'Intensity', 'Frequency']]
    return heat_event_metrics