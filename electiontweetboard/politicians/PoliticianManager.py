class PoliticianManager:
	# This will represent the one and only 'true' Politician Manager
	# for our application.
	_instance = None

	@staticmethod
	def getInstance():
		# This is where we return our instance :)
		if PoliticianManager._instance == None:
			PoliticianManager()
		return PoliticianManager._instance
	

	# ATTENTION: This is now a private constructor, if we want to
	# define a PoliticianManager object outside of this PoliticianManager
	# class from now on, we will have to use PoliticianManager.getInstance()
	def __init__(self):
		if PoliticianManager._instance != None:
			raise Exception("Derp de Herp Herp! PoliticianManager is a singleton mate!")
		else:
			PoliticianManager._instance = self
			PoliticianManager.politicians = [
				'Joe Biden', 'Marianne Williamson', 'Dean Phillips',
				'Donald Trump', 'Nikki Haley', 'Vivek Ramaswamy', 'Asa Hutchinson',
				'Ron DeSantis', 'Chris Christie'
			]

	def getPoliticians(self):
		return self.politicians