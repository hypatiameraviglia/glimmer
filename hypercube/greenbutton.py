#Runs all the scripts in appropriate order, then produces plots from the data and writes the info to a .txt file

from glimmer import absorp_error
from glimmer import calc_wiggled
from glimmer import kkr
from glimmer import kkr_prop
from glimmer import read_in_lit
from glimmer import ri_wiggler
from glimmer import t_fillout
from glimmer import w_fillout
from glimmer import ri

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

