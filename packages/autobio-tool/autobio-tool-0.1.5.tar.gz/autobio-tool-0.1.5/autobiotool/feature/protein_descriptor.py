import pandas as pd
import numpy as np
# from PyBioMed import Pyprotein
# from PyBioMed.PyProtein import CTD
import CTD


pro = pd.read_csv('./data/pro_seq.csv')
seq = pro['seq'].values.astype(str)

protein_descriptor=[]
for i in range(len(seq)):
    ctd = CTD.CalculateCTD(seq[i]).values()
    protein_descriptor.append(list(ctd))

protein_descriptor = np.array(protein_descriptor)
np.savetxt('./data/pro_ctd.txt',protein_descriptor,delimiter=',')