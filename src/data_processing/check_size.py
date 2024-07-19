import os

# Change to the directory containing your CSV files
directory = 'data/ghcn_reduced'

# Get the list of CSV files
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# Calculate the total size
total_size = sum(os.path.getsize(os.path.join(directory, f)) for f in csv_files)

# Convert to megabytes
total_size_mb = total_size / (1024 * 1024)

# Print the size of each file and the total size
for f in csv_files:
    file_size = os.path.getsize(os.path.join(directory, f)) / (1024 * 1024)
    print(f"{f}: {file_size:.2f} MB")

print(f"Total size: {total_size_mb:.2f} MB")
