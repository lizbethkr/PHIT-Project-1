import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

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

def plot_diurnal_cycle(station_id, station_data, output_dir):
    '''Plot diurnal cycle and save plot specified station.'''

    fig, axs = plt.subplots(2, 1, figsize=(14, 14))
    
    # Plot diurnal patterns across different seasons
    sns.lineplot(ax=axs[0], data=station_data, x='Hour', y='Temperature', hue='Season', marker='o')
    axs[0].set_title(f'Hourly Temperature Patterns for Station {station_id} by Season')
    axs[0].set_xlabel('Hour of the Day')
    axs[0].set_ylabel('Temperature (°C)')
    axs[0].legend(title='Season')
    axs[0].set_xticks(range(0, 24))
    axs[0].grid(True)

    # Plot diurnal patterns across different years
    sns.lineplot(ax=axs[1], data=station_data, x='Hour', y='Temperature', hue='Year', palette='tab20', marker='o', errorbar=None)
    axs[1].set_title(f'Hourly Temperature Patterns for Station {station_id} by Year')
    axs[1].set_xlabel('Hour of the Day')
    axs[1].set_ylabel('Temperature (°C)')
    axs[1].legend(title='Year', loc='upper right', bbox_to_anchor=(1, 1))
    axs[1].set_xticks(range(0, 24))
    axs[1].grid(True)

    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f'{station_id}_diurnal_cycle.png')
    plt.savefig(file_path)
    plt.close()

def get_diurnal_info(station_data):
    diurnal_data = station_data.groupby(['Year','Season','Hour']).agg({'Temperature':'mean'}).reset_index()
    return diurnal_data

def save_dirunal_plots(df, output_dir):
    station_ids = df['Station_ID'].unique()
    for station_id in station_ids:
        station_data = df[df['Station_ID'] == station_id]
        diurnal_data = get_diurnal_info(station_data)
        plot_diurnal_cycle(station_id, diurnal_data, output_dir)
        print(f'Plotted and saved dirunal cycle patterns for station: {station_id}')

    print('Plotted and saved diurnal cycle plots for all stations.')

