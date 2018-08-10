# Riley Karp
# C3PO
# Created 8/3/2018
# plot.py

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import sys

def readData( filename ):
    serial = []
    stiffness = []
    ic_volume = []
    density = []
    volume = []
    area = []

    data = { 'serial':serial,
            'stiffness':stiffness,
            'ic_volume':ic_volume,
            'density':density,
            'volume':volume,
            'area':area }

    file = open( filename, 'rU' )
    rows = csv.reader(file)
    next(rows,None)
    for row in rows:
        serial.append( row[0] )
        stiffness.append( float(row[1]) )
        ic_volume.append( float(row[2]) )
        density.append( float(row[3]) )
        volume.append( float(row[4]) )
        area.append( float(row[5]) )
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
        # color and linear regression based on thickness
        if snum[i][2] == '1': #1mm (not 1.5mm)
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

        # shape
        if snum[i][1] == 'N': #no infill
            m = 'x'
            face = c
        elif snum[i][1] == 'S': #square
            m = 's'
            face = 'none'
        elif snum[i][1] == 'C': #circle
            m = 'o'
            face = 'none'
        elif snum[i][1] == 'D': #diamond
            m = 'd'
            face = 'none'
        else:
            m = '.' #default shape is a point
            face = 'none'

        #plot point
        plt.scatter(x[i],y[i],marker=m,edgecolor=c,facecolor=face,s=50)


    # 1mm linear regreession line
    m1, b1, r1, p1, std1 = stats.linregress(lin1[0],lin1[1])
    eqn1 = 'y = ' + str( round(m1,3) ) + 'x + ' + str( round(b1,3) ) + ' , R^2 = ' + str( round(r1**2,3) )
    # plt.plot(lin1[0], b1 + m1*np.array(lin1[0]), 'r', label='1mm: '+ eqn1)

    # 2mm linear regreession line
    m2, b2, r2, p2, std2 = stats.linregress(lin2[0],lin2[1])
    eqn2 = 'y = ' + str( round(m2,3) ) + 'x + ' + str( round(b2,3) ) + ' , R^2 = ' + str( round(r2**2,3) )
    # plt.plot(lin2[0], b2 + m2*np.array(lin2[0]), 'g', label='2mm: ' + eqn2)

    # 3mm linear regreession line
    m3, b3, r3, p3, std3 = stats.linregress(lin3[0],lin3[1])
    eqn3 = 'y = ' + str( round(m3,3) ) + 'x + ' + str( round(b3,3) ) + ' , R^2 = ' + str( round(r3**2,3) )
    # plt.plot(lin3[0], b3 + m3*np.array(lin3[0]), 'b', label='3mm: ' + eqn3)

    # overall linear regreession line
    m, b, r, p, std = stats.linregress(x,y)
    eqn = 'y = ' + str( round(m,3) ) + 'x + ' + str( round(b,3) ) + ' , R^2 = ' + str( round(r**2,3) )
    plt.plot(x, b + m*np.array(x), 'k', label=eqn )

    # overall quadratic regression line
    p = np.poly1d(np.polyfit(x,y,2))
    SSE = sum((p(x)-y)**2)
    mean = np.array([ sum(y)/len(y) for i in range(len(y))])
    SSTO = sum((y-mean)**2)
    R2 = 1- (SSE/SSTO)
    print SSE
    print SSTO
    print R2

    t = np.linspace(min(data[indep]),max(data[indep]),500)
    plt.plot(t,p(t),'-',color='black',label=str(p) + ', R^2: ' +str(round(R2,3)) )

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


def main( argv ):
    if len(argv) < 3:
        print 'usage: %s <independent> <dependent> , where variables are [stiffness,ic_volume,density,volume,area]' % (argv[0])
        exit()
    data = readData('aggregate.csv')
    plotData(argv[1],argv[2],data)


if __name__ == '__main__':
    main(sys.argv)
