"""
will be used for vlm hw and possible other extensions 
"""


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
		
