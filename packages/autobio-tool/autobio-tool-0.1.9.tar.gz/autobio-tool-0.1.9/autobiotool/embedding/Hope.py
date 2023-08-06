from Embedding.hope import *

def Hope(input_file, output_file,matrix, dim=64):
    

    np.savetxt(input_file,matrix,fmt='%d')
    t1 = time.time()
    g = Graph()
    print("Reading...")

    g.read_edgelist(filename=input_file, weighted=False, directed=False)
    model = HOPE(graph=g, d=dim)


    t2 = time.time()
    print(t2-t1)
    print("Saving embeddings...")
    model.save_embeddings(output_file)
    Embedding=np.loadtxt(output_file, dtype=float, skiprows=1)
    return Embedding

# if __name__ == '__main__':
#     input_file = '../embeddingdata/input.txt'
#     matrix=np.loadtxt(input_file, dtype=float)
#     Embeddingdata = Hope(matrix, dim=64)
#     # print(Embeddingdata)