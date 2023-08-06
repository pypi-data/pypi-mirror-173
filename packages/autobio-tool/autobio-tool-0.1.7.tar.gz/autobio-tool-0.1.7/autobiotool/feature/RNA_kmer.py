import csv
csv.field_size_limit(500 * 1024 * 1024)

import os
import time
import numpy as np
# import pandas as pd
import math
import random
from MyKmer import MyKmer


def RNA_kmer(BiomoleculesSequence):
    BiomoleculesKmer = []
    counter = 0
    while counter < len(BiomoleculesSequence):
        try:       
            sequence = MyKmer(BiomoleculesSequence[counter][1])
            pair = []
            pair.append(BiomoleculesSequence[counter][0])
            pair.extend(sequence)
            BiomoleculesKmer.append(pair)
        except:   
            pair = []
            pair.append(BiomoleculesSequence[counter][0])
            pair.extend(np.zeros((1, 64), dtype=int)[0])           
            BiomoleculesKmer.append(pair)
        print(counter)
        counter = counter + 1

    return BiomoleculesKmer