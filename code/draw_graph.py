"""
    Provides the function draw_graph(W, o) that draws a nice graph
    when given:
    - the adjacency matrix W with trust-values as entries 
    - the opinion vector o
"""

import numpy as np
import math as m
import matplotlib.pyplot as plt

def gen_coords(W, o):
    """
    input: weighted adjacency matrix, opinion vector
    output: set of points (coordinates)
        where the distance between two points is dependent on their opinion difference
    method: simulates physical process where
        - edges are springs pulling u to v if W[u,v] != 0
        - length of spring = |o[u] - o[v]| (opinion distance)
        - mass of verices = sum of weights of edges going into u = popularity
          => more popular vertices move slower (I don't know if this is necessary.)
    """
    T = 100 # number of timesteps
    f = 0.05 # friction
    n = W.shape[0]
    # initialize random coordinates
    x = np.array(o) # separate diff. opinions along x-axis
    y = np.random.rand(n,)
    ax = ay = vx = vy = np.zeros(n) # acceleration and velocity in 2D
    for _ in range(T):
        # set acceleration
        ax = np.zeros(n)
        ay = np.zeros(n)
        for u in range(n):
            for v in range(n):
                d = m.sqrt((x[v] - x[u])*(x[v] - x[u]) + (y[v] - y[u])*(y[v] - y[u]))
                if d != 0:
                    # desired distance: |o[u] - o[v]|
                    e = (d - max(abs(o[u] - o[v]), 0.5)) / d
                    # a = F / m
                    mass = np.array(W[:,u]).sum() # mass = popularity
                    ax[u] += 0.01*e*(x[v] - x[u]) #e*W[u,v]*(x[v] - x[u])
                    ay[u] += 0.01*e*(y[v] - y[u]) #e*W[u,v]*(y[v] - y[u])
            ax[u] /= (mass + 1)
            ay[u] /= (mass + 1)
        # acceleration -> velocity
        vx += ax
        vy += ay
        # apply friction
        vx *= (1 - f)
        vy *= (1 - f)
        # velocity -> position
        x += vx
        y += vy
    
    return x, y

def show_graph(W, o, x, y):
    """
    Uses matplotlib to draw the graph with the vertices on their respective coordinates.
    """
    plt.figure(num=None, figsize=(5, 5), dpi=200, facecolor='w', edgecolor='k')
    n = x.size
    for u in range(n):
        vertex = plt.Circle((x[u], y[u]),
                            radius=(0.01 + m.pow(np.array(W[:,u]).sum(), 0.5)/n),
                            fc=[o[u], 0, 1-o[u]])
        plt.gca().add_patch(vertex)
        for v in range(n):
            if (W[u,v] != 0):
                line = plt.Line2D((x[u], x[v]), (y[u], y[v]), lw=0.5*W[u,v])
                plt.gca().add_line(line)
    
    plt.axis('scaled')
    plt.show()

def draw_graph(W, o):
    x, y = gen_coords(W, o)
    show_graph(W, o, x, y)