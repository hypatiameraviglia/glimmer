#wiggler.py
# Takes in organized, regridded arrays and randomly reselects each n and 
# k within their error bounds to be re-splined

import random
import copy
#from hypercube import ri
import numpy as np

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
"""
#Wiggle 'em
def wiggle_indices(karray_for_wiggling, narray_for_wiggling, dkarray_for_wiggling, dnarray_for_wiggling):
    #print("Length of wavel: ", len(ri_copy.wavel))
    #print("Length of n: ", len(ri_copy.n))
    #print("Length of nmin: ", len(ri_copy.nmin))
    for i in range(len(ri_copy.wavel)):
        #wiggle
        #print("ri_copy.n[i]:", ri_copy.n[i])
        #print("ri_copy.nmin[i]:", ri_copy.nmin[i])
        #print("ri_copy.nmax[i]:", ri_copy.nmax[i])
        ri_copy.n[i] = random.uniform(ri_copy.nmin[i], ri_copy.nmax[i])
        ri_copy.k[i] = random.uniform(ri_copy.kmin[i], ri_copy.kmax[i])
    return ri_copy
"""

def wiggle(array, darray):
    # calculate upper bound
    array_max = array + darray
    # calculate lower bound
    array_min = array - darray
    print("check array_max: ", array_max)
    print("check array_min: ", array_min)
    
    # array_min and array_max will contain some NaNs because the array does (we haven't interpolated yet) -- this will break np.random.uniform, so we have to maks them out
    # Create a mask for NaNs
    nan_mask = np.isnan(array_max) | np.isnan(array_min) # True where array_max OR array_min is NaN

    # Generate random values between B and C for valid positions
    wiggled_array = np.empty_like(array_max)
    valid_mask = ~nan_mask # False where array_max OR array_min is NaN
    
    # generate random number between upper and lower bounds for each valid data point
    wiggled_array[valid_mask] = np.random.uniform(array_min[valid_mask], array_max[valid_mask])

    # Set NaNs where the original arrays had NaNs
    wiggled_array[nan_mask] = np.nan

    # generate random number between upper and lower bounds
    #wiggled_array = np.random.uniform(array_min, array_max)

    return wiggled_array

def wiggle_arrays(karray_for_wiggling, narray_for_wiggling, dkarray_for_wiggling, dnarray_for_wiggling):
    
    #double check karray, narray, dkarray, and dnarray are the same shape
    if (karray_for_wiggling.shape == narray_for_wiggling.shape) and (dkarray_for_wiggling.shape == karray_for_wiggling.shape) and (dnarray_for_wiggling.shape == karray_for_wiggling.shape):
        pass
    else:
        print("Error: copied arrays (for wiggling) are not the same shape! Cannot wiggle.")

    #vectorized_wiggle = np.vectorize(wiggle)
    wiggled_karray = wiggle(karray_for_wiggling, dkarray_for_wiggling)
    wiggled_narray = wiggle(narray_for_wiggling, dnarray_for_wiggling)
    
    return wiggled_karray, wiggled_narray
