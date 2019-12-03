"""
    Provides the functions
    - draw_graph(vertices) that draws a nice graph (the color corresponds to the opinion)
    - make_csv(vertices) that makes a csv file that's compatible with gephi
  _____                      _              _ _ _   
 |  __ \                    | |            | (_) |  
 | |  | | ___    _ __   ___ | |_    ___  __| |_| |_ 
 | |  | |/ _ \  | '_ \ / _ \| __|  / _ \/ _` | | __|
 | |__| | (_) | | | | | (_) | |_  |  __/ (_| | | |_ 
 |_____/ \___/  |_| |_|\___/ \__|  \___|\__,_|_|\__|

"""

import numpy as np
import math as m
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import vertex as v

def gen_coords(vertices):
    """
    input: list of vertices from vertex class
    output: set of points (coordinates)
        where the distance between two points is dependent on their filter bubble (partition)
        and trust to each other
    method: simulates physical process where
        - edges are springs pulling u to v if trust(u,v) != 0
        - length of spring (u,v) is dependent on the trust of u in v
    """
    T = 100 # number of timesteps
    f = 0.05 # friction
    n = len(vertices)
    x_min = -10.0; x_max = 20.0; y_min = -10.0; y_max = 20.0 # position boundaries for vertices
    # initialize random coordinates
    x = np.zeros(n) # separate diff. opinions along x-axis
    for i in range(n): x[i] = vertices[i].opinion
    y = np.random.rand(n,)
    ax = ay = vx = vy = np.zeros(n) # acceleration and velocity in 2D
    # get partitions of vertices
    partition_of_u = [-1]*n
    partitions = find_partitions(vertices)
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
                    d_desired = (0.5, 1.2) [int(partition_of_u[u]!=partition_of_u[v])]
                    if v in vertices[u].trust:
                        d_desired = max(1.0-vertices[u].trust[v], d_desired)
                    # "error"
                    e = (d - d_desired) / d
                    if v in vertices[u].trust:
                        e = 0.1*e*vertices[u].trust[v]
                    else:
                        e = 0.01*e
                    ax[u] += e*(x[v] - x[u])
                    ay[u] += e*(y[v] - y[u])
            #mass = np.array(W[:,u]).sum() # mass = popularity
            # a = F / m
            #ax[u] /= max(mass, 1)
            #ay[u] /= max(mass, 1)
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

def show_graph(vertices, x, y):
    """
    Uses matplotlib to draw the graph with the vertices on their respective coordinates.
    """
    n = len(vertices)
    num_followers = n * [0]
    for u in vertices:
        for v in u.following: num_followers[v.number] += 1
    plt.figure(num=None, figsize=(3, 3), dpi=200, facecolor='w', edgecolor='k')
    for u in range(n):
        o = vertices[u].opinion
        vertex = plt.Circle((x[u], y[u]),
                            radius=(0.01 + 0.5*m.pow(num_followers[u], 0.5)/n),
                            fc=[o, 0, 1-o], zorder=2)
        plt.gca().add_patch(vertex)
        
        for v in range(n):
            if v in vertices[u].trust:
                line = plt.Line2D((x[u], x[v]), (y[u], y[v]), lw=0.5*vertices[u].trust[v], zorder=1)
                plt.gca().add_line(line)
    
    plt.axis('scaled')
    plt.xticks([])
    plt.yticks([])
    plt.show()

def draw_graph(vertices):
    x, y = gen_coords(vertices)
    show_graph(vertices, x, y)

def make_adj(vertices):
    tol = 0.01 # ignores edges with weight < tol
    n = len(vertices)
    adj = []
    for _ in range(n): adj.append([])
    for u in vertices:
        for v in u.following:
            if u.trust[v.number] >= tol:
                adj[u.number].append(v.number)
    return adj

def find_partitions(vertices):
    adj = make_adj(vertices)
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

def make_csv(vertices):
    """
    makes a csv file from vertices that's compatible with Gephi
    """
    with open('adj_matrix.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        n = len(vertices)
        writer.writerow(np.block([';', np.linspace(0, n-1, n)]))
        i = 0
        for u in vertices:
            trust_row = np.zeros(n)
            for v in u.following:
                if u != v: trust_row[v.number] = u.trust[v.number]
            writer.writerow(np.block([i, trust_row]))
            i += 1
        f.close()
