import os
import gzip
import pandas as pd

# Specify the directory containing the files
data_dir = "Data/GSE116256_RAW"

# Keywords for filtering
include_keywords = ["D0", "BM"]  # Files must include either of these
exclude_keyword = "38n"

# Filter files
filtered_files = [
    file for file in os.listdir(data_dir)
    if any(keyword in file for keyword in include_keywords)  # At least one include keyword
    and exclude_keyword not in file  # Exclude files with "38n"
    and file.endswith(".anno.txt.gz")  # Only process .anno.txt.gz files
]

print(f"Filtered files ({len(filtered_files)}):")
for file in filtered_files:
    print(file)

# Function to parse a single .anno.txt.gz file
def parse_annotation_file(file_path):
    with gzip.open(file_path, 'rt') as f:
        df = pd.read_csv(f, sep="\t")  # Assuming tab-separated values
    return df

# Combine relevant files into a single DataFrame
def load_filtered_annotations(data_dir, filtered_files):
    if not filtered_files:
        raise ValueError("No files matched the filtering criteria.")
    all_data = []
    for file in filtered_files:
        print(f"Parsing {file}...")
        file_path = os.path.join(data_dir, file)
        df = parse_annotation_file(file_path)
        all_data.append(df)
    return pd.concat(all_data, ignore_index=True)

# Load the filtered dataset
try:
    annotations = load_filtered_annotations(data_dir, filtered_files)

    # Check if "DonorID" and "CellType" are in the DataFrame
    required_columns = ["DonorID", "CellType"]
    missing_columns = [col for col in required_columns if col not in annotations.columns]

    if missing_columns:
        print(f"Missing columns: {missing_columns}")
    else:
        print("All required columns are present.")

    if "DonorID" in annotations.columns:
        print("Unique Donor IDs:")
        print(annotations["DonorID"].unique())

    if "CellType" in annotations.columns:
        print("\nUnique Cell Types:")
        print(annotations["CellType"].unique())

    print("Available columns in the annotations DataFrame:")
    print(annotations)


except ValueError as e:
    print(f"Error: {e}")
