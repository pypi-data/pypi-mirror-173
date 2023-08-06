from Embedding.node2vec import *
def node2vec(input_file, output_file, matrix,path_length = 80,num_paths = 10, dim= 64,workers=8, window=10, p=1.0, q=1.0, dw=True):

    np.savetxt(input_file,matrix,fmt='%d')
    t1 = time.time()
    g = Graph()
    print("Reading...")

    g.read_edgelist(filename=input_file, weighted=False, directed=False)
    model = Node2vec(graph=g, path_length = path_length,
                                num_paths = num_paths, dim= dim,
                                workers=workers, window=window,p=p, q=q, dw=True)


    t2 = time.time()
    print(t2-t1)
    print("Saving embeddings...")
    model.save_embeddings(output_file)
    Embedding=np.loadtxt(output_file, dtype=float, skiprows=1)
    return Embedding
