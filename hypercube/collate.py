# Combine experimental data from multiple studies into one ri object for easier
# interpolation and extrapolation

import os
import numpy as np
import copy

from hypercube import ri
from hypercube import read_in_lit
from hypercube import interpolate

#Location of experimental data files
#directory = "~/scattering/lit"

def read_all_data(ri, directory):
    # First use read_in_lit to collect data from .txt files into multiple 
    # ri objects

    ri_list = []
    i = 0
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):   #only the refrac files
            #print("files in dir that end with .txt: ", filename)
            #Create ri object populated with data from txt files
            data = read_in_lit.read_data(directory, filename)
            #print("data before deepcopy: ", data.dataset)
            #Get dks
            data.dk = read_in_lit.get_error(data)
            #Deepcopy each attribute in data to avoid overwriting
            dc_data = ri.ri("", [-1], [-1], "", [0], [0], [0], [0]) #Nonsense val
            dc_data.dataset = copy.deepcopy(data.dataset)
            dc_data.wavel = copy.deepcopy(data.wavel)
            dc_data.temp = copy.deepcopy(data.temp)
            #dc_data.errortype = copy.deepcopy(data.errortype)
            dc_data.n = copy.deepcopy(data.n)
            dc_data.k = copy.deepcopy(data.k)
            dc_data.dn = copy.deepcopy(data.dn)
            dc_data.dk = copy.deepcopy(data.dk)
            #print("deepcopy of read data: ", dc_data.dataset)
            #Add deepcopy to list of ris
            ri_list.append(dc_data)
            
    #print("ri_list after reading in data: ", ri_list[0].dataset, ", ", ri_list[1].dataset)
    #print("values within ri_list after reading in data: ")
    #print("wavel: ", ri_list[0].wavel, ", ", ri_list[1].wavel, "\n")
    #print("temp: ", ri_list[0].temp, ", ", ri_list[1].temp, "\n")
    #print("k: ", ri_list[0].k, ", ", ri_list[1].k, "\n")
    #print("n: ", ri_list[0].n, ", ", ri_list[1].n, "\n")


    """
    for i in ri_list:
        print("wavelengths in ", i.dataset, " are ", i.wavel, "right after being added to the list.")
    """
    return ri_list

def avg_stacked_pts(ri_list):

    #If two points from different datasets are at the same coordinates,
    # average em
    #print("ks for ri_list[0]: ", ri_list[0].k)
    #print("ks for ri_list[1]: ", ri_list[1].k)
    for a in range(len(ri_list)):
        for b in range(len(ri_list)):
            #print("dataset of ri_1: ", ri_1.dataset)
            #print("dataset of ri_2: ", ri_2.dataset)
            for c in range(len(ri_list[a].k)):
                #print("wavel in ", ri_1.dataset, " is ", wavel_1)
                for d in range(len(ri_list[b].k)):
                    #print("wavel in ", ri_2.dataset, " is ", wavel_2)
                    #print("Checking if ", ri_list[a].dataset, " ", ri_list[a].temp, " wavelength ", ri_list[a].wavel[c], " matches ", ri_list[b].dataset, " ", ri_list[b].temp, " wavelength ", ri_list[b].wavel[d])
                    if ri_list[a].wavel[c] == ri_list[b].wavel[d] and ri_list[a].temp == ri_list[b].temp:
                        if ri_list[a].k[c] != ri_list[b].k[d]:
                            # Average ks
                            ri_list[a].k[c] = (ri_list[a].k[c] + ri_list[b].k[d])/2
                
                            # Combine dks (assumes dks are same units as k, not % error)
                            #Index error here, not above
                            ri_list[a].dk[c]  = float(ri_list[a].k[c]*(np.sqrt((((ri_list[a].dk[c])/(ri_list[a].k[c]))**2) + (((ri_list[b].dk[d])/(ri_list[b].k[d])**2)))))
                            #print("After averaging, wavel in question is ", ri_list[b].wavel[d])
                        #Remove duplicate points
                        #ri_list[b].dk[d] = None
                        #ri_list[b].k[d] = None
                        #ri_list[b].wavel[d] = None
                        #print("ri_list[a].k: ", ri_list[a].k)
                        #print("ri_list[a].dk: ", ri_list[a].dk)
    #for i in ri_list:
        #print("After averaging and deleting, wavelengths in ", i.dataset, "are ", i.wavel)
        #print("After averaging and deleting, ks in ", i.dataset, "are ", i.k)
    
    return ri_list

