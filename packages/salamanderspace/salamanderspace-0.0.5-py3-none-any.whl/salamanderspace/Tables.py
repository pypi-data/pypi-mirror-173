"""
Name: Jason Saladiner Jr.
Date Created: 04/28/2022
Last Updated: 04/28/2022
Purpose: Create classes for useful tables
General Assumptions:

Included Functions/Submodules:
	class NACA1135
	class StandardAtmosphere
"""
import numpy as np







class NACA1135():
	

	def _createRow_(self,Mach):
		"""
		creates the row in the same fashion as NACA 1135 for given Mach
		"""
		
		from SalamanderSpace.Relations import Isentropic as I
		from math import pow,inf,asin,pi

		self.row = []
		self.M = Mach


		##Subsonic##
		
		self.row.append(self.M)
		self.row.append(pow(I.P0_P(Mach = self.M,gamma=self.g),-1))
		self.row.append(pow(I.den0_den(Mach=self.M,gamma = self.g),-1))
		self.row.append(pow(I.T0_T(Mach=self.M,gamma=self.g),-1))
		self.row.append(pow(abs(pow(self.M,2)-1),1/2))
		self.row.append(I.q_P(Mach=self.M,gamma=self.g)*pow(I.P0_P(Mach=self.M,gamma=self.g),-1))
		
		if Mach <= 1e-8:
			self.row.append(inf)
		else:
			from SalamanderSpace.Relations import Astar_A as A
			self.row.append(A(Mach=self.M,gamma = self.g))
		from SalamanderSpace.Relations import V_astar as V
		self.row.append(V(Mach=self.M,gamma = self.g))

		if self.M <1:
			self.row.append(None)
			self.row.append(None)
			self.row.append(None)
			self.row.append(None)
			self.row.append(None)
			self.row.append(None)
			return self.row

		from SalamanderSpace.Relations import ShockRelations as S
		self.row.append(S.prandtlmeyer(Mach = self.M,gamma = self.g))
		self.row.append(asin(1/self.M)*180/pi)
		self.row.append(S.mach2(Mach1 = self.M,gamma = self.g))
		self.row.append(S.pressureRatio(Mach1=self.M,gamma=self.g))
		self.row.append(S.densityRatio(Mach1=self.M,gamma=self.g))
		self.row.append(S.temperatureRatio(Mach1=self.M,gamma=self.g))

		###Need to add Rayleigh pitot ratios###
		return self.row
	def buildTable(self,n=10):
		"""
		creates the table from Mach 0->Mach n (default 10) at intervals of .01 Mach
		"""
		self.n = n
		#from numpy import linspace,array
		self.M1 = np.linspace(0,n,100*n+1)
		self.tab = []
		for i in range(len(self.M1)):
			self.tab.append(self._createRow_(self.M1[i]))

		self.Table =  np.array(self.tab,dtype = object)

		


	def getRow(self,**given):
		"""
		Returns NACA 1135 row for a given variable
		given must be in from string Varible = float Value
		Varibable names include:
			Mach1, isenPressure, isenDensity, isenTemperature, Beta, dynTotalPressure, AreaRatio, VaStar, 
			nu, mu, Mach2, shockPressure, shockDensity, shockTemperature, ***Pitot Values Not Added Yet*** 
		"""
		import SalamanderSpace.Relations as ssR
		import SalamanderSpace.Relations.Isentropic as I
		import SalamanderSpace.Relations.ShockRelations as S

		from math import sqrt, abs, sin
		self.varDict = {"mach1" : 0, "isenpressure" : I.P0_P, "isendensity" : I.den0_den, "isentemperature" : I.T0_T, "beta" : 4, "dyntotalpressure" : I.q_P,"arearatio" : ssR.Astar_A,"nu" : S.prandtlmeyer, "mu" : 9, "mach2" : S.mach2, "shockpressure": S.pressureRatio, "shockdensity" : S.densityRatio, "shocktemperature":S.temperatureRatio}
		
		for var,value in given.items():
			if self.varDict[var] == 0 :
				self.m = var
			elif self.varDict[var] == 4:
				self.m = sqrt(abs(value**2 - 1))
			elif self.varDict[var] == 9:
				self.m = 1 / (sin(value*pi/180))
			elif var.lower()[:2] == "is" or var.lower()[:2] == "dy" or var.lower()[:2] == "ar":
				self.m = self.varDict[var](value**-1,Mach=None,gamma=1.4)

		return self._createRow_(self.m)



		#self.roundM = round(Mach,2)
		
		#if self.roundM >=0 and self.roundM <=(len(self.Table)-1)/100:
		#	self.ind = np.where(abs(self.Table[:,0] - self.roundM) <=1e-6)
		#	self.row =  self.Table[self.ind]
		#	if self.roundM < 1:
		#		return self.row[0,0:8]
		#	return self.row[0]
		#elif self.roundM >= (len(self.Table[:,0])-1)/100:
		#	return self._createRow_(self.roundM)
		#else:
		#	import sys
		#	sys.exit("Mach is negative which is not possible.")


	#def findElement(self,*var,**given):
	#	"""
	#	def findElement will return the value of a given set of *variables (passed as strings) with some **given (string = num)
	#	Varibable names include:
	#		Mach1, isenPressure, isenDensity, isenTemperature, Beta, dynTotalPressure, AreaRatio, VaStar, 
	#		nu, mu, Mach2, shockPressure, shockDensity, shockTemperature, ***Pitot Values Not Added Yet*** 
	#	"""
	#	self.var = str(var).lower()
	#	self.varDict = {"mach1" : 0, "isenpressure" : 1, "isendensity" : 2, "isentemperature" : 3, "beta" : 4, "dyntotalpressure" : 5,
	#			  "arearatio" : 6, "vastar" : 7, "nu" : 8, "mu" : 9, "mach2" : 10, "shockpressure": 11, "shockdensity" : 12, "shocktemperature":13}
	#	self.indx = []
	#	self.value = []
	#	for i in given:
	#		self.indx.append(self.varDict[i[0].lower()])
	#		self.value.append(i[1])

	def printNames():
		"""
		0-Mach1, 1-isenPressure, 2-isenDensity, 3-isenTemperature, 4-Beta, 5-dynTotalPressure, 6-AreaRatio, 7-VaStar, 8-nu, 9-mu, 
		10-Mach2, 11-shockPressure, 12-shockDensity, 13-shockTemperature

		Isen: p/pt
		shock: 2/1
		"""
	def __init__(self,gamma = 1.4):
		
		self.g = gamma


