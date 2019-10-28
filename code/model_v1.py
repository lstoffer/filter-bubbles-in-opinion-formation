"""
    model_v1:
    - Version where everithing is computed with matrices and vectors
    - Slightly different than model_v2
    - Compatible with draw_graph
    - (maybe a little bit more difficult to understand)
"""

import numpy as np
import math as m
import random as r
import matplotlib.pyplot as plt

import draw_graph as sg
import helper as h

n = 50
p = 0.0 # IF p > 0 THEN THERE IS LESS POLARIZATION
bf = 20
bu = 5
T = 100
p_follow = lambda d: m.exp(-bf*abs(d))
p_unfollow = lambda w, deg: m.exp(-bu*deg/w)
opinion_generator = lambda x: (0.5*x, 0.5*x + 0.5) [int(x >= 0.5)]
confidence_generator = lambda x: min(x + 0.1, 1.0)

def simulation(W, o, c, bf, bu, T):
    n = W.shape[0]
    Ot = np.zeros((T, n))
    Ct = np.zeros((T, n))
 
    for t in range(T):
        Ot[t,:] = o
        Ct[t,:] = c
        """
        changing opinion
        """
        o = (np.multiply(o, c) + np.dot((np.identity(n) - np.diag(c)), np.dot(W, o.transpose()))).transpose()
        o = np.vectorize(h.constraint)(o, 0.0, 1.0)
        """
        changing weights W
        """
        # change followers
        for u in range(n):
            for v in range(n):
                if u == v: continue
                deg = np.count_nonzero(W[u,:])
                # suggest follower
                if W[u,v] == 0:
                    if r.random() < p_follow(o[u]-o[v]):
                        W[u,v] = 1 / (deg + 1)      
                        break
                # unfollow
                else:
                    if r.random() < p_unfollow(W[u,v], deg):
                        W[u,v] = 0
                        break
        # update W
        o_list = []
        for _ in range(n): o_list.append(o)
        O = np.row_stack(o_list)
        c_list = []
        for _ in range(n): c_list.append(c)
        C = np.row_stack(c_list)
        W += np.multiply(W, (C.transpose() - np.abs(O.transpose() - O)))
        h.normalize_rows(W)

        """
        changing confidence c
        """
        # d[u] = sum of weighted opinion differences between u and N(u)
        D = np.multiply(np.abs(O - O.transpose()), W)
        d = (np.sum(D, axis=1)).transpose()
        # average of d
        d_avg = np.sum(d) / n
        # update c
        c = c + (d_avg - d)
        c = np.vectorize(h.constraint)(c, 0.0, 1.0)
    
    return W, o, Ot, Ct

def init_model(n, p):
    """
    initializes the weighted adjacency matrix, opinion vector and confidence vector
    """
    # random W
    W = np.random.rand(n, n)
    # delete some edges
    for u in range(n):
        for v in range(n):
            if u == v or r.random() > p:
                W[u,v] = 0
    # normalize rows of W
    h.normalize_rows(W)
    # generate opinion randomly but seperating
    o = np.vectorize(opinion_generator)(np.random.rand(n))
    # random confidence
    c = np.vectorize(confidence_generator)(np.random.rand(n))
    return W, o, c


if __name__ == "__main__":
    # initialize model
    W, o, c = init_model(n, p)
    
    # show initial state of graph
    #sg.draw_graph(W, o)
    
    #simulation
    W, o, Ot, Ct = simulation(W, o, c, bf, bu, T)
    
    # show end state of graph
    sg.draw_graph(W, o)

    # show data over time
    plt.plot(Ot)
    plt.ylabel("opinion")
    plt.xlabel("time")
    plt.show()
    plt.plot(Ct)
    plt.ylabel("confidence")
    plt.xlabel("time")
    plt.show()