# Riley Karp
# C3PO
# Created 8/3/2018
# plot.py

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import sys


# Reads in data (assumes file is in the form of aggregate.csv)
# Returns a dictionary with keys: 'serial','stiffness', 'ic_volume','density',
# 'volume', and 'area'. Values are lists of the corresponding data from the
# aggregate.csv file.
def readData( filename ):
    # initialize empty lists for dictionary values
    serial = []
    stiffness = []
    ic_volume = []
    density = []
    volume = []
    area = []

    # initialize dictionary with keys as abbreviated column headers of aggregate.csv
    # may need to update this dictionary if more columns of data are added to aggregate.csv
    data = { 'serial':serial,
            'stiffness':stiffness,
            'ic_volume':ic_volume,
            'density':density,
            'volume':volume,
            'area':area }

    file = open( filename, 'rU' )
    rows = csv.reader(file)
    next(rows,None) # skip first row (column headers)
    for row in rows:
        serial.append( row[0] )
        stiffness.append( float(row[1]) )
        ic_volume.append( float(row[2]) )
        density.append( float(row[3]) )
        volume.append( float(row[4]) )
        area.append( float(row[5]) )
    file.close()

    return data


# Plots values from data<dictionary> and regression lines, with indep on the x axis
# and dep on the y axis indep and dep are keys in the data dictionary, which is
# assumed to be the result of calling readData() on aggregate.csv
def plotData( indep,dep, data ):
    snum = data['serial'] # list of serial numbers
    x = data[indep] # initialize independent variable
    y = data[dep] # initialize dependent variable

    # tuples of lists in the form (indep,dep) to later use for Linear
    # regression calculations for thicknesses of 1mm, 2mm, and 3mm
    lin1 = ([],[])
    lin2 = ([],[])
    lin3 = ([],[])

    # loop through data and plot each point. set size and shape based on serial number
    for i in range(len(snum)):
        # set point color and add values to linear regression tuples based on thickness
        # thickness 3rd character of serial number
        if snum[i][2] == '1': #1mm
            # don't plot the 1.5mm thick tendon since we only have the one.
            # and we don't want it to be included in the 1mm linear regression data
            if (len(snum[i]) > 3) and (snum[i][3] == '5'):
                continue
            else:
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

        # set point shape based on infill shape (2nd character of serial number)
        if snum[i][1] == 'N': #no infill
            m = 'x'
            face = c # solid colored x
        elif snum[i][1] == 'S': #square
            m = 's'
            face = 'none'
        elif snum[i][1] == 'C': #circle
            m = 'o'
            face = 'none' # hollow shape
        elif snum[i][1] == 'D': #diamond
            m = 'd'
            face = 'none' # hollow shape
        else:
            m = '.' #default shape is a point
            face = c # solid colored point

        #plot data point
        plt.scatter(x[i],y[i],marker=m,edgecolor=c,facecolor=face,s=50)


    # ----Calculate and plot linear regression / quadratic regression lines----

    # 1mm linear regression line
    m1, b1, r1, p1, std1 = stats.linregress(lin1[0],lin1[1])
    # string in the form 'y = ax + b, R^2 = _'
    eqn1 = 'y = ' + str( round(m1,3) ) + 'x + ' + str( round(b1,3) ) + ' , R^2 = ' + str( round(r1**2,3) )
    plt.plot(lin1[0], b1 + m1*np.array(lin1[0]), 'r', label='1mm: '+ eqn1)


    # 2mm linear regression line
    m2, b2, r2, p2, std2 = stats.linregress(lin2[0],lin2[1])
    # string in the form 'y = ax + b, R^2 = _'
    eqn2 = 'y = ' + str( round(m2,3) ) + 'x + ' + str( round(b2,3) ) + ' , R^2 = ' + str( round(r2**2,3) )
    plt.plot(lin2[0], b2 + m2*np.array(lin2[0]), 'g', label='2mm: ' + eqn2)


    # 3mm linear regression line
    m3, b3, r3, p3, std3 = stats.linregress(lin3[0],lin3[1])
    # string in the form 'y = ax + b, R^2 = _'
    eqn3 = 'y = ' + str( round(m3,3) ) + 'x + ' + str( round(b3,3) ) + ' , R^2 = ' + str( round(r3**2,3) )
    plt.plot(lin3[0], b3 + m3*np.array(lin3[0]), 'b', label='3mm: ' + eqn3)


    # overall linear regression line
    m, b, r, p, std = stats.linregress(x,y)
    # string in the form 'y = ax + b, R^2 = _'
    eqn = 'y = ' + str( round(m,3) ) + 'x + ' + str( round(b,3) ) + ' , R^2 = ' + str( round(r**2,3) )
    # plot linear regression line
    # plt.plot(x, b + m*np.array(x), 'k', label=eqn )


    # overall quadratic regression line
    poly = np.polyfit(x,y,2)
    p = np.poly1d(poly)
    # R^2 calculation
    mean = np.array([ sum(y)/len(y) for i in range(len(y))])
    R2 = 1 - ( sum((p(x)-y)**2) / sum((y-mean)**2) )
    # string in the form 'y = ax^2 + bx + c, R^2 = _'
    polyeq = 'y = ' + str( round(poly[0],3) ) + 'x^2 + ' + str( round(poly[1],3) ) + 'x + ' + \
        str( round(poly[2],3) ) + ', R^2: ' +str(round(R2,3))
    # plot quadratic regression curve
    t = np.linspace(min(data[indep]),max(data[indep]),500)
    # plt.plot(t,p(t),'-',color='black',label=polyeq)

    # print equations
    print '\n--------------- Linear Regression Equations ----------------'
    print '1mm: ' , eqn1
    print '2mm: ' , eqn2
    print '3mm: ' , eqn3
    print 'overall: ' , eqn
    print '\n---------------- Polynomial Fit Equation -------------------'
    print 'overall: ' , polyeq , '\n'


    # label plot
    plt.legend(loc=2)
    plt.xlabel(indep)
    plt.ylabel(dep)
    title = dep + ' vs. ' + indep
    plt.title(title)

    plt.show()


# Reads aggregate.csv and plots the data in the columns specified by the two
# command line arguments, where the 1st is the independent variable and
# the 2nd is the dependent variable to plot.
def main( argv ):
    if len(argv) < 3:
        print 'usage: %s <independent> <dependent> , where variables are [stiffness,ic_volume,density,volume,area]' % (argv[0])
        exit()
    data = readData('aggregate.csv')
    plotData(argv[1],argv[2],data)


if __name__ == '__main__':
    main(sys.argv)
