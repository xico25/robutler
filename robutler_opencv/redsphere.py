#!/usr/bin/env python3

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class RedSphereDetector:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        
        

    def callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            cv2.namedWindow("RawCamera",)
            cv2.imshow("Red Sphere Detection", cv_image)
            cv2.waitKey(1)
        except CvBridgeError as e:
            print(e)
        
def main():
    print("gay")
    hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    
    # Define the range of red color values in the HSV color space
    lower_red = cv2.inRange(hsv_image, (0, 50, 50), (10, 255, 255))
    upper_red = cv2.inRange(hsv_image, (160, 50, 50), (179, 255, 255))
    
    # Combine the lower and upper red ranges
    red_mask = cv2.bitwise_or(lower_red, upper_red)
    
    # Use morphological operations to remove noise and refine the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    
    # Find contours in the red mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    
    # Loop through the contours
    for c in contours:
        # Check the contour's area and circularity
        area = cv2.contourArea(c)
        if area < 100:
            continue
        (x, y), radius = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        radius = int(radius)
        if radius < 10:
            continue
        
        # Draw a circle around the red sphere
        # cv2.circle(cv_image, center, radius, (0, 0, 255), 2)
    
    # Display the image
    # cv2.namedWindow("RawCamera",)
    # cv2.imshow("Red Sphere Detection", cv_image)
    # cv2.imshow("Red Sphere Detection", cv_image)
    # cv2.waitKey(1)

if __name__ == '__main__':
    rospy.init_node('red_sphere_detector')
    detector = RedSphereDetector()
    rospy.spin()
   