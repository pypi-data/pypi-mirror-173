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

		
