import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem


drug = pd.read_csv('./data/drug_smiles.csv')
smiles = drug['smiles'].values
mols = [Chem.MolFromSmiles(x) for x in smiles]
fp = [AllChem.GetMorganFingerprintAsBitVect(x,2,nBits=1024,) for x in mols]
fp_array = np.array(fp)
np.savetxt('./data/morganfp.txt',fp_array,delimiter=',')
