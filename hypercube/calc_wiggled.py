#calc_wiggled.py
# Takes in wiggled copies of the k, n, dn, and dk from wiggle_ri.py and
# calulates the errors introduced by the spline applied to interpolated points

import numpy as np
from hypercube import ri_wiggler
from hypercube import ri
from hypercube import interpolate

num_wiggled_indices = 10

#TODO: read in # of wavels

#Wiggle indices num_wiggled_indices times
def wiggle_indices_n_times(ri):
    wiggled_ris = [None]*num_wiggled_indices
    for i in range(num_wiggled_indices):
        #Make a copy of the original indices list
        ri_copy = ri_wiggler.copy_ri(ri)
        #Wiggle each n and k at each wavelength point in list
        wiggled_ris[i] = ri_wiggler.wiggle_indices(ri_copy)
    pack = (ri, wiggled_ris)
    return pack

"""
def interpolate_wiggled_ris(wiggled_ris):
        #Interpolate via spline

        #For each n and k at each wavel, find avg and stdev across wiggles
"""

def extrapolate_wiggled_ris(pack):
    ri = pack[0]
    wiggled_ris = pack[1]
    #Extrapolate via spline
    n_extra = [None]*num_wiggled_indices
    k_extra = [None]*num_wiggled_indices
    for i in range(num_wiggled_indices):
        n_extra[i] = interpolate.spline(wiggled_ris[i])[6]
        k_extra[i] = interpolate.spline(wiggled_ris[i])[8]

    #For each n and k at each wavel, find avg and stdev across wiggles
    #print("len of ri.n_avg: ", len(ri.n_avg))
    #print("len of wiggled_ris[0].wavel: ", len(wiggled_ris[0].wavel))
    #print("n_extra: ", n_extra)
    #print("k_extra: ", k_extra)
    for i in range(len(wiggled_ris[0].wavel)):
        ri.n_avg[i] = np.nanmean(n_extra[i])
        ri.n_stdev[i] = np.nanstd(n_extra[i])
        ri.k_avg[i] = np.nanmean(k_extra[i])
        ri.k_stdev[i] = np.nanstd(k_extra[i])

    return ri.n_avg, ri.n_stdev, ri.k_avg, ri.k_stdev
