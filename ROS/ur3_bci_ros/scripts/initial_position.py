#!/usr/bin/env python

import rospy
import sys
import moveit_commander
from moveit_msgs.msg import DisplayTrajectory
from std_srvs.srv import Empty, EmptyResponse
from math import pi

class UR3InitPose(object):
    def initPoseCallback(self,req):
        joint_goal = self.move_group.get_current_joint_values()
        joint_goal[0] = -pi/2
        joint_goal[1] = -pi/6
        joint_goal[2] = -4*pi/6
        joint_goal[3] = -pi/6
        joint_goal[4] = pi/2
        joint_goal[5] = pi
        rospy.logdebug(joint_goal)

        self.move_group.go(joint_goal, wait=True)
        self.move_group.stop()

        return EmptyResponse()

    def __init__(self):
        
        moveit_commander.roscpp_initialize(sys.argv)

        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        
        group_name = "arm"
        self.move_group = moveit_commander.MoveGroupCommander(group_name)
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                        DisplayTrajectory,
                                                        queue_size=10)

        rospy.Service('initial_pose',Empty,self.initPoseCallback)

if __name__ == '__main__':
    rospy.init_node('ur3_initial_pose', anonymous=True, log_level=rospy.DEBUG)
    UR3InitPose()
    rospy.spin()