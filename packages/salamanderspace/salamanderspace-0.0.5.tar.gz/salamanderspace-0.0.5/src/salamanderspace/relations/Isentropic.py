"""
Name: Jason Saladiner Jr.
Date Created: 04/28/2022
Last Updated: 04/28/2022
Purpose: Act as a repository for Isentropic Relations
General Assumptions:
	Flow is...
	-Steady 
	-Adiabatic
	-Reversible

Included Functions:
	def P0_P(StaticPressureToPressure,Mach,Gamma)
	def den0_den(StaticDensityToDensity,Mach,Gamma)
	def T0_T(StaticTemperatureToTemperature,Mach,Gamma)
"""


def P0_P (StaticPressureToPressure=None,Mach=None,gamma = 1.4):
	"""
	The relationship between static pressure over pressure to mach at a given ratio of specific heats
	Pass None as variable of Interest
	"""
	import sys
	from math import pow,log
	
	pop = StaticPressureToPressure
	
	#Check inputs
	if (pop == None and Mach == None) or (pop !=None and Mach != None):
		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
	try:
		log(gamma-1)
	except:
		sys.exit("Gamma must be a real number greater than 1")
	
	#if pop is variable of interest
	if pop == None:
		try:
			return pow(1+(gamma-1)/2*pow(Mach,2),gamma/(gamma-1))
		except:
			sys.exit("StaticPressureToPressure was the variable of interest. Issue finding. Make sure Mach is a float")
	elif Mach == None:
		try:
			return pow(2/(gamma-1)*(pow(pop,(gamma-1)/gamma)-1),1/2)
		except:
			sys.exit("Mach was the variable of interest. Issue finding. Make sure StaticPressureToPressure is a float")
	else:
		sys.exit("Could not find Variable of interest")

def den0_den(StaticDensityToDensity = None,Mach = None,gamma = 1.4):
	"""
	The relationship between static density over density to mach at a given ratio of specific heats
	Pass None as variable of Interest
	"""
	import sys
	from math import pow,log
	
	pop = StaticDensityToDensity
	
	#Check inputs
	if (pop == None and Mach == None) or (pop !=None and Mach != None):
		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
	try:
		log(gamma-1)
	except:
		sys.exit("Gamma must be a real number greater than 1")
	
	#if pop is variable of interest
	if pop == None:
		try:
			return pow(1+(gamma-1)/2*pow(Mach,2),1/(gamma-1))
		except:
			sys.exit("StaticDensityToDensity was the variable of interest. Issue finding. Make sure Mach is a float")
	elif Mach == None:
		try:
			return pow(2/(gamma-1)*(pow(pop,(gamma-1))-1),1/2)
		except:
			sys.exit("Mach was the variable of interest. Issue finding. Make sure StaticDensityToDensity is a float")
	else:
		sys.exit("Could not find Variable of interest")

def T0_T(StaticTemperatureToTemperature = None,Mach= None,gamma = 1.4):
	"""
	The relationship between static Temperature over Temperature to mach at a given ratio of specific heats
	Pass None as variable of Interest
	"""
	import sys
	from math import pow,log
	
	pop = StaticTemperatureToTemperature
	
	#Check inputs
	if (pop == None and Mach == None) or (pop !=None and Mach != None):
		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
	try:
		log(gamma-1)
	except:
		sys.exit("Gamma must be a real number greater than 1")
	
	#if pop is variable of interest
	if pop == None:
		try:
			return 1 + (gamma-1)/2 *pow(Mach,2)
		except:
			sys.exit("StaticTemperatureToTemperature was the variable of interest. Issue finding. Make sure Mach is a float")
	elif Mach == None:
		try:
			return pow(2/(gamma-1)*(pop-1),1/2)
		except:
			sys.exit("Mach was the variable of interest. Issue finding. Make sure StaticTemperatureToTemperature is a float")
	else:
		sys.exit("Could not find Variable of interest")

def q_P(dynamicToStaticPressure = None, Mach = None, gamma =1.4):
	"""
	The relationship between dynamic to static pressure and Mach
	Pass None as variable of Interest
	"""
	import sys
	from math import pow,log
	
	pop = dynamicToStaticPressure
	
	#Check inputs
	if (pop == None and Mach == None) or (pop !=None and Mach != None):
		sys.exit("Incorrect number of None Variables. Make sure to pass only one None for variable of interest")
	try:
		log(gamma-1)
	except:
		sys.exit("Gamma must be a real number greater than 1")
	
	#if pop is variable of interest
	if pop == None:
		return gamma/2*pow(Mach,2)
	elif Mach == None:
		return pow(2*pop/gamma,1/2)
		
	else:
		sys.exit("Could not find Variable of interest in Relations.Isentropic.q_P()")

