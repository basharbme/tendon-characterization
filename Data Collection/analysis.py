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
    high = 1
    cur_plateau = False

    # loop through all points
    while high < len(data):
        # calculate slope between two consecutive points
        slope = abs( data[high] - data[high-1] )
        # print slope
        # if slope is flat enough, that is a plateau
        if slope <= 0.2 and cur_plateau == False:
            low = high-1
            cur_plateau = True
        # if slope becomes too large, plateau ends. find and record plateau average.
        elif slope > 0.2 and cur_plateau == True and (high-low) > 100:
            avg = sum( data[low:high-1] )/len( data[low:high-1] )

            print avg

            # check if current plateau is too similar to last plateau (accounts for noise)
            if len(plats) > 0 and abs(avg - plats[-1]) < 0.3:

                print avg,plats[-1]

                avg = (avg + plats[-1])/2
                plats[-1] = avg
            else:
                plats.append(avg)
            cur_plateau = False
            low = high

        # increment end index
        high += 1


    # start = 0
    # end = 99
    #
    # while end < len(data):
    #     avg = sum( data[start:end] )/len( data[start:end] )
    #     close = [ ( abs(avg-x) < 0.2 ) for x in data[start:end] ]
    #     if all(close):
    #         plats.append(avg)
    #         start = end + 1
    #         end += 100
    #     end += 1
    #     start += 1

    return plats


# Takes in 2 lists of data (independent & dependent variables) and plots them
# if only one list is given, it is plotted as the dependent variable with index
# as independent variable.
def plotData( dep, indep = [] ):
    if indep == []:
        plt.plot(dep, 'bo')
    else:
        if len(indep) != len(dep):
            print 'Inputs are not equal lengths. X has length ', len(indep) , \
            ' and Y has length ' , len(dep)
            return
        plt.plot(indep, dep, 'bo')
    plt.show()


if __name__ == '__main__':
    forces = collection.readLength(sys.argv[1])
    plats = getPlateaus( forces )
    print plats
    print len(plats)

    plotData(forces)
