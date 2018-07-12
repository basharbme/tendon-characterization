# Riley Karp
# C3PO
# Created 6/29/2018
# driver.py

import collection
import analysis
import sys

def main( argv ):

    '''Check if given cmd line args'''
    if len(argv) < 2:
        print 'usage: %s <filename>' % (argv[0])
        exit()

    lengths = collection.readLength(argv[1] + '_length.csv')
    forces = collection.readForce(argv[1] + '_force.csv')

    length_plats = analysis.getLengthPlateaus(lengths)
    force_plats = analysis.getForcePlateaus(forces)

    print 'length plats: ' , length_plats, len(length_plats)
    print 'force plats: ' , force_plats, len(force_plats)

    analysis.plotData(force_plats,length_plats)


if __name__ == '__main__':
  main(sys.argv)
