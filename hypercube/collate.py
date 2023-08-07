# Combine experimental data from multiple studies into one ri object for easier
# interpolation and extrapolation

import os

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
        ri_list.append(read_in_lit.read_data(directory))

    for obj in ri_list:
        read_in_lit.get_error(obj)

    return ri_list

def avg_stacked_pts(ri_list):

    #If two points from different datasets are at the same coordinates,
    # average em
    for a in range(len(ri_list)):
        for b in range(len(ri_list)):
            for c in range(len(ri_list[a].wavel)):
                for d in range(len(ri_list[b].wavel)):
                    for e in range(len(ri_list[a].temp)):
                        for f in range(len(ri_list[b].temp)):
                            if (ri_list[a].wavel[c] == ri_list[b].wavel[d] 
                                and ri_list[a].temp[e] == ri_list[b].temp[f]):
                                # Average ks
                                ri_list[a].k[c] = (ri_list[a].k[c] + ri_list[b].k[d])/2
                                # Remove duplicate point (only avg persists)
                                del(ri_list[b].k[d])
                                # Combine dks (assumes dks are same units as
                                # k, not % error)
                                ri_list[a].dk[c]  = ri_list[a].k[c]*(np.sqrt((((ri_list[a].dk[c])/(ri_list[a].k[c]))**2) + (((ri_list[b].dk[d])/(ri_list[b].k[d])**2))))
                                # Remove duplicate point
                                del(ri_list[b].dk[d])
    return ri_list

def collate(ri, ri_list):

    #Initialize empty object of class ri
    collated_ri = ri()

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

