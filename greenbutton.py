#Runs all the scripts in appropriate order, then produces plots from the data and writes the info to a .txt file

import numpy as np
import matplotlib.pyplot as plt
import copy
import csv
from hypercube import absorp_error
from hypercube import calc_wiggled
from hypercube import kkr
from hypercube import kkr_prop
from hypercube import read_in_lit
from hypercube import wiggler
from hypercube import ri
from hypercube import collate
from hypercube import interpolate
from hypercube import min_max
#import test_CT

directory = "./tests"

#Read in data from literature with dks
"""
Collate calls read_in_lit, which sorts data from .txt files into ri object
and calculates dk values. The collate.py adds all ris from all .txt files
together into one complete ri with stacked k points averaged and stacked dk
points recalculated.
"""
print("Reading data from files into one ri. . .")
data, ri_list = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, directory)))
print("Read k: ", data.k)
print("Read n: ", data.n)
print("Reading and collation successful.")

#Calculate real indices from imaginary indices using Kramers-Kronig Relation
print("Converting imaginary values to real values via KKR. . .")
#print("len ri.k in greenbutton.py: ", len(ri.k))
#print("len data.k in greenbutton.py: ", len(data.k))
data.n = kkr.inv_fft(kkr.fft_on_k(data), kkr.fft_on_inv_wavel(data))
print("check that n post-kkr is not empty: ", data.n)
if len(data.n) == len(data.k):
    print("len n and k are the same, we good")
else:
    print("len n and k are not the same, we bad")
print("KKR conversion complete.")

#Calculate error on real indices from error on imaginary indices using a 
#modified Kramers-Kronig relation
print("Calculating error on real indices via KKR. . .")
data.dn = kkr_prop.inv_fft(kkr_prop.fft_on_k(data), kkr_prop.fft_on_inv_wavel(data))
print("check that dn post-kkr is not empty: ", data.dn)
if len(data.dn) == len(data.k) and len(data.dn) == len(data.n):
    print("len dn, n, and k are the same, we good")
else:
    print("len dn, n, and k are not the same, we bad")
print("dn calculation complete.")

#Calculate upper and lower bounds for each n and k using their errors
# This step is handled as a vectorized operation by wiggler.py, but if you need to do it by item before organization and regridding, this is available:
"""
print("Calculating upper and lower bounds for n and k. . .")
data = min_max.get_min_max(data)
print("check that nmax is not empty: ", data.nmax)
print("check that nmin is not empty: ", data.nmin)
if len(data.nmax) == len(data.n) and len(data.nmin) == len(data.n):
    print("len nmax and nmin are the same as n, we good")
else:
    print("len nmax and nmin are not the same as n, we bad")
print("Bounds calculated.")
"""

#Organize k, n, dk, and dn into arrays of the dimensions wavel by temp for interpolation
print("Organizing indices into arrays of wavel by temp. . .")
#data, wtarray, karray, narray, dkarray, dnarray = collate.organize_array(data, ri_list)
karray, narray, dkarray, dnarray = collate.organize_arrayv2(data, ri_list)
#print("narray post organization: ", narray)
#print("karray post organization: ", karray)
print("shape of narray post organization: ", narray.shape)
print("shape of karray post organization: ", karray.shape)

# It's a surprise tool that will help us later (calc_wiggled.py)
karray_for_wiggling = copy.deepcopy(karray)
narray_for_wiggling = copy.deepcopy(narray)
dkarray_for_wiggling = copy.deepcopy(dkarray)
dnarray_for_wiggling = copy.deepcopy(dnarray)


#print("shape of wtarray post organization: ", wtarray.shape)
#TODO This step splits the n and k into subarrays at each temperature which contain a list of values in order of wavelength. 
print("Organization complete.")

#revised up to here 6/27/24

#Extrapolate and 2D (sheet) interpolate across T range and wavelength range
print("Weaving (interpolating) across wavel-temp space with univariate splines . . .")
interp_temp, interp_wavel, karray, narray = interpolate.splineweave(data, karray, narray)
print("Interpolation complete.")

