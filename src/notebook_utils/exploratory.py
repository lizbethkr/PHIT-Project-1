import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Source code for exploratory_data_analysis notebook in notebooks folder
def assign_season(month):
    ''' Map specific months to a season.'''
    
    if month in [12,1,2]:
        return 'Winter'
    elif month in [3,4,5]:
        return 'Spring'
    elif month in [6,7,8]:
        return 'Summer'
    elif month in [9,10,11]:
        return 'Fall'
    
def get_representative_stations(df):
    '''Calculate statistics for each station, identify representative stations,
    and return a dictionary of stations that should be presented.'''

    station_stats = df.groupby('Station_ID').agg(
        Mean_Temp = ('Temperature', 'mean'),
        Max_Temp = ('Temperature', 'mean'),
        Min_Temp = ('Temperature', 'min'),
        Temp_Range = ('Temperature', lambda x:x.max() - x.min())
    ).reset_index()

    highest_mean = station_stats.loc[station_stats['Mean_Temp'].idxmax()]
    lowest_mean = station_stats.loc[station_stats['Mean_Temp'].idxmin()]
    max_temp = station_stats.loc[station_stats['Max_Temp'].idxmax()]
    min_temp = station_stats.loc[station_stats['Min_Temp'].idxmin()]
    largest_range = station_stats.loc[station_stats['Temp_Range'].idxmax()]

    # dictionary to return

    rep_stations = {
        'Highest_Mean_Temp': highest_mean,
        'Lowest_Mean_Temp': lowest_mean,
        'Highest_Temp': max_temp,
        'Lowest_Temp': min_temp,
        'Largest_Range': largest_range
    }
    return rep_stations

def plot_diurnal_cycle(station_id, station_data):
    '''Plot diurnal cycle and save plot specified station.'''

    plt.figure(figsize=(14, 7))
    sns.lineplot(data=station_data, x='Hour', y='Temperature', hue='Season', marker='o')
    plt.title(f'Hourly Temperature Patterns for Station {station_id}')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Temperature (°C)')
    plt.legend(title= 'Season')
    plt.xticks(range(0,24))
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f'{station_id}_diurnal_cycle.png')
    plt.close()

