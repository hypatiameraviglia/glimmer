#Create class ri to store data from lit
import numpy as np

class ri:
    def __init__(self, dataset, wavel, temp, errortype, n, k, dn, dk):
        #wavelengths
        self.wavel = [ float(x) for x in wavel ]
        #dataset label
        self.dataset = dataset
        #errortype label
        self.errortype = errortype
        #temperature coord
        self.temp = [ float(x) for x in temp ]
        #real refractive index
        self.n = [ float(x) for x in n ] #Calculated in kkr.py
        #imaginary refractive index
        self.k = [ float(x) for x in k ]
        #error bar on real ref. ind.
        self.dn = [ float(x) for x in dn ] #Calculated in kkr_prop.py
        #error bar on imaginary ref. ind.
        self.dk = [ float(x) for x in dk ] #Calculated in read_in_lit.py
        #top of error bar for n
        self.nmax = [None]*len(wavel) #Calculated in min_max.py
        #bottom of error bar for n
        self.nmin = [None]*len(wavel)
        #top of error bar for k
        self.kmax = [None]*len(wavel)
        #bottom of error bar for k
        self.kmin = [None]*len(wavel)
        #avg n across many interpolations
        #self.n_avg = np.array([None]*len(wavel), dtype=np.float32),  # Calculated by calc_wiggled.extrapolate_wiggled_ris
        self.n_avg = np.empty(len(wavel))
        #avg k across many interpolations
        #self.k_avg = np.array([None]*len(wavel), dtype=np.float32)
        self.k_avg = np.empty(len(wavel))
        #stdev of n across many interpolations
        #self.n_stdev = np.array([None]*len(wavel), dtype=np.float32)
        self.n_stdev = np.empty(len(wavel))
        #stdev of k across many interpolations
        #self.k_stdev = np.array([None]*len(wavel), dtype=np.float32)
        self.k_stdev = np.empty(len(wavel))
    def __str__(self, dataset, wavel, n, k, dn, dk):
        print("{self.dataset} is a group of refractive indices of length ", len(n))

