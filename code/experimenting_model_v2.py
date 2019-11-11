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

import experimenting_vertex as v
import draw_graph as dg
import helper as h

n = 26 # number of vertices (individuals)
T = 50 # number of timesteps
max_follow = 3 # maximum amount one can add to following in one timestep
bf = 10 # see p_follow, p_unfollow
bu = 25
p_follow = lambda opinion_distance: m.exp(-bf*opinion_distance)
p_unfollow = lambda trust: m.exp(-bu*trust)

p_follow_trendSetter = lambda x: 0

t0 = int(T/7)

def init_model(n, sep):
    vertices = []
    for u in range(n):
        rop = r.random()
        op = [(1-sep)*rop, sep*(1-rop) + rop][rop >= 0.5]
        vertices.append(v.Vertex(u, op, r.random(), p_follow, p_unfollow, max_follow))
    return vertices

def simulation(vertices, T, trendsetter = False):
    # to observe opinions and confidence over time
    opinions_over_time = []
    confidence_over_time = []
    # simulation with T steps
    for t in range(T):
        # update each vertex
        opinions_thisStep = []
        confidence_thisStep = []
        for u in vertices:
            opinions_thisStep.append(u.opinion)
            confidence_thisStep.append(u.confidence)
            u.update_opinion()
            u.update_following(vertices)
            u.update_trust()
            u.update_confidence(len(vertices))
         
        if trendsetter:
                
            if t == t0: # add trendsetter at some opinion
                vertices.append(v.Vertex(len(vertices), 1.0, 1.0, p_follow_trendSetter, p_unfollow, max_follow))
                unew = vertices[-1]
                opinions_thisStep.append(unew.opinion)
                confidence_thisStep.append(unew.confidence)
                ts_followers = []
                # follow trendsetter with some probability
                for u in vertices[:-1]:
                    if r.random() < 0.5:
                        u.follow(vertices[-1])
                        u.update_trust()
                        u.update_confidence(len(vertices))
                ts_followers.append(unew.num_followers)
                
            if t > t0:
                ts_followers.append(vertices[-1].num_followers)
        
        opinions_over_time.append(opinions_thisStep.copy())
        confidence_over_time.append(confidence_thisStep.copy())
    
    if trendsetter:        
        return opinions_over_time, confidence_over_time, ts_followers
    
    return opinions_over_time, confidence_over_time

def determineConv(opinions, thr = 1e-3):
    maxD = 0.0
    for i in range(len(opinions)):
        for j in range(i, len(opinions)):
            if abs(opinions[i] - opinions[j]) > maxD:
                maxD = abs(opinions[i] - opinions[j])
                
    return maxD < thr
    

"""
    MAIN
"""


if __name__ == "__main__":
    
    # initialize model
    vertices = init_model(n, 0.1)
    
    # simulation
    opinions_over_time, confidence_over_time, ts_followers = simulation(vertices, T, trendsetter = True)
    
    b = np.zeros(len(vertices), dtype = int)
    b[-1] = t0

    # store graph in csv-file
    #W, o = h.build_W_o(vertices)
    #h.make_csv(W)
    # draw graph
    #dg.draw_graph(W, o)
    # show data over time
    

    plt.figure()
    for j in range(len(b)):
        X = np.arange(b[j], T)
        Y = [opinions_over_time[i][j] for i in X]
        plt.plot(X, Y)
    plt.ylabel("opinion")
    plt.xlabel("time")
    
    
    plt.figure()
    for j in range(len(b)):
        X = np.arange(T-b[j])
        Y = [confidence_over_time[T-i-1][j] for i in range(len(X))]
        Y.reverse()
        plt.plot(X, Y)
    plt.ylabel("confidence")
    plt.xlabel("time")
    plt.show()
    
    plt.figure()
    plt.plot(ts_followers)
    plt.show()
    
    
    #%%
    numSamples = 10
    seps = np.linspace(0, 1, 20)
    convProb = []
    
    for sep in seps:
        convSum = 0.0
        for i in range(numSamples):
            vertices = init_model(n, sep)
            ops, _ = simulation(vertices, T)
            convSum += determineConv(ops[-1])
        convProb.append(convSum/numSamples)
     
    #%%
    plt.plot(seps, convProb, '.')
    plt.xlabel('Separation')
    plt.ylabel('Mergin Probability')
    plt.savefig(r'convProb.pdf')
    plt.show()
    
    
    testConv = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 0.7, 0.5, 0.5, 0.4, 0.2, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])