import pandas as pd
import os

def fill_if_sandwiched(series):
    series_filled = series.copy()
    changes = []
    for i in range(1, len(series) - 1):
        if pd.isna(series.iloc[i]):
            if not pd.isna(series.iloc[i - 1]) and not pd.isna(series.iloc[i + 1]):
                series_filled.iloc[i] = (series.iloc[i - 1] + series.iloc[i + 1]) / 2
                changes.append(series.index[i])  # Use the original index
    return series_filled, changes

def fill_nan_sandwiched(input_file, output_file, txt_output_file):
    print(f"Processing file: {input_file}")
    
    df = pd.read_csv(input_file)
    
    filled_temperatures = []
    changes_log = []

    for name, group in df.groupby('Station_ID'):
        filled_group, changes = fill_if_sandwiched(group['temperature'])
        filled_temperatures.extend(filled_group)
        for change in changes:
            changes_log.append((name, change, group.loc[change, 'temperature'], filled_group.loc[change]))

    df['filled_temperature'] = filled_temperatures

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    os.makedirs(os.path.dirname(txt_output_file), exist_ok=True)
    
    # Save the filled dataframe to the output directory
    df.to_csv(output_file, index=False)
    
    # Log changes
    with open(txt_output_file, 'w') as log_file:
        log_file.write('Station_ID,Index,Original_Temperature,Filled_Temperature\n')
        for log in changes_log:
            log_file.write(f"{log[0]},{log[1]},{log[2]},{log[3]}\n")
    
    print(f"Filled data saved to: {output_file}")
    print(f"Changes log saved to: {txt_output_file}")

def main():
    input_directory = '../data/ghcn_reduced'
    output_directory = '../data/ghcn_filled'
    txt_output_directory = '../data/ghcn_filled_txt'
    
    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, f'filled_{filename}')
            txt_output_file = os.path.join(txt_output_directory, f'filled_{filename.replace(".csv", "_changes.txt")}')
            fill_nan_sandwiched(input_file, output_file, txt_output_file)

if __name__ == "__main__":
    main()
