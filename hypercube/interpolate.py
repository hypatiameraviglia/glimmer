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
    #Establish temperature and wavelength as 2d mesh
    temp_axis = np.linspace(min(ri.temp), max(ri.temp))
    wavel_axis = np.linspace(min(ri.wavel), max(ri.wavel))
    temp_axis, wavel_axis = np.meshgrid(temp_axis, wavel_axis)

    #Interpolate n
    n_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), ri.n)
    n_axis = n_interp(temp_axis, wavel_axis)

    #Interpolate k
    k_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), ri.k)
    k_axis = k_interp(temp_axis, wavel_axis)

    #Interpolate dn
    dn_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), ri.dn)
    dn_axis = dn_interp(temp_axis, wavel_axis)

    #Interpolate dk
    dk_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), ri.dk)
    dk_axis = dk_interp(temp_axis, wavel_axis)

return ri, temp_axis, wavel_axis, n_axis, k_axis, dn_axis, dk_axis

def plot_interpolation(ri, temp_axis, wavel_axis, n_axis, k_axis, dn_axis, dk_axis):
    #Plot interp'd n
    plt.pcolormesh(temp_axis, wavel_axis, n_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("n_interpolated_temp_wavel.png")

    #Plot interp'd k
    plt.pcolormesh(temp_axis, wavel_axis, k_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("k_interpolated_temp_wavel.png")

    #Plot interp'd dn
    plt.pcolormesh(temp_axis, wavel_axis, dn_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("dn_interpolated_temp_wavel.png")

    #Plot interp'd dk
    plt.pcolormesh(temp_axis, wavel_axis, dk_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("dk_interpolated_temp_wavel.png")

    #Plot all interp'd data together
    plt.pcolormesh(temp_axis, wavel_axis, n_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
        
    plt.pcolormesh(temp_axis, wavel_axis, k_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ob", label="original data")
    
    plt.pcolormesh(temp_axis, wavel_axis, dn_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "og", label="original data")
    
    plt.pcolormesh(temp_axis, wavel_axis, dk_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "oc", label="original data")

    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("all_interpolated_temp_wavel.png")

