#calc_wiggled.py
# Takes in wiggled copies of the k, n, dn, and dk from wiggler.py and
# calulates the errors introduced by the spline applied to interpolated points

import numpy as np
from hypercube import wiggler
from hypercube import interpolate

num_wiggled_indices = 10

def stats(data, karray_for_wiggling, narray_for_wiggling, dkarray_for_wiggling, dnarray_for_wiggling):
    
    # Create arrays of length num_wiggled_indices to hold the monte carlo'd n and k values as we create them
    wiggled_karrays = [None]*num_wiggled_indices
    wiggled_narrays = [None]*num_wiggled_indices
    
    #karray_for_wiggling and narray_for_wiggling are reorganized and regridded, containing only the original data and NaNs. They have not been interpolated. Recall that they were created via deepcopy immediately after the collate_organizedata step (see greenbutton.py)

    for i in range(num_wiggled_indices):
        # Wiggle the k and n arrays
        wiggled_karrays[i], wiggled_narrays[i] = wiggler.wiggle_arrays(karray_for_wiggling, narray_for_wiggling, dkarray_for_wiggling, dnarray_for_wiggling)

        # Interpolate the wiggled k and n arrays (fill in missing values)
        t, w, wiggled_karrays[i], wiggled_narrays[i] = interpolate.splineweave(data, wiggled_karrays[i], wiggled_narrays[i]) #these indices verifiable in interpolate.py

    #For each n and k at each wavel and temp, find avg and stdev across wiggles
    print("length of mc_narrays: ", len(wiggled_narrays))
    print("length of first monte carlo'd narray: ", len(wiggled_narrays[0]))
    
    # Stack the MC'd arrays, then calculate mean and stdev for each corresponding point across the stack.
    nstacked = np.stack(wiggled_narrays, axis=0)
    navg = np.nanmean(nstacked, axis=0)
    nstdev = np.nanstd(nstacked, axis=0)

    kstacked = np.stack(wiggled_karrays, axis=0)
    kavg = np.nanmean(kstacked, axis=0)
    kstdev = np.nanstd(kstacked, axis=0)

    # Test that the avg and stdev arrays are the same shape as the wiggled arrays, i.e., there should be one average and one stdev for each wavel-temp cooridnate
    # also check if they contain emoty spaces, which shouldn't happen post-interpolation

    for array in [navg, nstdev, kavg, kstdev]:
        if np.isnan(array).any() == True:
            print("WARNING: NaNs in the average or stdev arrays")
            print(array)
            break
        if array.shape != wiggled_narrays[0].shape:
            print("WARNING: average or stdev arrays are not the same shape as the wiggled arrays")
            break
        else:
            pass
    
    print("shape of navg: ", navg.shape)
    print("shape of nstdev: ", nstdev.shape)
    print("shape of kavg: ", kavg.shape)
    print("shape of kstdev: ", kstdev.shape)
    return navg, nstdev, kavg, kstdev
