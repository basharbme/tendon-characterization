# Riley Karp
# C3PO
# Created 6/29/2018
# driver.py

import collection
import analysis
import sys
import csv
import os.path


def readPlats( filename ):
    force_plats = []
    length_plats = []
    file = open( filename, 'rU' )
    rows = csv.reader(file)
    next(rows,None)
    for row in rows:
        force_plats.append( float(row[0]) )
        length_plats.append( float(row[1]) )
    file.close()

    return force_plats,length_plats


def getWork( forces, lengths ):
    # len_stretch, len_relax, force_stretch, force_relax = analysis.getStretchRelax(lengths, forces)
    # stretch = analysis.integrate(force_stretch,len_stretch)
    # relax = analysis.integrate(force_relax,len_relax)
    peak = forces.index(max(forces))
    stretch = analysis.integrate(forces[:peak+1],lengths[:peak+1])
    relax = analysis.integrate(forces[peak:]+[forces[0]],lengths[peak:]+[lengths[0]])
    return stretch, relax


# read force & length csv files, find and save plateaus as csv & plot force v. length
def getPlats( argv ):
    '''Check if given cmd line args'''
    if len(argv) < 2:
        print 'usage: %s <filename>' % (argv[0])
        exit()

    if os.path.isfile('../Data/' + argv[1] + '_plats.csv'):
        print 'reading'
        force_plats,length_plats = readPlats('../Data/' + argv[1] + '_plats.csv')

    else:
        print 'calculating'
        lengths = collection.readLength(argv[1] + '_length.csv')
        forces = collection.readForce(argv[1] + '_force.csv')

        length_plats = analysis.getLengthPlateaus(lengths)
        force_plats = analysis.getForcePlateaus(forces)

        plats = [ ['Force','Length'] ]
        for i in range(len(force_plats)):
            plats.append( [force_plats[i], length_plats[i]] )
        collection.save(plats, argv[1] + '_plats', plats = True)

    return force_plats,length_plats


def main( force_plats, length_plats ):
    stretch, relax = getWork(force_plats,length_plats)
    print 'Stretch: ' , stretch , 'J'
    print 'Relax: ' , relax , 'J'
    print 'Efficiency: ' , (relax/stretch)*100 , '%'
    analysis.plotData(force_plats,length_plats)


# Takes in filament stiffness, k, in N/cm and length in cm. Returns E in MPa
def elastic_mod(k,length,area):
    # E = k*length/area
    return (k*length) / (area*100)


if __name__ == '__main__':
  # print 'E: '  , elastic_mod(25.167,9.5,0.2*2.54) , ' MPa'
  forces,lengths = getPlats(sys.argv)
  main( forces,lengths )
