# Riley Karp
# C3PO
# Created 6/25/2018
# collection.py

import numpy as np
import cv2 as cv
import sys
import csv
import random

# This method does nothing. It just needs to be passed to the createTrackbar()
# method in getLength()
def nothing(x):
    pass


# Takes in initial measured length between the blue tape markers
# Creates a video capture frame, detects the two blue markers,
# calculates the distance between the markers in each frame, and returns a list
# of the lengths. Starts calculating lengths when the toggle switch at the top
# of the window is turned on (set to 1). Video capture ends when 'q' is pressed.
# When 's' is pressed, program ends after saveing the lengths as a CSV file with
# filename 'serialNumber_length.csv', where the serial number is given in terminal
# window when prompted. Returns a list of the collected lengths.
def getLength( measured_length ):

    '''Initialize video capture and intial lengths'''
    cap = cv.VideoCapture(0)
    len0 = float(measured_length) #original length in cm
    dist0 = None #original pixel distance
    lengths = []


    '''Create Toggle Switch To Record Length'''
    cv.namedWindow('original')
    switch = '0 : OFF , 1 : ON'
    cv.createTrackbar(switch, 'original',0,1,nothing)


    '''Find the 2 markers & calculate length between them in each frame'''
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:

            '''Find all blue contours in the frame'''
            # set region of interest (ROI) to middle rectangle of 400x200 pixels
            height = frame.shape[0]
            width = frame.shape[1]
            ROI = frame[ (height/2)-200:(height/2)+200 , (width/2)-100:(width/2)+100 ]

            # modify ROI and add to frame
            blurred = cv.GaussianBlur(ROI,(5,5),0)
            hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
            frame[ (height/2)-200:(height/2)+200 , (width/2)-100:(width/2)+100 ] = hsv

            # HSV Thresholds to identify blue chroma tape
            lower_blue_tape = np.array([110,20,20])
            upper_blue_tape = np.array([120,235,235])

            # create mask of all blue spots in the ROI & remove noise
            mask = cv.inRange(hsv, lower_blue_tape, upper_blue_tape)
            mask = cv.erode(mask, None, iterations=3)
            mask = cv.dilate(mask, None, iterations=3)

        	# find contours in the mask of identified blue spots in ROI
            conts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            conts = conts[1]


            '''Find and track the 2 markers'''
        	# only proceed if at least two blue contours were found
            if len(conts) > 1:

        		# find the 2 largest blue contours in the ROI
                conts.sort(key=cv.contourArea)
                box1 = conts[-1]
                box2 = conts[-2]

                # create bounding rectangles and centroids around the 2 largest contours
                x1,y1,h1,w1 = cv.boundingRect(box1)
                x2,y2,h2,w2 = cv.boundingRect(box2)

                center1 = ( x1+(h1/2) , y1+(w1/2) )
                center2 = ( x2+(h2/2) , y2+(w2/2) )


        		# only proceed and draw the rectangles if they arae a specified size
                '''May need to adjust sizes in if statement based on experimental setup.
                Adjust by printing h1,h2,w1,w2 to find desired contour sizes.
                Some commonly used boundaries can be seen commented out below'''
                # print h1,h2,w1,w2
                # if h1>25 and h2>25 and w1>8 and w2>8: # sheet tendon size
                if 20<h1<50 and 20<h2<50 and 10<w1<30 and 10<w2<30: # ribbon clamp size
                # if 5<h1<18 and 5<h2<18 and 5<w1<18 and 5<w2<18: # filament size
                # if 5<h1<20 and 5<h2<20 and 5<w1<20 and 5<w2<20: # wedge grip size
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
                    # and less than 16cm (max is usually no higher than ~14.5cm)
                    # these bounds account for some noise
                    if (len0-1) < length < 16:
                        lengths.append(length)

            '''Display frames'''
            cv.imshow('mask',mask) # black and white showing all blue items in ROI
            cv.imshow('original', frame)


            '''Quit if q is pressed'''
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            # save and quit if s is pressed
            elif cv.waitKey(1) & 0xFF == ord('s'):
                filename = raw_input('Type tendon serial number here: ')
                save(lengths, filename+'_length')
                break
        else:
            break

    # close all windows and end program
    cap.release()
    cv.destroyAllWindows()

    return lengths


# Takes in a list of data and a filename string and saves the data as a CSV file
# with the given filename.
def save( data, filename, plats = False ):
    file = filename + '.csv'
    f = open( '../Data/'+file, 'wb' )
    writer = csv.writer( f, delimiter=',', quoting=csv.QUOTE_MINIMAL )
    for x in data:
        if plats: # writing force & length plateaus to a file
            writer.writerow(x)
        else: # writing raw length data points to a file
            writer.writerow([x])
    f.close()


# Takes in a CSV filename. Assumes the data is in the form produced by the
# Force Gage, where the first row is the column headers and the forces are in
# the second column, and all negative (tension). Returns a list of the forces.
def readForce( filename ):

    forces = []
    file = open( '../Data/'+filename, 'rU' )
    rows = csv.reader(file)
    next(rows,None) # skip row of column headers
    for row in rows:
        if row[1] != '': # if there is a force value recorded in the row
            forces.append( float(row[1])*-1 )
    file.close()

    return forces


# Takes in a CSV filename. Assumes the data is in the form produced by the
# getLength method, where the file only contains one column (of lengths)
# Returns a list of the lengths.
def readLength( filename ):

    lengths = []
    file = open( '../Data/'+filename, 'rU' )
    rows = csv.reader(file)
    for row in rows:
        lengths.append( float(row[0]) )
    file.close()

    return lengths


# Randomly generate and return a list of floats >= the given minimum value and
# less than 150% of the minimum value.
# List length is given by the numLengths field.
# Ensures the difference between consecutive lengths is at least 0.5 to aid in
# plateau identification.
def randLengths( min, numLengths ):
    lens = [min]
    while len(lens) < numLengths:
        new = round( random.uniform(min, min+(0.5*min)) , 1 )
        if abs(new - lens[-1]) > 0.5:
            lens.append( new )
    return lens


# Print random lengths then open computer vision window
if __name__ == '__main__':
    print randLengths( float(sys.argv[1]), 11 )
    getLength( sys.argv[1] )
