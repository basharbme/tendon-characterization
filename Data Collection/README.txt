Data Collection Instructions
6/28/2018

SETUP
* Put 2 pieces of blue chroma tape on the tendon & measure the length between them.
* Attach tendon to the force gage and base using clamps, hooks, etc.
* Open the MESURLite force collection software and video capture program in collection.py

FORCE COLLECTION
* Turn on the force gage then plug it into a computer with the USB cable.
* Open the MESURLite Software on a Windows computer and click connect.
* Settings:
  - Continuous Readings
  - Readings per sec = 10
  - No. of Readings = 5000 (max)
* Acquisition:
  - Click Start button
  - Stretch tendon, waiting for ____sec at each plateau
  - Click Stop if you want to end data collection before it reaches 5000 data points
* Export to Excel. Save as CSV file for use with driver.py
* Use getForce() method in collection.py to return a list of the force values.
  - Run driver.py with command line arguments 'force' and the CSV filename with the force data

LENGTH COLLECTION
* Use the getLength() method in collection.py to return a list of length values.
  - Run driver.py with command line arguments 'length' and initial measured length.
  - Position the tendon in the colored rectangle in the center of the screen.
  - Toggle the switch at the top of the Window to 1 (towards the right side)
  to start recording length values.
  - Press q to quit the program.
