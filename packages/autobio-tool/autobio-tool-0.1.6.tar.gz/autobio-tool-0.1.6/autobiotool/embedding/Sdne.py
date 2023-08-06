from Embedding.sdne import *
def Sdne(input_file, output_file, matrix,alpha=1e-6, beta=5., nu1=1e-5, nu2=1e-4, batch_size=200, epoch=5, learning_rate=0.01):

    np.savetxt(input_file,matrix,fmt='%d')
    t1 = time.time()
    g = Graph()
    print("Reading...")


    g.read_edgelist(filename=input_file, weighted=False, directed=False)
    encoder_layer_list = [1000, 128]
    model = SDNE(g, encoder_layer_list=encoder_layer_list,
                alpha=alpha, beta=beta, nu1=nu1, nu2=nu2,
                batch_size=batch_size, epoch=epoch, learning_rate=learning_rate)


    t2 = time.time()
    print(t2-t1)
    print("Saving embeddings...")
    model.save_embeddings(output_file)
    Embedding=np.loadtxt(output_file, dtype=float, skiprows=1)
    return Embedding
