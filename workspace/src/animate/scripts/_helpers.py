from gazebo_msgs.msg import ModelState 
import numpy as np

def get_ModelState(name):
	_msg = ModelState()
	_msg.pose.position.x = 0
	_msg.pose.position.y = 0
	_msg.pose.position.z = 0
	_msg.pose.orientation.x = 0
	_msg.pose.orientation.y = 0
	_msg.pose.orientation.z = 0
	_msg.pose.orientation.w = 1
	_msg.model_name = name
	return _msg

# Logic for camera tracking (takes pitch and swivel as input)

def xyz_from_ps(offset, pitch, swivel):
    return [-1*offset*np.cos(-1*pitch)*np.cos(swivel),
            -1*offset*np.cos(-1*pitch)*np.sin(swivel),
            -1*offset*np.sin(-1*pitch)]

def quat_from_ps(pitch, swivel):
    # TODO : Remove roll terms
    roll = 0.0
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(swivel/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(swivel/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(swivel/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(swivel/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(swivel/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(swivel/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(swivel/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(swivel/2)
    return [qx, qy, qz, qw]

def set_xyz(camera_msg, offset, pitch, swivel):
    (camera_msg.pose.position.x,
     camera_msg.pose.position.y,
     camera_msg.pose.position.z) = xyz_from_ps(offset, pitch, swivel)

def set_quat(camera_msg, pitch, swivel):
    (camera_msg.pose.orientation.x,
     camera_msg.pose.orientation.y, 
     camera_msg.pose.orientation.z, 
     camera_msg.pose.orientation.w) = quat_from_ps(pitch, swivel) 