def collate(ri, ri_list):

    #Create a 2D array with wavelength on the y and temperature on the x, so
    #that the data can be pushed to collated_ri in an organized state
    #print("ri_list[0].wavel: ", ri_list[0].wavel, "ri_list[0].k: ", ri_list[0].k, "ri_list[1].wavel: ", ri_list[1].wavel, "ri_list[1].k: ", ri_list[1].k) 
    #karray = [None]*len(ri_list)
    #for i in range(len(ri_list)):
    #    karray[i] = np.array([ri_list[i].wavel, ri_list[i].k]).T 
    #print("karray 1: ", karray[0])
    #print("karray 2: ", karray[1])

    #print("ks after averaging: ", ri_list[1].k)
    #Initialize object of class ri
    collated_ri = ri.ri("", [], [], "", [], [], [], [])
    #Deepcopy each attribute in data to avoid overwriting
    #collated_ri.dataset = copy.deepcopy(ri_list[0].dataset)
    #collated_ri.wavel = copy.deepcopy(ri_list[0].wavel)
    #collated_ri.temp = copy.deepcopy(ri_list[0].temp)
    #collated_ri.errortype = copy.deepcopy(ri_list[0].errortype)
    #collated_ri.n = copy.deepcopy(ri_list[0].n)
    #collated_ri.k = copy.deepcopy(ri_list[0].k)
    #collated_ri.dn = copy.deepcopy(ri_list[0].dn)
    #collated_ri.dk = copy.deepcopy(ri_list[0].dk)

    #del(ri_list[0])

    # Does it matter if they're in order of temp and wavel as long as the 
    # ri data stays with its correct w/t coord?
    # I don't think it matters for KKR, absorp_error, and ik it doesn't
    # matter for plotting

    #For each wavelength and temperature in designated space, check if
    # there's data in our list of ris and if yes, add to collated ri obj
    """
    for wavel_index in range(interpolate.wavel_min, interpolate.wavel_max,
            interpolate.wavel_step):
        for temp_index in range(interpolate.temp_min, interpolate.temp_max,
                    interpolate.temp_step):
            for obj in ri_list:
                for wavel in obj.wavel:
                    for temp in obj.temp:
                        if wavel <= wavel_index and 
        """
    # Will this fuck up my indexing? Each column should have the same # 
    # of rows. So adding each column separately shouldn't disturb the index
    # of rows in each distinct ri relative to each other
    for i in (range(len(ri_list))):
        #i = i + 1 #Skip first obj in ri_list, since it's already added
        #print("wavels in obj: ", obj.wavel)
        #print("dataset in obj: ", obj.dataset)
        for j in range(len(ri_list[i].wavel)):
            if ri_list[i].wavel[j] not in collated_ri.wavel or ri_list[i].temp not in collated_ri.temp:
                collated_ri.wavel.append(copy.deepcopy(ri_list[i].wavel[j]))
                collated_ri.k.append(copy.deepcopy(ri_list[i].k[j]))
                collated_ri.dk.append(copy.deepcopy(ri_list[i].dk[j]))
        #Temps are a lil different, bc they're 1 float per dataset until
        #this point. Adding them together will add the floats, not append.
        #Gotta cast as arrays
        #print("During collation, dks are ", ri_list[i].dk)
        if ri_list[i].temp not in collated_ri.temp:
            collated_ri.temp.append(copy.deepcopy(ri_list[i].temp))

        #if ri_list[i].temp not in collated_ri.temp:
        #    collated_ri.temp.append(copy.deepcopy(ri_list[i].temp))
        #How to make ks match the wavels, even if k can repeat values unlike wavel?
        """
        for j in range(len(ri_list[i].k)):
            if ri_list[i].wavel[j] in collated_ri.wavel:
                collated_ri.k.append(copy.deepcopy(ri_list[i].k[j]))  
                collated_ri.dk.append(ri_list[i].dk[j])
        """
    #print("wavels after collation: ", collated_ri.wavel)
    #print("ks after collation: ", collated_ri.k)
    # Not adding ns even if some come from the source data bc ns missing from
    # some datasets would mess up the indexing
    return collated_ri, ri_list

