#calc_wiggled.py

import numpy as np
from hypercube import ri_wiggler

num_wiggled_indices = 10

#TODO: read in # of wavels
#Wiggle indices num_wiggled_indices times
def wiggle_indices_n_times(indices):
    wiggled_indices = [[0 for i in range(num_wiggled_indices)] for j in range(wavel)]
    for i in range(num_wiggled_indices):
        #Make a copy of original indices list
        indices_copy = ri_wiggler.copy_ri(indices)
        #Wiggle each index at each wavelength point in list
        wiggled_indices = ri_wiggler.wiggle_indices(indices_copy)
        
