"""
Made by Team Bubble Trouble for Agent-Based Modeling and Social System Simulation

Autumn Semester 2019

"""

import numpy as np
import math as m
import random as r
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import truncnorm
import time

import vertex as v
import draw_graph as dg

"""____                                _            
 |  __ \                              | |           
 | |__) |_ _ _ __ __ _ _ __ ___   ___ | |_ ___ _ __ 
 |  ___/ _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__|
 | |  | (_| | | | (_| | | | | | |  __/||   __/ |   
 |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|   
""" 

# ------------------------------------------------------------- #
# Specifiy the following parameters for network initialization. #
# ------------------------------------------------------------- #
n = 50 # number of vertices (agents)
T = 200 # number of timesteps
# less filter bubbles for bf -> 0 and bu -> infinity
bf = 50 # beta_f
bu = 20 # beta_u
trust_stability = 0.99
confidence_mean = 0.9
confidence_std = 0.1
max_follow = 3 # maximum amount one can add to following in one simulation step

# ------------------------------- #
# Specifiy what you want to plot. #
# ------------------------------- #
PLOT_OPINION = True
PLOT_CONFIDENCE_DIST = True
PLOT_NETWORK = False # could take some time for n > 100
MAKE_CSV = False # makes a csv file that's compatible with gephi (weighted adjacency matrix)



"""_____ _                 _       _   _             
  / ____(_)               | |     | | (_)            
 | (___  _ _ __ ___  _   _| | __ _| |_ _  ___  _ __  
  \___ \| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \ 
  ____) | | | | | | | |_| | | (_| | |_| | (_) | | | |
 |_____/|_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|
"""
# -----------------------#
#       Functions        #
# -----------------------#
def init_model(n, bf, bu):
    p_follow = lambda opinion_distance: m.exp(-bf*opinion_distance)
    p_unfollow = lambda trust: m.exp(-bu*trust)
    vertices = []
    a, b = (0.01 - confidence_mean) / confidence_std, (0.99 - confidence_mean) / confidence_std
    for u in range(n):
        o = r.random()
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

# ------------------#
#       MAIN        #
# ------------------#
if __name__ == "__main__":

    # initialize model
    vertices = init_model(n, bf, bu)

    # simulation
    opinions_over_time = simulation(vertices, T)

    # Show results
    # show opinion over time
    if PLOT_OPINION:
        plt.plot(opinions_over_time)
        plt.title("opinion change")
        plt.ylabel("opinion")
        plt.xlabel("time")
        plt.show()
    # show confidence distribution
    if PLOT_CONFIDENCE_DIST:
        c = np.zeros(n)
        for u in vertices:
            c[u.number] = u.confidence
        plt.xlim(0,1)
        plt.hist(c)
        plt.title("confidence distribution")
        plt.ylabel("number of vertices")
        plt.xlabel("confidence")
        plt.show()

    # show network
    if PLOT_NETWORK:
        dg.draw_graph(vertices)
    # store network csv file
    if MAKE_CSV:
        dg.make_csv(vertices)