def organize_array(collated_ri, ri_list):
    #Set up empty arrays of dimensions wavelength and temp
    #This step happens after KKR and KKR prop!
    #for ri in ri_list:
        #print("first wavels in ri_list: ", ri.wavel[0])
    wtarray = np.empty((1, 2))
    karray = np.empty((len(collated_ri.temp), len(collated_ri.wavel)))
    narray = np.empty((len(collated_ri.temp), len(collated_ri.wavel)))
    dkarray = np.empty((len(collated_ri.temp), len(collated_ri.wavel)))
    dnarray = np.empty((len(collated_ri.temp), len(collated_ri.wavel)))

    #print("collated wavels before sorting into array: ", collated_ri.wavel) 
    #print("collated ks before sorting into array: ", collated_ri.k)
    #Fill in points in array for which we have data
    for a in range(len(ri_list)):
        for b in range(len(collated_ri.temp)):
            for c in range(len(collated_ri.wavel)):
                for d in range(len(ri_list[a].wavel)):
                    #print("Temps: ", ri_list[a].temp, collated_ri.temp[b])
                    #print("wavels: ", ri_list[a].wavel[d], collated_ri.wavel[c])
                    #print("ks: ", ri_list[a].k[c], collated_ri.k[c])
                    if ri_list[a].temp == collated_ri.temp[b] and ri_list[a].wavel[d] == collated_ri.wavel[c] and ri_list[a].k[d] == collated_ri.k[c]:
                        wtarray = np.vstack((wtarray, [collated_ri.wavel[c], collated_ri.temp[b]]))
                        #print("wtarray: ", wtarray)
                        karray[b][d] = ri_list[a].k[d]
                        narray[b][d] = collated_ri.n[c]
                        dkarray[b][d] = ri_list[a].dk[d]
                        dnarray[b][d] = collated_ri.dn[c]
    #Clean up wtarray
    tupled_wtarray = [tuple(row) for row in wtarray[1:]]
    clean_wtarray = np.unique(tupled_wtarray, axis=0)
    
    #print("karray: ", karray)
    #print("narray: ", narray)
    #print("dkarray: ", dkarray)
    #print("dnarray: ", dnarray)
    #print("wtarray: ", clean_wtarray)

    return collated_ri, clean_wtarray, karray, narray, dkarray, dnarray

