#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class CameraNode:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.camera_callback)

    def camera_callback(self, data):
        while True:
            try:
                cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            except CvBridgeError as e:
                print(e)

            cv2.imshow("Robot Camera", cv_image)
        
            k = cv2.waitKey(1)
            if k == ord("p"):
                filename = "/home/francisco/catkin_ws/src/robutler/images/image_" + str(rospy.get_rostime().to_sec()) + ".jpg"
                cv2.imwrite(filename, cv_image)
                print("Image saved:", filename)
            elif k == ord("e"):
                cv2.destroyAllWindows()
                break

if __name__ == '__main__':
    rospy.init_node("photo")
    node = CameraNode()
    rospy.spin()
