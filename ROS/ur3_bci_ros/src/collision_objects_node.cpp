#include <ros/ros.h>
#include <ur3_bci_ros/CollisionObjects.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/CollisionObject.h>

int main(int argc, char** argv){
	ros::init(argc, argv, "add_collision_objects");
	ros::NodeHandle nh("~");
	ros::AsyncSpinner spinner(1);
	spinner.start();

	std::string planning_group = "arm";
	ur3_bci_ros::CollisionObjects add_collision_objects(nh, planning_group);

	return 0;
}
