import pandas as pd

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