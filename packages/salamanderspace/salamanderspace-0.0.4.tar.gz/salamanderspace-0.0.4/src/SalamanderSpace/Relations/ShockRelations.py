"""
Name: Jason Saladiner Jr.
Date Created: 04/28/2022
Last Updated: 04/28/2022
Purpose: Act as a repository for Shock relations
General Assumptions:
	Attatched Shocks
	Steady Flow
	Adiabatic Flow
Included Functions:
	
"""




def prandtlmeyer(nu=None,Mach=None,gamma=1.4):
	"""
	The relationship between prandl-Meyer angle and mach
	Pass None as variable of Interest
	Returns tuple of Machs. One sonic, One supersonic
	"""
	import sys
	from math import pow,log,sqrt,atan,pi,tan
	
	pop = nu
	
	#Check inputs
	if (pop == None and Mach == None) or (pop !=None and Mach != None):
		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
	try:
		log(gamma-1)
	except:
		sys.exit("Gamma must be a real number greater than 1")

	if pop == None:
		return (sqrt((gamma+1)/(gamma-1))*atan(sqrt((gamma-1)/(gamma+1)*(Mach**2 - 1)))-atan(sqrt(Mach**2 - 1)))*180/pi
	elif Mach == None:
		pop = pop
		
		C = sqrt((gamma-1)/(gamma+1))
		#Hall Relation
		f = lambda B : tan(C*(pop+atan(B)*180/pi)*pi/180)/C - B
		fprime = lambda B : -(1- C**2)*B**2 / (1 + B**2)
		
		from scipy.optimize import newton
		beta = newton(f,1.3,fprime)
		return sqrt(beta**2+1)


def prandtlequation(nu1=None,nu2=None,delta=None,gamma=1.4):
	"""
	needs docstring
	Needs to be generalized for starting not at delta1 = 0

	"""
	import sys
	from math import pow,log,sqrt,atan,pi,tan
	

	cNone = [nu1,nu2,delta].count(None)
	
	if cNone != 1:
		sys.exit("Incorrect number of None Variables in SalamanderSpace.Relations.Dimensionless.Mach. Make sure to pass only one None for variable of interest")


	if nu1 == None:
		return nu2+delta
	elif nu2 == None:
		return nu1-delta
	elif delta ==None:
		return -(nu2-nu1)





def mach2(Mach1=None,Mach2= None,gamma = 1.4):
	"""
	The relationship between mach1 and mach2 across normal shock
	Pass None as variable of Interest
	"""
	import sys
	from math import pow,log,sqrt,atan,pi
	x = Mach1
	pop = Mach2
	
	#Check inputs
	if (pop == None and x == None) or (pop !=None and x != None):
		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
	try:
		log(gamma-1)
	except:
		sys.exit("Gamma must be a real number greater than 1")

	if pop == None:
		return sqrt((2+(gamma-1)*x**2)/(2*gamma*x**2 - (gamma-1)))
	elif x == None:
		return sqrt((2+(gamma-1)*pop**2)/(2*gamma*pop**2 - (gamma-1)))

def densityRatio(Mach1 = None,Rho2ToRho1 = None,gamma = 1.4):
	"""
	The relationship between rho2/rho1 to mach1 across normal shock
	Pass None as variable of Interest
	"""
	import sys
	from math import pow,log,sqrt,atan,pi
	
	pop = Rho2ToRho1
	x = Mach1
	#Check inputs
	if (pop == None and x == None) or (pop !=None and x != None):
		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
	try:
		log(gamma-1)
	except:
		sys.exit("Gamma must be a real number greater than 1")

	if pop == None:
		return (gamma+1)*x**2 / (2 + (gamma-1)*x**2)
	elif x == None:
		return sqrt((2*pop )/( (gamma+1) - pop*(gamma-1)) )

def pressureRatio(Mach1 = None,P2ToP1 = None,gamma = 1.4):
	"""
	The relationship between p2/p1 to mach1 across normal shock
	Pass None as variable of Interest
	"""
	import sys
	from math import pow,log,sqrt,atan,pi
	
	pop = P2ToP1
	x = Mach1
	#Check inputs
	if (pop == None and x == None) or (pop !=None and x != None):
		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
	try:
		log(gamma-1)
	except:
		sys.exit("Gamma must be a real number greater than 1")

	if pop == None:
		return 1 + (2*gamma) / (gamma + 1) * (x**2 - 1)
	elif x == None:
		return sqrt( (pop-1)*(gamma+1)/(2*gamma) + 1 )

def temperatureRatio(Mach1 = None,T2ToT1 = None,gamma = 1.4):
	"""
	The relationship between T2/T1 to mach1 across normal shock
	Pass None as variable of Interest
	"""
	import sys
	from math import pow,log,sqrt,atan,pi
	
	pop = T2ToT1
	x = Mach1
	#Check inputs
	if (pop == None and x == None) or (pop !=None and x != None):
		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
	try:
		log(gamma-1)
	except:
		sys.exit("Gamma must be a real number greater than 1")


	C = 2*(gamma-1)*pow(gamma+1,-2)
	if pop == None:
		return 1 + C*pow(x,-2)*(x**2-1)*(gamma*x**2+1)
	elif x == None:
		f = lambda m2 : (1-pop)*m2 + C*(m2-1)*(gamma*m2 + 1)
		fprime = lambda m2 : (1-pop) + C*(2*gamma*m2 - (gamma-1))
		from scipy.optimize import newton
		m2 = newton(f,1.1,fprime)
		return sqrt(m2)


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

####Last Column. Finding Mach from P02ToP1 is hard. Needs to be figured out####
#def RayleighPitot(Mach1 = None,P02ToP1 = None,gamma = 1.4):
#	"""
#	The relationship between P02/P1 to mach1 across normal shock
#	Used for Pitot tubes only
#	Pass None as variable of Interest
#	"""
#	import sys
#	from math import pow,log,sqrt,atan,pi
	
#	pop = P02ToP1
#	x = Mach1
#	#Check inputs
#	if (pop == None and x == None) or (pop !=None and x != None):
#		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
#	try:
#		log(gamma-1)
#	except:
#		sys.exit("Gamma must be a real number greater than 1")


#	C = pow((gamma+1)/2,gamma/(gamma-1))
#	G = lambda b : 2*gamma / (gamma + 1) * pow(b,1-gamma) - (gamma-1)/(gamma+1)*pow(b,-gamma)
#	if pop == None:
#		return C*pow(G(x**2),-1/(gamma-1))
#	elif x == None:
#		f = lambda B: C*pow(G(B),-1/(gamma-1)) - pop
#		fprime = lambda B: C*(gamma/(gamma+1) * (2*pow(B,-gamma) + pow(B,-gamma-1)) * pow(G(B),-gamma))
		
#		print(G(.1))
#		print(f(.1))
#		print(fprime(.1))
#		from scipy.optimize import newton
#		beta = newton(f,15,disp = True)
#		return sqrt(beta)