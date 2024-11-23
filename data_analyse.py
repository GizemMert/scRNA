import os
import gzip
import pandas as pd

# Specify the directory containing the files
data_dir = "Data/GSE116256_RAW"

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
def parse_annotation_file(file_path, donor_id):
    with gzip.open(file_path, 'rt') as f:
        df = pd.read_csv(f, sep="\t")  # Assuming tab-separated values
        df["DonorID"] = donor_id  # Add the DonorID column
    return df


# Combine relevant files into a single DataFrame
def load_filtered_annotations(data_dir, filtered_files):
    all_data = []
    for file in filtered_files:
        print(f"Parsing {file}...")
        file_path = os.path.join(data_dir, file)

        # Extract DonorID from file name (e.g., AML419A from GSM3587954_AML419A-D0.anno.txt.gz)
        donor_id = file.split("_")[1].split("-")[0]

        df = parse_annotation_file(file_path, donor_id)
        all_data.append(df)
    return pd.concat(all_data, ignore_index=True)


# Load the filtered dataset
annotations = load_filtered_annotations(data_dir, filtered_files)

# Check for required columns
required_columns = ["DonorID", "CellType"]
missing_columns = [col for col in required_columns if col not in annotations.columns]

if missing_columns:
    print(f"Missing columns: {missing_columns}")
else:
    print("All required columns are present.")

# Display donor IDs and unique cell types
if "DonorID" in annotations.columns:
    print("Unique Donor IDs:")
    print(annotations["DonorID"].unique())

if "CellType" in annotations.columns:
    print("\nUnique Cell Types:")
    print(annotations["CellType"].unique())

# Display DataFrame structure
print("\nAvailable columns in the annotations DataFrame:")
print(annotations.columns.tolist())

# Save the annotations DataFrame to a CSV file
output_csv_path = "annotations_filtered.csv"
annotations.to_csv(output_csv_path, index=False)

print(f"Annotations saved to {output_csv_path}")

# Display the first few rows
print("\nFirst few rows of the annotations DataFrame:")
print(annotations.head())
