#!/usr/bin/env python

import rospy
import sys
import tf2_ros
import moveit_commander
from geometry_msgs.msg import Pose, TransformStamped
from moveit_msgs.msg import DisplayTrajectory
from roscpp_tutorials.srv import TwoInts, TwoIntsRequest, TwoIntsResponse
from std_srvs.srv import Empty, EmptyRequest

class UR3MoveGroup(object):

    def objSelectCallback(self, req):
        tool_request = TwoIntsRequest()
        tool_request.a = req.a
        rospy.logdebug("Request: " + str(req.a))

        predict = self.bci_prediction(tool_request)

        rospy.logdebug("Predicted stimulus: %d",predict.sum)

        if predict.sum == 1 and self.tf_bd.can_transform("base_link","obj1_frame",rospy.Time(0)):
            trans = self.tf_bd.lookup_transform("base_link","obj1_frame",rospy.Time(0))
            self.trans_pub.publish(trans)

            self.move_ur3_srv.call(EmptyRequest())

        elif predict.sum == 2 and self.tf_bd.can_transform("base_link","obj2_frame",rospy.Time(0)):
            trans = self.tf_bd.lookup_transform("base_link","obj2_frame",rospy.Time(0))
            self.trans_pub.publish(trans)
            rospy.logdebug("Sending request to execute motion")
            self.move_ur3_srv.call(EmptyRequest())
            rospy.logdebug("Motion executed")

        elif predict.sum == 3 and self.tf_bd.can_transform("base_link","obj3_frame",rospy.Time(0)):
            trans = self.tf_bd.lookup_transform("base_link","obj3_frame",rospy.Time(0))
            self.trans_pub.publish(trans)

            self.move_ur3_srv.call(EmptyRequest())

        elif predict.sum == 4 and self.tf_bd.can_transform("base_link","obj4_frame",rospy.Time(0)):
            trans = self.tf_bd.lookup_transform("base_link","obj4_frame",rospy.Time(0))
            self.trans_pub.publish(trans)

            self.move_ur3_srv.call(EmptyRequest())

        elif predict.sum == 5 and self.tf_bd.can_transform("base_link","obj5_frame",rospy.Time(0)):
            trans = self.tf_bd.lookup_transform("base_link","obj5_frame",rospy.Time(0))
            self.trans_pub.publish(trans)

            self.move_ur3_srv.call(EmptyRequest())

        resp = TwoIntsResponse()
        resp.sum = predict.sum

        return resp

    def __init__(self):
        
        self.tf_bd = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_bd, 5)

        self.trans_pub = rospy.Publisher('object_transform',TransformStamped,queue_size=5)

        rospy.wait_for_service('bci_prediction')
        self.bci_prediction = rospy.ServiceProxy('bci_prediction',TwoInts)

        rospy.wait_for_service('move_ur3_srv')
        self.move_ur3_srv = rospy.ServiceProxy('move_ur3_srv', Empty)

        rospy.Service('object_select', TwoInts, self.objSelectCallback)

if __name__ == '__main__':
    rospy.init_node('ur3_movegroup', anonymous=True, log_level=rospy.DEBUG)
    ur3_movegroup = UR3MoveGroup()
    rospy.spin()
