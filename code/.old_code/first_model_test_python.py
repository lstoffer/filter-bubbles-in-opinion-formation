#!/usr/bin/env python
# coding: utf-8


import numpy as np
import matplotlib.pyplot as plt
import random


class vertex:
    """
    CLASS FUNCTIONS

    init: set up vertex with tag and parameters
    update_opinion: determines how this vertex changes his opinion each time step depending on his connections
    update_following: determines how the vertex changes his connections each time step
    follow: adds a vertex to the connections
    unfollow: removes a vertex from the connections
    update_weight: determines how the bond weight for a connection is updated each time step
    status_report: prints list of connections (following)
    """
    
    def __init__(self, tag, params = {'p_accept': lambda x, y: 0.5,
                                      'p_unfollow': lambda x: 1.0 - x,
                                      'ud_bweight': lambda x, y: 0.5*(x + (1.0 - np.abs(y))),
                                      'g_degree': 0.5}):
        """
        additional parameters to manually set up 'controlling vertices'?
        p_accept: probability to follower a proposed vertex, function of own's opinion (x) and proposed vertex opinion (y)
        p_unfollow: probability to unfollow a vertex, function of bond weight
        ud_bweight: update the bond weight depending on the current weight and the difference in opinion
        g_degree: degree to which the vertex adheres to his opinion (see Review_Opinion_Dynamics p.4)
        """
        


        self.tag = tag # number (or name) to keep track of vertices
        
        # set up initial opinion (this can be changed). at the moment: 2 main groups with slight variations
        self.opinion = random.random() # opinion spectrum (or finite number of opinions?)
        if self.opinion >= 0.5:
            self.opinion += 0.5*(1.0 - self.opinion)
        else:
            self.opinion -= 0.5*self.opinion
            
            
        self.following = [] # list: [ [tag, weight] ] of followers
        self.p_a = lambda y: params['p_accept'](self.opinion, y)
        self.p_u = params['p_unfollow']
        self.ud_bw = params['ud_bweight']
        self.g = params['g_degree']
    
    def update_opinion(self):
        # THIS FUNCTION COULD BE ADDED AS A PARAMETER IN INIT
        # update the opinion according to
        # new_opinion = g*(old_opinion) + (1-g)*sum(partner_opinion*bond_weight)
        opinion_mean = 0.0
        tot_bondweight = 0.0
        for bond in self.following:
            tot_bondweight += bond[1]
            opinion_mean += get_vertex(bond[0]).opinion*bond[1]
            
        if tot_bondweight == 0:
            opinion_mean = self.opinion
        
        else:
            opinion_mean = opinion_mean/tot_bondweight
        
        self.opinion = self.g*self.opinion + (1.0 - self.g)*opinion_mean
    
    def update_following(self):
        # update the following list
        i = 0
        for bond in self.following:
            bond_op = get_vertex(bond[0]).opinion
            bond[1] = self.ud_bw(bond[1], self.opinion - bond_op)
            if random.random() > bond[1]:
                self.unfollow(i)
            i += 1
    
    def follow(self, tag, weight):
        # follow selected vertex
        self.following.append([tag, weight])
    
    def unfollow(self, i):
        # unfollow a vertex
        self.following.pop(i)
        
    def update_weight(self, i, weight):
        # assign new weight to connection
        self.following[i][1] = weight
        
    def status_report(self):
        # print following list
        print(self.following)
        
        

def get_vertex_generator(vertices):
    """
    input: list of vertices
    
    output: returns function get_vertex which returns the vertex with a given tag
    """
    
    def get_vertex(tag):
        # returns the vertex with tag
        return vertices[tag]
    
    return get_vertex
        



def suggest_vertex(v, i):
    """
    input:
        v: vertex who decides if to follow
        i: index of suggested vertex
    
    uses the vertex' v 'p_a' function to decide if v will follow vertex i
    """
    a = random.random()
    op = get_vertex(i).opinion
    if a < v.p_a(op):
        # initial bond strength can also be set differently
        v.follow(i, v.ud_bw(0.0, v.opinion - op))
    



def gen_p_suggest(b):
    # generates suggestion probability function
    
    def p_suggest(x):
        # probability to suggest a vertex depending on difference in opinion
        # to implement filter bubbles
        # x: absolute value of opinion difference
        return 0.75*np.exp(-b*x)
    
    return p_suggest

n_suggestions = 1 # maximal number of suggestions per time step

def manage_suggestions(vertices):
    """
    input: list of vertices

    iterates through vertices and suggests other vertices to follow with a certain probability
    """

    N = len(vertices)
    for i in range(N):
        n0 = 0
        v = get_vertex(i)
        v_op = v.opinion
        for j in range(N):
            if n0 < n_suggestions:
                if i != j:
                    a = random.random()
                    if a < p_suggest(np.abs( v_op - get_vertex(j).opinion )):
                        suggest_vertex(v, j)
                        n0 += 1
            else:
                break
                    



def time_step(vertices):
    """
    input: list of vertices

    one time step of updating the network

    output: list of current opinions and the total number of connections
    """

    N = len(vertices)
    ops = []
    n_connections = 0
    
    # suggest vertices
    manage_suggestions(vertices)
    
    for i in range(N):
    # update the vertices using their inbuilt functions
        v = get_vertex(i)
        v.update_following()
        v.update_opinion()
        ops.append(v.opinion)
        n_connections += len(v.following)
        
    return ops, n_connections

def iterate(T, vertices):
    """
    input:
        T: number of time steps
        vertices: list of vertices

    time iteration using time_tep

    output: complete opinion array and number of connections array
    """

    Ops = []
    N_connections = []
    
    for t in range(T):
        ops, n_connections = time_step(vertices)
        Ops.append(ops)
        N_connections.append(n_connections)
        
    return np.array(Ops), np.array(N_connections)



if __name__ == '__main__':

    """
    do the time iteration for different coefficients for the p_suggest function
    """

    coeffs = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0]
    plt.figure()
    R = 1

    for b in coeffs:

        # Generate the initial network

        # generate vertices
        p_suggest = gen_p_suggest(b)
        N = 25
        V = []
        for i in range(N):
            V.append(vertex(i))

        get_vertex = get_vertex_generator(V)

        # set up initial vertex connections for the network
        for i in range(N):
            v = get_vertex(i)
            for j in range(N):
                if i != j:
                    a = random.random()
                    if a < p_suggest(np.abs( v.opinion - get_vertex(j).opinion )): # arbitrary function
                        suggest_vertex(v, j)

        

        # begin time iteration with T time steps
        T = 75

        Ops, Ns = iterate(T, V)


        # plot in multiplot
        TA = np.linspace(0, T-1, T)
        plt.subplot(2,3,R)
        for i in range(Ops.shape[1]):
            plt.plot(TA, Ops[:,i], linewidth = 0.75)
        plt.xticks([])
        plt.yticks([])
        plt.title('b = {0:}'.format(b))
            
        R += 1
    plt.savefig('img/multiplots_test.pdf')        
    plt.show()


