"""
    Maybe not the most necessary file
"""

import numpy as np

def normalize_rows(A):
    nA = np.linalg.norm(A, ord=1, axis=1, keepdims=True)
    for i in range(np.size(nA)):
        if nA[i] == 0: nA[i] = 1 # avoid division by 0
    A /= nA # normalize

def constraint(x, a, b):
    if x < a: return a
    elif x > b: return b
    else: return x