Data Collection Instructions
7/3/2018

* See "Methods_Caitrin" in the C3PO Google Team Drive for more detailed instructions *

SETUP
* Attach tendon to the force gage and base using clamps, hooks, etc.
* Make sure blue chroma tape is on each clamp
* Measure the initial distance between clamps where force = 0.

FORCE COLLECTION
* Turn on the force gage then plug it into a computer with the USB cable.
* Open the MESURLite Software on a Windows computer and click connect.
* Adjust values under Settings tab if necessary. I used:
  - Continuous Readings
  - Readings per sec = 10
  - No. of Readings = 5000 (max)
* Under Acquisition:
  - Click Start button when ready to collect force data (after preparing for length collection)

LENGTH COLLECTION
* Run collection.py with the initial inter-clamp distance as a command line argument
* Write down the list of 11 numbers that are printed in the terminal.
  - These are the randomly generated lengths at which the tendon should be tested.
* Position the tendon in the red rectangle in the center of the screen.
  - Make sure a green box with a red dot in the middle appears around the blue markers
*Toggle the switch at the top of the Window to 1 (towards the right side)
  to start recording length values. Toggle back to 0 to stop recording values.
* Press q to quit the program.

DATA COLLECTION
* Click Start on the MESURLite Software
* Start length collection by toggling switch to the right in the computer vision window
* Wait for ~45 sec at each plateau before going to the next length from the randomly generated list
* Force collection will stop when it reaches 5000 data points
* Toggle slider in the computer vision window back to the left to stop collecting length data
* Press s to save lengths and quit the program.
  - The window should freeze, then type the tendon serial number in the terminal.
  - This will save the lengths as 'serialNumber_length.csv'
  * To save force data:
    - Click Export to Excel in the MESURLite window
    - Wait for all 5000 data points to load to the Excel file.
    - Save CSV file as 'serialNumber_force.csv'

  DATA ANALYSIS
  * Run analysis.py with the serial number as the command line argument
  * Double check the printed force and length plateaus against the force and length vs. time plots
  * Run driver.py with the serial number as the command line argument
    - This saves the plateaus to 'serialNumber_plats.csv'
    - Edit plateau CSV file if necessary
    - Run driver.py again to read plateaus from the CSV file to plot force vs. length
    - Slope of the force vs. length plot is tendon stiffness
