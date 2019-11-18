"""
    Some useful functions
"""

import numpy as np
import csv

import vertex_v3 as v

def build_W_o(vertices):
    """
    input: list of vertices from class Vertex
    output:
        - weighted adjaciency matrix W, where W[u,v] = trust that u has in v
          and = 0 if u doesn't follow v
        - opinion vector o, where o[u] = opinion of u
    """
    W = np.zeros((len(vertices), len(vertices)))
    o = np.zeros(len(vertices))
    for u in vertices:
        o[u.number] = u.opinion
        for v in u.following:
            if u.number != v.number:
                W[u.number,v.number] = u.trust[v.number]
    return W, o

def make_csv(W):
    """
    makes a csv file from weighted adjaciency matrix W that's compatible with Gephi
    """
    with open('adj_matrix.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        m = W.shape[0]
        n = W.shape[1]
        writer.writerow(np.block([';', np.linspace(0, n-1, n)]))
        for i in range(m):
            writer.writerow(np.block([i, W[i,:]]))
        f.close()