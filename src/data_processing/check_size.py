import os

# Run this code to check the size of the files within ghcn_reduced

directory = 'data/ghcn_clean'

csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

total_size = sum(os.path.getsize(os.path.join(directory, f)) for f in csv_files)

total_size_mb = total_size / (1024 * 1024)

for f in csv_files:
    file_size = os.path.getsize(os.path.join(directory, f)) / (1024 * 1024)
    print(f"{f}: {file_size:.2f} MB")

print(f"Total size: {total_size_mb:.2f} MB")