class standardAtmosphere():



	def _setBoundaries_(self,bondaries):
		"""
		Sets the boundaries of the atmospheric layers\n
		Input:\n
			\tlist boundaries = list of lists with each row corresponding to base of each atmospheric layer\n
			\t[base geopotential alt,Base Temp,Base Pressure,Base Density]\n
			\n
			\n
		**Note: Units should remain constant and are not check by this class.** \n
			\tfor SI: use meters, K, pascals, kg/m^3\n
			\tfor English Eng Units: use ft, Rankie, Atm, slugs/ft^3
		"""

	def _tempProfile_(self):
		"""
		Create a temperature profile from the given model\n
		Updates self.model to include lapse rate (between base temp and base pressure)
		"""


		
			
		#print(self.model)
		for self.i in range(len(self.model)-1):
			#print(self.model[i+1][1],self.model[i][1],self.model[i+1][0],self.model[i][0])
			print(self.i+1)

			self.lr = (self.model[self.i+1][1] - self.model[self.i][1])/(self.model[self.i+1][0]-self.model[self.i][0])

			self.model.insert(2,self.lr)
	
	

	def _iso_(self,T,dh):
		"""
		find the ratio of final to inital pressure and temp in isothermal region
		return tuple 
		"""
		from math import exp
		self.rat = exp(-(self.g*dh)/(self.R*T))
		return self.rat,self.rat

	def _grad_(self,T,Ti,lr):
		"""
		find the ratio of final to inital pressure and temp in gradient region
		return tuple = p/pi, rho/rhoi
		"""
		from math import pow
		self.prat = pow(T/Ti,-self.g/lr/self.R)
		self.rhorat = pow(T/Ti,-(self.g/lr/self.R+1))

		return self.prat,self.rhorat


	def fromGP(self,height):
		"""
		Get the standard atmosphere values at a given geopotential alt\n
		**Inputs**\n
		-- float height = geopotential altitude above mean sea level\n
		**Returns**\n
		-- list atmosphere = [height,Temp,pressure,density]
		"""
		self.atmosphere = []
		self.atmosphere.append(height)
		for i in range(len(self.model)):
			if height - self.model[i][0] < 1e-6:
				self.atmosphere.append(self.model[i][1])
				self.atmosphere.append(self.model[i][3])
				self.atmosphere.append(self.model[i][4])
				return self.atmosphere
			elif height < self.model[i][0]:
				self.dh = height - self.model[i-1][0]
				self.tnew = self.model[i-1][1] + self.model[i-1][2] * self.dh
				
				self.atmosphere.append(self.tnew)

				#check if iso or gradient
				if self.model[i-1][2] < 1e-6:
					self.rats = self._iso_(self.tnew,self.dh)
				else:
					self.rats = self._grad_(self.tnew,self.model[i-1][1],self.model[i-1][2])

				self.atmosphere.append(self.rats[0] * self.model[i-1][3])
				self.atmosphere.append(self.rats[1] * self.model[i-1][4])
				return self.atmosphere
		
		self.i = len(self.model)
		self.dh = height - self.model[i-1][0]
		self.tnew = self.model[i-1][1] + self.model[i-1][2] * self.dh
				
		self.atmosphere.append(self.tnew)

		#check if iso or gradient
		if self.model[i-1][2] < 1e-6:
			self.rats = self._iso_(self.tnew,self.dh)
		else:
			self.rats = self._grad_(self.tnew,self.model[i-1][1],self.model[i-1][2])

		self.atmosphere.append(self.rats[0] * self.model[i-1][3])
		self.atmosphere.append(self.rats[1] * self.model[i-1][4])
		return self.atmosphere


	def fromGM(self,height):
		"""
		Get the standard atmosphere values at a given geometric alt\n
		**Inputs**\n
		-- float height = geometric altitude above mean sea level\n
		**Returns**\n
		-- list atmosphere = [height,Temp,pressure,density]
		"""

		#self.gp = 

	def __init__(self,g,**kwargs):
		"""
		Create a standard atmosphere for estimations using US 1976 Standard Atmosphere Equations\n
		Can change to different inital conditions/atmoshpere boundaries\n
			\tDefaults to ISA 1976
		**Inputs:**\n
		g = gravitational constant at mean sea level\n
		\n
		
		kwargs\n
		--string units = used units [SI or EE]     *Currently supports SI and English Eng. Units (Defaults to SI)*\n
		--float gamma = ratio of specific heats\n
		--list model = list of list setting boundaries \tfor SI: use meters, K, pascals, kg/m^3\n
		"""
		self.g = g

		##KWARGS
		
		try:			#Units
			self.units = kwargs["units"]
		except:
			self.units = "SI"
		try:			#gamma
		   self.gamma = kwargs["gamma"]
		except:
			self.gamma = 1.4
		try:			#Model
			self.model = kwargs["model"]
		except:
			self.ISA1976 = [[-610,292.15,108900,1.2985],[11000,216.65,22632,0.3639],[20000,216.65,5474.9,0.0880],[32000,228.65,868.02,0.0132],[47000,270.65,110.91,0.0020],[51000,270.65,66.939,0],[71000,214.65,3.9564,0],[84852,186.87,0.3734,0]]
			self.model = self.ISA1976
		

		self._tempProfile_()