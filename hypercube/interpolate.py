#Takes in ri object with data from all studies added together and 2d 
# interpolates across temperature and wavelength axes

import matplotlib:
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import LinearNDInterpolator

#temperature bounds in Kelvin
temp_max = 130
temp_min = 200
temp_step = 0.1

#wavelength bounds in microns
wavel_min = 0.1
wavel_max = 30
wavel_step = 0.05

def interpolate(ri):
    #Cubic spline interpolation
    temp_axis = np.linspace(min(ri.temp), max(ri.temp))
    wavel_axis = np.linspace(min(ri.wavel), max(ri.wavel))
    temp_axis, wavel_axis = np.meshgrid(temp_axis, wavel_axis)

    n_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), ri.n)
    n_axis = n_interp(temp_axis, wavel_axis)

    k_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), ri.k)
    k_axis = k_interp(temp_axis, wavel_axis)

return temp_axis, wavel_axis, n_axis, k_axis

def plot_interpolation(ri, temp_axis, wavel_axis, n_axis, k_axis):
    #Plotting interpolated n
    plt.pcolormesh(temp_axis, wavel_axis, n_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("n_interpolated_temp_wavel.png")

    #Plotting interpolated k
    plt.pcolormesh(temp_axis, wavel_axis, k_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("k_interpolated_temp_wavel.png")
