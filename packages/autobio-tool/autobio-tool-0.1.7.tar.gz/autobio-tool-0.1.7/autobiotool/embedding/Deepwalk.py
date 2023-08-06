from Embedding.node2vec import *

def Deepwalk(input_file, output_file, matrix,path_length = 80,num_paths = 10, dim= 64,workers=8, window=10):
    
    np.savetxt(input_file,matrix,fmt='%d')
    t1 = time.time()
    g = Graph()
    print("Reading...")

    g.read_edgelist(filename=input_file, weighted=False, directed=False)
    model = Node2vec(graph=g, path_length = path_length,
                                num_paths = num_paths, dim= dim,
                                workers=workers, window=window, dw=True)


    t2 = time.time()
    print(t2-t1)
    print("Saving embeddings...")
    model.save_embeddings(output_file)
    Embedding=np.loadtxt(output_file, dtype=float, skiprows=1)
    return Embedding

# if __name__ == '__main__':
#     input_file = '../embeddingdata/input.txt'
#     matrix=np.loadtxt(input_file, dtype=float)
#     Embeddingdata = Deepwalk(matrix,path_length = 80,num_paths = 10, dim= 64,workers=8, window=10)
#     # print(Embeddingdata)
