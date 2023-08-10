#Reads in He (2022), which records their data by wavenumbers, and converts them to wavelength in microns.

import copy

directory = "."
old_filenames = ["old_he2022_30K.txt", "old_he2022_75K.txt", "old_he2022_105K.txt", "old_he2022_135K.txt"]
new_filenames = ["new_he2022_30K.txt", "new_he2022_75K.txt", "new_he2022_105K.txt", "new_he2022_135K.txt"]
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
    for l in data_lines:
        line = l.split(' ')
        freq.append(copy.deepcopy(float(line[0]))) #check splitting chars
        #print("first freq from ", old_filenames[i], " is ", freq[0])
        k.append(copy.deepcopy(float(line[1])))
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
    g.write("wavel  k\n")
    #print("first wavel when being written to the new file from ", old_filenames[i], " are ", wavel[0])
    for i in range(len(wavel)):
        g.write(str(wavel[i]) + "  n  " + str(k[i]) + "\n")
    g.close()
