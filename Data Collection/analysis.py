# Riley Karp
# C3PO
# Created 7/2/2018
# analysis.py

import numpy as np
import sys
import csv
# import matplotlib.pyplot as plt


# Takes in a CSV filename as a command line argument. Assumes the data is in
# the form produced by the Force Gage, where the first row is the column headers
# and the forces are in the second column. Returns a list of the forces.
def getForce( filename ):

    forces = []
    file = open( filename, 'rU' )
    rows = csv.reader(file)
    next(rows,None)
    for row in rows:
        forces.append( float(row[1]) )
    file.close()

    return forces


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
    pass


if __name__ == '__main__':
    # getLength( sys.argv[1] )
    # getForce( sys.argv[1] )
    plats = getPlateaus( getForce(sys.argv[1]) )
    print plats
    print len(plats)
