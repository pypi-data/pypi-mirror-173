"""
Name: Jason Saladiner Jr.
Date Created: 04/28/2022
Last Updated: 04/28/2022
Package Summary: 
	This package serves as a repository of fundamental relations found throughout Aerospace Engineering
Included Functions/Submodules:
	.Isentropic
	.Shock
"""



def Astar_A(As_A = None,Mach = None,gamma = 1.4):
	"""
	The relationship between dynamic to static pressure and Mach
	Pass None as variable of Interest
	Returns tuple of Machs. One sonic, One supersonic
	"""
	import sys
	from math import pow,log
	
	pop = As_A
	
	#Check inputs
	if (pop == None and Mach == None) or (pop !=None and Mach != None):
		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
	try:
		log(gamma-1)
	except:
		sys.exit("Gamma must be a real number greater than 1")
	
	#if pop is variable of interest
	if pop == None:
		return pow((gamma+1)/2,(gamma+1)/(2*gamma-2))*Mach*pow(1+(gamma-1)/2*Mach**2,(gamma+1)/(2-2*gamma))

	elif Mach == None:
		from scipy.optimize import newton
		C = pow((gamma+1)/2,(gamma+1)/(2*gamma-2))
		E = - (gamma+1) / (2*gamma - 2)

		f = lambda M: C*M*pow(1+(gamma-1)/2 * pow(M,2),E) - pop
		fprime = lambda M: C*pow(1+(gamma-1)/2*pow(M,2),E) + C*E*(gamma-1)*pow(M,2)*pow(1 + (gamma - 1) / 2 *pow(M,2),E-1)
		return newton(f,.5,fprime),newton(f,1.5,fprime)

		
	else:
		sys.exit("Could not find Variable of interest in Relations.Astar_A()")


def V_astar(V_astar = None,Mach=None,gamma = 1.4):
	"""
	The relationship between V/a* and Mach
	Pass None as variable of Interest
	"""
	import sys
	from math import pow,log,sqrt
	
	pop = V_astar
	
	#Check inputs
	if (pop == None and Mach == None) or (pop !=None and Mach != None):
		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
	try:
		log(gamma-1)
	except:
		sys.exit("Gamma must be a real number greater than 1")

	if pop == None:
		vasq = (gamma+1)/2 * Mach**2 * pow(1+(gamma-1)/2 * Mach **2,-1)
		return sqrt(vasq)
	elif Mach == None:
		msq = 2/(gamma+1)*pop**2 * pow(1- (gamma-1)/(gamma+1)*pop**2,-1)
		return sqrt(msq)