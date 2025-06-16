import pandas as pd
from utils.pubchem_utils import load_or_init_pubchem_cache, save_pubchem_cache

def classify_relationship(row):
    if pd.isna(row["parent_molregno"]):
        return "No parent info"
    if row["molregno"] == row["parent_molregno"] == row["active_molregno"]:
        return "Parent compound"
    if row["molregno"] != row["parent_molregno"] and row["active_molregno"] == row["parent_molregno"]:
        return "Salt form"
    if row["molregno"] == row["parent_molregno"] and row["active_molregno"] != row["parent_molregno"]:
        return "Prodrug"
    if row["molregno"] != row["parent_molregno"] and row["active_molregno"] != row["parent_molregno"]:
        return "Prodrug salt form"
    return "Other"

def resolve_molecule_type(row):
    mt, mtp = row["Molecule type"], row["parent_molecule_type"]
    if pd.notnull(mt) and mt.lower() != "unknown":
        return mt
    if pd.notnull(mtp) and mtp.lower() != "unknown":
        return mtp
    if any(pd.notnull(row.get(k)) for k in [
        "Canonical SMILES", "Preferred name", 
        "Molecular formula of full compound", 
        "Molecular weight of full compound"
    ]):
        return "TBD"
    return None

def update_molecule_type_with_pubchem(df_chembl: pd.DataFrame, pubchem_cache_path: str) -> pd.DataFrame:
    """
    Update 'Molecule type' from 'TBD' to 'Peptide (Inferred via PubChem)' using PubChem cache.
    Also prints how many rows and unique molecules were affected.
    """
    df_cache, _ = load_or_init_pubchem_cache(pubchem_cache_path)
    peptide_ids = set(df_cache[df_cache["Is Peptide"] == True]["Molecule ChEMBL ID"].dropna())
    update_mask = (df_chembl["Molecule type"] == "TBD") & (df_chembl["Molecule ChEMBL ID"].isin(peptide_ids))
    df_chembl.loc[update_mask, "Molecule type"] = "Peptide (Inferred via PubChem)"
    print(f"Updated {update_mask.sum()} molecules to 'Peptide (Inferred via PubChem)' based on PubChem cache.")
    rows_updated = df_chembl[
        (df_chembl["Molecule type"] == "Peptide (Inferred via PubChem)") &
        (df_chembl["Molecule ChEMBL ID"].isin(peptide_ids))
    ]
    print(f"Number of updated rows: {rows_updated.shape[0]}")
    print(f"Unique ChEMBL IDs updated: {rows_updated['Molecule ChEMBL ID'].nunique()}")
    return df_chembl
