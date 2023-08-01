#Create class ri to store data from lit
class ri:
    def __init__(self, dataset, wavel, temp, errortype, n, k, dn, dk):
        self.wavel = float(wavel)
        self.dataset = dataset
        self.errortype = errortype
        self.temp = float(temp)
        self.n = float(n)
        self.k = float(k)
        self.dn = float(dn)
        self.dk = float(dk)
        self.nmax = [ ni + ni*dni for ni in n for dni in dn ]
        self.nmin = [ ni - ni*dni for ni in n for dni in dn ]
        self.kmax = [ ki + ki*dki for ki in k for dki in dk ]
        self.kmin = [ ki - ki*dki for ki in k for dki in dk ]
    def __str__(self, dataset, wavel, n, k, dn, dk):
        print("{self.dataset} is a group of ref. ind. of length ", len(n))

