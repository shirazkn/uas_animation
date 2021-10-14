import os
import pickle
from copy import deepcopy
from math import floor

IF_DEBUG = False
HEIGHT = 30.0


class Simulation:
	def __init__(self, endtime=None, dt=None, filename=None, offset=None, slowdown_factor=1.0):
		if filename is None:
			raise ValueError

		self.data = read_file(filename)
		self.i_final = len(self.data['drone']['x']) - 1

		self.is_finished = False
		self.dt = dt if dt is not None else self.data["dt"]
		self.dt = self.dt*slowdown_factor
		self.offset = offset if offset is not None else [0.0, 0.0, 0.0]

		self.DEBUG = {"t": [], "i": [], "last_i": -1}

	def get_i_from_t(self, t):
		return floor(t/self.dt)

	def get_drone_xyz_from_i(self, i):
		# Note: Will give an index error if you speed up simulation 
		return (self.data['drone']['x'][i] + self.offset[0], 
				self.data['drone']['y'][i] + self.offset[1], 
				HEIGHT + self.offset[2])


	def get_ghost_relative_xyz_from_i(self, i):
		return (self.data['ghost']['x'][i] - self.data['drone']['x'][i], 
				self.data['ghost']['y'][i] - self.data['drone']['y'][i], 
				0.0)

	def get_rpy(self, t, key):
		i = self.get_i_from_t(t)
		return (self.data['rolls'][key][i], self.data['pitches'][key][i], self.data['yaws'][key][i]) 

	def get_drone_xyz(self, t):
		i = self.get_i_from_t(t)
		self.DEBUG["t"].append(t)
		self.DEBUG["i"].append(i)

		self.is_finished = (i >= self.i_final)
		if IF_DEBUG and self.DEBUG["last_i"] < i:
			self.DEBUG["last_i"] = i
			print(f"Data-point {i} when {t} seconds elapsed for drone.\n")

		return self.get_drone_xyz_from_i(i)

	def get_ghost_xyz(self, t):
		# Note: Ghost drone uses separate instance of this class
		# so the is_finished check should be duplicated in this method
		i = self.get_i_from_t(t)
		self.is_finished = (i >= self.i_final)
		return self.get_ghost_relative_xyz_from_i(i)


def read_file(filename):
	data = {}
	data['drone'] = {'x': [], 'y': []}
	data['ghost'] = {'x': [], 'y': []}

	dir_path = os.path.dirname(os.path.realpath(__file__))
	file_path = os.path.join(dir_path, filename)

	if os.path.splitext(filename)[-1] == '.obj':
		with open(file_path, 'rb') as f:
			raw_data = pickle.load(f)

		data['ghost']['x'] = deepcopy(raw_data['kf'][0])
		data['ghost']['y'] = deepcopy(raw_data['kf'][1])

		data['drone']['x'] = deepcopy(raw_data['kfam'][0])
		data['drone']['y'] = deepcopy(raw_data['kfam'][1])

		data["dt"] = raw_data.get("dt")
		if "rolls" in raw_data.keys():
			data["rolls"] = deepcopy(raw_data["rolls"])
			data["pitches"] = deepcopy(raw_data["pitches"])
			data["yaws"] = deepcopy(raw_data["yaws"])

	else:
		raise NotImplementedError

	return data