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

OFFSET = 2
PITCH = 30  # up-down tilt (Degrees) of camera wrt drone trajectory
SWIVEL = 0
PITCH = np.deg2rad(PITCH)
SWIVEL = np.deg2rad(SWIVEL)


def quat_from_ps(pitch, swivel):
    # TODO : Remove roll terms
    roll = 0.0
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(swivel/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(swivel/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(swivel/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(swivel/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(swivel/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(swivel/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(swivel/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(swivel/2)
    return [qx, qy, qz, qw]

def xyz_from_ps(pitch, swivel):
    return [OFFSET*np.cos(pitch)*np.cos(swivel),
            OFFSET*np.cos(pitch)*np.sin(swivel),
            OFFSET*np.sin(pitch)]

def set_xyz(camera_msg, xyz):
    (camera_msg.pose.position.x,
     camera_msg.pose.position.y,
     camera_msg.pose.position.z) = xyz_from_ps(pitch, swivel)

def set_quat(camera_msg, pitch, swivel):
    (camera_msg.pose.orientation.x,
     camera_msg.pose.orientation.y, 
     camera_msg.pose.orientation.z, 
     camera_msg.pose.orientation.w) = quat_from_ps(-pitch, -swivel) 

def main():
    rospy.init_node('set_camera_pose')

    camera_msg = h.get_ModelState('camera_1')
    camera_msg.reference_frame = 'drone'

    # Bookkeeping for ros/gazebo
    rospy.wait_for_service('/gazebo/set_model_state')
    start = rospy.get_rostime()
    elapsed = 0
    iteration = -1
    end_time = 10
    rate = rospy.Rate(100)
    
    # Camera tracking logic
    pitch = PITCH
    swivel = SWIVEL
    while elapsed <= end_time:
        now = rospy.get_rostime()
        elapsed = (now - start).to_sec()
        rospy.wait_for_service('/gazebo/set_model_state')

        if True:
            iteration += 1
            try:
                set_xyz(camera_msg, pitch, swivel)
                set_quat(camera_msg, pitch, swivel)

                set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
                resp = (set_state(camera_msg))

            except rospy.ServiceException as e:
                print("Service call failed: {:s}".format(str(e)))

        rate.sleep()

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
