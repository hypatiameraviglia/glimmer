#Guide from "A numerical demonstration of the Kramers-Kronig relations" retrieved from http://people.exeter.ac.uk/sh481/kramers-kronig-relations.html, accessed 31 May 2023

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as ft
#from matplotlib import rc #Pretty text
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#rc('text',usetex=True)

g = 0.1
w0 = 5.0
def chii(w):
    return(g**2)/((w - w0)**2 + g**2)

w = np.linspace(0, 10, 800)

fig, ax = plt.subplots()
ax.plot(w, ft.hilbert(chii(w)), label = '${\\rm Re}[\chi(\omega)]$')
ax.plot(w, chii(w), 'r-', label = '${\\rm Im}[\chi(\omega)]$')
ax.set_xlabel('$\omega$" fontsize = 18')
ax.set_ylabel("${\\rm Im}[\chi(\omega)]$", fontsize = 18)
ax.set_title("Real RI calculated from Imaginary RI via KKR")
ax.legend()
plt.show()
