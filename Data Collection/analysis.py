# Riley Karp
# C3PO
# Created 7/2/2018
# analysis.py

import sys
import matplotlib.pyplot as plt
import collection
import numpy as np
from scipy import stats

# Takes in a list of length data point and returns a list of the median plateau values.
def getLengthPlateaus( data ):

    plats = []
    lenPlat = 10 # num pts corresponding to last 3sec of plateau (~10pts/sec)

    idx = 30 #start by checking the difference between the 1st and 30th point (accounts for noise in consecutive points)
    # loop through the raw length data to find plateaus
    while idx < len(data):
        # calculate difference between points
        dif = abs( data[idx] - data[idx-30] )
        # if dif is too large, or you reach the end of the dataset,
        # then calculate median of plateau before the large change in length
        if (dif > 0.02) or (idx == ( len(data)-1 )):
            median = np.median( data[idx-lenPlat : idx] )

            # if the same plateau is found more than once (2 consecutive plateaus are
            # close in value), then average the values found and update the plateau list
            # else, append the new median plateau value to the list
            if len(plats) > 0 and abs(median - plats[-1]) < 0.5:
                plats[-1] = abs(median+plats[-1])/2
            else:
                plats.append(median)
            # increment index to skip ~3.5sec of lengths, to get to the next plateau
            idx += 35
        # otherwise, if the difference is not large, increment to check the next data point
        else:
            idx += 1

    return plats


# Takes in a list of force data and returns a list of the median plateau values
def getForcePlateaus( data ):

    plats = []
    lenPlat = 30 # num pts corresponding to last 3sec of plateau (~10 pts/sec)

    step = 4 #check the slope between 4 points (accounts for noise in consecutive points)
    # loop through all points
    idx = step
    # loop through force data and calculate slopes between points
    while idx < len(data):
        # calculate magnitude of the slope between two points
        slope = abs( data[idx] - data[idx-step] )/step
        # if slope is too steep, calculate median of plateau before steep part
        if (slope > 0.75) or (idx == ( len(data)-1 )):
            median = np.median( data[idx-lenPlat : idx] )

            # if plateau is found more than once (2 consecutive plateaus are
            # close in value), then average the values found and update plateau list
            if len(plats) > 0 and abs(median - plats[-1]) < ( max(data)*0.05 ):
                plats[-1] = abs(median+plats[-1])/2
            else: # otherwise, append new median plateau value to plateaus
                plats.append(median)

            # increment index to skip ~4sec of lengths, to get to the next plateau
            idx += 40

        else: # otherwise, if the slope is not large, increment to check the next data point
            idx += 1
    return plats


# Takes in 2 lists of data (independent & dependent variables) and plots them
# with a linear regression line (equation printed in terminal)
# if only one list is given, it is plotted as the dependent variable with index
# as independent variable.
# Optional argumetnts have the following defaults:
#  xlabel: Length (cm), ylabel: Force (N), title: Force vs. Length
def plotData( dep, indep=[], xlabel='Length (cm)', ylabel='Force (N)', title = 'Force vs. Length' ):
    # if only one list of data is given, plot that data vs. index
    if indep == []:
        plt.plot(dep, 'bo')
        xlabel = 'Reading Number'
    # if 2 lists of data are given, plot dep vs. indep
    else:
        # if lists are unequal lengths, print error message and return
        if len(indep) != len(dep):
            print 'Inputs are not equal lengths. X has length ', len(indep) , \
            ' and Y has length ' , len(dep)
            return
        # plot stretch pts in blue & relaxation in yellow
        indep_stretch, indep_relax, dep_stretch, dep_relax = getStretchRelax(indep,dep)

        plt.plot(indep_stretch, dep_stretch, 'bo', label='stretch')
        plt.plot(indep_relax, dep_relax, 'yo', label='relaxation')

        # Overall Linear regreession
        m, b, r, p, stde = stats.linregress(indep,dep)
        print 'Lin reg: y = ', m , 'x + ', b
        print 'R-squared: ', r**2
        plt.plot(indep, b + m*np.array(indep), 'r', label='linear fit')
        plt.legend(loc=2)

    # Set title and axis labels and show plot
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


# Takes in lists of data for idependent and dependent variables (length and force)
# returns 4 lists: stretch lengths, relax lengths, stretch foorces, and relax forces
# Used in plotData() to plot stretch and relax points in different colors
def getStretchRelax( indep, dep ):
    indep_stretch = [ indep[0] ]
    indep_relax = []
    dep_stretch = [ dep [0] ]
    dep_relax = []
    for i in range(1,len(dep)):
        if indep[i-1] < indep[i]:
            indep_stretch.append( indep[i] )
        else:
            indep_relax.append( indep[i] )

        if dep[i-1] < dep[i]:
            dep_stretch.append( dep[i] )
        else:
            dep_relax.append( dep[i] )
    return indep_stretch, indep_relax, dep_stretch, dep_relax


# plot force vs. reading number and length vs. reading number in the same window
def subplots( force, length ):
    plt.subplot(2,1,1)
    plt.plot(force, 'bo')
    plt.xlabel('Reading #')
    plt.ylabel('Force (N)')
    plt.title('Force & Length vs. Reading #')

    plt.subplot(2,1,2)
    plt.plot(length, 'bo')
    plt.xlabel('Reading #')
    plt.ylabel('Length (cm)')

    plt.show()


# Returns integral of force (N) and length (cm) data, given as lists
def integrate( force, length ):
    integral = 0
    for i in range( len(force)-1 ):
        # rectangle area
        rect = min(force[i],force[i+1]) * abs(length[i]-length[i+1])
        # triangle area
        tri = abs(force[i]-force[i+1]) * abs(length[i]-length[i+1]) * 0.5
        # full trapezoid area
        integral += ( rect + tri )
    return integral/100 # divide by 100 to get units in Joules


# Plots force vs. reading number and/or length vs. reading number based on
# command line argument given. calculate and print list of plateaus for each plot
def main(argv):
    if len(sys.argv) == 2:
        filename = sys.argv[1]

        # if given a force filename, read the forces, find and print the plateaus,
        # and plot force vs. reading number
        if 'force' in filename:
            data = collection.readForce(filename)
            plats = getForcePlateaus( data )
            print plats
            print len(plats)
            plotData(data)

        # if given a length filename, read the lengths, find and print the plateaus,
        # and plot length vs. reading number
        elif 'length' in filename:
            data = collection.readLength(filename)
            plats = getLengthPlateaus( data )
            print plats
            print len(plats)
            plotData(data)

        # if given a serial number, read the force and length files with that serial
        # number, find and print the force and length plateaus, and plot
        # force vs. reading number and length vs. reading number
        else:
            force = collection.readForce(filename + '_force.csv')
            length = collection.readLength(filename + '_length.csv')

            fplats = getForcePlateaus( force )
            lplats = getLengthPlateaus( length )

            print 'Force Plats: (', len(fplats), ') ' , fplats
            print
            print 'Length Plats: (', len(lplats), ') ' , lplats

            subplots(force,length)
    else:
        print 'usage: %s <serial number or force filename or length filename>' % (argv[0])
        exit()


if __name__ == '__main__':
    main(sys.argv)
