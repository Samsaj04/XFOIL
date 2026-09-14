# Code for airfoil geometry generation
# PARSEC - 11 method
# Author: Diego Hidalgo Ph.D.
import numpy as np
import matplotlib.pyplot as plt
from math import floor, log

# ---------------========== PARSEC 11 ===========--------------------
#
#### NOTES #### 
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# INPUT VECTOR FOR PARSEC-11 ROUTINE
#
# # UP---------------------------------
# 	x1 = xa[0] #Rle 		--- Leading edge radius
# 	x2 = xa[1] #Zteup 		--- Trailing edge vertical position
# 	x3 = xa[2] #Xup 		--- Max height x position
# 	x4 = xa[3] #Zup 		--- Max height (+)
# 	x5 = xa[4] #toTeup 		--- theta trailing edge 
# 	x6 = xa[5] #d2dXup 		--- Max curvature 
# # LOW---------------------------------
# 	x7 = xa[6] #Xlow 		--- Max height x position
# 	x8 = xa[7] #Zlow 		--- Max height (-)
# 	x9 = xa[8] #toTelow 	--- theta trailing edge 
# 	x10 = xa[9] #d2dXlow 	--- Max curvature 
# 	x11 = xa[10] #Ztelow 	--- Trailing edge vertical position
# 	x12 = xa[11] #Rlelow 	--- Leading edge radius
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

def parsec(xa,ncx): #ncx -> Number Count of X
	x1 = xa[0]
	x2 = xa[1]
	x3 = xa[2]
	x4 = xa[3]
	x5 = xa[4]
	x6 = xa[5]
 
	x7 = xa[6]
	x8 = xa[7]
	x9 = xa[8]
	x10 = xa[9]
	x11 = xa[10]
	x12 = xa[11]

	# Equations of slide (72)
	Xte = 1.0 				   # Chord lenght (unitary)
	a1up = (2*(x1))**(0.5)     # First alpha term upper surface
	a1low = -(2*(x12))**(0.5)  # First alpha term lower surface
	ncx = int(ncx)

	# Method matrix arragnement in slide 71 of lecture notes.
	# aero_Lab_AFGeometry.pdf

	#  Upper line ----------------------------------------------------
	Aup = np.array( [ 
		[Xte**(3/2),Xte**(5/2),  Xte**(7/2),  Xte**(9/2),  Xte**(11/2)],
		[x3**(3/2) ,x3**(5/2), x3**(7/2), x3**(9/2), x3**(11/2)],
		[(3/2)*Xte**(1/2),(5/2)*Xte**(3/2), (7/2)*Xte**(5/2), (9/2)*Xte**(7/2), (11/2)*Xte**(9/2)],
		[(3/2)*x3**(1/2),(5/2)*x3**(3/2), (7/2)*x3**(5/2), (9/2)*x3**(7/2), (11/2)*x3**(9/2)],
		[(3/4)*x3**(-1/2),(15/4)*x3**(1/2), (35/4)*x3**(3/2), (53/4)*x3**(5/2), (99/4)*x3**(7/2)] 
		] )

	invAup = np.linalg.inv(Aup)

	Bup = np.array([
		[x2 - a1up * (Xte**(1/2))],
		[x4 - a1up * (x3**(1/2))],
		[np.tan(x5) - (1/2) * a1up * (Xte**(-1/2))],
		[(-1/2) * a1up * (x3**(-1/2))],
		[(1/4)* a1up + x6 ]
		])

	alphaup = invAup.dot(Bup) # X = B * A^-1
	alphaup = np.insert(alphaup, 0, np.array([a1up]))

	# print(alphaup)
	#  Lower line ----------------------------------------------------
	Alow = np.array( [ 
		[Xte**(3/2),Xte**(5/2),  Xte**(7/2),  Xte**(9/2),  Xte**(11/2)],
		[x7**(3/2) ,x7**(5/2), x7**(7/2), x7**(9/2), x7**(11/2)],
		[(3/2)*Xte**(1/2),(5/2)*Xte**(3/2), (7/2)*Xte**(5/2), (9/2)*Xte**(7/2), (11/2)*Xte**(9/2)],
		[(3/2)*x7**(1/2),(5/2)*x7**(3/2), (7/2)*x7**(5/2), (9/2)*x7**(7/2), (11/2)*x7**(9/2)],
		[(3/4)*x7**(-1/2),(15/4)*x7**(1/2), (35/4)*x7**(3/2), (53/4)*x7**(5/2), (99/4)*x7**(7/2)] 
		] )

	invAlow = np.linalg.inv(Alow)

	Blow = np.array([
		[x11 - a1low*(Xte**(1/2))],
		[x8 - a1low * (x7**(1/2))],
		[np.tan(x9) - (1/2) * a1low * (Xte**(-1/2))],
		[(-1/2) * a1low * (x7**(-1/2))],
		[(1/4)* a1low + x10 ]
		])

	alphalow = invAlow.dot(Blow)
	alphalow = np.insert(alphalow, 0, np.array([a1low]))

	# nc = 35  # keep odd xc.size
	ang = np.linspace(0,np.pi,ncx)
	xc = 0.5-0.5*np.cos(ang) 

	# Building up the summ equation (slide 70) -----------------------
	Zupper = np.sum([alphaup[i]*xc**(i+1/2) for i in range(6)], axis=0)
	Zlower = np.sum([alphalow[i]*xc**(i+1/2) for i in range(6)], axis=0)

	# Flipping arrays to match airfoil dat file convention -----------
	Zupper = np.flipud(Zupper)
	xcup = np.flipud(xc)
	xclow = xc
	
	# Vector containing the airfoil coordinates -------------------
	Vectout=np.zeros((2*ncx-1,2))

	for i in range(ncx):
		Vectout[i][0]=xcup[i]
		Vectout[i+ncx-1][0]=xclow[i]
		Vectout[i][1]=Zupper[i]
		Vectout[i+ncx-1][1]=Zlower[i] 

	return Vectout, xc, alphaup, alphalow

