#!/usr/bin/env python

import rospy
import cv2
import os
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

def main():
    # Initialize ROS node
    rospy.init_node('rosbag_image_saver', anonymous=True)
    
    # Create a CV bridge
    bridge = CvBridge()
    
    # Add a counter for received messages
    message_count = 0
    
    # Ensure tmp directory exists
    tmp_dir = 'tmp_v2'
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        rospy.loginfo(f"Created directory: {tmp_dir}")
    
    def image_callback(msg):
        nonlocal message_count
        message_count += 1
        rospy.loginfo("Received image #%d with timestamp %s", message_count, msg.header.stamp)
        
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # Save the image to tmp folder
            image_filename = f'{tmp_dir}/image_{message_count:04d}.jpg'
            cv2.imwrite(image_filename, cv_image)
            
            # Print image dimensions and saved location
            rospy.loginfo("Image dimensions: %s x %s", cv_image.shape[1], cv_image.shape[0])
            rospy.loginfo(f"Saved image to {image_filename}")
            
        except Exception as e:
            rospy.logerr("Error processing image: %s", str(e))
    
    # Subscribe to the RGB image topic
    # Try different common topic names
    rgb_topics = [
        "/rgb/image_raw"
    ]
    
    # Find available image topics
    all_topics = rospy.get_published_topics()
    image_topics = [t[0] for t in all_topics if t[1] == 'sensor_msgs/Image']
    
    rospy.loginfo("Available image topics:")
    for topic in image_topics:
        rospy.loginfo("  - %s", topic)
    
    # Subscribe to the first topic in our list that exists
    rgb_topic = None
    for topic in rgb_topics:
        if topic in image_topics:
            rgb_topic = topic
            break
    
    if rgb_topic is None and image_topics:
        rgb_topic = image_topics[0]  # Use the first available image topic
        
    if rgb_topic:
        rospy.loginfo("Subscribing to topic: %s", rgb_topic)
        rospy.Subscriber(rgb_topic, Image, image_callback)
    else:
        rospy.logerr("No image topics found. Make sure your rosbag is playing.")
    
    rospy.loginfo(f"Saving images to {tmp_dir}/ folder")
    
    # Keep the node running
    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass
    
    rospy.loginfo(f"Saved {message_count} images to {tmp_dir}/ folder")

if __name__ == '__main__':
    main()
