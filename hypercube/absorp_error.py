#Takes in absorption spectrum and calculates error on k (to then be fed to kkr_prop to calculate error on n), via methods in Leger et al. 1983

import numpy as np
import matplotlib.pyplot as plt
#TODO: Error on wavelength? Changes equation for error prop -- no longer linear

#Leger et al., 1983
def leger(ri):
    if ri.dataset == "leger1983":
        dalpha = 0.10 #% absolute error, Leger p. 165
        for i in ri.wavel:
            ri.dk[i] = (dalpha*ri.wavel[i])/(4*np.pi)
    return ri.dk

