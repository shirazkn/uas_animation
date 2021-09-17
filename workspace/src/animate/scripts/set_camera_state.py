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

OFFSET = [-3, 0, 2]
ROTATION = []


def main():
    rospy.init_node('set_camera_pose')

    camera_msg = h.get_ModelState('camera_1')

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
        # if elapsed/h.DT > (iteration + 1):
        if True:
            iteration += 1
            try:
                camera_msg.pose.position.x, camera_msg.pose.position.y \
                    = h.get_drone_xy(elapsed)
                camera_msg.pose.position.x = 0
                camera_msg.pose.position.y = 0
                camera_msg.pose.position.z = 0

                camera_msg.reference_frame = 'drone'

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
