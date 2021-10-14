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


def save_debug_plot(sim):
    plt.figure()
    plt.plot(sim.DEBUG["t"], np.array(sim.DEBUG["i"])*sim.dt)
    plt.title("DEBUG: This should be linear!")
    plt.ylabel("Simulation Time from Data")
    plt.xlabel("Gazebo Simulation Time")
    plt.xlim([0, 0.5])
    plt.ylim([0, 0.5])
    plt.savefig("debug_plot_drone")


def main():
    rospy.init_node('set_pose')
    rospy.wait_for_service('/gazebo/pause_physics')
    pause_phys = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
    pause_phys(EmptyRequest())
    rospy.wait_for_service('/gazebo/set_model_state')

    state_msg = h.get_ModelState('drone')
    start = rospy.get_rostime()
    rate = rospy.Rate(drone_update_rate)

    while not sim.is_finished:
        rospy.wait_for_service('/gazebo/set_model_state')
        elapsed = (rospy.get_rostime() - start).to_sec()

        try:
            state_msg.pose.position.x, state_msg.pose.position.y, state_msg.pose.position.z \
                = sim.get_drone_xyz(elapsed)
            set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
            _ = (set_state(state_msg))
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
