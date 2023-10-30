from scipy.interpolate import CloughTocher2DInterpolator
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

temp_step = 0.1
wavel_step = 0.05

def test_plot(ri, wtarray, narray):
    #rng = np.random.default_rng()
    #x = [1, 3, 5, 7, 9, 11]
    #y = [0, 2, 4, 6, 8, 10]
    #x = ri.temp
    #y = ri.wavel

    #The temp_axis and wavel_axis are arrays evenly dividing the parameter space we're interested in. they are NOT the coordinates of the actually narray data. Hence why narray and temp,wavel are different shapes. 
    #BUT on the other hand we actually use this for the grid system and not the interpolation -- see use of combined
    temp_axis_num = int((max(ri.temp) - min(ri.temp))/temp_step + 1)
    temp_axis = np.linspace(min(ri.temp), max(ri.temp), temp_axis_num)
    wavel_axis_num = int((max(ri.wavel) - min(ri.wavel))/wavel_step + 1)
    wavel_axis = np.linspace(min(ri.wavel), max(ri.wavel), wavel_axis_num)

    x = temp_axis
    y = wavel_axis
    #print("Shape of x and y before linspacing: ", x.shape, y.shape)

    #print("x and y: ", x, y)
    #z = np.hypot(x, y)
    z = narray.transpose()
    #print("Shape of n values before interpolation: ", z.shape)
    X = np.linspace(min(x), max(x))
    Y = np.linspace(min(y), max(y))
    X, Y = np.meshgrid(X, Y)  # 2D grid for interpolation
    
    #temp_mesh, wavel_mesh = np.meshgrid(temp_axis, wavel_axis)
    
    #REAL ACTUAL WT COORDS for the n data we're interpolating; same shape as narray
    #combined = np.vstack((x, y)).T
    combined = wtarray
    #print("combined: ", combined)
    print("shape of combined: ", combined.shape)

    #What does the Delaunay actually contribute? breaks in the same way without it
    #tri = Delaunay(combined)
    interp = CloughTocher2DInterpolator(combined, z)
    Z = interp(X, Y)
    print("Z values: ", Z)
    #Z is 3d and pcolormesh can't handle that -- why 3d?
    print("shape of 2d grid: ", X.shape, Y.shape)
    print("shape of Z: ", Z.shape)
    #Try splitting Z into N 2d arrays where N is the length of the third dimension of Z, i.e., split Z into 2 2d layers
    z2d1 = Z[:,:,0]
    z2d2 = Z[:,:,1]
    #Check these slices are actually 2d
    print("shape of z2d1: ", z2d1.shape)
    print("shape of z2d2: ", z2d2.shape)
    for z2d in [z2d1, z2d2]:
        plt.pcolormesh(X, Y, z2d, shading='auto')
        #plt.plot(x, y, "ok", label="input point") #this is failing bc they are different shape,s but also I think x and y arem't really the input points I need, because they're even slices of the space and not the actual wavelengths and temps of the data
        plt.legend()
        plt.colorbar()
        plt.axis("equal")
        plt.savefig("test_CT_axis_" + str(z2d) + ".png")
        print("fig saved")
        #plt.show()
