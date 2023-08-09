# Combine experimental data from multiple studies into one ri object for easier
# interpolation and extrapolation

import os
import numpy as np
import copy

from hypercube import ri
from hypercube import read_in_lit
from hypercube import interpolate

#Location of experimental data files
directory = "~/scattering/lit"

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
            for c in range(len(ri_list[a].k) - 1):
                #print("wavel in ", ri_1.dataset, " is ", wavel_1)
                for d in range(len(ri_list[b].k) - 1):
                    #print("wavel in ", ri_2.dataset, " is ", wavel_2)
                    if ri_list[a].k[c] != ri_list[b].k[d] and ri_list[a].wavel[c] == ri_list[b].wavel[d] and ri_list[a].temp == ri_list[b].temp:
                        # Average ks
                        ri_list[a].k[c] = (ri_list[a].k[c] + ri_list[b].k[d])/2
                
                        # Combine dks (assumes dks are same units as k, not % error)
                        #Index error here, not above
                        ri_list[a].dk[c]  = float(ri_list[a].k[c]*(np.sqrt((((ri_list[a].dk[c])/(ri_list[a].k[c]))**2) + (((ri_list[b].dk[d])/(ri_list[b].k[d])**2)))))
                        #print("After averaging, wavel in question is ", ri_list[b].wavel[d])
                        # Remove duplicate point
                        del(ri_list[b].dk[d])
                        del(ri_list[b].k[d])
                        del(ri_list[b].wavel[d])
    #for i in ri_list:
        #print("After averaging and deleting, wavelengths in ", i.dataset, "are ", i.wavel)
        #print("After averaging and deleting, ks in ", i.dataset, "are ", i.k)
    return ri_list

def collate(ri, ri_list):

    #Initialize object of class ri, add in first ri from list
    collated_ri = ri_list[0]
    #Deepcopy each attribute in data to avoid overwriting
    collated_ri = ri.ri("", [-1], [-1], "", [0], [0], [0], [0]) #Nonsense val
    collated_ri.dataset = copy.deepcopy(ri_list[0].dataset)
    collated_ri.wavel = copy.deepcopy(ri_list[0].wavel)
    collated_ri.temp = copy.deepcopy(ri_list[0].temp)
    #collated_ri.errortype = copy.deepcopy(ri_list[0].errortype)
    collated_ri.n = copy.deepcopy(ri_list[0].n)
    collated_ri.k = copy.deepcopy(ri_list[0].k)
    collated_ri.dn = copy.deepcopy(ri_list[0].dn)
    collated_ri.dk = copy.deepcopy(ri_list[0].dk)

    del(ri_list[0])
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
    for obj in ri_list:
        #print("wavels in obj: ", obj.wavel)
        #print("dataset in obj: ", obj.dataset)
        collated_ri.wavel = collated_ri.wavel + obj.wavel
        #Temps are a lil different, bc they're 1 float per dataset until
        #this point. Adding them together will add the floats, not append.
        #Gotta cast as arrays
        collated_ri.temp = [collated_ri.temp] + [obj.temp]
        collated_ri.k = collated_ri.k + obj.k
        collated_ri.dk = collated_ri.dk + obj.dk
        #print("wavels after everything: ", collated_ri.wavel)
    # Not adding ns even if some come from the source data bc ns missing from
    # some datasets would mess up the indexing

    return collated_ri

