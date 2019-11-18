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
    x_min = -10.0; x_max = 20.0; y_min = -10.0; y_max = 20.0 # position boundaries for vertices
    # initialize random coordinates
    x = np.array(o) # separate diff. opinions along x-axis
    y = np.random.rand(n,)
    ax = ay = vx = vy = np.zeros(n) # acceleration and velocity in 2D
    # get partitions of vertices
    partition_of_u = [-1]*n
    partitions = find_partitions(make_adj(W))
    for i in range(len(partitions)):
        for u in partitions[i]:
            partition_of_u[u] = i
    # start simulation
    for _ in range(T):
        # set acceleration
        ax = np.zeros(n)
        ay = np.zeros(n)
        for u in range(n):
            # check boundaries
            out_of_bounds = False
            if x[u] < x_min: ax[u] = 0.0; vx[u] = 0.0; x[u] = x_min; out_of_bounds = True
            if x[u] > x_max: ax[u] = 0.0; vx[u] = 0.0; x[u] = x_max; out_of_bounds = True
            if y[u] < y_min: ay[u] = 0.0; vy[u] = 0.0; y[u] = y_min; out_of_bounds = True
            if y[u] > y_max: ay[u] = 0.0; vy[u] = 0.0; y[u] = y_max; out_of_bounds = True
            if out_of_bounds: continue
            # calculate force between u and other vertices
            for v in range(n):
                # calculate the force from u to v
                d = m.sqrt((x[v] - x[u])*(x[v] - x[u]) + (y[v] - y[u])*(y[v] - y[u]))
                if d != 0:
                    # desired distance: |o[u] - o[v]|
                    d_min = (0.5, 1.2) [int(partition_of_u[u]!=partition_of_u[v])]
                    #d_desired = max(abs(o[u] - o[v]), d_min)
                    d_desired = max(1.0-W[u,v], d_min)
                    # "error"
                    e = (d - d_desired) / d
                    if W[u,v] != 0:
                        e = 0.1*e*W[u,v]
                    else:
                        e = 0.01*e
                    ax[u] += e*(x[v] - x[u])
                    ay[u] += e*(y[v] - y[u])
            mass = np.array(W[:,u]).sum() # mass = popularity
            # a = F / m
            ax[u] /= max(mass, 1)
            ay[u] /= max(mass, 1)
        # acceleration -> velocity
        vx += ax
        vy += ay
        # apply friction
        vx *= (1 - f)
        vy *= (1 - f)
        # velocity -> position
        x += vx
        y += vy
    
        for u in range(n):
            if x[u] < x_min: ax[u] = 0.0; vx[u] = 0.0; x[u] = x_min
            if x[u] > x_max: ax[u] = 0.0; vx[u] = 0.0; x[u] = x_max
            if y[u] < y_min: ay[u] = 0.0; vy[u] = 0.0; y[u] = y_min
            if y[u] > y_max: ay[u] = 0.0; vy[u] = 0.0; y[u] = y_max
        
    return x, y

def show_graph(W, o, x, y):
    """
    Uses matplotlib to draw the graph with the vertices on their respective coordinates.
    """
    partitions = find_partitions(make_adj(W))
    num_partitions = len(partitions)

    plt.figure(num=None, figsize=(3, 3), dpi=200, facecolor='w', edgecolor='k')
    n = x.size
    for u in range(n):
        vertex = plt.Circle((x[u], y[u]),
                            radius=(0.01 + m.pow(np.array(W[:,u]).sum(), 1.0)/n),
                            fc=[o[u], 0, 1-o[u]], zorder=2)
        plt.gca().add_patch(vertex)

        for i in range(num_partitions):
            if u in partitions[i]:
                plt.text(x[u], y[u], str(i), fontsize=5)
        
        for v in range(n):
            if (W[u,v] != 0):
                line = plt.Line2D((x[u], x[v]), (y[u], y[v]), lw=0.5*W[u,v], zorder=1)
                plt.gca().add_line(line)
    
    plt.axis('scaled')
    plt.xticks([])
    plt.yticks([])
    plt.show()

def draw_graph(W, o):
    x, y = gen_coords(W, o)
    show_graph(W, o, x, y)

def make_adj(W):
    tol = 0.1
    n = len(W[0,:])
    adj = []
    for i in range(n): adj.append([])
    for i in range(n):
        for j in range(n):
            if W[i,j]+W[j,i] > tol and j not in adj[i]:
                adj[i].append(j)
                adj[j].append(i)
    return adj


def find_partitions(adj):
    n = len(adj)
    partitions = []
    visited = [False] * n
    queue = []
    for s in range(n):
        if visited[s]: continue
        # bfs to find the whole partition of s
        partition = []
        queue.append(s)
        partition.append(s)
        while len(queue) != 0:
            u = queue.pop()
            for v in adj[u]:
                if not visited[v] and v != 0:
                    queue.append(v)
                    visited[v] = True
                    partition.append(v)
        partitions.append(partition)
    return partitions