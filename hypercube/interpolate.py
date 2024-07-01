#Takes in ri object with data from all studies added together and 2d 
# interpolates across temperature and wavelength axes

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import LinearNDInterpolator
#from scipy.interpolate import CloughTocher2DInterpolator
from scipy.interpolate import UnivariateSpline
#from scipy.spatial import Delaunay

#temperature bounds in Kelvin
temp_max = 200
temp_min = 135 #temp of He (2022)
temp_step = 1

#wavelength bounds in microns
wavel_min = 0.25 #lower bound of He (2022)
wavel_max = 333 #upper bound of Bertie (1969)
wavel_step = 0.01

def splineweave(data, karray, narray):
    """
    This function takes in data that has been organized (made 2D, along temperature and wavelength) and remapped (placed into a new grid of user-defined step size, where missing data is represented by NaN). It interpolates this data by fitting splines first along the temperature axis, then again perpendicularly along the wavelength axis. This is done for both the k and n arrays. The function returns the interpolated k and n arrays.
    """

    #define temp and wavel axes for spline to interpolate/extrapolate along
    #T = range(temp_min, temp_max, temp_step)
    #W = range(wavel_max*100 - wavel_min*100, wavel_step*100)/100 #avoid float errors
    # for interpolation -- find bounds of original data and use them, rather than externally defining -- for now
    T = np.arange(min(data.temp), max(data.temp), 1) #step size is 1 K
    W = np.arange(min(data.wavel), max(data.wavel), 0.01) #step size is 0.01 micron
    #print("T: ", T)   
    #print("W: ", W)

    for array in [karray, narray]:
        # Interpolating/extrapolating along the T axis
        for i in range(len(W)):
            y = array[:, i]
            mask = ~np.isnan(y)

            if np.sum(mask) >= 4: # need at least 4 points for cubic spline
                spline = UnivariateSpline(T[mask], y[mask], k=3, s=0, ext=0) #cubic
                y_interp = spline(T)
                array[:, i][~mask] = y_interp[~mask]  # Only fill in gaps
            elif np.sum(mask) < 4 and np.sum(mask) >= 2: #need at least 2 points for linear spline
                spline = UnivariateSpline(T[mask], y[mask], k=1, s=0, ext=0) #linear 
                y_interp = spline(T)
                array[:, i][~mask] = y_interp[~mask]  # Only fill in gaps
            else:
                pass # leaves NaNs in place, in case W axis spline can fill them in. If not, they will remain NaNs

        # Interpolating/extrapolating along the W axis
        for j in range(len(T)):
            y = array[j, :]
            mask = ~np.isnan(y)
            
            if np.sum(mask) >= 4: # need at least 4 points for cubic spline
                spline = UnivariateSpline(W[mask], y[mask], k=3, s=0, ext=0) #cubic
                y_interp = spline(W)
                array[j, :][~mask] = y_interp[~mask]  # Only fill in gaps
            elif np.sum(mask) < 4 and np.sum(mask) >= 2: #need at least 2 points for linear spline
                #check for strictly increasing
                spline = UnivariateSpline(W[mask], y[mask], k=1, s=0, ext=0)
                y_interp = spline(W)
                array[j, :][~mask] = y_interp[~mask]
            else:
                pass

    print("After spline interpolation\n")
    print("Does karray contain NaNs? ", np.isnan(karray).any())
    print("Does narray contain NaNs? ", np.isnan(narray).any())
    
    #print("T after interpolation: ", T)
    #print("W after interpolation: ", W)

    return T, W, karray, narray

def ct(ri, wtarray, karray, narray):
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
    #print("shape temp_mesh: ", temp_mesh.shape)
    #print("shape wavel_mesh: ", wavel_mesh.shape)

    #Establish goal temperature and wavelength as 2d mesh (extrapolation)
    #temp_extra_num = int((temp_max - temp_min)/temp_step + 1)
    #temp_extra = np.linspace(temp_min, temp_max, temp_extra_num)
    #wavel_extra_num = int((wavel_max - wavel_min)/wavel_step + 1)
    #wavel_extra = np.linspace(wavel_min, wavel_max, wavel_extra_num)
    #temp_extra_mesh, wavel_extra_mesh = np.meshgrid(temp_extra, wavel_extra)

    #Delaunay triangulation on the array of data temps and wavels
    tri = Delaunay(wtarray)

    #Interpolated vaues coming out as NaNs. 1/8/24
    #Is input NaNs?
    #print("Is temp_mesh NaNs? ", temp_mesh[0:4], "...")
    #print("Is wavel_mesh NaNs? ", wavel_mesh[0:4], "...")
    #Neither are NaNs.
    #NaN issue must be caused by either 1) Delaunay function or 2) Clough Tocher
    #Clough Tocher fills in values outside the "convex hull of input points" with NaN -- could it be that the whole thing is outside the convex hull?
    #Test with option fill_value. Fill value appears to affect one of the color scales but not change the appearance of the graph. See n_interp_fillval5.png and fill_interp_fillval0.png
    #See if the extrapolated plots have the same problem?

    #Interpolate and extrapolate n
    n_interp = CloughTocher2DInterpolator(tri, narray.transpose())
    n_axis = n_interp(temp_mesh, wavel_mesh)
    #n_extra = n_interp(temp_extra_mesh, wavel_extra_mesh)
    
    #Interpolate and extrapolate k
    #k_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), karray)
    k_interp = CloughTocher2DInterpolator(tri, karray.transpose())
    k_axis = k_interp(temp_mesh, wavel_mesh)
    #k_extra = k_interp(temp_extra_mesh, wavel_extra_mesh)
    #print("k_extra from interpolate: ", k_extra)
    
    #Interpolate and extrapolate dn
    #dn_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), dnarray)
    #dn_interp = CloughTocher2DInterpolator(tri, dnarray.transpose())
    #dn_axis = dn_interp(temp_mesh, wavel_mesh)
    #dn_extra = dn_interp(temp_extra_mesh, wavel_extra_mesh)
    
    #Interpolate and extrapolate dk
    #Is it important to inteprolate dk and dn, since they will be calculated down the line at calc_wiggled.py?
    #dk_interp = CloughTocher2DInterpolator(tri, dkarray.transpose())
    #dk_interp = LinearNDInterpolator(list(zip(ri.temp, ri.wavel)), dkarray)
    #dk_axis = dk_interp(temp_mesh, wavel_mesh)
    #dk_extra = dk_interp(temp_extra_mesh, wavel_extra_mesh)

    #return ri, temp_mesh, wavel_mesh, temp_extra_mesh, wavel_extra_mesh, k_axis, k_extra, n_axis, n_extra, dk_axis, dk_extra, dn_axis, dn_extra

    return ri, temp_mesh, wavel_mesh, k_axis, n_axis

