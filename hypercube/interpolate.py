#Takes in ri object with data from all studies added together and 2d 
# interpolates across temperature and wavelength axes

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import CloughTocher2DInterpolator
from scipy.spatial import Delaunay

#temperature bounds in Kelvin
temp_max = 200
temp_min = 130
temp_step = 0.1

#wavelength bounds in microns
wavel_min = 0.1
wavel_max = 30
wavel_step = 0.05

def spline(ri, wtarray, karray, narray, dkarray, dnarray):
    #Establish studied temperature and wavelength as 2d mesh (interpolation)
    temp_axis_num = int((max(ri.temp) - min(ri.temp))/temp_step + 1)
    #print("temp_axis_num: ", temp_axis_num)
    temp_axis = np.linspace(min(ri.temp), max(ri.temp), temp_axis_num)
    #print("shape temp_axis: ", temp_axis.shape)
    wavel_axis_num = int((max(ri.wavel) - min(ri.wavel))/wavel_step + 1)
    #print("wavel_axis_num: ", wavel_axis_num)
    wavel_axis = np.linspace(min(ri.wavel), max(ri.wavel), wavel_axis_num)
    #print("shape wavel_axis: ", wavel_axis.shape)
    temp_mesh, wavel_mesh = np.meshgrid(temp_axis, wavel_axis)
    print("shape temp_mesh: ", temp_mesh.shape)
    print("shape wavel_mesh: ", wavel_mesh.shape)

    #Establish goal temperature and wavelength as 2d mesh (extrapolation)
    temp_extra_num = int((temp_max - temp_min)/temp_step + 1)
    temp_extra = np.linspace(temp_min, temp_max, temp_extra_num)
    wavel_extra_num = int((wavel_max - wavel_min)/wavel_step + 1)
    wavel_extra = np.linspace(wavel_min, wavel_max, wavel_extra_num)
    temp_extra_mesh, wavel_extra_mesh = np.meshgrid(temp_extra, wavel_extra)

    #Delaunay triangulation on the array of data temps and wavels
    tri = Delaunay(wtarray)

    #Interpolate and extrapolate n
    n_interp = CloughTocher2DInterpolator(tri, narray.transpose())
    n_axis = n_interp(temp_mesh, wavel_mesh)
    n_extra = n_interp(temp_extra_mesh, wavel_extra_mesh)
    
    #Interpolate and extrapolate k
    #k_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), karray)
    k_interp = CloughTocher2DInterpolator(tri, karray.transpose())
    k_axis = k_interp(temp_mesh, wavel_mesh)
    k_extra = k_interp(temp_extra_mesh, wavel_extra_mesh)
    #print("k_extra from interpolate: ", k_extra)
    
    #Interpolate and extrapolate dn
    #dn_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), dnarray)
    dn_interp = CloughTocher2DInterpolator(tri, dnarray.transpose())
    dn_axis = dn_interp(temp_mesh, wavel_mesh)
    dn_extra = dn_interp(temp_extra_mesh, wavel_extra_mesh)
    
    #Interpolate and extrapolate dk
    dk_interp = CloughTocher2DInterpolator(tri, dkarray.transpose())
    #dk_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), dkarray)
    dk_axis = dk_interp(temp_mesh, wavel_mesh)
    dk_extra = dk_interp(temp_extra_mesh, wavel_extra_mesh)

    return ri, temp_mesh, wavel_mesh, temp_extra_mesh, wavel_extra_mesh, k_axis, k_extra, n_axis, n_extra, dk_axis, dk_extra, dn_axis, dn_extra

def plot_interpolation(ri, temp_mesh, wavel_mesh, k_axis, n_axis, dk_axis, dn_axis):
   
    #print("temp_axis: ", temp_axis)
    #print("wavel_axis: ", wavel_axis)

    print("n_axis: ", n_axis)
    print("n_axis shape: ", n_axis.shape)

    #Plot interp'd n
    plt.pcolormesh(wavel_mesh, temp_mesh, n_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("n_interpolated_temp_wavel.png")
    
    #Plot interp'd k
    plt.pcolormesh(temp_mesh, wavel_mesh, k_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("k_interpolated_temp_wavel.png")
    
    #Plot interp'd dn
    plt.pcolormesh(temp_mesh, wavel_mesh, dn_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("dn_interpolated_temp_wavel.png")
    
    #Plot interp'd dk
    plt.pcolormesh(temp_mesh, wavel_mesh, dk_axis, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("dk_interpolated_temp_wavel.png")

    #Plot all interp'd data together
    plt.pcolormesh(temp_mesh, wavel_mesh, n_axis, shading='auto')
    plt.pcolormesh(temp_mesh, wavel_mesh, k_axis, shading='auto')
    plt.pcolormesh(temp_mesh, wavel_mesh, dn_axis, shading='auto')
    plt.pcolormesh(temp_mesh, wavel_mesh, dk_axis, shading='auto')
    
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")

    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("all_interpolated_temp_wavel.png")

def plot_extrapolation(ri, temp_extra, wavel_extra, k_extra, n_extra, dk_extra, dn_extra):
    
    #Plot extrap'd n
    plt.pcolormesh(temp_extra, wavel_extra, n_extra, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("n_extrapolated_temp_wavel.png")
    
    #Plot extrap'd k
    plt.pcolormesh(temp_extra, wavel_extra, k_extra, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("k_extrapolated_temp_wavel.png")
    
    #Plot extrap'd dn
    plt.pcolormesh(temp_extra, wavel_extra, dn_extra, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("dn_extrapolated_temp_wavel.png")
    
    #Plot extrap'd dk
    plt.pcolormesh(temp_extra, wavel_extra, dk_extra, shading='auto')
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("dk_extrapolated_temp_wavel.png")

    #Plot all extrap'd data together
    #plt.pcolormesh(temp_extra, wavel_extra, n_extra, shading='auto')
    plt.pcolormesh(temp_extra, wavel_extra, k_extra, shading='auto')
    #plt.pcolormesh(temp_extra, wavel_extra, dn_extra, shading='auto')
    plt.pcolormesh(temp_extra, wavel_extra, dk_extra, shading='auto')
    
    plt.plot(ri.temp, ri.wavel, "ok", label="original data")

    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("all_extrapolated_temp_wavel.png")

