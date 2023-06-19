#Open .txt files from literature studies and populate ri objects with data
import ri from ri.py

directory = "~/scattering/lit" #TODO: does this reach into subdir?
for filename in os.listdir(directory):
        if filename.endswith('.txt'):   #only the refrac files
            f = open(filename, "r")

#refrac data by wavel
lines = f.readlines()[3:]

#TODO: what happens when two studies overlap? (same wavel, same T)
for i in lines:
    ri.wavel.append(float(i.split('   ')[1])) #check splitting chars
    ri.n.append(float(i.split('   ')[2]))
    ri.k.append(float(i.split('   ')[3]))

f.close()

