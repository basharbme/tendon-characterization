# Riley Karp
# C3PO
# Created 8/3/2018
# plot.py

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def readData( filename ):
    serial = []
    stiffness = []
    ic_volume = []
    density = []
    volume = []

    data = { 'serial':serial,
            'stiffness':stiffness,
            'ic_volume':ic_volume,
            'density':density,
            'volume':volume }

    file = open( filename, 'rU' )
    rows = csv.reader(file)
    next(rows,None)
    for row in rows:
        serial.append( row[0] )
        stiffness.append( float(row[1]) )
        ic_volume.append( float(row[2]) )
        density.append( float(row[3]) )
        volume.append( float(row[4]) )
    file.close()

    return data


def plotData( indep,dep, data ):
    snum = data['serial']
    x = data[indep]
    y = data[dep]

    lin1 = ([],[])
    lin2 = ([],[])
    lin3 = ([],[])
    for i in range(len(snum)):
        # shape
        if snum[i][1] == 'N': #no infill
            m = 'x'
        elif snum[i][1] == 'S': #square
            m = 's'
        elif snum[i][1] == 'C': #circle
            m = 'o'
        else:
            m = '.' #default shape is a point

        # color and linear regression based on thickness
        if snum[i][2] == '1': #1mm
            c = 'r'
            lin1[0].append(x[i])
            lin1[1].append(y[i])
        elif snum[i][2] == '2': #2mm
            c = 'g'
            lin2[0].append(x[i])
            lin2[1].append(y[i])
        elif snum[i][2] == '3': #3mm
            c = 'b'
            lin3[0].append(x[i])
            lin3[1].append(y[i])
        else:
            c = (0,0,0) #default color to black

        #plot point
        plt.scatter(x[i],y[i],marker=m,color=c)

    # 1mm linear regreession line
    m1, b1, r1, p1, std1 = stats.linregress(lin1[0],lin1[1])
    eqn1 = 'y = ' + str(m1) + 'x + ' + str(b1) + ' , R^2 = ' + str(r1**2)
    plt.plot(lin1[0], b1 + m1*np.array(lin1[0]), 'r', label='1mm')

    # 2mm linear regreession line
    m2, b2, r2, p2, std2 = stats.linregress(lin2[0],lin2[1])
    eqn2 = 'y = ' + str(m2) + 'x + ' + str(b2) + ' , R^2 = ' + str(r2**2)
    plt.plot(lin2[0], b2 + m2*np.array(lin2[0]), 'g', label='2mm')

    # 3mm linear regreession line
    m3, b3, r3, p3, std3 = stats.linregress(lin3[0],lin3[1])
    eqn3 = 'y = ' + str(m3) + 'x + ' + str(b3) + ' , R^2 = ' + str(r3**2)
    plt.plot(lin3[0], b3 + m3*np.array(lin3[0]), 'b', label='3mm')

    # overall linear regreession line
    m, b, r, p, std = stats.linregress(x,y)
    eqn = 'y = ' + str(m) + 'x + ' + str(b) + ' , R^2 = ' + str(r**2)
    # plt.plot(x, b + m*np.array(x), 'k', label='overall')

    # print equations
    print '1mm: ' , eqn1
    print '2mm: ' , eqn2
    print '3mm: ' , eqn3
    print 'overall: ' , eqn

    plt.legend(loc=2)
    plt.xlabel(indep)
    plt.ylabel(dep)
    title = dep + ' vs. ' + indep
    plt.title(title)

    plt.show()


if __name__ == '__main__':
    data = readData('aggregate.csv')
    plotData('density','stiffness',data)
