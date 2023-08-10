# Calculates error propagation through Hilbert transform version of 
#Kramers-Kronig Relation (eq. 17 in Musardo 2017)

import numpy as np
from numpy.fft import fft
from hypercube import ri

def fft_on_k(ri):
#Adapted from Warren Weckesser on stackoverflow
    # FFT of imaginary index
    #fft_k = fft(k)
    print("len of ir.k: ", len(ri.k))
    fft_k = fft(ri.k, axis=-1)

    # return fft_k.var(axis=0)
    return fft_k

def fft_on_inv_wavel(ri):
    pi_wavel = [None]*len(ri.wavel)
    for i in range(len(ri.wavel)):
        # set up fft(1/pi*wavel)
        pi_wavel[i] = 1/(np.pi*ri.wavel[i])

    fft_wavel = fft(pi_wavel, axis=-1)

    return fft_wavel

def inv_fft(fft_k, fft_wavel):
    n = np.fft.ifft(fft_k*fft_wavel)
    print("n as calculated by kkr: ", n)
    print("len of kkr'd n: ", len(n))
    ri.n = n
    #for i in range(len(n)):
    #    ri.n[i] = n[i]

    return list(n)

"""
Old method using Hilbert transform
Sets I as function of chi which is a function of frequency

g = 0.1
w0 = 5.0
def chii(w):
    return(g**2)/((w - w0)**2 + g**2)
k = chii(w)
n = ft.hilbert(chii(w))
w = np.linspace(0, 10, 800)
n = ft.hilbert(k)
"""

