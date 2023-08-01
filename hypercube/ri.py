#Create class ri to store data from lit
class ri:
    def __init__(self, dataset, wavel, temp, errortype, n, k, dn, dk):
        self.wavel = [ float(x) for x in wavel ]
        self.dataset = dataset
        self.errortype = errortype
        self.temp = [ float(x) for x in temp ]
        self.n = [ float(x) for x in temp ]
        self.k = [ float(x) for x in k ]
        self.dn = [ float(x) for x in dn ]
        self.dk = [ float(x) for x in dk ]
        self.nmax = [ ni + ni*dni for ni in n for dni in dn ]
        self.nmin = [ ni - ni*dni for ni in n for dni in dn ]
        self.kmax = [ ki + ki*dki for ki in k for dki in dk ]
        self.kmin = [ ki - ki*dki for ki in k for dki in dk ]
    def __str__(self, dataset, wavel, n, k, dn, dk):
        print("{self.dataset} is a group of ref. ind. of length ", len(n))

