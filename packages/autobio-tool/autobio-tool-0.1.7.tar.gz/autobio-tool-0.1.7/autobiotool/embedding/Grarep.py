from Embedding.grarep import *

def Grarep(input_file, output_file, matrix,Kstep= 4, dim=64):


    np.savetxt(input_file,matrix,fmt='%d')
    t1 = time.time()
    g = Graph()
    print("Reading...")

    g.read_edgelist(filename=input_file, weighted=False, directed=False)
    model = GraRep(graph=g, Kstep= Kstep, dim=dim)

    t2 = time.time()
    print(t2-t1)
    print("Saving embeddings...")
    model.save_embeddings(output_file)
    Embedding=np.loadtxt(output_file, dtype=float, skiprows=1)
    return Embedding

