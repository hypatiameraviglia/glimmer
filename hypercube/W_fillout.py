import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

wavel_min =
wavel_max =
wavel_step = 

#Get original data
f = open('warren1984_refrac.txt', "r")
study = f.readlines()[0]
lines = f.readlines()[3:]
wavel = []
real = []
imaginary = []

for i in lines:
    wavel.append(float(i.split('   ')[1])) #check splitting chars
    real.append(float(i.split('   ')[2]))
    imaginary.append(float(i.split('   ')[3]))
f.close()

#Plot original data
plt.scatter(wavel, real, s=4,  label = "Real (original)")
plt.scatter(wavel, imaginary, s=4,  label = "Imaginary (original)")
plt.legend()
plt.savefig('warren1984_uninterpolated.png') #TODO: put study variable in filename

#Cubic spline interpolation
cs_real = interpolate.CubicSpline(wavel, real)
cs_imaginary = interpolate.CubicSpline(wavel, imaginary)

wavel_spline = np.arange(wavel_max, wavel_min, wavel_step)

plt.plot(wavel_spline, cs_real(wavel_s), label = "Real (spline)")
plt.plot(wavel_spline, cs_imaginary(wavel_s), label = "Imaginary (spline)")
plt.legend()
plt.title(study, ": Interpolated RI vs. wavelength")
plt.savefig('warren1984_interpolated.png') #TODO: put study variable in filename