#Assign interpolated values to a new ri object
interpd_data = ri.ri("interpolated", [], [], "N/A", [], [], [], [])
interpd_data.wavel = interp_wavel
interpd_data.temp = interp_temp
interpd_data.n = narray
interpd_data.k = karray

print("interpd_data.temp: ", interpd_data.temp)
print("interpd_data.wavel: ", interpd_data.wavel)

"""
#Assign extrapolated values to a new ri object
extrapd_data = ri.ri("extrapolated", [], [], "N/A", [], [], [], [])
extrapd_data.wavel = wavel_extra
extrapd_data.temp = temp_extra
extrapd_data.n = n_extra
extrapd_data.k = k_extra
extrapd_data.dn = dn_extra
extrapd_data.dk = dk_extra
"""
#print("check interpolated data made it over to the new ri object alright. n: ", interpd_data.n)
#print("check interpolated data made it over to the new ri object alright. k: ", interpd_data.k)

#Plot interpolation
print("Plotting interpolated data. . .")
interpolate.plot_interpolation(data, interpd_data)
print("Plotting interpolation complete.")

#Calculate new error introduced into estimated areas by use of spline, using a
#Monte Carlo-style method of "wiggling"
"""
calc_wiggled calls ri_wiggler to wiggle each n and k many (calc_wiggled.num_wiggled_indices) times, then averages each n and k across these wiggled values. THe standard deviation represents the complete error, both the experimental error and the error introduced by the spline.
"""
print("Calculating new errors on n and k by wiggling splines. . .")
"""
Using deep copies of the organized, regridded orignal data, each original data point is given a new, random value within the boundaries of the error bars (dk for the imaginary indicies and dn for the real indicies.
On these new data points, the spline inteprolation is redone to fill in the missing points.
These two steps are done a user-defined number of times (num_wiggled_indices).Scale this up for better statistics.
Finally, across all the runs (total is num_wiggled_indices), the average and standard deviation of the n and k values are calculated at each point in the wavel-temp space.
"""
interpd_data.n_avg, interpd_data.n_stdev, interpd_data.k_avg, interpd_data.k_stdev = calc_wiggled.stats(data, karray_for_wiggling, narray_for_wiggling, dkarray_for_wiggling, dnarray_for_wiggling)

print("n_avg: ", interpd_data.n_avg)
print("n_avg type: ", type(interpd_data.n_avg))
print("n_stdev: ", interpd_data.n_stdev)
print("k_avg: ", interpd_data.k_avg)
print("k_stdev: ", interpd_data.k_stdev)

print("Wiggling complete.")

#Plots and datafiles
def plot_errors(interpd_data):
    #TODO: MUST MAKE A NEW FIGURE EACH TIME LMAO
    """
    #Plot wiggled dn
    print("extrapd_data.temp shape", extrapd_data.temp.shape)
    print("extrapd_data.wavel shape", extrapd_data.wavel.shape)
    print("extrapd_data.n_stdev shape", extrapd_data.n_stdev.shape) #empty
    plt.pcolormesh(extrapd_data.temp, extrapd_data.wavel, extrapd_data.n_stdev, shading='auto')
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("ic_n_stdev_extrapd.png")
    
    #Plot wiggled dk
    plt.pcolormesh(extrapd_data.temp, extrapd_data.wavel, extrapd_data.k_stdev, shading='auto')
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("ic_k_stdev_extrapd.png")
    """
    #print("n_stdev right before plotting: ", interpd_data.n_stdev)

    #Plot wiggled dn
    plt.clf() # clear figure
    plt.pcolormesh(interpd_data.wavel, interpd_data.temp, interpd_data.n_stdev, shading='auto')
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("ic_n_stdev_interpd.png")
    
    #Plot wiggled dk
    plt.clf() # clear figure
    plt.pcolormesh(interpd_data.wavel, interpd_data.temp, interpd_data.k_stdev, shading='auto')
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("ic_k_stdev_interpd.png")

