#calc_wiggled.py
# Takes in wiggled copies of the k, n, dn, and dk from wiggle_ri.py and
# calulates the errors introduced by the spline applied to interpolated points

import numpy as np
from hypercube import ri_wiggler
from hypercube import ri

num_wiggled_indices = 100

#TODO: read in # of wavels

#Wiggle indices num_wiggled_indices times
def wiggle_indices_n_times(ri):
    # wiggled_indices = [[0 for i in range(num_wiggled_indices)] for j in range(ri.wavel)]
    for i in range(num_wiggled_indices):
        #Make a copy of original indices list
        ri_copy = ri_wiggler.copy_ri(ri)
        #Wiggle each n and k at each wavelength point in list
        wiggled_ris[i] = ri_wiggler.wiggle_indices(ri_copy)
    return wiggled_ris

"""
def interpolate_wiggled_ris(wiggled_ris):
        #Interpolate via spline

        #For each n and k at each wavel, find avg and stdev across wiggles
"""

def extrapolate_wiggled_ris(wiggled_ris):
        #Extrapolate via spline
        for i in range(num_wiggled_indices):
            n_extra[i] = interpolate.spline(wiggled_ris[i])[6]
            k_extra[i] = interpolate.spline(wiggled_ris[i])[8]

        #For each n and k at each wavel, find avg and stdev across wiggles
        for i in range(len(ri.wavel)):
            ri.n_avg[i] = np.average(n_extra[i])
            ri.n_stdev[i] = np.std(n_extra[i])
            ri.k_avg[i] = np.average(k_extra[i])
            ri.k_stdev[i] = np.std(k_extra[i])

    return ri.n_avg, ri.n_stdev, ri.k_avg, ri.k_stdev
