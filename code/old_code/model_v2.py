"""
    model_v2:
    - Version where everithing is computed with objects (class vertex)
    - Slightly different than model_v1, more similar to Beat's approach
    - To use draw_graph, you have to generate the adjacency matrix with trust-values as entries.
"""

import numpy as np
import math as m
import random as r
import matplotlib.pyplot as plt

import vertex as v
import draw_graph as dg
import helper as h

n = 50 # number of vertices (individuals)
T = 50 # number of timesteps
max_follow = 3 # maximum amount one can add to following in one timestep
b = 25 # see p_follow, p_unfollow
p_follow = lambda opinion_distance: m.exp(-b*opinion_distance)
p_unfollow = lambda trust: m.exp(-b*trust)

def init_model(n):
    vertices = []
    for u in range(n):
        vertices.append(v.Vertex(u, r.random(), r.random(), p_follow, p_unfollow, max_follow))
    return vertices

def simulation(vertices, T):
    # to observe opinions and confidence over time
    opinions_over_time = np.zeros((T, len(vertices)))
    confidence_over_time = np.zeros((T, len(vertices)))
    # simulation with T steps
    for t in range(T):
        # update each vertex
        for u in vertices:
            opinions_over_time[t,u.number] = u.opinion
            confidence_over_time[t,u.number] = u.confidence
            u.update_opinion()
            u.update_following(vertices)
            u.update_trust()
            u.update_confidence(n)
    return opinions_over_time, confidence_over_time

"""
    MAIN
"""
if __name__ == "__main__":
    
    # initialize model
    vertices = init_model(n)
    
    # simulation
    opinions_over_time, confidence_over_time = simulation(vertices, T)

    # store graph in csv-file
    W, o = h.build_W_o(vertices)
    #h.make_csv(W)
    # draw graph
    dg.draw_graph(W, o)

    # show data over time
    plt.plot(opinions_over_time)
    plt.ylabel("opinion")
    plt.xlabel("time")
    plt.figure()
    plt.plot(confidence_over_time)
    plt.ylabel("confidence")
    plt.xlabel("time")
    plt.show()