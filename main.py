import gzip

# Path to your .gz file
file_path = "Data/GSE116256_RAW/GSM3587923_AML1012-D0.dem.txt.gz"

# Open and read the file
with gzip.open(file_path, 'rt') as f:
    for i, line in enumerate(f):
        print(line.strip())  # Print each line
        if i >= 10:  # Stop after 10 lines
            break
