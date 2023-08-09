#Takes in absorption spectrum and calculates error on k (to then be fed to kkr_prop to calculate error on n), via methods in Leger et al. 1983

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants

#TODO: Error on wavelength? Changes equation for error prop -- no longer linear

def calc_error_from_dalpha(ri, perc_dalpha):
    #See Meraviglia et al. (2023) appendix A and Leger et al. (1983) for 
    # details on calculation of error from absorption coefficient
    #Convert wavelength in units of microns to units of cm
    microns_to_cm = float(1E-4)
    for i in range(len(ri.wavel)):
        ri.dk[i] = float(np.absolute(ri.k[i])*(perc_dalpha*ri.wavel[i]*microns_to_cm)/(4*np.pi))
    return ri.dk

def perovich(ri, dalpha_array):
    for i in range(len(dalpha_array)):
        ri.dk[i] = ri.k[i]*(dalpha_array[i]*ri.wavel[i])/(4*np.pi*scipy.constants.c)
    return ri.dk

