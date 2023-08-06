from Embedding.lap import *
def Lap(input_file, output_file, matrix, rep_size=64):

    np.savetxt(input_file,matrix,fmt='%d')
    t1 = time.time()
    g = Graph()
    print("Reading...")

    g.read_edgelist(filename=input_file, weighted=False, directed=False)
    model = LaplacianEigenmaps(graph=g, rep_size = rep_size)


    t2 = time.time()
    print(t2-t1)
    print("Saving embeddings...")
    model.save_embeddings(output_file)
    Embedding=np.loadtxt(output_file, dtype=float, skiprows=1)
    return Embedding
