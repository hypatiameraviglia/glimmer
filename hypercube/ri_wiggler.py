#ri_wiggler.py
import random
import copy

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

#Deep copy (keep original) of refractive indices
def copy_ri(indices):
    indices_copy = copy.deepcopy(indices)
    return indices_copy

#Wiggle 'em
def wiggle_indices(indices_copy):
    for index in indices_copy:
        #Establish bounds
        n_max = n + dn
        n_min = n - dn
        k_max = k + dk
        k_min = k - dk

        #wiggle
        n = random.uniform(n_bottom, n_top)
        k = random.uniform(k_bottom, k_top)
    return indices_copy
