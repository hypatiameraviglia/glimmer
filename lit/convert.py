#Reads in data from studies which records their data by wavenumbers and converts them to wavelength in microns.

import copy

directory = "."
old_filenames = ["old_hudgins1993_10K.txt", "old_hudgins1993_40K.txt", "old_hudgins1993_80K.txt", "old_hudgins1993_100K.txt", "old_hudgins1993_120K.txt", "old_hudgins1993_140K.txt"]
new_filenames = ["new_hudgins_10K.txt", "new_hudgins_40K.txt", "new_hudgins1993_80K.txt", "new_hudgins1993_100K.txt", "new_hudgins1993_120K.txt", "new_hudgins1993_140K.txt"]
freq = []
dataset = ""
temp = ""
errortype = ""
k = []

for i in range(len(old_filenames)):
    path = str(directory + "/" + old_filenames[i])
    f = open(path, "r")
    lines = f.readlines()

    #refrac data by wavel
    dataset = copy.deepcopy(lines[0])
    temp = copy.deepcopy(lines[1])
    errortype = copy.deepcopy(lines[2])
    data_lines = copy.deepcopy(lines[4:])
    freq = []
    k = []
    n = []
    for l in data_lines:
        line = l.split(' ')
        freq.append(copy.deepcopy(float(line[0]))) #check splitting chars
        #print("first freq from ", old_filenames[i], " is ", freq[0])
        n.append(copy.deepcopy(float(line[1])))
        k.append(copy.deepcopy(float(line[2])))
    f.close()

    wavel = [None]*len(freq)

    for j in range(len(freq)):
        wavel[j] = round(((1/(freq[j]))*10000), 10)
        #print("first wavel after conversion from ", old_filenames[i], " are ", wavel[0])

    path = str(directory + "/" + new_filenames[i])
    g = open(path, "w")
    g.write(str(dataset) + "\n")
    g.write(str(temp) + "\n")
    g.write(str(errortype) + "\n")
    g.write("wavel  n  k\n")
    #print("first wavel when being written to the new file from ", old_filenames[i], " are ", wavel[0])
    for i in range(len(wavel)):
        g.write(str(wavel[i]) + "  " + str(n[i]) + "  " + str(k[i]) + "\n")
    g.close()
