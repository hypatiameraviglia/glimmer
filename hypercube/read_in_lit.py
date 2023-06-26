#Open .txt files from literature studies and populate ri objects with data
import ri from ri.py

directory = "~/scattering/lit" #TODO: does this reach into subdir?
for filename in os.listdir(directory):
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

#Populate error based on study; see paper
if filename == "warren1984":

if filename == "mastrapa2008_Ic":

if filename == "toon1994":
    for i in ri.k:
        ri.dk[i] = ri.k[i]*0.20

if filename == "warrenbrandt2008":

if filename == "bertie1969":
    for i in ri.k:
        ri.dk[i] = ri.k[i]*0.05

if filename == "clapp1995":

if filename == "he2022":
    for i in ri.k:
        ri.dk[i] = ri.k[i]*0.01
if filename == "perovichandgovoni1991":

if filename == "leger1983":

if filename == "mukaiandkraetschmer1986":

if filename == "hudgins1993":
    for i in ri.k:
        ri.dk[i] = ri.k[i]*0.05

if filename == "mastrapa2008_Ia":

if filename == "browellandanderson1975":
    for i in ri.k:
        ri.dk[i] = ri.k[i]*0.10

if filename == "rousch1997":

if filename == "kofman2019":


