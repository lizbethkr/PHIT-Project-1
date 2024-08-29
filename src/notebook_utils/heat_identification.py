import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
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
    heat_event_metrics = heat_groups_df.groupby(['Station_name', 'Latitude', 'Longitude', 'heat_event_group', 'Year']).agg(
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
    heat_event_metrics = heat_event_metrics[['Station_name', 'Latitude','Longitude', 'Year', 'heat_event_group', 'Start_date', 'End_date', 'Duration', 'Intensity', 'Frequency']]
    return heat_event_metrics


def create_heat_event_map(ca_gdf):
    ca_gdf['Year'] = ca_gdf['Year'].astype(str)

    min_intensity = ca_gdf['Intensity'].min()
    ca_gdf['Intensity_size'] = (ca_gdf['Intensity'] - min_intensity + 1).round(1)

    min_frequency = ca_gdf['Frequency'].min()
    max_frequency = ca_gdf['Frequency'].max()

    fig = px.scatter_mapbox(
        ca_gdf, 
        lat="Latitude", 
        lon="Longitude", 
        color="Frequency",
        size="Intensity_size",
        hover_name="Station_name", 
        animation_frame="Year", 
        color_continuous_scale=px.colors.sequential.YlOrRd, 
        range_color=[min_frequency, max_frequency], 
        size_max=15, 
        zoom=5, 
        mapbox_style="open-street-map",
        title="Heat Event Occurrence and Intensity in California (2003-2023)"
    )

    fig.update_layout(
        mapbox=dict(
            center={'lat': 37, 'lon': -120},
            zoom=5
        ),
        mapbox_bounds={"west": -130, "east": -110, "south": 30, "north": 43},
        margin={"r": 40, "t": 40, "l": 40, "b": 40},
        width=700,
        height=800,
        coloraxis_colorbar=dict(
            title="Heat Event Frequency",
            titlefont_size=13,
        ),
        updatemenus=[dict(type="buttons", showactive=False, y=-0.09, x=0.0, xanchor="left", yanchor="bottom")],
        sliders=[dict(active=0, y=0.08, x=0.2, xanchor="left", yanchor="top")],
    )

    fig.show()