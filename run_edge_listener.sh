#!/bin/bash
source /root/catkin_ws/devel/setup.bash

#configure ROS
ros_master

#launch roscore
roscore &

sleep 2

#start listener to subscribe to pointcloud topic
rostopic echo /head_front_camera/depth/color/points > /dev/null 2>&1 &

#monitor and log network traffic
sudo tcpdump -i <interface> src port <port num> > logfile

#kill ros listener when done
