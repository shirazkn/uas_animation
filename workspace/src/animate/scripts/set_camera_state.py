#!/usr/bin/env python3
from io import open_code
from copy import deepcopy

import numpy as np
import rospy 
import rospkg 
from gazebo_msgs.srv import SetModelState
import geometry_msgs.msg
import tf2_ros

import _helpers as h
import scipy.spatial.transform as t
import numpy as np
from params import *

OFFSET = 5.0  # Dist. from camera to drone (+ve moves camera along x-)
PITCH = 50.0  # up-down tilt (+ve looks downwards, towards z)
SWIVEL = 170.0  # Swivel (+ve looks towards y+)
# When pitch and swivel are 0, camera is at (-OFFSET, 0, 0) aligned towards x+


def main():
    rospy.init_node('set_camera_pose')
    rospy.wait_for_service('/gazebo/set_model_state')
    start = rospy.get_rostime()
    rate = rospy.Rate(camera_update_rate)
    
    camera_msg = h.get_ModelState('camera_1')
    camera_msg.reference_frame = 'drone'
    pitch = np.deg2rad(PITCH)
    swivel = np.deg2rad(SWIVEL)

    while not sim.is_finished:
        rospy.wait_for_service('/gazebo/set_model_state')
        elapsed = (rospy.get_rostime() - start).to_sec()

        try:
            swivel = swivel - 0.0007 
            pitch = pitch - 0.0004
            h.set_xyz(camera_msg, OFFSET, pitch, swivel)
            h.set_quat(camera_msg, pitch, swivel)
            set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
            _ = (set_state(camera_msg))
            rate.sleep()

        except rospy.ServiceException as e:
            print("Service call failed: {:s}".format(str(e)))

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
