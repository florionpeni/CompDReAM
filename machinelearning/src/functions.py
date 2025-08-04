# Core libraries
import os
import json
import time
import glob
import requests
import numpy as np
from tqdm import tqdm

# RDKit
from rdkit import Chem
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator
from rdkit.DataStructs.cDataStructs import ConvertToNumpyArray

# Transformers (ProtBERT)
from transformers import BertTokenizer, BertModel

# PyTorch
import torch

generator = GetMorganGenerator(radius=2, fpSize=2048)

def smiles_to_morgan_fp(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        fp = generator.GetFingerprint(mol)
        arr = np.zeros((1,), dtype=int)
        ConvertToNumpyArray(fp, arr)
        return arr
    return None

def fetch_uniprot_sequences(uniprot_ids, delay=0.5):
    base_url = "https://rest.uniprot.org/uniprotkb/"
    headers = {"accept": "application/json"}
    params = {"fields": ["sequence"]}
    id_to_sequence = {}
    for uid in tqdm(uniprot_ids):
        url = base_url + uid
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.ok:
                seq = response.json().get("sequence", {}).get("value", "")
                if seq:
                    id_to_sequence[uid] = seq
            else:
                print(f"[!] Failed for {uid}: {response.status_code}")
        except Exception as e:
            print(f"[!] Error fetching {uid}: {str(e)}")
        time.sleep(delay)
    return id_to_sequence

def batch_embed_sequences(sequences, batch_size=128, max_length=1024, cache_prefix="/content/drive/MyDrive/CompDReAM/protbert/protbert_batch"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = BertTokenizer.from_pretrained("Rostlab/prot_bert", do_lower_case=False)
    model = BertModel.from_pretrained("Rostlab/prot_bert").to(device).eval()
    spaced_seqs = [' '.join(list(seq)) for seq in sequences]
    embeddings = []
    for i in tqdm(range(0, len(spaced_seqs), batch_size), desc="Embedding sequences"):
        batch_path = f"{cache_prefix}_{i//batch_size}.npy"
        if os.path.exists(batch_path):
            continue  # already saved
        batch_seqs = spaced_seqs[i:i+batch_size]
        tokens = tokenizer(batch_seqs, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
        tokens = {k: v.to(device) for k, v in tokens.items()}
        with torch.no_grad():
            outputs = model(**tokens)
            batch_embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        np.save(batch_path, batch_embeddings)
    print("✓ All batches embedded and saved to disk.")