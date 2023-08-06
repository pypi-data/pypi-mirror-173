"""
Name: Jason Saladiner Jr.
Date Created: 04/28/2022
Last Updated: 04/28/2022
Purpose: 
General Assumptions:

Included Functions/Submodules:
	
"""



def Sutherland(T,mu_ref = 1.716e-5, T_ref = 273.15, S_mu = 110.6):
	"""
	Sutherland's law finds the dynmic viscosity at a given temperature based on reference values.
	Default values are for dry air.

	Returns float mu
	"""
	from math import pow
	Trat = pow(T/T_ref,3/2)
	Tadd = (T_ref + S_mu) / (T + S_mu)

	return mu_ref*Trat*Tadd



class methodOfCharacteristics():


	def setDeflection(self,delta,N,height):
		"""
		set the deflection characteristics of expansion fan
		float delta = deflection of flow (should be negative)
		int N = number of waves
		float height = height of tunnel



		****Needs to write out units****
		"""
		import sys
		self.d = delta
		self.n = N
		self.h = height

		
		from numpy import linspace
		self.deflections = linspace(0,self.d,self.n)

	def _initalizeWaves_(self):
		import SalamanderSpace.Relations.ShockRelations as S
		
		self.waves = []
		self.waves.append(ExpansionWave(self.M,self.deflections[0],self.g))

		
		for i in range(1,self.n):
			self.deli = self.deflections[i]
			self.waves.append(ExpansionWave(S.prandtlmeyer(S.prandtlequation(self.waves[0].nu,None,self.deli,self.g),None,self.g),self.deli,True,self.g))
		for i in range(self.n):
			self.waves[i].setStart(0,0)
	
			
	def _findIntersect_(self,y1,y2):
		"""
		given two lambda functions
		"""
	
		self.f = lambda x: y1(x) - y2(x)
		from scipy.optimize import newton
		self.xroot = newton(self.f,1)
		self.yroot = y1(self.xroot)

		return (self.xroot,self.yroot)

	def _whichWave_(self,index):
		self.pi = -1
		self.ni = -1
		for i in range(len(self.posIndex)):
			if self.posIndex[i].count(index) !=0:
				self.pi = i
		for i in range(len(self.negIndex)):
			if self.negIndex[i].count(index) !=0:
				self.ni = i
		return (self.ni,self.pi)


	def runMethod(self):
		"""
		Run the method of characteristics
		"""
		import numpy as np


		
		self._initalizeWaves_()

		self.points = []
		self.points.append((0,0))

		self.wallindx = []
		self.wallindx.append(1)
		for i in range(self.n,1,-1):
			self.wallindx.append(self.wallindx[len(self.wallindx)-1] + i)

		self.totPoints = int(self.n * (self.n+1) / 2)

		self.posIndex = []
		self.negIndex = []
		for i in range(1,self.n+1):
			self.curWave = []
			self.curWave.append(i)
			for j in range(1,i):
				self.curWave.append(self.curWave[j-1] + self.n - j)
			self.posIndex.append(self.curWave)

		#print(self.posIndex)
		for i in range(self.n+1,self.n*2+1):
			
			self.curWave = []
			self.curWave.append(self.posIndex[i-self.n-1][-1])
			for j in range(1,2*self.n - i + 1):
				
				self.curWave.append(self.curWave[j-1] + 1)
			self.negIndex.append(self.curWave)

		
		#print(self.negIndex)
		self.ywall = lambda x: self.h
		
		for i in range(1,self.totPoints+1):
			if i in self.wallindx:
				self.nw, self.pw = self._whichWave_(i)
				self.p = self._findIntersect_(self.ywall,self.waves[self.pw].line())
				self.points.append(self.p)

				self.waves.append(ExpansionWave(self.waves[self.pw].M,self.waves[self.pw].d,False,self.waves[self.pw].g))
				self.waves[len(self.waves)-1].setStart(self.p[0],self.p[1])
			else:
				self.nw, self.pw = self._whichWave_(i)
				self.nw = self.nw+self.n
				
				self.p = self._findIntersect_(self.waves[self.nw].line(),self.waves[self.pw].line())
				self.points.append(self.p)

				self.newNu = 1/2* (self.waves[self.nw].K + self.waves[self.pw].K)
				self.newD = 1/2* (self.waves[self.nw].K - self.waves[self.pw].K)

				self.waves[self.nw].updateWave(self.newNu,self.newD)
				self.waves[self.nw].setStart(self.p[0],self.p[1])

				self.waves[self.pw].updateWave(self.newNu,self.newD)
				self.waves[self.pw].setStart(self.p[0],self.p[1])
		#print(self.points)
		




	def __init__(self,Mach,gamma=1.4):
		self.M = Mach
		self.g = gamma



