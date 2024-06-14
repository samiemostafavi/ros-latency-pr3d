#!/usr/bin/env python

import rospy
import rosbag
from sensor_msgs.msg import PointCloud2
import time
import signal
import sys

# Flag to indicate when to stop the replay
stop_replay = False

def signal_handler(sig, frame):
    global stop_replay
    stop_replay = True
    rospy.loginfo("Shutting down gracefully...")

def message_callback(msg):
    # rospy.loginfo(msg)
    # timestamp here
    rospy.loginfo(msg.header.seq)

def replay_bag(bag_file, topic):
    rospy.init_node('bag_replayer', anonymous=True)
    pub = rospy.Publisher(topic, PointCloud2, queue_size=10)  # Change String to the appropriate message type
    rate = rospy.Rate(1)  # Adjust the rate as needed

    with rosbag.Bag(bag_file, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=[topic]):
            if rospy.is_shutdown() or stop_replay:
                break
            pub.publish(msg)
            message_callback(msg)
            rate.sleep()

if __name__ == '__main__':
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    try:
        bag_file = '/root/2024-06-13-17-52-44.bag'  # Change to your bag file path
        topic = '/tell_me_now'  # Change to your topic
        replay_bag(bag_file, topic)
    except rospy.ROSInterruptException:
        pass
    except Exception as e:
        rospy.logerr(e)
    finally:
        rospy.loginfo("Node has been shut down.")
