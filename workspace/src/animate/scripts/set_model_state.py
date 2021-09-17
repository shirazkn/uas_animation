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


def main():
    rospy.init_node('set_pose')

    state_msg = h.get_ModelState('drone')


    rospy.wait_for_service('/gazebo/pause_physics')
    pause_phys = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
    pause_phys(EmptyRequest())

    rospy.wait_for_service('/gazebo/set_model_state')
    start = rospy.get_rostime()
    elapsed = 0
    iteration = -1
    end_time = 10
    rate = rospy.Rate(100)
    # while not rospy.is_shutdown():
    while elapsed <= end_time:
        now = rospy.get_rostime()
        elapsed = (now - start).to_sec()
        rospy.wait_for_service('/gazebo/set_model_state')
        if True:
            iteration += 1
            try:
                state_msg.pose.position.x, state_msg.pose.position.y \
                    = h.get_drone_xy(elapsed) 
                    # Currently overloading! replace elapsed with iteration (int)
                set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
                resp = (set_state(state_msg))

            except rospy.ServiceException as e:
                print("Service call failed: {:s}".format(str(e)))
        rate.sleep()

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