def plot_avgd_nk(interpd_data):
    """
    #Plot averaged n
    plt.pcolormesh(extrapd_data.temp, extrapd_data.wavel, extrapd_data.n_avg, shading='auto')
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("ic_n_avg_extrapd.png")
    
    #Plot averaged k
    plt.pcolormesh(extrapd_data.temp, extrapd_data.wavel, extrapd_data.k_avg, shading='auto')
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("ic_k_avg_extrapd.png")
    """
    
    #Plot averaged n
    plt.clf() # clear figure
    plt.pcolormesh(interpd_data.wavel, interpd_data.temp, interpd_data.n_avg, shading='auto')
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("ic_n_avg_interpd.png")
    
    #Plot averaged k
    plt.clf() # clear figure
    plt.pcolormesh(interpd_data.wavel, interpd_data.temp, interpd_data.k_avg, shading='auto')
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("ic_k_avg_interpd.png")

#Produce on .txt file containing the modelled points
def write_model(interpd_data):
    #2D array: temperature along row and wavelength along column, with data in grid by temp and wavel -- separate files for n, k, dk, and dn because they are all 2D arrays
    print("Shape of k_stdev: ", interpd_data.k_stdev.shape)
    print("Shape of n_stdev: ", interpd_data.n_stdev.shape)
    print ("Shape of wavel: ", interpd_data.wavel.shape)
    print("Shape of temp: ", interpd_data.temp.shape)
    #tranposed_wavel = np.transpose(interpd_data.wavel)
    
    # Shared info across files
    temps = interpd_data.temp.tolist()
    expo2 = "Temperatures (K) across columns, wavelengths (microns) across rows"
        
    with open('ic_n_interpolated.csv', 'w', newline='') as f:
        # Explanatory lines
        writer = csv.writer(f)
        expo1 = "Interpolated database of real index (n) values for Ic water ice"
        writer.writerow(expo1 + "\n" + expo2)

        # Write temperatures (by column) across top
        writer.writerow(temps)

        # Write the data rows (wavelengths and corresponding data)
        for i, w in enumerate(interpd_data.wavel):
            row = [w] + interpd_data.n[i].tolist()
            writer.writerow(row)

    with open('ic_k_interpolated.txt', 'w') as f:
        # Explanatory lines
        writer = csv.writer(f)
        expo1 = "Interpolated database of imaginary index (k) values for Ic water ice"
        writer.writerow(expo1 + "\n" + expo2)

        # Write temperatures (by column) across top
        writer.writerow(temps)   

        # Write the data rows (wavelengths and corresponding data)
        for i, w in enumerate(interpd_data.wavel):
            row = [w] + interpd_data.k[i].tolist()
            writer.writerow(row)

    with open('ic_kstdev_interpolated.txt', 'w') as f:
        # Explantory lines
        writer = csv.writer(f)
        expo1 = "Interpolated database of errors on the imaginary (k) values for Ic water ice"
        writer.writerow(expo1 + "\n" + expo2)

        # Write temperatures (by column) across top
        writer.writerow(temps)   

        # Write the data rows (wavelengths and corresponding data)
        for i, w in enumerate(interpd_data.wavel):
            row = [w] + interpd_data.k_stdev[i].tolist()
            writer.writerow(row)
    
    with open('ic_nstdev_interpolated.txt', 'w') as f:
        # Explantory lines
        writer = csv.writer(f)
        expo1 = "Interpolated database of errors on real index (n) values for Ic water ice"
        writer.writerow(expo1 + "\n" + expo2)

        # Write temperatures (by column) across top
        writer.writerow(temps)   

        # Write the data rows (wavelengths and corresponding data)
        for i, w in enumerate(interpd_data.wavel):
            row = [w] + interpd_data.n_stdev[i].tolist()
            writer.writerow(row)
    
#Map error magnitudes by wavel-temp
print("Plotting errors and averages. . .")
plot_errors(interpd_data)
plot_avgd_nk(interpd_data)
print("Plots complete.")
print("Writing model to .txt files. . .")
write_model(interpd_data)
print("Model written to .txt files.")
print("All processes complete.")
#print("add quote about indra's net here before publication")
