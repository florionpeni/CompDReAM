#!/bin/bash

set -e
echo "Uploading updated cache files to Google Drive..."

# Resolve absolute paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/data"
DF_FILE="${DATA_DIR}/df_chembl.csv"
PARQUET_FILE="${DATA_DIR}/sql_chembl_cache.parquet"
META_FILE="${DATA_DIR}/.cache_meta.json"

# Google Drive file IDs
DF_ID="1eu-jaosbrOfSKQ49_duSOB0lmCZlydJe"
PARQUET_ID="1YP5RBI2H51OYawkhkxPv-uJcd-bPiAzK"

# Upload files
echo "Updating df_chembl.csv..."
gdrive files update "$DF_ID" "$DF_FILE"

echo "Updating sql_chembl_cache.parquet..."
gdrive files update "$PARQUET_ID" "$PARQUET_FILE"

# Update metadata file
echo "Updating .cache_meta.json..."
DF_MTIME=$(stat -c %Y "$DF_FILE")
PARQUET_MTIME=$(stat -c %Y "$PARQUET_FILE")

cat > "$META_FILE" <<EOF
{
  "df_chembl.csv": $DF_MTIME,
  "sql_chembl_cache.parquet": $PARQUET_MTIME
}
EOF

echo "Cache metadata file updated: $META_FILE"

