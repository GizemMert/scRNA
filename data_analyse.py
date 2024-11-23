import os
import gzip
import pandas as pd
import matplotlib.pyplot as plt


# Specify the directory containing the files
data_dir = "Data/GSE116256_RAW"

# Criteria for filtering
include_keywords = ["-D0", "BM"]  # Files must include either of these
exclude_keyword = "38n"

# Filter files
filtered_files = [
    file for file in os.listdir(data_dir)
    if any(keyword in file for keyword in include_keywords)  # Include files with keywords
    and exclude_keyword not in file  # Exclude files with "38n"
    and file.endswith(".anno.txt.gz")  # Only process .anno.txt.gz files
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

cell_type_counts = annotations["CellType"].value_counts()
print("Cell Type Frequencies:")
print(cell_type_counts)

# Cell type frequencies per donor
donor_cell_type_counts = annotations.groupby("DonorID")["CellType"].value_counts()
print("\nCell Type Frequencies per Donor:")
print(donor_cell_type_counts)

# Save summary statistics to CSV
cell_type_counts.to_csv("cell_type_frequencies.csv")
donor_cell_type_counts.to_csv("donor_cell_type_frequencies.csv")

# Save printed results to a text file
with open("donor_cell_type_counts.txt", "w") as f:
    f.write("Cell Type Frequencies Across All Data:\n")
    f.write(cell_type_counts.to_string())
    f.write("\n\nCell Type Frequencies per Donor:\n")
    f.write(donor_cell_type_counts.to_string())


# Iterate over all unique donors
unique_donors = annotations["DonorID"].unique()

for donor in unique_donors:
    # Create a bar plot for the current donor
    plt.figure(figsize=(10, 6))
    donor_data = annotations[annotations["DonorID"] == donor]["CellType"].value_counts()
    donor_data.plot(kind="bar")

    plt.title(f"Cell Type Frequencies for {donor}")
    plt.xlabel("Cell Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)

    # Save the plot as a PNG file
    plt.savefig(f"cell_type_frequencies_{donor}.png")

    # Optionally display the plot
    # plt.show()  # Uncomment if you want to see each plot during the loop

    plt.close()  # Close the plot to avoid overlap
