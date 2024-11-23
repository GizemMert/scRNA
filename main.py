import gzip

# Path to your .gz file
file_path = "Data/GSE116256-GPL18573_series_matrix.txt.gz"

# Open and read the file
with gzip.open(file_path, 'rt') as f:
    for i, line in enumerate(f):
        print(line.strip())  # Print each line
        if i >= 10:  # Stop after 10 lines
            break
