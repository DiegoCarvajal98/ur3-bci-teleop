#! /usr/bin/env python

import rospy
import tf2_ros
from geometry_msgs.msg import TransformStamped

class ArucoTfBroadcast():

    def ob1TfCallback(self,msg):
        self.tf_bd.sendTransform(msg)

    def ob2TfCallback(self,msg):
        self.tf_bd.sendTransform(msg)

    def ob3TfCallback(self,msg):
        self.tf_bd.sendTransform(msg)

    def ob4TfCallback(self,msg):
        self.tf_bd.sendTransform(msg)

    def ob5TfCallback(self,msg):
        self.tf_bd.sendTransform(msg)

    def __init__(self):
        self.tf_bd = tf2_ros.TransformBroadcaster()

        self.tf_sub_ob1 = rospy.Subscriber('/obj1/aruco_single/transform',TransformStamped,self.ob1TfCallback, queue_size=5)
        self.tf_sub_ob1 = rospy.Subscriber('/obj2/aruco_single/transform',TransformStamped,self.ob1TfCallback, queue_size=5)
        self.tf_sub_ob1 = rospy.Subscriber('/obj3/aruco_single/transform',TransformStamped,self.ob1TfCallback, queue_size=5)
        self.tf_sub_ob1 = rospy.Subscriber('/obj4/aruco_single/transform',TransformStamped,self.ob1TfCallback, queue_size=5)
        self.tf_sub_ob1 = rospy.Subscriber('/obj5/aruco_single/transform',TransformStamped,self.ob1TfCallback, queue_size=5)

if __name__ == '__main__':
    rospy.init_node('aruco_tf_bradcast')
    ArucoTfBroadcast()
    rospy.spin()