def organize_arrayv2(collated_ri, ri_list):
    """
    Drafted partially with chatgpt, HM June 26 2024
    This function takes in the ri object after data from all the sources has been collated, i.e., added to one ri object and overlapping points averaged. The purpose of this function is to create arrays of k, n, dk, and dn where original data is placed at indices wavel, temp. Indices where we don't have original data get a NaN. The NaNs are essential for the interpolation fucntion to apply its mask correctly.
    The output arrays (n, k, dn, and dk) should be of shape (T, W) where T is length of the array of temperature we wish to interpolate over (i.e., from the lowest temperature we have original data for to the highest temperature we have data for in steps of arbitrary size t_step. similarly for wavelength.) 
    """
    #Set up empty arrays of dimensions wavelength and temp
    #This step happens after KKR and KKR prop!
    #wtarray = np.empty((1, 2))
    karray = np.empty((len(collated_ri.temp), len(collated_ri.wavel)))
    narray = np.empty((len(collated_ri.temp), len(collated_ri.wavel)))
    dkarray = np.empty((len(collated_ri.temp), len(collated_ri.wavel)))
    dnarray = np.empty((len(collated_ri.temp), len(collated_ri.wavel)))
    
    #Fill in points in array for which we have data
    for a in range(len(ri_list)):
        for b in range(len(collated_ri.temp)):
            for c in range(len(collated_ri.wavel)):
                for d in range(len(ri_list[a].wavel)):
                    if ri_list[a].temp == collated_ri.temp[b] and ri_list[a].wavel[d] == collated_ri.wavel[c] and ri_list[a].k[d] == collated_ri.k[c]:
                        #wtarray = np.vstack((wtarray, [collated_ri.wavel[c], collated_ri.temp[b]]))     
                        karray[b][d] = ri_list[a].k[d]
                        narray[b][d] = collated_ri.n[c]
                        dkarray[b][d] = ri_list[a].dk[d]
                        dnarray[b][d] = collated_ri.dn[c]
    # Check that the newly organized narray, karray, dnarray, and dkarray are the same shape
    if narray.shape == karray.shape:
        print("narray and karray are same shape, we good")
    else:
        print("narray and karray are different shapes, we bad")
    if dnarray.shape == karray.shape:
        print("dnarray and karray are same shape, we good")
    else:
        print("dnarray and karray are different shapes, we bad")
    if dkarray.shape == karray.shape:
        print("dkarray and karray are same shape, we good")
    else:
        print("dkarray and karray are different shapes, we bad")

    #Clean up wtarray
    #tupled_wtarray = [tuple(row) for row in wtarray[1:]]
    #clean_wtarray = np.unique(tupled_wtarray, axis=0)

    #Place original data into a matrix of defined size, where coordinates without data receiev NaN
    #Note: this local definition of T and W defines a space of interpolation, not extrapolation. in interpolate.py, one can define a larger range of temps and wavels to extrapolate over if desired. For this purpose, however, we just want a grid to interpolate over.
    """
    T = int(collated_ri.temp[-1] - collated_ri.temp[0]) #steps between max and min temp, step sizes is 1 K
    W = int(collated_ri.wavel[-1]*100000 - collated_ri.wavel[0]*100000) #steps between max and min wavel, step size is 0.000001 micron, TODO update
    #print("w: ", W)
    #print("t: ", T)
    Warray = np.linspace(collated_ri.wavel[0], collated_ri.wavel[-1], W)
    Tarray = np.linspace(collated_ri.temp[0], collated_ri.temp[-1], T)

    #bucket to hold output for each n, k, dn, dk
    bucket = []

    for array in [karray, narray, dkarray, dnarray]:
        # Initialize the array of real indicies with NaNs
        data = np.full((T, W), np.nan)

        # Convert array to a list of tuples (t, w, value)
        array_tuples = [(i, j, array[i, j]) 
                        for i in range(len(collated_ri.temp)) 
                        for j in range(len(collated_ri.wavel))]

        # Populate the data array with values from n_array_tuples
        for t, w, value in array_tuples:
            if t < T and w < W:
                data[t, w] = value

        bucket.append(data)

    f = open("bucket_n.txt", "w")
    for i in bucket[0]:
        for j in i:
            f.write(str(j) + ",")
        f.write("\n")
    f.close()
    """
    # Define new, higher-resolution temp and wavel arrays
    new_temp = np.arange(min(collated_ri.temp), max(collated_ri.temp), 1) #step size is 1 K
    new_wavel = np.arange(min(collated_ri.wavel), max(collated_ri.wavel), 0.01) #step size is 0.01 micron

    # Initialize the new data array with NaNs
    data = np.full((len(new_temp), len(new_wavel)), np.nan)

    # Initialize arrays to store differences
    # narray, karray, dnarray, dkarray should all be the same shape -- checked immediately after organization step
    temp_diff = np.full(narray.shape, np.nan)
    wavel_diff = np.full(narray.shape, np.nan)

    arrays = [] # bucket to store the regridded data in for return
    
    # Function to find the closest index in the new grid
    def find_closest_index(array, value):
        # Subtracts the value from each item in the array and returns the index of the item with the minimum difference, i.e., the index of the item closest in value to the given value
        return (np.abs(array - value)).argmin()

    # Populate the new data array with values from n_array at mapped positions and calculate differences
    for array in [karray, narray, dkarray, dnarray]:
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                new_t_index = find_closest_index(new_temp, collated_ri.temp[i])
                new_w_index = find_closest_index(new_wavel, collated_ri.wavel[j])
                data[new_t_index, new_w_index] = array[i, j]

                #check that the points haven't been shifted too much during mapping to the new, higher-resolution grid
                temp_diff[i, j] = new_temp[new_t_index] - collated_ri.temp[i]
                wavel_diff[i, j] = new_wavel[new_w_index] - collated_ri.wavel[j]

                if temp_diff[i, j] > 0.5:
                        print("WARNING: during mapping, the index/error at ", collate_ri.temp[i], collate_ri.wavel[j], " has been shifted in temperature more than 0.5 K.")

                if wavel_diff[i, j] > 0.005:
                        print("WARNING: during mapping, the index/error at ", collate_ri.temp[i], collate_ri.wavel[j], " has been shifted in wavelength more than 0.005 micron.")
        
        #Add the new gridded array, now with all the original data added and all the empty spaces NaN, to the bucket
        arrays.append(data)

    # check formatting of organized and remapped data is correct
    f = open("bucket_n.txt", "w")
    for i in arrays[0]:
        for j in i:
            f.write(str(j) + ",")
        f.write("\n")
    f.close()

    return arrays[0], arrays[1], arrays[2], arrays[3]

