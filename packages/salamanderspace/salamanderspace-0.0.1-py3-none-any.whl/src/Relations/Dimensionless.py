"""
Name: Jason Saladiner Jr.
Date Created: 04/29/2022
Last Updated: 04/29/2022
Purpose: Act as a repository for Isentropic Relations
General Assumptions:

Included Functions:
    def Mach(velocity,a,Mach)
    def Reynolds(density,velocity,length,dynamicViscosity,Reynolds)
"""


def Mach(velocity=None,a=None,Mach=None):
	import sys
	
	#count of the number of None Types
	cNone = [velocity,a,Mach].count(None)
	
	if cNone != 1:
		sys.exit("Incorrect number of None Variables in SalamanderSpace.Relations.Dimensionless.Mach. Make sure to pass only one None for variable of interest")

	if Mach == None:
		return velocity/a
	elif a == None:
		return velocity / Mach
	elif velocity == None:
		return a*Mach

def Reynolds(density = None,flowSpeed = None,Length = None,dynamicViscosity = None,ReynoldsNumber = None):
	import sys
	from math import prod
	var = [density,flowSpeed,Length,dynamicViscosity,ReynoldsNumber]
	
	if var.count(None) != 1:
		sys.exit("Incorrect number of None Variables in SalamanderSpace.Relations.Dimensionless.Reynolds. Make sure to pass only one None for variable of interest")

	interest = var.index(None)

	if interest == 3 or interest == 4:
		return prod(var[0:3]) / var[2*interest-7]
	else:
		rhs = var[0:3]
		return prod(var[3:])/(rhs[interest-1]*rhs[interest-2])