#!/bin/bash

echo "Downloading large cache files hosted from Google Drive..."

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/data"

# Ensure data/ directory exists
mkdir -p "$DATA_DIR"

# df_chembl.csv
if [ ! -f "$DATA_DIR/df_chembl.csv" ]; then
    echo "Downloading df_chembl.csv..."
    gdrive files download 1eu-jaosbrOfSKQ49_duSOB0lmCZlydJe --destination "$DATA_DIR"
else
    echo "$DATA_DIR/df_chembl.csv already exists."
fi

# sql_chembl_cache.parquet
if [ ! -f "$DATA_DIR/sql_chembl_cache.parquet" ]; then
    echo "Downloading sql_chembl_cache.parquet..."
    gdrive files download 1YP5RBI2H51OYawkhkxPv-uJcd-bPiAzK --destination "$DATA_DIR"
else
    echo "$DATA_DIR/sql_chembl_cache.parquet already exists."
fi

echo "All cache files are ready!"

