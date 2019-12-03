import numpy as np
import math as m
import random as r
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import time as t

import vertex_v3 as v
import draw_graph as dg
import helper as h

n = 50 # number of vertices (individuals)
T = 100 # number of timesteps
max_follow = 5 # maximum amount one can add to following in one 
# less filter bubbles for bf -> 0 and bu -> infinity
bu = 10
bf = 5
p_follow = lambda opinion_distance: m.exp(-bf*opinion_distance)
p_unfollow = lambda trust: m.exp(-bu*trust)
trust_stability = 0.75
confidence_mean = 0.75
confidence_std = 0.1

def init_model(n):
    vertices = []
    a, b = (0.01 - confidence_mean) / confidence_std, (0.99 - confidence_mean) / confidence_std
    for u in range(n):
        o = r.random()
        c = truncnorm.rvs(a, b, loc = confidence_mean, scale = confidence_std)
        vertices.append(v.Vertex(u, o, c, p_follow, p_unfollow, max_follow, trust_stability))
    return vertices

def init_model_wrapper(n, confidence_mean, confidence_std, max_follow, sep, p_follow, p_unfollow, trust_stability):
    vertices = []
    a, b = (0.01 - confidence_mean) / confidence_std, (0.99 - confidence_mean) / confidence_std
    for u in range(n):
        rop = r.random()
        o = [(1-sep)*rop, sep*(1-rop) + rop][rop >= 0.5]
        c = truncnorm.rvs(a, b, loc = confidence_mean, scale = confidence_std)
        vertices.append(v.Vertex(u, o, c, p_follow, p_unfollow, max_follow, trust_stability))
    return vertices
                       
def simulation(vertices, T):
    # to observe opinions over time
    opinions_over_time = np.zeros((T, len(vertices)))
    # simulation with T steps
    for t in range(T):
        # update each vertex
        for u in vertices:
            opinions_over_time[t,u.number] = u.opinion
            u.update_opinion()
            u.update_following(vertices)
            u.update_trust()
    return opinions_over_time

"""
    MAIN
"""
if __name__ == "__main__":
    # initialize model
    vertices = init_model(n)

    # simulation
    tstart = t.time()
    opinions_over_time = simulation(vertices, T)
    tend = t.time()
    print(r"Completed after {0:} s".format(tend-tstart))

    # store graph in csv-file
    #W, o = h.build_W_o(vertices)
    #h.make_csv(W)
    # draw graph
    #dg.draw_graph(W, o)
    
    # show data over time
    plt.plot(opinions_over_time)
    #plt.title("opinion change")
    plt.ylabel("Opinion")
    plt.xlabel("Step")
    plt.savefig(r"sample_conv.pdf")
    plt.show()
    # show confidence distribution
    c = np.zeros(n)
    for u in vertices:
        c[u.number] = u.confidence
    plt.xlim(0,1)
    plt.hist(c)
    plt.title("confidence distribution")
    plt.ylabel("number of vertices")
    plt.xlabel("confidence")
    plt.show()
    