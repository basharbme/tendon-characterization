# Riley Karp
# C3PO
# Created 6/29/2018
# driver.py

import collection
import analysis
import sys

def main( argv ):

    # '''Check if given cmd line args'''
    # if len(argv) < 3:
    #     print 'usage: %s <length in cm> <force filename' % (argv[0])
    #     exit()
    #
    # lengths = collection.getLength(argv[1])
    # forces = collection.getForce(argv[2])
    #
    # length_plats = analysis.getPlateaus(lengths)
    # force_plats = analysis.getPlateaus(forces)
    #
    # analysis.plotData(force_plats,length_plats)

    '''Check if given cmd line args'''
    if len(argv) < 3:
        print 'usage: %s <length or force> <length in cm or filename' % (argv[0])
        exit()

    if argv[1] == 'length':
        return collection.getLength(argv[2])
    elif argv[1] == 'force':
        return collection.readForce(argv[2])
    else:
        print 'usage: %s <length or force> <length in cm or filename' % (argv[0])


if __name__ == '__main__':
  main(sys.argv)
