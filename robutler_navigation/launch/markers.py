#!/usr/bin/env python3
from interactive_markers.interactive_marker_server import InteractiveMarker, InteractiveMarkerServer
import rospy
from interactive_markers.menu_handler import MenuHandler
import move_base 

def processFeedback(feedback):
    move_base.move_base(feedback.menu_entry_id)

if __name__ == '__main__':
    rospy.init_node('interactive_marker_menu')
    server = InteractiveMarkerServer("interactive_marker_menu")
    menu_handler = MenuHandler()
    
    quarto_int_marker = InteractiveMarker()
    quarto_int_marker.header.frame_id = "map"
    quarto_int_marker.name = "quarto"
    quarto_int_marker.description = "Go to Quarto"
    quarto_int_marker.pose.position.x = 0.17
    quarto_int_marker.pose.position.y = 3.53
    quarto_int_marker.pose.orientation.w = 1.0

    menu_handler.insert("Quarto", callback=processFeedback)
    menu_handler.apply(server, quarto_int_marker.name)
    server.insert(quarto_int_marker, processFeedback)
    server.applyChanges()
    rospy.spin()