#!/bin/bash

echo "Downloading large cache files hosted from Google Drive..."

# df_chembl.csv
if [ ! -f data/df_chembl.csv ]; then
    echo "Downloading df_chembl.csv..."
    gdrive files download 1eu-jaosbrOfSKQ49_duSOB0lmCZlydJe --destination data/
else
    echo "data/df_chembl.csv already exists."
fi

# sql_chembl_cache.parquet
if [ ! -f data/sql_chembl_cache.parquet ]; then
    echo "Downloading sql_chembl_cache.parquet..."
    gdrive files download 1YP5RBI2H51OYawkhkxPv-uJcd-bPiAzK --destination data/
else
    echo "data/sql_chembl_cache.parquet already exists."
fi

echo "All cache files are ready!"

