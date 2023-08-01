# Combine experimental data from multiple studies into one ri object for easier
# interpolation and extrapolation

from hypercube import ri
from hypercube import read_in_lit
from hypercube import interpolate

#Location of experimental data files
directory = "~/scattering/lit"

def read_all_data(ri):
    # First use read_in_lit to collect data from .txt files into multiple 
    # ri objects

    ri_list = []
    
    for filename in os.listdir(directory):
        ri_list.append(read_in_lit.read_data(directory))

    for obj in ri_list:
        read_in_lit.get_error(obj)

    return ri_list

def collate(ri, ri_list):

    #Initialize empty object of class ri
    collated_ri = ri()

    #For each wavelength and temperature in designated space, check if
    # there's data in our list of ris and if yes, add to collated ri obj
    for wavel_index in range(interpolate.wavel_min, interpolate.wavel_max, 
            interpolate.wavel_step):
        for temp_index in range(interpolate.temp_min, interpolate.temp_max,
                    interpolate.temp_step):
            for obj in ri_list:
                collated_ri.wavel = collated_ri.wavel + obj.wavel
                collated_ri.temp = collated_ri.temp + obj.temp
                collated_ri.k = collated_ri.k + obj.k
                collated_ri.n = collated_ri.n + obj.n

    return collated_ri

def avg_stacked_pts(ri_list):

    #If two points from different datasets are at the same coordinates,
    # average em
    for a in len(ri_list):
        for b in len(ri_list):
            for c in ri_list[a].wavel:
                for d in ri_list[b].wavel:
                    for e in ri_list[a].temp:
                        for f in ri_list[b].temp:
                            if (ri_list[a].wavel[c] == ri_list[b].wavel[d] 
                                and ri_list[a].temp[e] == ri_list[b].temp[f]:
                                ri_list[a].k[c] = ri_list[b].k[d] = (ri_list[a].k[c] + ri_list[b].k[d])/2

    return ri_list
