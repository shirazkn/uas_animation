from gazebo_msgs.msg import ModelState 
import numpy as np

FLIGHT_HEIGHT = 20
DT = 1.0/25.0


def get_ModelState(name):
	_msg = ModelState()
	_msg.pose.position.x = 0
	_msg.pose.position.y = 0
	_msg.pose.position.z = FLIGHT_HEIGHT
	_msg.pose.orientation.x = 0
	_msg.pose.orientation.y = 0
	_msg.pose.orientation.z = 0
	_msg.pose.orientation.w = 1
	_msg.model_name = name
	return _msg


def get_drone_xy(i):
	"""
	i : Iteration number
	"""
	x = 30*np.sin(2*np.pi*i*0.1)
	y = 15*np.cos(2*np.pi*i*0.1)
	return x,y