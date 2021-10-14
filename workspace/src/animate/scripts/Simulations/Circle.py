import numpy as np
HEIGHT = 50.0

class Simulation:
	def __init__(self, endtime=None, _=None):
		if endtime is None:
			raise ValueError

		self.endtime = endtime
		self.is_finished = False

	def get_drone_xyz(self, t):
		x = 30*np.sin(2*np.pi*t*0.1*0.5)
		y = 15*np.cos(2*np.pi*t*0.1*0.5)
		z = HEIGHT

		self.is_finished = (t >= self.endtime)

		return x,y,z