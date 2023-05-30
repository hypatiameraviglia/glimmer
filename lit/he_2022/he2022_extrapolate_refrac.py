import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

#Get original data
f = open('he2022_real_refrac.txt', "r")
lines = f.readlines()[1:]
#Wavenumber:
freq = []
real = []
imaginary = []

for i in lines:
    freq.append(float(i.split(' ')[0]))
    #print(wavel)
    real.append(float(i.split(' ')[1]))
    #print(real)
f.close()

#Real and imagianry indices stored in two different files for this data set
f = open('he2022_imag_refrac.txt', "r")
lines = f.readlines()[1:]
for i in lines:
    imaginary.append(float(i.split(' ')[1]))
f.close()

#print("Real (unextrapolated): ", real)
#print("Imaginary (unextrapolated): ", imaginary)

#Calculate wavelength in microns from frequency in cm^-1
wavel = [None]*len(freq)
for i in range(0, len(freq)):
    wavel[i] = (1/freq[i])*10000

print("Beginning of wavelength range: ", wavel[0])
print("End of wavelength range: ", wavel[-1])
#print("Real (unextrapolated): ", real)
#print("Imaginary (unextrapolated): ", imaginary)

#Plot original data
plt.figure()
plt.scatter(wavel, real, s=4,  label = "Real (original)")
plt.savefig('he2022_unextrapolated_real.png')

plt.figure()
plt.scatter(wavel, imaginary, s=4, label = "Imaginary (original)")
plt.savefig('he2022_unextrapolated_imaginary.png')

print("Wavenumber closest to laser: ", freq[22])
print("Wavelength closest to laser: ", wavel[22])
print("Real index near laser wavelength: ", real[22])
print("Imaginary index near laser wavelength: ", imaginary[22])

#He 2022 covers our laser wavelength. No need to extrapolate
"""
#Fit 1D poly to last two points
last2real = real[0:-1]
last2imaginary = imaginary[0:-1]
last2wavel = wavel[0:-1]
#REMEMBER: change to first or last two points depending on range
real_fit = np.polyfit(last2wavel, last2real, 1)
imaginary_fit = np.polyfit(last2wavel, last2imaginary, 1) #y = Nx + b

real_line = np.poly1d(real_fit)
imaginary_line = np.poly1d(imaginary_fit)

#num_extrapolation_pts = int((2.500 - 0.4)/0.005)
#print("Number of points extrapolated from data: ", num_extrapolation_pts)
#new_wavel = np.linspace(0.400, 2.500, num_extrapolation_pts)
new_wavel = np.arange(0.400, 2.500, 0.005)
real_extrapolation = real_line(new_wavel)
imaginary_extrapolation = imaginary_line(new_wavel)

#print("New wavelengths: ", new_wavel)

#Get real and imaginary components of refractive index at 0.44 micrometers
laser_wavel = float(0.44)
#i = list((i for i, e in enumerate(new_wavel) if e == laser_wavel))
#i = np.where(np.isclose(new_wavel, laser_wavel))
#print(i)
i = 8 #index of 0.44 from 0.400 at given step size, 0.005
real_at_wavel = real_extrapolation[i]
#print("Real (extrapolated): ", real_extrapolation)
imaginary_at_wavel = imaginary_extrapolation[i]
#print("Imaginary (extrapolated)", imaginary_extrapolation)

print("Real component at ", laser_wavel, ": ", real_at_wavel)
print("Imaginary component at ", laser_wavel, ": ", imaginary_at_wavel)

#Plot extrapolation
plt.figure()
plt.plot(new_wavel, real_extrapolation, label = "Extrapolated real")
plt.scatter(wavel, real, s=4, label = "Real (original)")
#plt.legend()
#plt.title('Leger (1983): real index vs. wavelength')
#plt.savefig('leger1983_extrapolated_real.png')

#plt.figure()
plt.plot(new_wavel, imaginary_extrapolation, label = "Extrapolated imaginary")
plt.scatter(wavel, imaginary, s=4, label = "Imaginary (original)")
plt.legend()
#plt.ylim(-6e-9, 1.5e-8)
plt.title('Mukai and Kraetschmer (1986): imaginary index vs. wavelength')
plt.savefig('mukai1986_extrapolated_both.png')

"""