#-----------------------------------------------------------------
#-----------------------------------------------------------------
# Plot------------------------------------------------------------
def plot_foil(coords):
	fig = plt.figure()
	plt.plot(coords[:,0],coords[:,1],label= 'Xoi')
	plt.scatter(coords[:,0],coords[:,1], color="black", s=5, zorder=10)
	plt.legend()
	plt.grid()

	fig1 = plt.figure()
	plt.plot(coords[:,0],coords[:,1],label= 'Xoi')
	plt.scatter(coords[:,0],coords[:,1], color="black", s=5, zorder=10)
	plt.legend()
	# try using the aspect ratio setting, note that the proportional view 
	# will hide geometry mismatchings, you can use the line below 
	# to check it. The previous figure will help you better by highligting the 
	# geometry behavior.
	plt.gca().set_aspect('equal', 'box') 
	plt.grid()
 
	plt.show()
#-----------------------------------------------------------------
#-----------------------------------------------------------------
# Test geometry NACA 0012-----------------------------------------

# # UP---------------------------------
# 	x1 = xa[0] #Rle 		--- Leading edge radius
# 	x2 = xa[1] #Zteup 		--- Trailing edge vertical position
# 	x3 = xa[2] #Xup 		--- Max height x position
# 	x4 = xa[3] #Zup 		--- Max height
# 	x5 = xa[4] #toTeup 		--- theta trailing edge 
# 	x6 = xa[5] #d2dXup 		--- Max curvature 
# # LOW---------------------------------
# 	x7 = xa[6] #Xlow 		--- Max height x position
# 	x8 = xa[7] #Zlow 		--- Max height (-)
# 	x9 = xa[8] #toTelow 	--- theta trailing edge 
# 	x10 = xa[9] #d2dXlow 	--- Max curvature 
# 	x11 = xa[10] #Ztelow 	--- Trailing edge vertical position
# 	x12 = xa[11] #Rlelow 	--- Leading edge radius
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

def main():
	x0=np.array([ # NACA-0012 representative
	# # Both---------------------------------	
		0.01550,
	# # UP---------------------------------	
		0.0000,
		0.29663,
		0.06002,
		0.00000,
		-0.45150,
	# # LOW---------------------------------	
		0.29663,
		-0.06002,
		0.0000,
		0.45150,
		0.0000,
		0.01550	
		])
 
	# Dfine a number of x points along the chord to generate the geometry.
	ncx = 60; # it has to be integer ----------------int((rows+1)/2)

	coords, xcors, Avals_up, Avals_low = parsec(x0,ncx)
	plot_foil(coords)

	def orderOfMagnitude(number):
		return floor(log(number, 10))

	number = 0.00027
	order = orderOfMagnitude(number)
	print('order', order)

if __name__ == "__main__":
    main()