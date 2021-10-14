#!/usr/bin/env python3
from io import open_code
from copy import deepcopy

import numpy as np
import rospy 
import rospkg 
from gazebo_msgs.srv import SetModelState
import geometry_msgs.msg
import tf2_ros
from std_srvs.srv import Empty, EmptyRequest

import _helpers as h
from params import *

OFF_CAMERA = (0, 0, -100)


def main():
    rospy.init_node('set_pose_ghost')
    rospy.wait_for_service('/gazebo/set_model_state')

    state_msg = h.get_ModelState('ghost_drone')
    state_msg.reference_frame = 'drone'
    start = rospy.get_rostime()
    rate = rospy.Rate(ghost_update_rate)

    while not sim.is_finished:
        rospy.wait_for_service('/gazebo/set_model_state')
        elapsed = (rospy.get_rostime() - start).to_sec()

        try:
            if elapsed < GHOST_STOP_TIME:
                state_msg.pose.position.x, state_msg.pose.position.y, state_msg.pose.position.z \
                    = sim.get_ghost_xyz(elapsed) \

                r, p, s = sim.get_rpy(elapsed, 'kf')
                state_msg.pose.orientation.x, state_msg.pose.orientation.y, state_msg.pose.orientation.z, state_msg.pose.orientation.w \
                = h.quat_from_ps(roll=5*r, pitch=4*p, swivel=-1*s)
            
            else:
                state_msg.pose.position.x, state_msg.pose.position.y, state_msg.pose.position.z \
                    = OFF_CAMERA

            set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
            _ = (set_state(state_msg))
            rate.sleep()

        except rospy.ServiceException as e:
            print("Service call failed: {:s}".format(str(e)))

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
