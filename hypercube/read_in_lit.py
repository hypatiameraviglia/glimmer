#Open .txt files from literature studies and populate ri objects with data
from hypercube import ri
from hypercube import calc_absorp

#Location of experimental data files
directory = "~/scattering/lit"

def read_data(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):   #only the refrac files
            f = open(filename, "r")

            #refrac data by wavel
            ri.dataset = f.readlines()[0]
            ri.temp = f.readlines()[1]
            lines = f.readlines()[3:]

            for i in lines:
                ri.wavel.append(float(i.split('   ')[1])) #check splitting chars
                ri.n.append(float(i.split('   ')[2]))
                ri.k.append(float(i.split('   ')[3]))
    
            f.close()
    
    return ri

def get_error(ri):
#Populate error based on study; see respective papers
    if ri.dataset == "test2023":
    #Test file
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20
    #Test file
    if ri.dataset == "test2024":
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.30
    # Start of real data
    if ri.dataset == "warren1984":
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "mastrapa2008_Ic":
        # Couldn't find reported error for Mastrapa et al. 2008, although
        # they note substantial error in high transmittance areas.
        # Error estimated at a flat 20%, which is on the upper end of 
        # reasonable for RI experiments
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20
    
    if ri.dataset == "toon1994":
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "warrenbrandt2008":

    if ri.dataset == "bertie1969":
        # Calc from abs spec (dabs = 10 %)
        dalpha = 0.10 #% error on absorption spectrum, Bertie et al. (1969)
        ri.dk = calc_absorp.calc_error_from_dalpha(ri, dalpha)

    if ri.dataset == "clapp1995":
        # No error reported
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "he2022":
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.01
    
    if ri.dataset == "perovichandgovoni1991":
        # Error by data point

    if ri.dataset == "leger1983":
        #Calc from abs spec
        dalpha = 0.10 #% absolute error, Leger et al. (1983), p. 165
        ri.dk = calc_absorp.calc_error_from_dalpha(ri, dalpha)
    
    if ri.dataset == "mukaiandkraetschmer1986":
        # No error reported
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "hudgins1993":
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.05

    if ri.dataset == "mastrapa2008_Ia":
        # Couldn't find reported error, estimated 20%
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "browellandanderson1975":
        # Calc from abs spec
        dalpha = 0.10 #% error on absorption coefficient, Browell and Anderson (1975)
        ri.dk = calc_absorp.calc_error_from_dalpha(ri, dalpha)

    return ri
