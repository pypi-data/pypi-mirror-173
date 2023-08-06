from Embedding.line import *
def Line(input_file, output_file, matrix, rep_size=128, batch_size=1000, epoch=10, negative_ratio=5, order=3, label_file=None, clf_ratio=0.5, auto_save=True):

    np.savetxt(input_file,matrix,fmt='%d')
    t1 = time.time()
    g = Graph()
    print("Reading...")

    g.read_edgelist(filename=input_file, weighted=False, directed=False)
    model = LINE(g, rep_size=rep_size, batch_size=batch_size, epoch=epoch, 
                negative_ratio=negative_ratio, order=order, label_file=label_file, 
                clf_ratio=clf_ratio, auto_save=auto_save)

    t2 = time.time()
    print(t2-t1)
    print("Saving embeddings...")
    model.save_embeddings(output_file)
    Embedding=np.loadtxt(output_file, dtype=float, skiprows=1)
    return Embedding
