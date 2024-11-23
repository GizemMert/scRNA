import os
import gzip
import pandas as pd
import numpy as np
import umap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load gene expression data from .dem.txt.gz
def load_expression_file(file_path):
    with gzip.open(file_path, 'rt') as f:
        df = pd.read_csv(f, sep="\t", index_col=0)  # Assuming the first column is the index
    return df

# Load metadata from .anno.txt.gz
def load_annotation_file(file_path):
    with gzip.open(file_path, 'rt') as f:
        df = pd.read_csv(f, sep="\t")
    return df

# Specify the files
data_dir = "Data/GSE116256_RAW"
dem_file = os.path.join(data_dir, "GSM3587923_AML1012-D0.dem.txt.gz")  # Example dem file
anno_file = os.path.join(data_dir, "GSM3587924_AML1012-D0.anno.txt.gz")  # Corresponding anno file

# Load the data
expression_data = load_expression_file(dem_file)
print(expression_data.describe())
print(expression_data.columns)

total_counts_per_cell = expression_data.sum(axis=1)
print(total_counts_per_cell.describe())
gene_variances = expression_data.var(axis=0)
print(gene_variances.describe())


# Example: Plot distributions for a few genes
expression_data.iloc[:, :5].boxplot()
plt.title("Gene Expression Distributions")
plt.ylabel("Expression Levels")
plt.savefig("distribution.png")


annotations = load_annotation_file(anno_file)

# Merge gene expression with metadata on 'Cell'
merged_data = pd.merge(
    annotations,
    expression_data.T,  # Transpose gene expression to match cell-wise format
    left_on="Cell",
    right_index=True
)

# Separate features (genes) and labels
gene_expression = merged_data.iloc[:, len(annotations.columns):]  # Assuming last columns are gene data
labels = merged_data["CellType"]  # Example: Use CellType as labels

# Normalize gene expression data
scaler = StandardScaler()
normalized_data = scaler.fit_transform(gene_expression)

# Perform UMAP
reducer = umap.UMAP(random_state=42)
embedding = reducer.fit_transform(normalized_data)

# Convert to DataFrame
embedding_df = pd.DataFrame(embedding, columns=["UMAP1", "UMAP2"])
embedding_df["CellType"] = labels

# Plot UMAP
plt.figure(figsize=(10, 8))
for cell_type in embedding_df["CellType"].unique():
    subset = embedding_df[embedding_df["CellType"] == cell_type]
    plt.scatter(subset["UMAP1"], subset["UMAP2"], label=cell_type, alpha=0.7, s=10)

plt.title("UMAP of Gene Expression Data")
plt.xlabel("UMAP1")
plt.ylabel("UMAP2")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Cell Type", fontsize='small')
plt.tight_layout()
plt.savefig("umap_gene_expression.png")
plt.show()
