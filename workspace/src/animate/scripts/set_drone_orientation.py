#!/usr/bin/env python3
from io import open_code
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt

import rospy 
import rospkg 
from gazebo_msgs.srv import SetModelState
import geometry_msgs.msg
import tf2_ros
from std_srvs.srv import Empty, EmptyRequest

import _helpers as h
from params import *


def main():
    rospy.init_node('set_pose')
    rospy.wait_for_service('/gazebo/pause_physics')
    pause_phys = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
    pause_phys(EmptyRequest())
    rospy.wait_for_service('/gazebo/set_model_state')

    drone_msg = h.get_ModelState('drone_orientation')
    drone_msg.reference_frame = 'drone'
    start = rospy.get_rostime()
    rate = rospy.Rate(drone_update_rate)

    while not sim.is_finished:
        rospy.wait_for_service('/gazebo/set_model_state')
        elapsed = (rospy.get_rostime() - start).to_sec()

        try:
            r, p, s = sim.get_rpy(elapsed, 'kfam')
            drone_msg.pose.orientation.x, drone_msg.pose.orientation.y, drone_msg.pose.orientation.z, drone_msg.pose.orientation.w \
                = h.quat_from_ps(roll=3*r, pitch=4*p, swivel=-1*s)
            set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
            _ = (set_state(drone_msg))
            rate.sleep()

        except rospy.ServiceException as e:
            print("Service call failed: {:s}".format(str(e)))

    save_debug_plot(sim)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
