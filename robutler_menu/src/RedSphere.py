#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
import actionlib
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal



class RedColorDetector:

    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.callback)
        
    def callback(self, data):
    
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv_image, lower_red, upper_red)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        res = cv2.bitwise_and(cv_image, cv_image, mask=mask)
        
        
        cv2.waitKey(1)
       
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate over all contours and find the one with maximum area
        max_area = 0
        max_cnt = None
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                max_cnt = cnt

        # Check if we found a red object
        if max_cnt is not None:
            print("Red Sphere Detected")
            print("Mission susceeded")
            rospy.signal_shutdown("Red Sphere Found")
            # Draw a circle around the red object
            ((x, y), radius) = cv2.minEnclosingCircle(max_cnt)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(res, center, radius, (0, 255, 0), 2)
        else:
            print("We didn t find any red sphere")

        
if __name__ == '__main__':
    rospy.init_node("red_color_detector")
    RedColorDetector()
    rospy.spin()