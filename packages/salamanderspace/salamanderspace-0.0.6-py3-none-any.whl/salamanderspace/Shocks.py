"""
Name: Jason Saladiner Jr.
Date Created: 04/28/2022
Last Updated: 04/28/2022
Purpose: Create classes for full shock regiments
General Assumptions:

Included Functions/Submodules:
	class NormalShock
	class ObliqueShock
"""


####Do we need??? What was use case/outputs
class NormalShock:





	def __init__(self,Mach,gamma=1.4):
		"""
		NormalShock will create a shock and apply normal shock relations across it
		"""
		
		
		self.M = Mach
		self.g = gamma

		



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



