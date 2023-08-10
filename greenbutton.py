#Runs all the scripts in appropriate order, then produces plots from the data and writes the info to a .txt file

from hypercube import absorp_error
from hypercube import calc_wiggled
from hypercube import kkr
from hypercube import kkr_prop
from hypercube import read_in_lit
from hypercube import ri_wiggler
from hypercube import ri
from hypercube import collate
from hypercube import interpolate

directory = "./lit/crystalline_ris"

#Read in data from literature with dks
"""
Collate calls read_in_lit, which sorts data from .txt files into ri object
and calculates dk values. The collate.py adds all ris from all .txt files
together into one complete ri with stacked k points averaged and stacked dk
points recalculated.
"""
print("Reading data from files into one ri. . .")
data = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, directory)))
print("Reading and collation successful.")

#Calculate real indices from imaginary indices using Kramers-Kronig Relation
print("Converting imaginary values to real values via KKR. . .")
data.n = kkr.inv_fft(kkr.fft_on_k(ri), kkr.fft_on_inv_wavel(ri))
print("KKR conversion complete.")

#Calculate error on real indices from error on imaginary indices using a 
#modified Kramers-Kronig relation
print("Calculating error on real indices via KKR. . .")
data.dn = kkr_prop.inv_fft(kkr_prop.fft_on_k(data), kkr_prop.fft_on_inv_wavel(data))
print("dn calculation complete.")

#Extrapolate and 2D (sheet) interpolate across T range (130 K - 200 K) and 
#wavelength range (0.1 - 30 microns)
print("Interpolating and extrapolating across wavel-temp space with splines . . .")
data, temp_axis, wavel_axis, temp_extra, wavel_extra, n_axis, n_extra, k_axis, k_extra, dn_axis, dn_extra, dk_axis, dk_extra = interpolate.spline(data)
print("Interpolation and extrapolation complete.")

#Assign interpolated values to a new ri object
interpd_data = ri.ri("interpolated", [], [], "N/A", [], [], [], [])
interpd_data.wavel = wavel_axis
interpd_data.temp = temp_axis
interpd_data.n = n_axis
interpd_data.k = k_axis
interpd_data.dn = dn_axis
interpd_data.dk = dk_axis

#Assign extrapolated values to a new ri object
extrapd_data = ri.ri("extrapolated", [], [], "N/A", [], [], [], [])
extrapd_data.wavel = wavel_extra
extrapd_data.temp = temp_extra
extrapd_data.n = n_extra
extrapd_data.k = k_extra
extrapd_data.dn = dn_extra
extrapd_data.dk = dk_extra

#Plot interpolation and extrapolation
print("Plotting interpolated and extrapolated data. . .")
interpolate.plot_interpolation(interpolate.spline(data))
print("Plotting interpolation and extrapolation complete.")

#Calculate new error introduced into estimated areas by use of spline, using a
#Monte Carlo-style method of "wiggling"
"""
calc_wiggled calls ri_wiggler to wiggle each n and k many (calc_wiggled.num_wiggled_indices) times, then averages each n and k across these wiggled values. THe standard deviation represents the complete error, both the experimental error and the error introduced by the spline.
"""
print("Calculating new errors on n and k by wiggling splines. . .")
extrapd_data.n_avg, extrapd_data.n_stdev, extrapd_data.k_avg, extrapd_data.k_stdev = calc_wiggled.extrapolate_wiggled_ris(wiggle_indices_n_times(extrapd_data))
print("Wiggling complete.")

#Map error magnitudes by wavel-temp
plot_errors(data)

def plot_errors(data):
    #Plot wiggled dn
    plt.pcolormesh(extrapd_data.temp, extrapd_data.wavel, extrapd_data.n_stdev, shading='auto')
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("n_stdev_extrapolated_temp_wavel.png")

    #Plot wiggled dk
    plt.pcolormesh(extrapd_data.temp, extrapd_data.wavel, extrapd_data.k_stdev, shading='auto')
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("k_stdev_extrapolated_temp_wavel.png")
