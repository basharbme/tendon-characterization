# Riley Karp
# C3PO
# Created 6/25/2018
# collection.py

import numpy as np
import cv2 as cv
import sys

# This method does nothing. It just needs to be passed to the createTrackbar()
# method in getLength()
def nothing(x):
    pass


# Takes in initial measured length between the markers
# Creates a video capture frame, detects the two blue markers,
# calculates the distance between the markers in each frame, and returns a list
# of the lengths. Starts calculating lengths when the toggle switch at the top
# of the window is turned on (set to 1). Video capture ends when q is pressed.
# Returns a list of the collected lengths.
def getLength( measured_length ):

    '''Initialize video capture and intial lengths'''
    cap = cv.VideoCapture(0)
    len0 = float(measured_length) #original length in mm
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
                '''May need to adjust sizes in if statement based on experimental setup'''
                if h1>5 and h2>5 and w1<30 and w2<30 and h1<20 and h2<20:
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


            '''Display frames'''
            cv.imshow('mask',mask)
            cv.imshow('original', frame)


            '''Quit if q is pressed'''
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv.destroyAllWindows()

    return lengths


if __name__ == '__main__':
    getLength( sys.argv[1] )
