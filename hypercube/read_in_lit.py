#Open .txt files from literature studies and populate ri objects with data
from hypercube import ri
    
    #Location of experimental data files
    directory = "~/scattering/lit"

def read_data(directory):
    if filename.endswith('.txt'):   #only the refrac files
        f = open(filename, "r")

        #refrac data by wavel
        ri.dataset = f.readlines()[0]
        ri.temp = f.readlines()[1]
        lines = f.readlines()[3:]

        #TODO: what happens when two studies overlap? (same wavel, same T)
        for i in lines:
            ri.wavel.append(float(i.split('   ')[1])) #check splitting chars
            ri.n.append(float(i.split('   ')[2]))
            ri.k.append(float(i.split('   ')[3]))
    
    f.close()
    
    return ri

def get_error(ri):
#Populate error based on study; see respective papers
    if ri.dataset == "test2023":
    #Test file for use by test_read_in_lit.py
        for i in ri.wavel:
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "warren1984":

    if ri.dataset == "mastrapa2008_Ic":

    if ri.dataset == "toon1994":
        for i in ri.k:
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "warrenbrandt2008":

    if ri.dataset == "bertie1969":
        for i in ri.k:
            ri.dk[i] = ri.k[i]*0.05

    if ri.dataset == "clapp1995":

    if ri.dataset == "he2022":
        for i in ri.k:
            ri.dk[i] = ri.k[i]*0.01
    if ri.dataset == "perovichandgovoni1991":

    if ri.dataset == "leger1983":

    if ri.dataset == "mukaiandkraetschmer1986":

    if ri.dataset == "hudgins1993":
        for i in ri.k:
            ri.dk[i] = ri.k[i]*0.05

    if ri.dataset == "mastrapa2008_Ia":

    if ri.dataset == "browellandanderson1975":
        for i in ri.k:
            ri.dk[i] = ri.k[i]*0.10

    if ri.dataset == "rousch1997":

    if ri.dataset == "kofman2019":

    return ri
