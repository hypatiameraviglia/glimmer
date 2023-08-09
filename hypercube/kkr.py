#Guide from "A numerical demonstration of the Kramers-Kronig relations" retrieved from http://people.exeter.ac.uk/sh481/kramers-kronig-relations.html, accessed 31 May 2023

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as ft
#from matplotlib import rc #Pretty text
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#rc('text',usetex=True)

#dataset = "../lit/he_2022/he2022_imag_refrac.txt"

#Sets I as function of chi which is a function of frequency

#g = 0.1
#w0 = 5.0
#def chii(w):
#    return(g**2)/((w - w0)**2 + g**2)
#k = chii(w)
#n = ft.hilbert(chii(w))

#w = np.linspace(0, 10, 800)

#Reads in array of I from lit
f = open(dataset, "r")
lines = f.readlines()[1:]
w = []
k = []
for i in lines:
    w.append(float(i.split(' ')[0]))
    k.append(float(i.split(' ')[1]))
f.close()

n = ft.hilbert(k)

#Plot n and k by freq
fig, ax = plt.subplots()
ax.plot(w, n, label = '${\\rm Re}[w]$')
ax.plot(w, k, 'r-', label = '${\\rm Im}[w]$')
ax.set_xlabel("$\omega$", fontsize = 18)
ax.set_ylabel("${\\rm Im}[w]$", fontsize = 18)
ax.set_title("Real RI calculated from Imaginary RI via KKR")
ax.legend()
plt.show()
