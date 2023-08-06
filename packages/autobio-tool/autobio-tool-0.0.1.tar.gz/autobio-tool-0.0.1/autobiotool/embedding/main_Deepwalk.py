from embedding.Deepwalk import *


input_file = './embeddingdata/input.txt'
output_file = './embeddingdata/output.txt'
matrix=np.loadtxt(input_file, dtype=float)
Embeddingdata = Deepwalk(input_file, output_file, matrix,path_length = 80,num_paths = 10, dim= 64,workers=8, window=10)
# print(Embeddingdata)
