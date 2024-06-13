#!/bin/bash
source /root/catkin_ws/devel/setup.bash

#configure ROS
ari_slave <edge IP>

#play rosbag looping in background with no stdout or stderr
rosbag play -l </path/to/bag> --topics /head_front_camera/depth/color/points > /dev/null 2>&1 &

#monitor and log network traffic
sudo tcpdump -i <interface> src port <port num> > logfile

#kill rosbag when done
