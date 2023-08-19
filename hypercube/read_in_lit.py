#Open .txt files from literature studies and populate ri objects with data

import os

from hypercube import ri
from hypercube import absorp_error

#Location of experimental data files
#directory = "~/scattering/glimmer/lit"

def read_data(directory, filename):
    path = str(directory + "/" + filename)
    f = open(path, "r")
    lines = f.readlines()
    
    print("Reading data from ", filename, ". . .")
    #refrac data by wavel
    ri.dataset = lines[0]
    #print(ri.dataset)
    ri.temp = float(lines[1])
    #print(ri.temp)
    data_lines = lines[4:]
    wavel = []
    n = []
    k = []
    for i in data_lines:
        line = i.split('  ')
        #print("First row of each column: ", line[0][0], " ", line[1][0], " ", line[2][0])
        #print("line split into array by read_lin_lit: ", line)
        wavel.append(float(line[0])) #check splitting chars
        #print("wavelengths: ", wavel)
        #n.append(float(line[1]))
        #print("ns: ", n)
        k.append(float(line[2]))
        #print("ks read in by read_in_lit: ", k)
    
    ri.wavel = wavel
    ri.n = n
    ri.k = k
    ri.dn = [None]*len(ri.wavel)
    ri.dk = [None]*len(ri.wavel)
    ri.n_avg = [None]*len(ri.wavel)
    ri.k_avg = [None]*len(ri.wavel)
    ri.n_stdev = [None]*len(ri.wavel)
    ri.k_stdev = [None]*len(ri.wavel)
    print("Read successful.")
    f.close()
    return ri

def get_error(ri):
    #trigger = False
    #print("ri.dataset before get_error: ", ri.dataset)
    #print("evaluating filename: ", bool(ri.dataset == "test2023\n"))
    #print("ri.dk: ", ri.dk)
