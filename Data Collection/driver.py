# Riley Karp
# C3PO
# Created 6/29/2018
# driver.py

import collection
import analysis
import sys
import csv


# read force & length csv files, find and save plateaus as csv & plot force v. length
def getPlats( argv ):

    '''Check if given cmd line args'''
    if len(argv) < 2:
        print 'usage: %s <filename>' % (argv[0])
        exit()

    lengths = collection.readLength(argv[1] + '_length.csv')
    forces = collection.readForce(argv[1] + '_force.csv')

    length_plats = analysis.getLengthPlateaus(lengths)
    force_plats = analysis.getForcePlateaus(forces)

    plats = [ ['Force','Length'] ]
    for i in range(len(force_plats)):
        plats.append( [force_plats[i], length_plats[i]] )
    collection.save(plats, argv[1] + '_plats', plats = True)

    analysis.plotData(force_plats,length_plats)


def readPlats( argv ):
    filename = argv[1] + '_plats.csv'
    force_plats = []
    length_plats = []
    file = open( '../Data/'+filename, 'rU' )
    rows = csv.reader(file)
    next(rows,None)
    for row in rows:
        force_plats.append( float(row[0]) )
        length_plats.append( float(row[1]) )
    file.close()

    analysis.plotData(force_plats,length_plats)


if __name__ == '__main__':
  readPlats(sys.argv)
