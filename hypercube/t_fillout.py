import matplotlib:
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import LinearNDInterpolator

#temperature bounds in Kelvin
t_max = 130
t_min = 200
t_step = 0.1

#Get original data and categorize by T
studies = []
t = []

directory = "~/scattering/data" #TODO: put all data in one directory "data"
for filename in os.listdir(directory):
        if filename.endswith('.txt'):   #only the refrac files
        f = open('file_refrac.txt', "r") #open files already inteprolated by wavelength
        f.readlines()[0]
        t.append(float(f.readlines()[1]))

#refrac data by wavel
lines = f.readlines()[3:]
wavel = []
real = []
imaginary = []

#TODO: what happens when two studies overlap? (same wavel, same T)
for i in lines:
    wavel.append(float(i.split('   ')[1])) #check splitting chars
    real.append(float(i.split('   ')[2]))
    imaginary.append(float(i.split('   ')[3]))

f.close()

#Cubic spline interpolation
t_axis = np.linspace(min(t), max(t))
wavel_axis = np.linspace(min(wavel), max(wavel))
t_axis, wavel_axis = np.meshgrid(t_axis, wavel_axis)

real_interp = LinearNDInterpolator(list(zip(t, wavel)), real)
R_axis = real_interp(t_axis, wavel_axis)

imag_interp = LinearNDInterpolator(list(zip(t, wavel)), imaginary)
I_axis = imag_interp(t_axis, wavel_axis)

#Plotting inteprolated real index data
plt.pcolormesh(t_axis, wavel_axis, R_axis, shading='auto')
plt.plot(t, wavel, "ok", label="original data")
plt.legend()
plt.colorbar()
plt.axis("equal")
plt.savefig("R_interpolated_T_wavel.png")

#Plotting interpolated imaginary index data
plt.pcolormesh(t_axis, wavel_axis, I_axis, shading='auto')
plt.plot(t, wavel, "ok", label="original data")
plt.legend()
plt.colorbar()
plt.axis("equal")
plt.savefig("R_interpolated_T_wavel.png")
