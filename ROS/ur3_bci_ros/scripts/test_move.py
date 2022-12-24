##! /usr/bin/env python

import sys
import rospy
import actionlib
import moveit_commander
from std_srvs.srv import Empty, EmptyResponse, EmptyRequest
from geometry_msgs.msg import Pose, TransformStamped
from moveit_msgs.msg import DisplayTrajectory
from robotiq_2f_gripper_msgs.msg import CommandRobotiqGripperFeedback, CommandRobotiqGripperActionResult, CommandRobotiqGripperAction, CommandRobotiqGripperGoal
from robotiq_2f_gripper_control.robotiq_2f_gripper_driver import Robotiq2FingerGripperDriver as Robotiq
from tf.transformations import *

def objTransCallback(msg):
    global pose_target
    pose_target.position.x = msg.transform.translation.x
    pose_target.position.y = msg.transform.translation.y - 0.07
    pose_target.position.z = msg.transform.translation.z + 0.3
    (roll, pitch, yaw) = euler_from_quaternion([msg.transform.rotation.x,
                                msg.transform.rotation.y,
                                msg.transform.rotation.z,
                                msg.transform.rotation.w])
    
    roll += 3.14159

    q = quaternion_from_euler(roll, pitch, yaw)

    pose_target.orientation.x = q[0]
    pose_target.orientation.y = q[1]
    pose_target.orientation.z = q[2]
    pose_target.orientation.w = q[3]

if __name__ == '__main__':
    global pose_target
    rospy.init_node('move_ur3', log_level=rospy.DEBUG)
    # MoveIt definitions
    moveit_commander.roscpp_initialize(sys.argv)

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    
    group_name = "arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                    DisplayTrajectory,
                                                    queue_size=10)

    # Message definitions
    pose_target = Pose()

    # Robotiq gripper action server
    # self.action_name = rospy.get_param('~action_name', 'command_robotiq_action')
    # self.robotiq_client = actionlib.SimpleActionClient(self.action_name, CommandRobotiqGripperAction)
    # self.robotiq_client.wait_for_server()
    
    rospy.Subscriber('object_transform',TransformStamped,objTransCallback,queue_size=5)

    # rospy.logdebug("Request received")
    rospy.logdebug("Moving above the target")
    move_group.go(pose_target, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    # # Robotiq.goto(self.robotiq_client, pos=0.085, speed=0.05, force=5)

    # pose_target.position.z -= 0.2

    # rospy.logdebug("Moving to target")
    # move_group.go(pose_target, wait=True)
    # move_group.stop()
    # move_group.clear_pose_targets()

    # # Robotiq.goto(robotiq_client, pos=0.0, speed=0.05, force=10)

    # pose_target.position.z += 0.4

    # rospy.logdebug("Lifting object")
    # move_group.go(pose_target, wait=True)
    # move_group.stop()
    # move_group.clear_pose_targets()

    # joint_goal = move_group.get_current_joint_values()
    # joint_goal[0] = -1.22178
    # joint_goal[1] = -2.44354
    # joint_goal[2] = -0.69803
    # joint_goal[3] = 3.4906
    # joint_goal[4] = 1.57076
    # joint_goal[5] = 1.57079
    # rospy.logdebug("Moving above target pose")
    # move_group.go(joint_goal, wait=True)
    # move_group.stop()

    # pose_target.position.z -=0.05
    # rospy.logdebug("Moving to target pose")
    # move_group.go(self.pose_target, wait=True)
    # move_group.stop()
    # move_group.clear_pose_targets()

    # # Robotiq.goto(robotiq_client, pos=0.0, speed=0.05, force=10)

    # pose_target.position.z += 0.05
    # rospy.logdebug("Moving above target pose")
    # move_group.go(pose_target, wait=True)
    # move_group.stop()
    # move_group.clear_pose_targets()
    # rospy.logdebug("Moving to initial pose")
    # init_pose_srv.call(init_pose_req)