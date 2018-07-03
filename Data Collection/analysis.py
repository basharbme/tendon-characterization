# Riley Karp
# C3PO
# Created 7/2/2018
# analysis.py

import sys
import matplotlib.pyplot as plt
import collection


# Takes in a list of data and returns a list of the average value at each plateau
def getPlateaus( data ):
    plats = []
    start = 0
    end = 99

    while end < len(data):
        avg = sum( data[start:end] )/len( data[start:end] )
        close = [ ( abs(avg-x) < 0.2 ) for x in data[start:end] ]
        if all(close):
            plats.append(avg)
            start = end + 1
            end += 100
        end += 1
        start += 1

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
    forces = collection.getForce(sys.argv[1])
    plats = getPlateaus( forces )
    print plats
    print len(plats)

    plotData(forces)
