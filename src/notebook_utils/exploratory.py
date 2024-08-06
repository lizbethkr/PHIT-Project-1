import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
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

def plot_diurnal_cycle(group_id, group_data, output_dir, group_type):
    '''Plot diurnal cycle and save plot specified station.'''

    fig, axs = plt.subplots(2, 1, figsize=(14, 14))
    
    # Plot diurnal patterns across different seasons
    sns.lineplot(ax=axs[0], data=group_data, x='Hour', y='Temperature', hue='Season', marker='o')
    axs[0].set_title(f'Hourly Temperature Patterns for {group_type} {group_id} by Season')
    axs[0].set_xlabel('Hour of the Day')
    axs[0].set_ylabel('Temperature (°C)')
    axs[0].legend(title='Season')
    axs[0].set_xticks(range(0, 24))
    axs[0].grid(True)

    # Plot diurnal patterns across different years
    sns.lineplot(ax=axs[1], data=group_data, x='Hour', y='Temperature', hue='Year', palette='tab20', marker='o', errorbar=None)
    axs[1].set_title(f'Hourly Temperature Patterns for {group_type} {group_id} by Year')
    axs[1].set_xlabel('Hour of the Day')
    axs[1].set_ylabel('Temperature (°C)')
    axs[1].legend(title='Year', loc='upper right', bbox_to_anchor=(1, 1))
    axs[1].set_xticks(range(0, 24))
    axs[1].grid(True)

    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f'{group_id}_diurnal_cycle.png')
    plt.savefig(file_path)
    plt.close()

def get_diurnal_info(group_data):
    diurnal_data = group_data.groupby(['Year','Season','Hour']).agg({'Temperature':'mean'}).reset_index()
    return diurnal_data

def save_diurnal_plots(df, output_dir, group_col, group_type):
    group_ids = df[group_col].unique()
    for group_id in group_ids:
        group_data = df[df[group_col] == group_id]
        diurnal_data = get_diurnal_info(group_data)
        plot_diurnal_cycle(group_id, diurnal_data, output_dir, group_type)
        print(f'Plotted and saved dirunal cycle patterns for {group_type}: {group_id}')

    print('Plotted and saved diurnal cycle plots for all stations.')

def get_county(latitude, longitude, geolocator):
    ''' Use geolocator to find the county name using latitude and longitude.'''

    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True, timeout=10)
        if location:
            address = location.raw['address']
            return address.get('county', '')
        
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f'Error: {e}')

    return 'Unknown'

def get_city(latitude,longitude, geolocator):
    ''' Use geolocator to find the city name using latitude and longitude.'''

    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True, timeout=10)
        if location:
            address = location.raw['address']
            return address.get('city', '') or address.get('town', '')
        
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f'Error: {e}')

    return 'Unknown'

def station_geo(df,geolocator):
    '''Find county and city names for all stations.'''
    
    unique_stations = df[['Station_ID','Latitude', 'Longitude']].drop_duplicates()
    station_county = {}
    station_city = {}

    for _,row in unique_stations.iterrows():
        latitude, longitude = row['Latitude'], row['Longitude']
        station_id = row['Station_ID']
        
        # get county and city for the station
        county = get_county(latitude, longitude, geolocator)
        city = get_city(latitude, longitude, geolocator)
        
        # save county and city name
        station_county[station_id] = county
        station_city[station_id] = city

        print('County and city name saved.')

    # create dataframes
    station_info_df = pd.DataFrame({
        'Station_ID': station_county.keys(),
        'County': station_county.values(),
        'City': station_city.values()
    })

    return station_info_df

def add_county_city(df, station_data_df):
    df = df.merge(station_data_df, on='Station_ID', how='left')
    df['County'] = df['County'].fillna('Unknown')
    df['City'] = df['City'].fillna('Unknown')
    
    return df