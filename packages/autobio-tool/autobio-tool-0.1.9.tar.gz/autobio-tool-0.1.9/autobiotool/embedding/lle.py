from Embedding.lle import *
def lle(input_file, output_file, matrix,d=64):

    np.savetxt(input_file,matrix,fmt='%d')
    t1 = time()
    g = Graph()
    print("Reading...")

    g.read_edgelist(filename=input_file, weighted=False, directed=False)
    model = LLE(graph=g, d=d)


    t2 = time()
    print(t2-t1)
    print("Saving embeddings...")
    model.save_embeddings(output_file)
    Embedding=np.loadtxt(output_file, dtype=float, skiprows=1)
    return Embedding

