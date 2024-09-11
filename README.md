# PHIT-Project 1
This project is for UCI's Public Health Informatics and Technology (PHIT) internship with [Wu Enviornmental Lab]([https://drwulab.net/]) at UCI.

#### -- Project Status: [Active]

## Project Intro/Objective
The purpose of this project is to understand the importance of monitoring temperature trends and the impact of extreme heat events on public health and the enviornment. This will be done via understanding spatiotemporal and diurnal variations of temperatures, distinguishing between urban and rural areas, and identifying heat events in California over the past 20 years using hourly data. 

### Technologies
* Python
* Pandas, jupyter


## Project Description
(Provide more detailed overview of the project.  Talk a bit about your data sources and what questions and hypothesis you are exploring. What specific data analysis/visualization and modelling work are you using to solve the problem? 

Questions: 
1. Spatiotemporal Variation in Temperatures:
   - How do temperature patterns vary across different geographical regions and over time?
   - Identify areas most susceptible to rapid temperature changes and extreme heat events.
3. Impact of Extreme Heat Events:
   - Assess the immediate and long-term effects of extreme heat events on local ecosystems and urban environments.
   - Evaluate the resilience of various land-use types to increasing temperatures.
4. Interactions Between Land-Use, Vegetation, and Temperature:
   - Investigate how different land-use practices and vegetation cover contribute to the urban heat island effect.
   - Determine the role of green spaces in mitigating heat and supporting ecosystem and public health.
5. Influence on Population Health:
   - Analyze the correlation between temperature variations/extreme heat events and public health outcomes.
   - Identify vulnerable populations and areas with high health risks due to heat stress.

## Data Folder Structure
The data directory contains 3 sub folders: external, processed, and raw. 

1. raw/
   a. ghcn_csv/
      - Contains a CSV-format version of the origianl GHCN hourly dataset with only California Stations, and with only relevant columns.
   b. ghcn_raw/
      - Contains the rawest form of the CHCN hourly data for California stations, with all columns.
   c. shapefiles/
      - Contains geographic shapefiles specific to California, which are used for mapping and spatial analysis.
2. processed/
   a. ghcn_clean/
      - Contains cleaned hourly temperature data for CA stations. 
   b. ghcn_cleaned/
      - Contains files identical to the files in ghcn_clean, except it has 2 extra columns: County and City.
   c. ghcn_meteo_cleaned/
      - Contains files from ghcn_cleaned, but with relative_humidity, wind_speed, and precipitation columns merged and cleaned.
   d. ghcn_full/
      - Contains all hourly temperature observations for CA stations.
   e. ghcn_reduced/
      - Contains only the last fourth of CA station hourly temperature data. The purpose is to speed up the process for creating code to process it.
3. external/
   a. ghcn_filled.txt/
      - Contains files listing filled temperature values.
   b. temperature_statistics/
      - Contains files summarising statitics for all of the temperature observations.
   c. ca_stations.txt
      - TXT file containing all California Station_ID's within the GHCN hourly dataset.

## References
NOAA National Centers for Environmental Information. (2024). Global Historical Climatology Network (GHCN) - Hourly Data. NOAA. https://www.ncei.noaa.gov/products/land-based-station/ghcn-hourly

Hulley, G.C., Dousset, B. and Kahn, B.H., 2020. Rising trends in heatwave metrics across southern California. Earth's Future, 8(7), p.e2020EF001480.

