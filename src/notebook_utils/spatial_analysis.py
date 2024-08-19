import streamlit as st
import plotly.express as px
import pandas as pd


def create_interactive_map(ca_gdf):
    ca_gdf['Year'] = ca_gdf['Year'].astype(str)

    min_temp = ca_gdf['Temperature_avg'].min()
    ca_gdf['Temperature_size'] = (ca_gdf['Temperature_avg'] - min_temp + 1).round(1)

    fig = px.scatter_mapbox(
        ca_gdf, 
        lat="Latitude", 
        lon="Longitude", 
        color="Temperature_avg", 
        size="Temperature_size",
        hover_name="Station_name", 
        animation_frame="Year", 
        color_continuous_scale=px.colors.sequential.YlOrRd, 
        size_max=15, 
        zoom=5, 
        mapbox_style="open-street-map",
        title="Average Temperature by Station in California (2003-2023)"
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
            title="Average Temperature",
            titlefont_size=13,
        ),
        updatemenus=[dict(type="buttons", showactive=False, y=-0.09, x=0.0, xanchor="left", yanchor="bottom")],
        sliders=[dict(active=0, y=0.08, x=0.2, xanchor="left", yanchor="top")],
    )

    fig.show()