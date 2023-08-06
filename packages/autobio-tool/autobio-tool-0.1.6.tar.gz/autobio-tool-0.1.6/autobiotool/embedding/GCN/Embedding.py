
import numpy as np
import random
from graph import *
import node2vec
import time
import ast

class Graph(object):
    def __init__(self):
        self.G = None
        self.look_up_dict = {}
        self.look_back_list = []
        self.node_size = 0
        
    def encode_node(self):
        look_up = self.look_up_dict
        look_back = self.look_back_list
        for node in self.G.nodes():
            look_up[node] = self.node_size
            look_back.append(node)
            self.node_size += 1
            self.G.nodes[node]['status'] = ''
    def read_edgelist(self, filename, weighted=False, directed=False):
        self.G = nx.DiGraph()

        if directed:
            def read_unweighted(l):
                src, dst = l.split()
                self.G.add_edge(src, dst)
                self.G[src][dst]['weight'] = 1.0

            def read_weighted(l):
                src, dst, w = l.split()
                self.G.add_edge(src, dst)
                self.G[src][dst]['weight'] = float(w)
        else:
            def read_unweighted(l):
                src, dst = l.split()
                self.G.add_edge(src, dst)
                self.G.add_edge(dst, src)
                self.G[src][dst]['weight'] = 1.0
                self.G[dst][src]['weight'] = 1.0

            def read_weighted(l):
                src, dst, w = l.split()
                self.G.add_edge(src, dst)
                self.G.add_edge(dst, src)
                self.G[src][dst]['weight'] = float(w)
                self.G[dst][src]['weight'] = float(w)
        fin = open(filename, 'r')
        func = read_unweighted
        if weighted:
            func = read_weighted
        while 1:
            l = fin.readline()
            if l == '':
                break
            func(l)
        fin.close()
        self.encode_node()


def deepwalkembedding(input_file, output_file, path_length, num_paths, dim, workers, window):
    t1 = time.time()
    g = Graph()
    print("Reading...")

    g.read_edgelist(filename=input_file, weighted=False, directed=False)
    model = node2vec.Node2vec(graph=g, path_length = path_length,
                                num_paths = num_paths, dim= dim,
                                workers=workers, window=window, dw=True)

    t2 = time.time()
    print(t2-t1)
    print("Saving embeddings...")
    model.save_embeddings(output_file)

if __name__ == "__main__":
    
    random.seed(32)
    np.random.seed(32)
    input_file = '../../data/cora/cora_edgelist.txt'
    output_file = '../../data/cora/cora_embedding.txt'
    path_length = 80
    num_paths = 10
    dim = 64
    workers = 8
    window = 10
    dw=True
    deepwalkembedding(input_file, output_file, path_length, num_paths, dim, workers, window)
