"""
Creates list of lower bounds and upper bounds for k and n by adding or subtracting their associated errors. nmin, nmax, kmin, and kmax are then used as limits in the wiggling process as defined in ri_wiggler.py
"""
from hypercube import ri

def get_min_max(data):
    data.nmin = [None]*len(data.wavel)
    data.nmax = [None]*len(data.wavel)
    data.kmin = [None]*len(data.wavel)
    data.kmax = [None]*len(data.wavel)
    for i in range(len(data.wavel)):
        #print("Length of wavel: ", len(data.wavel))
        #print("Length of n: ", len(data.n))
        #print("Length of dn: ", len(data.dn))
        #print("Length of nmin: ", len(data.nmin))
        #n calculated by kkr.py
        data.nmin[i] = data.n[i] - data.dn[i]
        data.nmax[i] = data.n[i] + data.dn[i]
        #k read from data
        data.kmin[i] = data.k[i] - data.dk[i]
        data.kmax[i] = data.k[i] + data.dk[i]
    return data
