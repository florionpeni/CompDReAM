# CompDReAM
Hierarchy-aware drug repurposing framework using ChEMBL + DisGeNET.

## Machine Learning data

The contents of this folder, including large `.npy`, `.pkl`, and `.csv` files, are too large for GitHub and are therefore hosted externally.

🔗 [Access all machine learning files via Google Drive](https://drive.google.com/drive/folders/1mRygsFos3uz1a1xfzNeKEeRWZUxRZJy2?usp=drive_link)

---

### Folder contents on Drive

- `/v1`, `/v2`, ..., `/v5`: Model versions (Random Forest, SVR, etc.)
- `/vX/protbert/`: Protein embeddings (e.g., `X_prot.npy`, `X_combined.npy`)
- `training_dataset.csv`, `training_dataset_scoregda.csv`: Datasets used in training
- `rf_model.pkl`, `rf_metadata_summary.csv`, `feature_importance.png`: Model metadata and visualisations

---

## How to use these files (in Colab or locally)

```python
from google.colab import drive
drive.mount('/content/drive')

# Example: Load combined features for v5
import numpy as np
X = np.load('/content/drive/MyDrive/CompDReAM/v5/X_combined.npy')

# Load trained model
import joblib
model = joblib.load('/content/drive/MyDrive/CompDReAM/v5/Random_Forest.pkl')

---
