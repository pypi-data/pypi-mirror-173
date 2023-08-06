from Embedding.gf import *

def GF(input_file, output_file,matrix,rep_size=128, epoch=120, learning_rate=0.003, weight_decay=1.):
    

    np.savetxt(input_file,matrix,fmt='%d')
    t1 = time.time()
    g = Graph()
    print("Reading...")

    g.read_edgelist(filename=input_file, weighted=False, directed=False)
    model = GraphFactorization(graph=g, rep_size=rep_size, epoch=epoch, learning_rate=learning_rate, weight_decay=weight_decay)

    t2 = time.time()
    print(t2-t1)
    print("Saving embeddings...")
    model.save_embeddings(output_file)
    Embedding=np.loadtxt(output_file, dtype=float, skiprows=1)
    return Embedding
