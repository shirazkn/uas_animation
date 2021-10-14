import pickle
from copy import deepcopy
import numpy as np
from matplotlib import pyplot as plt

FILENAME = "data_rkf"
ROLL_DOT_FACTOR = 0.5
ROLL_DOT_CLAMP_FACTOR = 0.03
ROLL_MAX = 0.25
debug_length = None
turn_stop = 1000

with open(FILENAME + '.obj', 'rb') as f:
    data = pickle.load(f)

data["rolls"] = {"kf": [], "kfam": []}
data["pitches"] = {"kf": [], "kfam": []}
data["yaws"] = {"kf": [], "kfam": []}

def get_avg_velocity(xs, i, dt):
	window = 10
	vel = np.array([[0.0],[0.0]])
	for j in range(i, i+window):
		if j > (len(xs) - 2):
			break 
		vel += (xs[j+1] - xs[j-1])*0.5

	return vel/(dt*window)

def get_angle(v):
	angle = -(np.arctan(v[1]/v[0]))
	if abs(angle) > 1.0:
		angle = abs(angle)*-1
	return angle

def lap_smoothing(vec, passes=15, scale=True):
	smoothed_vec = deepcopy(vec)
	for _ in range(passes):
		for i in range(1, len(vec)-1):
			smoothed_vec[i] = np.mean(smoothed_vec[i-1:i+1])
	smoothed_vec[-1] = smoothed_vec[-2]
	return np.array(smoothed_vec)*10.0 if scale else np.array(smoothed_vec)

for ts_key in ["kfam", "kf"]:
	rolls = []
	pitches = []
	yaws = []
	
	forces = []

	posx = data[ts_key][0]
	posy = data[ts_key][1]
	xs = [np.array([[x],[y]]) for x, y in zip(posx, posy)]

	xs = xs[:debug_length]
	roll_dot = 0.0 
	roll = 0.0
	for i in range(1, len(xs)-1):
		delx = xs[i+1] - xs[i] - (xs[i] - xs[i-1])
		force = np.cross(delx.T, xs[i+1].T - xs[i].T)[0]
		roll_dot += ROLL_DOT_FACTOR*force if abs(roll)<0.9*ROLL_MAX else 0.0
		roll_dot -= ROLL_DOT_CLAMP_FACTOR*(roll**2 * np.sign(roll) + 0.5*roll)
		roll_dot_clipped = (1 - abs(roll)/ROLL_MAX)*roll_dot
		roll += roll_dot_clipped
		rolls.append(deepcopy(roll))
		forces.append(deepcopy(force))
		
		vel = get_avg_velocity(xs, i, data["dt"])
		vel_angle = get_angle(vel)

		yaws.append(vel_angle)
	
	roll_means = [0 for _ in range(380)] + [-1*ROLL_MAX for _ in range(50)] + [0 for _ in range(169)]
	rolls = 0.2*lap_smoothing(rolls, 10, False) + lap_smoothing(roll_means, 60, False) \
	+ 4*lap_smoothing(forces, 3, False)
	for i in range(turn_stop, len(yaws)):
		yaws[i] = -np.pi*0.5
	yaws = lap_smoothing(yaws, 10, False)
	pitches = [0.05]

	def fill_array(v):
		v = v.tolist() if type(v) == np.ndarray else v
		while len(v) < len(xs):
			v.append(v[-1])
		return v

	yaws = fill_array(yaws)
	rolls = fill_array(rolls)
	pitches = fill_array(pitches)

	plt.plot(yaws, label='yaws')
	plt.plot(rolls, label='rolls')
	plt.plot(pitches, label='pitches')
	plt.legend()
	plt.show()

	data["rolls"][ts_key] = rolls
	data["yaws"][ts_key] = yaws
	data["pitches"][ts_key] = pitches

with open(FILENAME + '_rpy' + '.obj', 'wb') as f:
    pickle.dump(data, f)