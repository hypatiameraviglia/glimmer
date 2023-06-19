# Caclculates error propogation through Hilbert transform version of 
#Kramer-Kronig Relation (eq. 17 in Musardo 2017)

import numpy as np
from numpy.fft import fft
import matplotlib.pyplot as plt

from ri import ri

def fft_on_k(ri):
#Adapted from Warren Weckesser on stackoverflow
    # pull imaginary index from object ri
    k = ri.k

    # FFT of imaginary index
    fft_k = fft(k)

    # pull error on imaginary index from object ri
    dk = ri.dk

    # FFT the k + dk
    kn = [None]*len(k)
    for i in k: 
        kn[i] = k[i] + dk[i]

    fft_kn = fft(kn, axis=-1)
    
    # return fft_kn.var(axis=0)
    return fft_kn

def fft_on_inv_wavel(ri):
    # pull imaginary index from object ri
    wavel = ri.wavel

    # set up fft(1/pi*wavel)
    fft_wavel = fft(1/(np.pi*wavel))
    
    return fft_wavel

def inv_fft(fft_kn, fft_wavel)
    
