#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2

def callback(data):
    # Republish the received message
    # pub.publish(data)
    rospy.loginfo(data.header.seq)

def listener():
    # Initialize the ROS node
    rospy.init_node('receiver', anonymous=True)

    # Subscribe to the existing topic
    rospy.Subscriber('/tell_me_now', PointCloud2, callback)

    # Keep the node running
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