#Populate error based on study; see respective papers
    if ri.dataset == "test2023\n":
    #Test file
        #trigger = True
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20
    #Test file
    if ri.dataset == "test2024\n":
        #trigger = True
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.30
    #Test file
    if ri.dataset == "test2025\n":
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.10

    # Start of real data
    if ri.dataset == "warren1984\n":
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "mastrapa2008_Ic\n":
        # Couldn't find reported error for Mastrapa et al. 2008, although
        # they note substantial error in high transmittance areas.
        # Error estimated at a flat 20%, which is on the upper end of 
        # reasonable for RI experiments
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20
    
    if ri.dataset == "toon1994\n":
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "warrenbrandt2008\n":
        for i in range(len(ri.wavel)):
            if wavel[i] <= 0.6: #microns
                #Warren and Brandt (2006), fig 7
                for wb2006_dk.txt in os.listdir(directory):
                    f = open(filename, "r")
                    lines = f.readlines()[2:]
                    wavel, k, k_min, k_max = []
                    for line in lines:
                        wavel.append(0.001*(float(line.split(' ')[0])))
                        k_min.append(float(line.split(' ')[2]))
                        k_max.append(float(line.split(' ')[3]))
                        dk[line] = k_max[line] - k_min[line]
                        if wavel[i] >= wavel[line] and wavel[i] < wavel[line + 1]:
                            ri.dk[i] = dk[line]
            if wavel[i] > 0.6 and wavel[i] < 0.7:
                #Grenfell and Perovich (1981), table 1
                ri.dk[i] = ri.k[i]*0.10
            if wavel[i] >= 0.7 and wavel[i] < 1:
                #Grenfell and Perovich (1981), table 1
                ri.dk[i] = ri.k[i]*0.08
            if wavel[i] >= 1 and wavel[i] <= 1.4:
                #Grenfell and Perovich (1981), table 1
                ri.dk[i] = ri.k[i]*0.10
            if wavel[i] > 1.4 and wavel[i] <= 2.9:
                #Gosse et al. (1995), table 1
                for gosse1995_dk.txt in os.listdir(directory):
                    f = open(filename, "r")
                    lines = f.readlines()[2:]
                    wavel, perc_err = []
                    for line in lines:
                        wavel.append(float(line.split(' ')[0]))
                        perc_err.append(float(line.split(' ')[1]))
                        if wavel[i] >= wavel[line] and wavel[i] < wavel[line + 1]:
                            ri.dk[i] = ri.k[i]*perc_err[line]

            if wavel[i] > 2.9 and wavel[i] < 3.4:
                #Could not find Schaaf and Williams (1973), table 3
                # Instead, estimated error from plot of k uncertainties
                # in Warren and Brandt (2008) figure 8
               ri.dk[i] = ri.k[i]*0.10 
            if wavel[i] >= 3.4 and wavel[i] <= 7.8125:
                #Gosse et al. (1995), table 1
                for gosse1995_dk.txt in os.listdir(directory):
                    f = open(filename, "r")
                    lines = f.readlines()[2:] # Should this be 3?
                    wavel, perc_err = []
                    for line in lines:
                        wavel.append(float(line.split(' ')[0]))
                        perc_err.append(float(line.split(' ')[1]))
                        if wavel[i] >= wavel[line] and wavel[i] < wavel[line + 1]:
                            ri.dk[i] = ri.k[i]*perc_err[line]
            if wavel[i] > 7.8125 and wavel[i] <= 10.3:
                # Warren and BRandt (2008), fig 8
                ri.dk[i] = ri.k[i]*0.10
            if wavel[i] > 10.3 and wavel[i] <= 26:
                # Warren and Brandt (2008), fig 8
                ri.dk[i] = ri.k[i]*0.70
            if wavel[i] > 26 and wavel[i] <= 200:
                # Estimated by Warren and Brandt (2008), in excess of Curtis et al. (2005)
                for wb2008_k.txt in os.listdir(directory):
                    wb = open(filename, "r")
                    wb_lines = wb.readlines()[2:]
                    wb_wavel, k_266 = []
                    for wb_line in wb_lines:
                        wb_wavel.append(float(wb_line.split(' ')[0]))
                        k_266.append(float(wb_line.split(' ')[1]))
                    for curtis2005_k.txt in os.listdir(directory):
                        curtis = open(filename, "r")
                        curtis_lines = curtis.readlines()[2:] # Should this be 3
                        curtis_wavel, k_176 = []
                        for curtis_line in curtis_lines:
                            curtis_wavel.append(10000/(float(line.split(' ')[0]))) # Convert freq in cm-1 to wavel in microns 
                            k_176.append(float(line.split(' ')[1]))
                            # Calculation of dk according to Warren and Brandt (2008)'s uncertainty estimation on pg. 7
                            dk = []
                            for j in range(len(curtis_lines)):
                                dk[j] = ((k_266[j] - k_176[j])/k_266[j]) 
                            if wavel[i] >= curtis_wavel[curtis_line] and wavel[i] < curtis_wavel[curtis_line]:
                                ri.dk[i] = dk[curtis_line]
            if wavel[i] > 200:
            # Warren and Brandt (2008), fig 8
                ri.dk[i] = ri.k[i]*0.10

    if ri.dataset == "bertie1969\n":
        # Calc from abs spec (dabs = 10 %)
        perc_dalpha = 0.10 #% error on absorption spectrum, Bertie et al. (1969)
        ri.dk = absorp_error.calc_error_from_dalpha(ri, perc_dalpha)

    if ri.dataset == "clapp1995\n":
        # No error reported
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "he2022\n":
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.01
    
    if ri.dataset == "perovichandgovoni1991\n":
        # Error by data point
        dalpha_array = []
        for perovich_1991_absorp_error.txt in os.listdir(directory):
            f = open(filename, "r")
            lines = f.readlines()[2:] # Should this be 2?
            for i in lines:
                dalpha_array.append(float(i.split(' ')[1]))
            
                ri.dk = absorp_error.perovich(ri, dalpha_array)

    if ri.dataset == "leger1983\n":
        #Calc from abs spec
        perc_dalpha = 0.10 #% absolute error, Leger et al. (1983), p. 165
        ri.dk = calc_absorp.calc_error_from_dalpha(ri, perc_dalpha)
    
    if ri.dataset == "mukaiandkraetschmer1986\n":
        # No error reported
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "hudgins1993\n":
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.05

    if ri.dataset == "mastrapa2008_Ia\n":
        # Couldn't find reported error, estimated 20%
        for i in range(len(ri.k)):
            ri.dk[i] = ri.k[i]*0.20

    if ri.dataset == "browellandanderson1975\n":
        # Calc from abs spec
        perc_dalpha = 0.10 #% error on absorption coefficient, Browell and Anderson (1975)
        ri.dk = calc_absorp.calc_error_from_dalpha(ri, perc_dalpha)
    #print("ri.dk after get_error: ", ri.dk)
    #print("trigger value: ", trigger)
    return ri.dk
