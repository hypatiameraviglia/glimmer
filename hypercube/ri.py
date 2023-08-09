#Create class ri to store data from lit
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
        self.nmax = [ ni + dni for ni,dni in zip(n,dn)]
        #bottom of error bar for n
        self.nmin = [ ni - dni for ni,dni in zip(n,dn)]
        #top of error bar for k
        self.kmax = [ ki + dki for ki,dki in zip(k,dk)]
        #bottom of error bar for k
        self.kmin = [ ki - dki for ki,dki in zip(k,dk)]
        #avg n across many interpolations
        self.n_avg = [None]*len(wavel) # Calculated by calc_wiggled.extrapolate_wiggled_ris
        #avg k across many interpolations
        self.k_avg = [None]*len(wavel)
        #stdev of n across many interpolations
        self.n_stdev = [None]*len(wavel)
        #stdev of k across many interpolations
        self.k_stdev = [None]*len(wavel)
    def __str__(self, dataset, wavel, n, k, dn, dk):
        print("{self.dataset} is a group of refractive indices of length ", len(n))

