#! /usr/bin/env python 

import rospy
from roscpp_tutorials.srv import TwoInts, TwoIntsRequest

class ObjectSelection():
    def __init__(self):
        obj_srv = rospy.ServiceProxy("object_select", TwoInts)
        obj_msg = TwoIntsRequest()
        allowed_lst = [1,2,3,4,5]
        while not rospy.is_shutdown():
            rospy.loginfo("Seleccione el numero del objeto que quiere manipular (1-5):")
            obj = int(input())
            if obj in allowed_lst:
                obj_msg.a = obj
                result = obj_srv.call(obj_msg)
                rospy.loginfo("Objeto manipulado: ")
                rospy.loginfo(result)
            else:
                rospy.logwarn("El objeto seleccionado es erroneo")
                continue

if __name__ == '__main__':
    rospy.init_node("object_selection")
    ObjectSelection()
