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

import draw_graph as sg
import helper as h

n = 50 # number of vertices (individuals)
bf = 10 # see p_follow
bu = 5 # see p_unfollow
T = 100 # number of timesteps

p_follow = lambda d: m.exp(-bf*abs(d)) # the joint probability of p_accept and p_suggest
p_unfollow = lambda trust, deg: m.exp(-bu*deg/(trust+1)) # or 1 - trust
opinion_generator = lambda x: (0.5*x, 0.5*x + 0.5) [int(x >= 0.5)]
confidence_generator = lambda x: min(x + 0.1, 1.0)

"""
    VERTEX CLASS
"""
class Vertex:
    def __init__(self, number, opinion, confidence):
        self.number = number
        self.opinion = opinion
        self.confidence = confidence
        self.neighbours = []  # list of individuals this vertex follows
        self.trust = {}  # maps for all neighbours from v.number to "trust in v"-value
    
    def update_opinion(self):
        other_opinions = 0.0
        for v in self.neighbours:
            other_opinions += self.trust[v.number] * v.opinion
        self.opinion = self.opinion*self.confidence + (1.0-self.confidence)*other_opinions
    
    def update_neighbours(self, vertices):
        # (this function is implemented in a different way then Beat's function)
        for v in vertices:
            if v in self.neighbours:
                # unfollow
                deg = len(self.neighbours)
                if deg > 0:
                    if r.random() < p_unfollow(self.trust[v.number], float(deg)):
                        self.neighbours.remove(v)
                        del self.trust[v.number]
            else:
                # suggest follower
                if r.random() < p_follow(self.opinion - v.opinion):
                    self.neighbours.append(v)
                    self.trust[v.number] = 1.0 / max(n, 1.0)
    
    def update_trust(self):
        trust_sum = 0.0
        for v in self.neighbours:
            self.trust[v.number] += self.trust[v.number] * (v.confidence - abs(self.opinion - v.opinion))
            trust_sum += self.trust[v.number]
        # normalize => sum of "given trust" should be the same (1.0) for all individuals
        for v in self.neighbours:
            self.trust[v.number] /= trust_sum
    
    def update_confidence(self, avg_d):
        # avg_d = average of opinion_differences
        self.confidence += avg_d - self.opinion_differences()
        # make sure that confidence stays between 0.0 and 1.0
        self.confidence = h.constraint(self.confidence, 0.0, 1.0)
    
    def opinion_differences(self):
        # returns average of opinion differences between its neighbours
        opinion_difference = 0.0
        for v in self.neighbours:
            opinion_difference += abs(self.opinion - v.opinion)
            # alternative: += self.trust[v.number] * abs(self.opinion - v.opinion)
        return opinion_difference / max(1.0, len(self.neighbours))

"""
    FUNCTIONS for SIMULATION
"""
def avg_opinion_difference(vertices):
    sum = 0.0
    for u in vertices:
        sum += u.opinion_differences()
    return sum / len(vertices)

def init_model(n):
    vertices = []
    for u in range(n):
        vertices.append(Vertex(u, opinion_generator(r.random()), confidence_generator(r.random())))
    return vertices

def simulation(vertices, T):
    opinions_over_time = np.zeros((T, len(vertices)))
    confidence_over_time = np.zeros((T, len(vertices)))
    avg_d_over_time = np.zeros(T)
    for t in range(T):
        avg_d = avg_opinion_difference(vertices)
        avg_d_over_time[t] = avg_d
        for u in vertices:
            opinions_over_time[t,u.number] = u.opinion
            confidence_over_time[t,u.number] = u.confidence
            u.update_opinion()
            u.update_neighbours(vertices)
            u.update_trust()
            u.update_confidence(avg_d)
    return opinions_over_time, confidence_over_time, avg_d_over_time

"""
    MAIN
"""
if __name__ == "__main__":
    
    # initialize model
    vertices = init_model(n)
    
    #simulation
    opinions_over_time, confidence_over_time, avg_d_over_time = simulation(vertices, T)

    # show data over time
    plt.plot(opinions_over_time)
    plt.ylabel("opinion")
    plt.xlabel("time")
    plt.show()
    plt.plot(confidence_over_time)
    plt.ylabel("confidence")
    plt.xlabel("time")
    plt.show()
    plt.plot(avg_d_over_time)
    plt.ylabel("average opinion difference")
    plt.xlabel("time")
    plt.show()