# Combine experimental data from multiple studies into one ri object for easier
# interpolation and extrapolation

import os
import numpy as np

from hypercube import ri
from hypercube import read_in_lit
from hypercube import interpolate

#Location of experimental data files
directory = "~/scattering/lit"

def read_all_data(ri, directory):
    # First use read_in_lit to collect data from .txt files into multiple 
    # ri objects

    ri_list = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):   #only the refrac files
            ri_list.append(read_in_lit.read_data(directory, filename))

    for ri_obj in ri_list:
        ri_obj = read_in_lit.get_error(ri_obj)
        #print("datasets pulled by collate.py: ", ri_obj.dataset)
    return ri_list

def avg_stacked_pts(ri_list):

    #If two points from different datasets are at the same coordinates,
    # average em
    for ri_1 in ri_list:
        for ri_2 in ri_list:
            for wavel_1 in ri_1.wavel:
                for wavel_2 in ri_2.wavel:
                    if ri_1 != ri_2 and wavel_1 == wavel_2 and ri_1.temp == ri_2.temp:
                        # Average ks
                        a = ri_list.index(ri_1)
                        b = ri_list.index(ri_2)
                        c = ri_1.wavel.index(wavel_1)
                        d = ri_2.wavel.index(wavel_2)
                        ri_list[a].k[c] = (ri_list[a].k[c] + ri_list[b].k[d])/2
                
                        # Combine dks (assumes dks are same units as k, not % error)
                        #Index error here, not above
                        print("ri_list[a].dk[c]: ", ri_list[a].dk[c])
                        print("ri_list[a].k[a]: ", ri_list[a].k[c])
                        print("ri_list[b].dk[d]: ", ri_list[b].dk[d])
                        print("ri_list[b].k[d]: ", ri_list[b].k[d])
                        ri_list[a].dk[c]  = ri_list[a].k[c]*(np.sqrt((((ri_list[a].dk[c])/(ri_list[a].k[c]))**2) + (((ri_list[b].dk[d])/(ri_list[b].k[d])**2))))
                
                        # Remove duplicate point
                        del(ri_list[b].dk[d])
                        del(ri_list[b].k[d])
                        del(ri_list[b].wavel[d])
    return ri_list
"""
    for a in range(len(ri_list)):
        for b in range(len(ri_list)):
            for c in range(len(ri_list[a].wavel)):
                for d in range(len(ri_list[b].wavel)):
                    if (ri_list[a].wavel[c] == ri_list[b].wavel[d]) and (ri_list[a].temp == ri_list[b].temp):
"""

def collate(ri, ri_list):

    #Initialize object of class ri, add in first ri from list
    collated_ri = ri_list[0]
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
        collated_ri.wavel = collated_ri.wavel + obj.wavel
        collated_ri.temp = collated_ri.temp + obj.temp
        collated_ri.k = collated_ri.k + obj.k
        collated_ri.dk = collated_ri.dk + obj.dk

    # Not adding ns even if some come from the source data bc ns missing from
    # some datasets would mess up the indexing

    return collated_ri

