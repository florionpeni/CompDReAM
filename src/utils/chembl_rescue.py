import os
import json
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

def rescue_from_chembl(chembl_id):
    url = f"https://www.ebi.ac.uk/chembl/compound_report_card/{chembl_id}/"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return (chembl_id, None, None, None, None)
        soup = BeautifulSoup(response.text, "html.parser")
        json_tag = soup.find("script", {"type": "application/ld+json"})
        if not json_tag:
            return (chembl_id, None, None, None, None)
        data = json.loads(json_tag.string)
        return (
            chembl_id,
            data.get("molecularFormula"),
            data.get("smiles"),
            data.get("name"),
            data.get("molecularWeight")
        )
    except Exception as e:
        print(f"Error for {chembl_id}: {e}")
        return (chembl_id, None, None, None, None)

def load_or_init_chembl_cache(cache_path):
    if os.path.exists(cache_path):
        df_cache = pd.read_csv(cache_path)
        return {
            row["Molecule ChEMBL ID"]: row for _, row in df_cache.iterrows()
        }, df_cache
    else:
        return {}, pd.DataFrame(columns=[
            "Molecule ChEMBL ID", "Rescued Formula", 
            "Rescued SMILES", "Rescued Name", "Rescued MW"
        ])

def save_chembl_cache(cache_dict, path):
    df_cache = pd.DataFrame.from_dict(cache_dict, orient="index")
    df_cache.to_csv(path, index=False)
