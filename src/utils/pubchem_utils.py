import os
import time
import requests
import pandas as pd
from datetime import datetime, timezone

def fetch_pubchem_cid_from_chembl(chembl_id, retries=5, backoff=1.5):
    """
    Given a ChEMBL ID, returns the corresponding PubChem CID using the name endpoint.
    Retries on 503 or network failure with exponential backoff.
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chembl_id}/cids/JSON"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 503:
                raise requests.exceptions.RequestException("503 Server Busy")
            response.raise_for_status()
            return response.json()["IdentifierList"]["CID"][0]
        except requests.exceptions.RequestException as e:
            print(f"[{chembl_id}] Attempt {attempt+1}/{retries} failed — {e}")
            if attempt < retries - 1:
                sleep_time = backoff * (2 ** attempt)
                print(f"   ↪ Retrying after {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
            else:
                print(f"   ✖ Final failure for {chembl_id}")
                return None

def check_peptide_by_pubchem(cid):
    """
    Given a PubChem CID, checks whether the compound contains 'PEPTIDE' in title or section content.
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        title = data.get("Record", {}).get("RecordTitle", "").upper()
        if "PEPTIDE" in title:
            return True
        for section in data.get("Record", {}).get("Section", []):
            if "PEPTIDE" in str(section).upper():
                return True
        return False
    except:
        return False

def process_id(chembl_id):
    """
    Given a ChEMBL ID, fetch CID and peptide inference result from PubChem.
    """
    cid = fetch_pubchem_cid_from_chembl(chembl_id)
    is_peptide = check_peptide_by_pubchem(cid) if cid else False
    timestamp = datetime.now(timezone.utc).astimezone().isoformat()
    print(f"[{chembl_id}] CID={cid} | Peptide={is_peptide}")
    return (chembl_id, cid, is_peptide, timestamp)

def load_or_init_pubchem_cache(cache_path):
    """
    Load peptide inference cache from CSV, or initialize an empty DataFrame.
    Returns a DataFrame and a set of cached ChEMBL IDs.
    """
    if os.path.exists(cache_path):
        df_cache = pd.read_csv(cache_path)
        df_cache = df_cache.drop_duplicates("Molecule ChEMBL ID")
        cached_ids = set(df_cache["Molecule ChEMBL ID"])
    else:
        df_cache = pd.DataFrame(columns=["Molecule ChEMBL ID", "PubChem CID", "Is Peptide", "Last Updated"])
        cached_ids = set()
    return df_cache, cached_ids

def save_pubchem_cache(df_cache, cache_path):
    """
    Saves the cache DataFrame to disk.
    """
    df_cache.to_csv(cache_path, index=False)
