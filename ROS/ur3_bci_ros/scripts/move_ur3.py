#! /usr/bin/env python

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
from ur_dashboard_msgs.srv import Load, LoadRequest
from std_srvs.srv import Trigger, TriggerRequest

class MoveUR3():
    def shutdown(self):
        stop_req = TriggerRequest()
        self.stop_prog.call(stop_req)
        rospy.logdebug("SHUTTING DOWN")

    def moveUR3Callback(self, req):
        rospy.logdebug("Request received")
        rospy.logdebug("Moving above the target")
        self.move_group.go(self.pose_target, wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()

        Robotiq.goto(self.robotiq_client, pos=0.085, speed=0.05, force=5)

        self.pose_target.position.z -= 0.1

        rospy.logdebug("Moving to target")
        self.move_group.go(self.pose_target, wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()

        Robotiq.goto(self.robotiq_client, pos=0.0, speed=0.05, force=10)

        self.pose_target.position.z += 0.1

        rospy.logdebug("Lifting object")
        self.move_group.go(self.pose_target, wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()

        joint_goal = [-1.335724178944723, -2.3388989607440394, -0.5742242972003382, -1.8045862356769007, 1.5877408981323242, 3.4109175205230713]
        rospy.logdebug("Moving above target pose")
        self.move_group.go(joint_goal, wait=True)
        self.move_group.stop()

        self.pose_target = self.move_group.get_current_pose().pose
        self.pose_target.position.z -=0.05
        rospy.logdebug("Moving to target pose")
        self.move_group.go(self.pose_target, wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()

        Robotiq.goto(self.robotiq_client, pos=0.085, speed=0.05, force=10)

        self.pose_target.position.z += 0.05
        rospy.logdebug("Moving above target pose")
        self.move_group.go(self.pose_target, wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()
        rospy.logdebug("Moving to initial pose")
        self.init_pose_srv.call(self.init_pose_req)

        resp = EmptyResponse()

        return resp

    def objTransCallback(self, msg):
        self.pose_target.position.x = msg.transform.translation.x
        self.pose_target.position.y = msg.transform.translation.y - 0.07
        self.pose_target.position.z = 0.3
        (roll, pitch, yaw) = euler_from_quaternion([msg.transform.rotation.x,
                                    msg.transform.rotation.y,
                                    msg.transform.rotation.z,
                                    msg.transform.rotation.w])
        
        roll += 3.14159
        yaw += 3.14159

        q = quaternion_from_euler(roll, pitch, yaw)

        self.pose_target.orientation.x = q[0]
        self.pose_target.orientation.y = q[1]
        self.pose_target.orientation.z = q[2]
        self.pose_target.orientation.w = q[3]

    def __init__(self):
        rospy.on_shutdown(self.shutdown)

        # MoveIt definitions
        moveit_commander.roscpp_initialize(sys.argv)

        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        
        group_name = "arm"
        self.move_group = moveit_commander.MoveGroupCommander(group_name)
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                        DisplayTrajectory,
                                                        queue_size=10)

        # Message definitions
        self.pose_target = Pose()
        self.init_pose_req = EmptyRequest()

        # Robotiq gripper action server
        self.action_name = rospy.get_param('~action_name', 'command_robotiq_action')
        self.robotiq_client = actionlib.SimpleActionClient(self.action_name, CommandRobotiqGripperAction)
        self.robotiq_client.wait_for_server()
        
        rospy.Subscriber('object_transform',TransformStamped,self.objTransCallback,queue_size=5)

        # Start UR3 robot
        rospy.wait_for_service("ur_hardware_interface/dashboard/load_program")
        self.load_prog =  rospy.ServiceProxy("ur_hardware_interface/dashboard/load_program", Load)
        load_req = LoadRequest()
        load_req.filename = "ROS_control.urp"
        self.load_prog.call(load_req)

        rospy.wait_for_service("ur_hardware_interface/dashboard/play")
        self.play_prog =  rospy.ServiceProxy("ur_hardware_interface/dashboard/play", Trigger)
        play_req = TriggerRequest()
        self.play_prog.call(play_req)

        rospy.wait_for_service("ur_hardware_interface/dashboard/stop")
        self.stop_prog =  rospy.ServiceProxy("ur_hardware_interface/dashboard/stop", Trigger)

        # Move to initial pose service
        rospy.wait_for_service('initial_pose')
        self.init_pose_srv = rospy.ServiceProxy('initial_pose', Empty)
        self.init_pose_srv.call(self.init_pose_req)

        # Advertise service
        rospy.Service('move_ur3_srv',Empty,self.moveUR3Callback)

if __name__ == '__main__':
    rospy.init_node('move_ur3', log_level=rospy.DEBUG)
    move_ur3 = MoveUR3()
    rospy.spin()