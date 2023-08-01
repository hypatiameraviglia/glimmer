#ri_wiggler.py
# Takes in an ri object, makes a deep copy, and randomly reselects each n and 
# k within their error bounds to be re-splined

import random
import copy
from hypercube import ri

"""
#TODO: set up separate doc with n, k, dn, dk
#Read in array of indices from lit
def read_ri(dataset):
    for dataset in [n, k, dn, dk]:
        f = open(dataset, "r")
        lines = f.readlines()[1:]
        dataset = []
        for i in lines:
            dataset.append(float(i.split(' ')[1]))
        f.close()
    return [n, k, dn, dk]
"""

#Deep copy (keep original) of refractive indices
def copy_ri(ri):
    ri_copy = copy.deepcopy(ri)
    return ri_copy

#Wiggle 'em
def wiggle_indices(ri_copy):
    for i in range(len(ri_copy.wavel)):
        #wiggle
        ri_copy.n[i] = random.uniform(ri_copy.nmin[i], ri_copy.nmax[i])
        ri_copy.k[i] = random.uniform(ri_copy.kmin[i], ri_copy.kmax[i])
    return ri_copy
