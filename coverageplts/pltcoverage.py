import matplotlib.pyplot as plt
import csv
import matplotlib.patches as patches

acsv = 'amorphous'
ccsv = 'crystalline'

def readcsv(csvfile):
    with open(csvfile + '.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)
        data = []
        for row in reader:
            data.append((str(row[0]), float(row[1]), float(row[3]), str(row[5]), str(row[6]))) #name, temp, wavel, color, mark
            data.append((str(row[0]), float(row[1]), float(row[4]), str(row[5]), str(row[6])))
            data.append((str(row[0]), float(row[2]), float(row[3]), str(row[5]), str(row[6])))
            data.append((str(row[0]), float(row[2]), float(row[4]), str(row[5]), str(row[6])))

    # Organize data
    labels = [item[0] for item in data]
    temps = [item[1] for item in data]
    wavels = [item[2] for item in data]
    colors = [item[3] for item in data]
    marks = [item[4] for item in data]
    
    return labels, temps, wavels, colors, marks

def plotcoverage(csvfile, labels, temps, wavels, colors, marks):

    # Plot coverage
    fig, ax = plt.subplots()
    units = [] #make list of plots for legend
    for i,label in enumerate(labels):
        unit = ax.scatter(temps[i], wavels[i], marker=marks[i], s=10, color=colors[i]) #tol
        units.append(unit)
   
    # Add context: JWST and HST, environ temps, ice phase transitions
    alpha = 0.15 #opacity

    jwst = [0.6, 28.5] #microns, NIRCAM and MIRI
    hst = [0.115, 1.7] #microns, STIS and WFC3
    # Plot telescope ranges
    #jwst
    ax.axhspan(jwst[0], jwst[1], xmin=0, xmax=1, alpha=alpha, color='#88CCEE')
    ax.text(290, 3.5, 'JWST', rotation=90, fontsize='small')
    #hst
    ax.axhspan(hst[0], hst[1], xmin=0, xmax=1, alpha=alpha, color='#DDCC77')
    ax.text(290, 0.4, 'HST', rotation=90, fontsize='small')

    # Plot temps of relevant environments
    plumes = [130, 200] #K, Postberg et al. 2018b
    europa = [72,130] #K, from Galilieo's sampling of ~20% of the surface, equitorially biased, Rathbun et al. 2010
    sossb = [10,90] #K, Lisse et al. 2021]
    marspolar = [140, 200] #K, range of seasonal variation, Mendoza et al. 2021, fig. 5 especially
    pluto = [37,47] #K, surface, New Horizons, Lisse et al. 2021

    #plumes
    ax.axvspan(plumes[0], plumes[1], ymin=0, ymax=1, alpha=alpha, color='#44AA99')
    ax.text(165, 0.035, 'Enceladus plumes', fontsize='xx-small', horizontalalignment='center')
    #mars poles
    ax.axvspan(marspolar[0], marspolar[1], ymin=0, ymax=1, alpha=alpha, color='#117733')
    ax.text(170, 0.06, 'Mars poles', fontsize='xx-small', horizontalalignment= 'center')
    #europa
    ax.axvspan(europa[0], europa[1], ymin=0, ymax=1, alpha=alpha, color='#999933')
    ax.text(100, 0.06, 'Europa', fontsize='xx-small', horizontalalignment= 'center')
    #pluto
    ax.axvspan(pluto[0], pluto[1], ymin=0, ymax=1, alpha=alpha, color='#CC6677')
    ax.text(42, 0.06, 'Pluto surface', fontsize='xx-small', horizontalalignment= 'center')
   #small outer solar system bodies 
    ax.axvspan(sossb[0], sossb[1], ymin=0, ymax=1, alpha=alpha, color='#332288')
    ax.text(50, 0.035, 'Small outer solar system bodies', fontsize='xx-small', horizontalalignment= 'center')
    
    #Mark freezing temp between Ia and Ic
    ax.axvline(x=140, color='#332288', linestyle='--', linewidth=1)
    ax.text(135, 100, 'freezes amorphous', rotation=90, fontsize='xx-small', verticalalignment='center')
    ax.text(142, 100, 'freezes crystalline', rotation=90, fontsize='xx-small', verticalalignment='center')

    #Repeat plotting so that marker colors are on top of tints, ik it's stupid
    for i,label in enumerate(labels):
        ax.scatter(temps[i], wavels[i], marker=marks[i], s=10, color=colors[i]) #tol
    
    # Connect points with lines
    for label in set(labels):
        label_points = [(temps[i], wavels[i]) for i, l in enumerate(labels) if l == label]
        min_temp = min(temp for temp, _ in label_points)
        max_temp = max(temp for temp, _ in label_points)
        min_wavel = min(wavel for _, wavel in label_points)
        max_wavel = max(wavel for _, wavel in label_points)
        width = max_temp - min_temp
        height = max_wavel - min_wavel
        color = [colors[i] for i, l in enumerate(labels) if l == label][0]
        rectangle = patches.Rectangle((min_temp, min_wavel), width, height, linewidth=1.5, edgecolor=color, facecolor='none', linestyle='-')
        ax.add_patch(rectangle)

    #Add paper reference labels
    if csvfile == 'amorphous':
        subpltlabel = 'A'
    else:
        subpltlabel = 'B'

    # Description
    ax.set_yscale('log')
    ax.grid(color='grey', linestyle='--', linewidth=0.25)
    ax.set_xlabel('Temperature (K)')
    ax.set_ylabel('Wavelength (microns)')
    ax.set_title(f'{subpltlabel}) Literature coverage of refractive indices for {csvfile} water ice')
    ax.set_xlim(0, 300) #make plots easily comparable
    ax.set_ylim(0.03, 2700)
    
    #Legend
    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.15, box.width, box.height * 0.9])
    ax.legend(units[0::4],labels[0::4],loc='upper center', bbox_to_anchor=(0.5,-0.15),ncol=4,fontsize='xx-small') #every fourth item, because there are four artists per dataset

    plt.savefig(f'{csvfile}_coverage.png', dpi=1200)


    return

labels, temps, wavels, colors, marks = readcsv(acsv)
plotcoverage(acsv, labels, temps, wavels, colors, marks)
labels, temps, wavels, colors, marks = readcsv(ccsv)
plotcoverage(ccsv, labels, temps, wavels, colors, marks)

