#!/bin/bash

echo "Uploading updated cache files to Google Drive..."

# Define local file paths
DF_FILE="data/df_chembl.csv"
PARQUET_FILE="data/sql_chembl_cache.parquet"

# Define remote file IDs
DF_ID="1eu-jaosbrOfSKQ49_duSOB0lmCZlydJe"
PARQUET_ID="1YP5RBI2H51OYawkhkxPv-uJcd-bPiAzK"

# Upload (overwrite) each file
echo "Updating df_chembl.csv..."
gdrive files update --file "$DF_FILE" --name "df_chembl.csv" "$DF_ID"

echo "Updating sql_chembl_cache.parquet..."
gdrive files update --file "$PARQUET_FILE" --name "sql_chembl_cache.parquet" "$PARQUET_ID"

echo "Google Drive cache updated successfully!"