class ExpansionWave():

	def line(self):
		from math import tan, pi
		
		if self.phi >= 0:
			
			self.y = lambda x: (x-self.start[0])*tan(self.phi*pi/180) + self.start[1]
		else:
			self.y = lambda x: (x-self.start[0])*tan(self.phi*pi/180) + self.start[1]
		return self.y
	def setStart(self,x,y):
		
		self.start = (x,y)
		

	def updateWave(self,NewNu,NewDelta):
		self.nu = NewNu
		self.d = NewDelta

		import SalamanderSpace.Relations.ShockRelations as S

		self.M = S.prandtlmeyer(self.nu,None,self.g)
		from math import asin,pi
		self.mu = asin(1/self.M) *180/pi 
		
		self.phi = self.d + self.mu
		
		if self.pos == False:
			self.phi = self.d - self.mu
		

	def __init__(self,Mach,delta,positive,gamma=1.4):
		self.M= Mach
		self.d = delta
		self.g = gamma
		self.pos = positive
		
		import SalamanderSpace.Relations.ShockRelations as S
		from math import asin,pi
		self.mu = asin(1/self.M) *180/pi 
		
			
		
		self.nu = S.prandtlmeyer(None,self.M,self.g)
		self.phi = self.d + self.mu
		
		if self.pos == False:
			self.phi = self.d - self.mu
			
		
		self.K = self.nu - self.d




	def _printVars_(self):
		print("Mach:",self.M,"\nDelta:",self.d,"\nmu:",self.mu,"\nnu:",self.nu,"\nphi:",self.phi,"\nK:",self.K)
		print("\n\n")







class flatWingGeometry():
	"""
	This class will contain the geomertry of a flat plate at a specific resolution. The geomertry is created by transforming a flat rectangle in numerous methods.
	"""

	def plot3d(self):
		"""
		plots the current iteration of the wing using matplotlib
		"""
	
		import matplotlib.pyplot as plt
		fig = plt.figure()
		ax = fig.add_subplot(111, projection = '3d')
		
		ax.scatter(self.points[:,0],self.points[:,1],self.points[:,2])
		plt.xlim([0,.4])
		plt.ylim([-.5,.5])
		ax.set_zlim3d(-.1,.1)
		#plt.show()
	
	def Dihedral(self,gamma):
		import numpy as np
		from math import sin,cos


		self.g = gamma
		self.temp = self.points[0][1]
		if self.temp < 0:
			self.g = - gamma
		self.dihed = np.array([1,0,0,0,cos(self.g),-sin(self.g),0,sin(self.g),cos(self.g)]).reshape((3,3))


		for i in range(len(self.points[:,0])):
			if not self.points[i][1] == self.temp:
				self.g = gamma
				if self.points[i][1] <0:
					self.g = -gamma
				self.dihed = np.array([1,0,0,0,cos(self.g),-sin(self.g),0,sin(self.g),cos(self.g)]).reshape((3,3))
			self.points[i] = np.matmul(self.dihed,self.points[i])
			self.temp = self.points[i][1]
		

	def LESweep(self,lamb):
		self.l = lamb
		import numpy as np
		from math import tan
		self.shear = np.array([1,tan(self.l),0,0,1,0,0,0,1]).reshape((3,3))
		for i in range(len(self.points[:,0])):
			if self.points[i][1] < 0:
				self.shear[0][1] = -tan(self.l)
			else:
				self.shear[0][1] = tan(self.l)
			self.points[i] = np.matmul(self.shear,self.points[i])


	def _washTrans_(self,theta):
		from math import cos,sin

		self.line0 = [cos(theta),0,sin(theta)]
		self.line1 = [0,1,0]
		self.line2 = [-sin(theta),0,cos(theta)]

		return [self.line0,self.line1,self.line2]


	def linWashout(self,washout):
		"""
		applies a linear washout to a defined wing. washout should be provided in radians
		"""
		import numpy as np
		
		theta = lambda y : washout * (1 - abs(y))
		
		self.tempy = self.tempy = self.points[0][1]
		self.tempTrans = self._washTrans_(theta(self.tempy))

		for i in range(len(self.points[:,0])):
			if not self.points[i][1] == self.tempy:
				self.tempTrans = self._washTrans_(theta(self.points[i][1]))
				self.tempy = self.points[i][1]
			
			self.points[i] = np.matmul(self.tempTrans,self.points[i])
	

	
	
		
		
	def _cofy_(self,y):
		"""
		c(y) nondimensionalized (scaled by b)
		"""
		
		
		self.cr = 2 / (self.AR*(1+self.taper))

		return self.cr*(1-2*(1-self.taper)*abs(y))



	def __init__(self,AR,taper,yrange = (-.5,.5),res = (.25,.1)):
		"""
		arguments:
		span/b = m
		area/s = m^2
		taper = dimensionless
		sweep = rad
		AR = dimensionless
		
		
		###TODO make it allow swept leading edge
		
		"""
		import numpy as np
		self.AR = AR
		self.taper = taper
		self.xr = res[0]
		self.yr = res[1]
		self.ymax = yrange[1]
		self.z = 0.

		self.LE = 0.


		self.points = []

		#creates a list of y points. Will always have the start and stop values of yrange even if the resolution is smaller inbetween last points
		self.ypoints = np.append(np.arange(yrange[0],yrange[1],self.yr),yrange[1])
		
		for y in self.ypoints:
			self.curC = self._cofy_(y)
			
			self.xpoints = np.append(np.arange(self.LE,self.LE + self.curC,self.curC*self.xr),self.curC+self.LE)

			for x in self.xpoints:
				self.points.append([x,y,self.z])
		

		self.points = np.array(self.points)
		