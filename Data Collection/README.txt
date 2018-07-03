Data Collection Instructions
7/3/2018

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
  - Stretch tendon, waiting for __(TBD)__ sec at each plateau
  - Click Stop if you want to end data collection before it reaches 5000 data points
* Export to Excel. Save as CSV file for use with driver.py

LENGTH COLLECTION
* Run driver.py to use the getLength() method in collection.py to return a list of length values.
  - Position the tendon in the colored rectangle in the center of the screen.
  - Toggle the switch at the top of the Window to 1 (towards the right side)
  to start recording length values.
  - Press q to quit the program.
  - Press s to save lengths and quit the program.
