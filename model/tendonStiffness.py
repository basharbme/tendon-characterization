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
	plt.title("Tendon stiffness (N/cm)\nE = {0:4.2f} MPa".format(e))
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
	
	responseSurface( 12.0 )
	responseSurface( 6.4 )	

	# Plot just the 10 cm rest length predictions for the empirical and 
	# manufacturer's elastic moduli
	a   = np.linspace(0.01, 1.0, num=201)
	k6  =  6.4 * 10.0**6 / 100.0**2 * np.divide( a, 10.0 )
	k12 = 12.0 * 10.0**6 / 100.0**2 * np.divide( a, 10.0 )
	plt.figure()
	plt.xlabel("Average cross-sectional area (cm^2)")
	plt.ylabel("Stiffness (N/cm)")
	plt.title("Tendon stiffness (N/cm)")	

	# Plot empirical data from printed tendon experiments
	empiricalData = np.genfromtxt("../Plotting/aggregate.csv", delimiter=',', autostrip=True, skip_header=1)
	empiricalCSA = empiricalData[:,5]
	empiricalStiffness = empiricalData[:,1]
	plt.plot( empiricalCSA, empiricalStiffness, '.k')

	# Linear regression of the empirical data from printed tendon experiments
	slope, intercept, r_value, p_value, std_err = stats.linregress(empiricalCSA, empiricalStiffness)
	rmse = (np.sum(np.mean(np.square(empiricalStiffness - slope*empiricalCSA+intercept))))**0.5
	rsqLinear   = r_value**2
	print( "slope =", slope/10.0, "MPa" )
	print( "intercept =", intercept, "N/cm" )
	print( "rmse =", rmse )
	print( "R^2 =", rsqLinear )
	kFit = slope * a + intercept
	plt.plot( a, kFit, '--', label="E = {0:2.1f} MPa".format(slope/10.0) )

	# Plot the 10 cm rest length predictions
	plt.plot( a, k12, '-', label="E = 12.0 MPa" )
	plt.plot( a, k6,  '-', label="E = 6.0 MPa" )

	plt.legend()
	plt.show()
	
	
if __name__=="__main__":
	main()
		

