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


# Takes in 2 lists of data (independent (x) & dependent (y) variables) and plots them
def plotData( x, y ):
    if len(x) != len(y):
        print 'Inputs are not equal lengths. X has length ', len(x) , \
        ' and Y has length ' , len(y)
        return
    plt.plot(x,y, 'bo')
    plt.show()


if __name__ == '__main__':
    plats = getPlateaus( collection.getForce(sys.argv[1]) )
    print plats
    print len(plats)

    plotData([1,2,3,4,5],[1,2,3,4,5])
