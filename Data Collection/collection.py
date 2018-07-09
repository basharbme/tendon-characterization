# Riley Karp
# C3PO
# Created 6/25/2018
# collection.py

import numpy as np
import cv2 as cv
import sys
import csv
import time

# This method does nothing. It just needs to be passed to the createTrackbar()
# method in getLength()
def nothing(x):
    pass


# Takes in initial measured length between the markers
# Creates a video capture frame, detects the two blue markers,
# calculates the distance between the markers in each frame, and returns a list
# of the lengths. Starts calculating lengths when the toggle switch at the top
# of the window is turned on (set to 1). Video capture ends when 'q' is pressed.
# When 's' is pressed, saves the lengths as a CSV file with filename given as
# raw input in command line, then ends the program.
# Returns a list of the collected lengths.
def getLength( measured_length ):

    '''Initialize video capture and intial lengths'''
    cap = cv.VideoCapture(0)
    len0 = float(measured_length) #original length in cm
    dist0 = None #original pixel distance
    lengths = []
    # t0 = 0
    # times = []


    '''Create Toggle Switch To Record Length'''
    cv.namedWindow('original')
    switch = '0 : OFF , 1 : ON'
    cv.createTrackbar(switch, 'original',0,1,nothing)


    '''Find the 2 markers & calculate length between them in each frame'''
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:

            '''Find all blue contours in the frame'''
            # set ROI to middle rectangle of 400x200 pixels
            height = frame.shape[0]
            width = frame.shape[1]
            ROI = frame[ (height/2)-200:(height/2)+200 , (width/2)-100:(width/2)+100 ]

            # modify ROI and add to frame
            blurred = cv.GaussianBlur(ROI,(5,5),0)
            hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
            frame[ (height/2)-200:(height/2)+200 , (width/2)-100:(width/2)+100 ] = hsv

            # HSV Thresholds
            lower_blue_tape = np.array([105,0,0])
            upper_blue_tape = np.array([125,255,255])

            # create mask & remove noise
            mask = cv.inRange(hsv, lower_blue_tape, upper_blue_tape)
            mask = cv.erode(mask, None, iterations=3)
            mask = cv.dilate(mask, None, iterations=3)

        	# find contours in the mask
            conts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            conts = conts[1]


            '''Find and track the 2 markers'''
        	# only proceed if at least two contours were found
            if len(conts) > 1:

        		# find the 2 largest contours in the mask
                conts.sort(key=cv.contourArea)
                box1 = conts[-1]
                box2 = conts[-2]

                # create bounding rectangles and centroids
                x1,y1,h1,w1 = cv.boundingRect(box1)
                x2,y2,h2,w2 = cv.boundingRect(box2)

                center1 = ( x1+(h1/2) , y1+(w1/2) )
                center2 = ( x2+(h2/2) , y2+(w2/2) )


        		# only proceed if the rectangles meet a minimum size
                '''May need to adjust sizes in if statement based on experimental setup.
                Adjust by printing h1,h2,w1,w2 to find desired contour sizes.'''
                # print h1,h2,w1,w2
                if h1>25 and h2>25 and w1>8 and w2>8:
        			# draw the rectangles and centroids on the frame
                    cv.rectangle( ROI, (int(x1),int(y1)), (int(x1+h1),int(y1+w1)), (0, 255, 0), 1 )
                    cv.circle( ROI, center1, 5, (0, 0, 255), -1)

                    cv.rectangle( ROI, (int(x2),int(y2)), (int(x2+h2),int(y2+w2)), (0, 255, 0), 1 )
                    cv.circle( ROI, center2, 5, (0, 0, 255), -1)


                '''Find the vertical distance between the 2 markers'''
                on = cv.getTrackbarPos(switch,'original')
                if on == 1:
                    # find the pixel distance between the inner edges of the 2 rectangles
                    pix = abs( max(y1,y2) - min(y1+w1,y2+w2) )

                    # instantiate dist0 if it's the first measurement frame
                    if dist0 == None:
                        dist0 = pix

                    # calculate actual length using initial measured lengths
                    length = pix * len0 / dist0
                    print length
                    # only record length if it's greater than the starting length
                    # this accounts for some noise
                    if length > (len0-1):
                        lengths.append(length)


            # curTime = time.time()*1000
            # dif = curTime - t0
            # t0 = curTime
            # times.append(dif)
            # print dif

            '''Display frames'''
            cv.imshow('mask',mask)
            cv.imshow('original', frame)


            '''Quit if q is pressed'''
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv.waitKey(1) & 0xFF == ord('s'):
                filename = raw_input('Save lengths as: ')
                save(lengths, filename)
                break
        else:
            break

    cap.release()
    cv.destroyAllWindows()

    # times = times[1:]
    # print 'max: ' , max(times) , ', min: ' , min(times) , ', avg: ' , sum(times)/len(times)

    return lengths


# Takes in a list of data and a filename string and saves the data as a CSV file
# with the given filename.
def save( data, filename ):
    file = filename + '.csv'
    f = open( '../Data/'+file, 'wb' )
    writer = csv.writer( f, delimiter=',', quoting=csv.QUOTE_MINIMAL )
    for x in data:
        writer.writerow([x])
    f.close()


# Takes in a CSV filename. Assumes the data is in the form produced by the
# Force Gage, where the first row is the column headers and the forces are in
# the second column. Returns a list of the forces.
def readForce( filename ):

    forces = []
    file = open( '../Data/'+filename, 'rU' )
    rows = csv.reader(file)
    next(rows,None)
    for row in rows:
        forces.append( float(row[1])*-1 )
    file.close()

    return forces


# Takes in a CSV filename. Assumes the data is in the form produced by the
# getLength method, where the file only contains one column of lengths
# Returns a list of the lengths.
def readLength( filename ):

    lengths = []
    file = open( '../Data/'+filename, 'rU' )
    rows = csv.reader(file)
    for row in rows:
        lengths.append( float(row[0]) )
    file.close()

    return lengths


if __name__ == '__main__':
    getLength( sys.argv[1] )
