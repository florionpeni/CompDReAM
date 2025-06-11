#!/bin/bash

echo "Downloading cache files from Google Drive..."

# Create data folder if missing
mkdir -p data

# Download df_chembl.csv
if [ ! -f data/df_chembl.csv ]; then
    echo "Downloading df_chembl.csv..."
    curl -L -o data/df_chembl.csv "https://drive.google.com/uc?export=download&id=1eu-jaosbrOfSKQ49_duSOB0lmCZlydJe"
else
    echo "data/df_chembl.csv already exists."
fi

# Download sql_chembl_cache.parquet
if [ ! -f data/sql_chembl_cache.parquet ]; then
    echo "Downloading sql_chembl_cache.parquet..."
    curl -L -o data/sql_chembl_cache.parquet "https://drive.google.com/uc?export=download&id=1YP5RBI2H51OYawkhkxPv-uJcd-bPiAzK"
else
    echo "data/sql_chembl_cache.parquet already exists."
fi

echo "Cache files are ready!"