def plot_interpolation(data, interpd_data):
   
    #print("temp_axis: ", temp_axis)
    #print("wavel_axis: ", wavel_axis)

    #print("n_axis: ", n_axis)
    #print("n_axis shape: ", n_axis.shape)

    #PLOT DEBUGGING REMINDERS
    #Original data lines commented out because ri.temp and ri.wavel are different sizes, and plt.plot doesn't know how to plot them in the context of the mesh
    #Added [:,:,0] to pick out one slice of the 3D result of Clough Tocher. Doesn't have to be 0, can be 1. Need to test both or combine them.

    #Plot interp'd n
    plt.pcolormesh(interpd_data.wavel, interpd_data.temp, interpd_data.n, shading='nearest')
    plt.colorbar()
    plt.xlabel("Temperature (K)")
    plt.ylabel("Wavelength (microns)")
    plt.title("Interpolated real indices")
    plt.savefig("n_interpolated_temp_wavel.png")
    
    #Plot interp'd k
    plt.clf()
    plt.pcolormesh(interpd_data.wavel, interpd_data.temp, interpd_data.k, shading='nearest')
    plt.colorbar()
    plt.xlabel("Temperature (K)")
    plt.ylabel("Wavelength (microns)")
    plt.title("Interpolated imaginary indices")
    plt.savefig("k_interpolated_temp_wavel.png")
    """
    #Plot interp'd dn
    plt.pcolormesh(temp_mesh, wavel_mesh, dn_axis[:,:,0], shading='auto')
    #plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("dn_interpolated_temp_wavel.png")
    
    #Plot interp'd dk
    plt.pcolormesh(temp_mesh, wavel_mesh, dk_axis[:,:,0], shading='auto')
    #plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("dk_interpolated_temp_wavel.png")
    """
    #Plot all interp'd data together
    #plt.pcolormesh(interpd_data.temp, interpd_data.wavel, interpd_data.n, shading='nearest')
    #plt.pcolormesh(interpd_data.temp, interpd_data.wavel, interpd_data.k, shading='nearest')
    #plt.pcolormesh(temp_mesh, wavel_mesh, dn_axis[:,:,0], shading='auto')
    #plt.pcolormesh(temp_mesh, wavel_mesh, dk_axis[:,:,0], shading='auto')
    
    #plt.plot(ri.temp, ri.wavel, "ok", label="original data")

    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("all_interpolated_temp_wavel.png")
"""
def plot_extrapolation(ri, temp_extra, wavel_extra, k_extra, n_extra, dk_extra, dn_extra):
    
    #Plot extrap'd n
    plt.pcolormesh(temp_extra, wavel_extra, n_extra[:,:,0], shading='auto')
    #plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("n_extrapolated_temp_wavel.png")
    
    #Plot extrap'd k
    plt.pcolormesh(temp_extra, wavel_extra, k_extra[:,:,0], shading='auto')
    #plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("k_extrapolated_temp_wavel.png")
    
    #Plot extrap'd dn
    plt.pcolormesh(temp_extra, wavel_extra, dn_extra[:,:,0], shading='auto')
    #plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("dn_extrapolated_temp_wavel.png")
    
    #Plot extrap'd dk
    plt.pcolormesh(temp_extra, wavel_extra, dk_extra[:,:,0], shading='auto')
    #plt.plot(ri.temp, ri.wavel, "ok", label="original data")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("dk_extrapolated_temp_wavel.png")

    #Plot all extrap'd data together
    #plt.pcolormesh(temp_extra, wavel_extra, n_extra, shading='auto')
    plt.pcolormesh(temp_extra, wavel_extra, k_extra[:,:,0], shading='auto')
    #plt.pcolormesh(temp_extra, wavel_extra, dn_extra, shading='auto')
    plt.pcolormesh(temp_extra, wavel_extra, dk_extra[:,:,0], shading='auto')
    
    #plt.plot(ri.temp, ri.wavel, "ok", label="original data")

    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.savefig("all_extrapolated_temp_wavel.png")
"""
