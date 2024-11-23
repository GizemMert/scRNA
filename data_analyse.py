import os
import gzip
import pandas as pd

# Specify the directory containing the files
data_dir = "/home/aih/gizem.mert/scRNA/scRNA/Data/GSE116256_RAW"

# Criteria for filtering
day_0_keyword = "-D0"
bm_keyword = "BM"
exclude_keyword = "38n"

# Filter files
filtered_files = [
    file for file in os.listdir(data_dir)
    if day_0_keyword in file and bm_keyword in file and exclude_keyword not in file and file.endswith(".anno.txt.gz")
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
    all_data = []
    for file in filtered_files:
        print(f"Parsing {file}...")
        file_path = os.path.join(data_dir, file)
        df = parse_annotation_file(file_path)
        all_data.append(df)
    return pd.concat(all_data, ignore_index=True)

# Load the filtered dataset
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
print(annotations.columns.tolist())

