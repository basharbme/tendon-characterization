# tendonStiffness.py : A computational model that predicts the stiffness
# of a 3D printed sheet tendon as a function of average cross-sectional 
# area and rest length, and visualizes this relationship with matplotlib.
#
# Caitrin Eaton
# 13 January 2018

import sys
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

def responseSurface( e=6.0 ):
	'''Generate a stiffness response surface by modeling sheet tendons with a 
	range of cross-sectional areas and rest lengths, given a constant
	elastic modulus (e) in MPa.'''
	
	eSI = e * 10.0**6 		# MEGA Pascals! In SI units, 1 MPa = 1,000,000 N / 1 m**2
	ecm = eSI / 100.0**2	# converted into N/cm**2
	
	# Independent variables: area (cm^2) and rest length (cm)
	a = np.linspace(0.01, 2.0, num=201)
	l = np.linspace(2.5, 20.1, num=201)
	
	# 2D arrays to aggregate performance metrics
	A, L = np.meshgrid(a, l )										# for plotting in cm
	
	# Dependent variable: stiffness
	# From the equation for Young's Modulus: k = EA/L
	K = ecm * np.divide( A, L )
	K[K>500]=500
	
	# Visualize the response surface
	plt.figure()
	plt.xlabel("Average cross-sectional area (cm^2)")
	plt.ylabel("Rest length (cm)")
	#plt.title("Tendon stiffness (N/cm)\nE = {0:4.2f} MPa".format(e))
	plt.title("E = {0:4.2f} MPa".format(e))
	levels=np.linspace(0,500,11)
	contourK = plt.contourf( A, L, K, levels )
	plt.colorbar( contourK )
	
	# Highlight predictions with a typical printed tendons' rest length
	# of approximately 10 cm. (Typical in our Summer 2018 experiments).
	l10 = 10.0 * np.ones( l.shape )
	plt.plot( a, l10, '--c', label="L=10.0 cm" )
	#plt.legend()	
	

def main():
	'''Generate response surfaces for both the filament manufacturer's
	reported elastic modulus (12.0 MPa) and the empirically derived
	printed tendon elastic modulus (6.0 MPa).'''

	# Pull empirical data from CSV
	empiricalData = np.genfromtxt("../Plotting/aggregate.csv", delimiter=',', autostrip=True, skip_header=1)
	empiricalStiffness = empiricalData[:,1]
	empiricalVolume = empiricalData[:, 2]
	empiricalDensity = empiricalData[:,3]
	empiricalCSA = empiricalData[:,5]
	pocketType = empiricalData[:,6] # 0=solid, 1=square, 2=circle
	thickness = empiricalData[:,7]	# in mm, not in cm!
	solidRows = pocketType==0
	squareRows = pocketType==1
	circleRows = pocketType==2
	mm1Rows = thickness==1
	mm2Rows = thickness==2
	mm3Rows = thickness==3

	# Create a figure window to illustrate traces for stiffnesses at 9.72 cm rest lengths
	a   = np.linspace(0.01, 0.75, num=75)
	plt.figure()
	plt.xlabel("Average cross-sectional area (cm^2)")
	plt.ylabel("Stiffness (N/cm)")
	#plt.title("Tendon stiffness (N/cm)")	

	# Plot empirical data from printed tendon experiments
	for i in range(max(empiricalData.shape)):
		color = ""
		if solidRows[i]:
			color += "x"
		elif circleRows[i]:
			color += "o"
		else:
			color += "s"
		if thickness[i] == 1:
			color += "k"
		elif thickness[i] == 2:
			color += "g"
		else:
			color += "b"
		plt.plot(empiricalCSA[i], empiricalStiffness[i], color, markerfacecolor="w")

	# Linear regression of the empirical data from printed tendon experiments
	slope, intercept, r_value, p_value, std_err = stats.linregress(empiricalCSA, empiricalStiffness)
	L_rest = 0.0972
	E6 = slope * L_rest
	rmse = (np.sum(np.mean(np.square(empiricalStiffness - slope*empiricalCSA+intercept))))**0.5
	rsqLinear   = r_value**2
	print( "slope =", slope, "MPa/cm" )
	print( "intercept =", intercept, "N/cm" )
	print( "rmse =", rmse )
	print( "R^2 =", rsqLinear )
	print( "Regression's E =", E6, "MPa" )
	kFit = slope * a + intercept
	
	# Plot just the 9.72 cm rest length predictions for the empirical and 
	# manufacturer's elastic moduli
	k6  =   E6 * 10.0**6 / 100.0**2 * np.divide( a, 10.0 )
	k12 = 12.0 * 10.0**6 / 100.0**2 * np.divide( a, 10.0 )

	# Plot the 10 cm rest length predictions
	plt.plot( a, k12, '-', label="E = 12.0 MPa" )
	plt.plot( a, k6,  '-', label="E = {0:3.1f} MPa".format(E6) )
	# When including the outlier with stiffness > 50, the Y-intercept becomes noticeably negative:
	#plt.plot( a, k6,  '-', label="E = {0:3.1f} MPa, intercept 0 N/cm".format(E6) )
	#plt.plot( a, kFit, '--', label="E = {0:3.1f} MPa, intercept {1:3.1f} N/cm".format(E6, intercept) )

	plt.legend()
		
	
	# Create a figure window to illustrate stiffness as a function of density
	rhoN = empiricalData[empiricalData[:,6]==0,3]
	rhoS = empiricalData[empiricalData[:,6]==1,3]
	rhoC = empiricalData[empiricalData[:,6]==2,3]
	kN = empiricalStiffness[empiricalData[:,6]==0]
	kS = empiricalStiffness[empiricalData[:,6]==1]
	kC = empiricalStiffness[empiricalData[:,6]==2]
	plt.figure()
	plt.xlabel("Density (% solid volume)")
	plt.ylabel("Stiffness (N/cm)")
	for i in range(max(empiricalData.shape)):
		color = ""
		if solidRows[i]:
			color += "x"
		elif circleRows[i]:
			color += "o"
		else:
			color += "s"
		if thickness[i] == 1:
			color += "k"
		elif thickness[i] == 2:
			color += "g"
		else:
			color += "b"
		plt.plot(empiricalDensity[i], empiricalStiffness[i], color, markerfacecolor="w")
	
	# Linear regression by thickness
	rho   = np.linspace(50, 110, num=51)
	slope1mm, intercept1mm, r_value, p_value, std_err = stats.linregress(empiricalDensity[mm1Rows], empiricalStiffness[mm1Rows])
	slope2mm, intercept2mm, r_value, p_value, std_err = stats.linregress(empiricalDensity[mm2Rows], empiricalStiffness[mm2Rows])
	slope3mm, intercept3mm, r_value, p_value, std_err = stats.linregress(empiricalDensity[mm3Rows], empiricalStiffness[mm3Rows])
	plt.plot( rho, rho*slope1mm + intercept1mm, '--k', label="1 mm thick: k = {0:3.1f}*density + {1:3.1f}".format(slope1mm, intercept1mm))
	plt.plot( rho, rho*slope2mm + intercept2mm, '--g', label="2 mm thick: k = {0:3.1f}*density + {1:3.1f}".format(slope2mm, intercept2mm))
	plt.plot( rho, rho*slope3mm + intercept3mm, '--b', label="3 mm thick: k = {0:3.1f}*density + {1:3.1f}".format(slope3mm, intercept3mm))
	plt.legend()

	# Generate response surfaces for manufacturer's reported and empirically derived elastic moduli
	responseSurface( 12.0 )
	responseSurface( E6 )

	plt.show()
	
	
if __name__=="__main__":
	main()
		

