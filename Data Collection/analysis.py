# Riley Karp
# C3PO
# Created 7/2/2018
# analysis.py

import sys
import matplotlib.pyplot as plt
import collection
import numpy as np

# length getPlateaus
def getLengthPlateaus( data ):

    plats = []
    lenPlat = 30 # num pts corresponding to last 3sec of plateau
    # length: ____ pts/sec

    # loop through all points
    for idx in range(2,len(data)):
        # calculate magnitude of the slope between two consecutive points
        slope = abs( data[idx] - data[idx-2] )
        # if slope is too steep, calc median of plateau before it
        if (slope > 0.2) or (idx == ( len(data)-1 )):
            median = np.median( data[idx-lenPlat : idx] )

            if len(plats) > 0 and abs(median - plats[-1]) < 0.2:
                plats[-1] = abs(median+plats[-1])/2
            else:
                plats.append(median)
    return plats


# Takes in a list of data and returns a list of the median value at each plateau
def getForcePlateaus( data ):

    plats = []
    lenPlat = 30 # num pts corresponding to last 3sec of plateau
    # force: 10 pts/sec = 30 pts in 3sec

    # loop through all points
    for idx in range(1,len(data)):
        # calculate magnitude of the slope between two consecutive points
        slope = abs( data[idx] - data[idx-1] )
        # if slope is too steep, calc median of plateau before it
        if (slope > 0.5) or (idx == ( len(data)-1 )):
            median = np.median( data[idx-lenPlat : idx] )
            print median
            plats.append(median)

    return plats


# Takes in 2 lists of data (independent & dependent variables) and plots them
# if only one list is given, it is plotted as the dependent variable with index
# as independent variable.
def plotData( dep, indep = [] ):
    if indep == []:
        plt.plot(dep, 'bo')
    else:
        if len(indep) != len(dep):
            print 'Inputs are not equal lengths. X has length ', len(indep) , \
            ' and Y has length ' , len(dep)
            return
        plt.plot(indep, dep, 'bo')
    plt.show()


if __name__ == '__main__':
    # data = collection.readForce(sys.argv[1])
    # plats = getForcePlateaus( data )

    data = collection.readLength(sys.argv[1])
    plats = getLengthPlateaus( data )

    print plats
    print len(plats)

    plotData(data)
