# Riley Karp
# C3PO
# Created 6/29/2018
# driver.py

import compVision
import sys

def main( argv ):

    '''Check if given cmd line args'''
    if len(argv) < 3:
        print 'usage: %s <length or force> <length in mm or filename' % (argv[0])
        exit()

    if argv[1] == 'length':
        return compVision.getLength(argv[2])
    elif argv[1] == 'force':
        return compVision.getForce(argv[2])
    else:
        print 'usage: %s <length or force> <length in mm or filename' % (argv[0])


if __name__ == '__main__':
  main(sys.argv)
