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

if ri.dn == []:
    ri.dn = absorp_error.dn(ri)
    ri.dk = absorp_error.dk(ri)

if n == []:
    ri.n = kkr.inv_fft(fft_k, fft_wavel)

if 
