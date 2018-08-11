# Riley Karp
# C3PO
# Created 6/29/2018
# driver.py

import collection
import analysis
import sys
import csv
import os.path


# Reads the force and length plateau values from the given CSV file with
# forces in the first column and lengths in the second.
# Returns lists of the force and length plateau values.
def readPlats( filename ):
    force_plats = []
    length_plats = []
    file = open( filename, 'rU' )
    rows = csv.reader(file)
    next(rows,None) # skip first row with column headers
    for row in rows:
        force_plats.append( float(row[0]) )
        length_plats.append( float(row[1]) )
    file.close()

    return force_plats,length_plats


# Takes in lists of force and length plateau values.
# Calculates and returns two floats that are the work required to stretch and relax the tendon.
def getWork( forces, lengths ):
    peak = forces.index(max(forces))
    stretch = analysis.integrate(forces[:peak+1],lengths[:peak+1])
    relax = analysis.integrate(forces[peak:]+[forces[0]],lengths[peak:]+[lengths[0]])
    return stretch, relax


# Takes one command line argument, which is assumed to be the tendon serial number.
# Reads force and lentgh plateaus from 'serialNumber_plats.csv' file if it exists.
# Otherwise, reads raw force and length data and calculates plateaus using methods
# from analysis.py, and saves plateaus in a file named 'serialNumber_plats.csv'.
# Calculates and prints work required to stretch and relax tendon, and its efficiency.
# (work data is only accurate for work loop. not when tendon was tested at random lengths)
# Plots force vs. length using plotData() method from analysis.py
def main( argv ):
    '''Check if given cmd line args'''
    if len(argv) < 2:
        print 'usage: %s <serial number>' % (argv[0])
        exit()

    # Read plateaus from file if it exists
    if os.path.isfile('../Data/' + argv[1] + '_plats.csv'):
        print 'reading'
        force_plats,length_plats = readPlats('../Data/' + argv[1] + '_plats.csv')

    # Calculate plateaus from raw data if plateau file doesn't already exist
    else:
        print 'calculating'
        lengths = collection.readLength(argv[1] + '_length.csv')
        forces = collection.readForce(argv[1] + '_force.csv')

        length_plats = analysis.getLengthPlateaus(lengths)
        force_plats = analysis.getForcePlateaus(forces)

        plats = [ ['Force','Length'] ]
        for i in range( max( len(force_plats),len(length_plats) ) ):
            if i >= len(force_plats):
                force = 0
            else:
                force = force_plats[i]
            if i >= len(length_plats):
                length = 0
            else:
                length = length_plats[i]

            plats.append( [force, length] )

        # save plateaus to CSV file named 'serialNumber_plats.csv'
        collection.save(plats, argv[1] + '_plats', plats = True)


    # calculate and print work data (only accurate for work loop, not random lengths)
    stretch, relax = getWork(force_plats,length_plats)
    print 'Stretch: ' , stretch , 'J'
    print 'Relax: ' , relax , 'J'
    print 'Efficiency: ' , (relax/stretch)*100 , '%'

    # plot force vs. length. Slope of line is tendon stiffness
    analysis.plotData(force_plats,length_plats)


# Takes in filament stiffness, k, in N/cm and length in cm. Returns E in MPa
def elastic_mod(k,length,area):
    # E = k*length/area
    return (k*length) / (area*100)


if __name__ == '__main__':
  main( sys.argv )
