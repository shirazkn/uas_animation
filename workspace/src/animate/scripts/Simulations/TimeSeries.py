from math import floor

class Simulation:
	def __init__(self, endtime=None, dt=None):
		if dt is None:
			raise ValueError

		self.i_final = NotImplementedError - 1

		self.is_finished = False
		self.dt = dt

	def get_i_from_t(t):
		return floor(time/self.dt)

	def get_drone_xy_from_i(i):
		return NotImplementedError

	def get_drone_xy(t):
		i = get_i_from_t(t)
		self.is_finished = (i >= self.i_final)
		return get_drone_xy_from_i(i)