import random
import numpy
import scipy
import matplotlib.pyplot as plt
import math as m
import time as t

from model_v3 import *


"""
############################################################
Specifiy the following parameters for network initialisation.
############################################################
"""

# number of vertices n
# suggested n: 50 to 100. For n >> 100, runtimes are slow.
n = 50

# parameters for normal distribution of vertex confidence; mean and standard deviation
confidence_mean = 0.75
confidence_std = 0.1

# cap on how many vertices can be followed per step (higher number -> longer runtimes typically)
max_follow = 5

# separation of opinions: creates two strands which are separated by sep
# sep must be in [0,1]
sep = 0.0

# following and unfollowing probabilities. (higher bf, lower bu -> more filter bubbles)
# suggested bf: 5, 10, 20. suggested bu: 5, 10, 20.
# you can also implement different p_follow, for example a cutoff p(x) = 0 for x > x_critical
bf = 5
bu = 10
p_follow = lambda opinion_distance: m.exp(-bf*opinion_distance)
p_unfollow = lambda trust: m.exp(-bu*trust)

# trust stability (lower trust stability -> more filter bubbles)
trust_stability = 0.75

"""
############################################################
Initialising the model with the chosen parameters.
############################################################
"""

V = init_model_wrapper(n, confidence_mean, confidence_std, max_follow, sep, p_follow, p_unfollow, trust_stability)

"""
############################################################
Iteration (simulation). Specify the number of steps.
############################################################
"""

# number of steps
# suggested Steps: 100 to 300.
Steps = 100

tstart = t.time()
opinions_over_time = simulation(V, Steps)
tend = t.time()

print(r"Completed after {0:} s".format(tend-tstart))

"""
############################################################
Plotting the opinions.
############################################################
"""

plt.figure()
plt.plot(opinions_over_time)
plt.ylabel("Opinion")
plt.xlabel("Step")
plt.show()
