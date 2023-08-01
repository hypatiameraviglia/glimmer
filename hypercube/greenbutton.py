#Runs all the scripts in appropriate order, then produces plots from the data and writes the info to a .txt file

from hypercube import absorp_error
from hypercube import calc_wiggled
from hypercube import kkr
from hypercube import kkr_prop
from hypercube import read_in_lit
from hypercube import ri_wiggler
from hypercube import t_fillout
from hypercube import w_fillout
from hypercube import ri

ri = read_in_lit.pull_data()

#Calculate error on imaginary index from absorption coefficient "alpha", 
#using method layed out in Clapp et al. 1995
if ri.dk == []:
    ri.dk = absorp_error(ri)

#Calculate real indices from imaginary indices using Kramers-Kronig Relation
if n == []:
    ri.n = kkr.inv_fft(fft_k, fft_wavel)

#Calculate error on real indices from error on imaginary indices using a 
#modified Kramers-Kronig Relation
if dn == []:
    ri.dn = kkr_prop.inv_fft(kkr_prop.fft_on_k(ri), kkr_prop.fft_on_inv_wavel(ri))

#Extrapolate and 2D (sheet) interpolate across T range (130 K - 200 K)

#Extrapolate and 2D (sheet) interpolate across wavelength range 
#(0.1 microns - 30 microns)

#Calculate new error introduced into estimated areas by use of spline, using a
#Monte Carlo-style method of "wiggling"

