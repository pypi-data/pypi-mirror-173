





def variationOfProperties(entropy=None,entropyAtEnthalpy=None,pressure=None,R=.28716):
	"""
	Finding the variation of Properties (s,h,p) for a gas above a standard pressure (1 bar for air)
	entropyAtEnthalpy is usually based on tabulated values.
	pressure is given in bars and entropys are given in kJ/KgK by default (for R = .28716). Change R for different units.
	Pass None as variable of Interest
	"""
	import sys
	from math import pow,log,exp
	
	s = entropy
	sh = entropyAtEnthalpy
	p = pressure
	#count of the number of None Types
	cNone = [s,sh,p].count(None)
	
	if cNone != 1:
		sys.exit("Incorrect number of None Variables in SalamanderSpace.Relations.Dimensionless.Mach. Make sure to pass only one None for variable of interest")

	if s == None:
		return sh-R*log(p)
	elif sh == None:
		return s + R*log(p)
	elif p == None:
		return exp(-(s-sh)/R)



def Sutherland(T,mu_ref = 1.716e-5, T_ref = 273.15, S_mu = 110.6):
	"""
	Sutherland's law finds the dynmic viscosity at a given temperature based on reference values.
	Default values are for dry air.

	Returns float mu
	"""

	##TODO Find a proper home for this
	from math import pow
	Trat = pow(T/T_ref,3/2)
	Tadd = (T_ref + S_mu) / (T + S_mu)

	return mu_ref*Trat*Tadd
