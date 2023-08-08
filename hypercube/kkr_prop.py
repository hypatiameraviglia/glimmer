# Calculates error propagation through Hilbert transform version of 
#Kramers-Kronig Relation (eq. 17 in Musardo 2017)

import numpy as np
from numpy.fft import fft
import matplotlib.pyplot as plt

from hypercube import ri

def fft_on_k(ri):
#Adapted from Warren Weckesser on stackoverflow
    # FFT of imaginary index
    #fft_k = fft(k)

    # FFT the k + dk
    k_dk = [None]*len(ri.k)
    for i in range(len(ri.k)): 
        k_dk[i] = ri.k[i] + ri.dk[i]

    fft_k_dk = fft(k_dk, axis=-1)
    
    # return fft_k_dk.var(axis=0)
    return fft_k_dk

def fft_on_inv_wavel(ri):
    pi_wavel = [None]*len(ri.wavel)
    for i in range(len(ri.wavel)):
        # set up fft(1/pi*wavel)
        pi_wavel[i] = 1/(np.pi*ri.wavel[i])
    
    fft_wavel = fft(pi_wavel, axis=-1)
    
    return fft_wavel

def inv_fft(fft_k_dk, fft_wavel):
    dn = np.fft.ifft(fft_k_dk*fft_wavel)
    
    for i in range(len(dn)):
        ri.dn[i] = dn[i]
    
    return dn
