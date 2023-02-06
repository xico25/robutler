#!/usr/bin/env python3

import rospy
import actionlib
from interactive_markers.interactive_marker_server import *
from interactive_markers.menu_handler import *
from visualization_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from functools import partial
from goal import movebase_client

server = None
menu_handler = MenuHandler()
locations = [
    "Living Room",
    "Bedroom",
    "Kitchen"
]

objects = [
    "Computador",
    "Cadeira"
]

missions = [
    "Procurar um computador no escritório",
    "Contar o número de cadeiras na sala"
]

def Menu():

    # client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    # client.wait_for_server()

    # goal = MoveBaseGoal()
    # goal.target_pose.header.frame_id = "map"
    # goal.target_pose.header.stamp = rospy.Time.now()
    # bedroom = (0.17,3.53,1)
    # bathroom = (0.17,3.53,1)
    # gym = (0.17,3.53,1)
    # kitchen = (0.17,3.53,1)

    # if feedback.event_type == InteractiveMarkerFeedback.MENU_SELECT:
    #     if feedback.menu_entry_id == 1:
    #         # Go to the kitchen
    #         rospy.loginfo("Going to the kitchen")
    #         goal.target_pose.pose.position.x = kitchen[0]
    #         goal.target_pose.pose.position.y = kitchen[1]
    #         goal.target_pose.pose.orientation.w = kitchen[2]
    #         print("Arrived, I want a beer")
    #     elif feedback.menu_entry_id == 2:
    #         # Go to the bedroom
    #         rospy.loginfo("Going to the bedroom")
    #         goal.target_pose.pose.position.x = bedroom[0]
    #         goal.target_pose.pose.position.y = bedroom[1]
    #         goal.target_pose.pose.orientation.w = bedroom[2]
    #         print("Arrived, going to sleep kkkkkkk")
    #     client.send_goal(goal)

    # Menu de Navegação
    go_to = menu_handler.insert("Divisões da Casa")
    for loc in locations:
        menu_handler.insert(loc, parent=go_to, callback=partial(Navigation, loc))

    # Menu de Visualização
    photo_handle = menu_handler.insert("Tirar uma foto", callback = Photo)
    detect_handle = menu_handler.insert("Procurar")
    for obj in objects:
        menu_handler.insert(obj, parent=detect_handle, callback=partial(Detect, obj))
    
    # Menu Contador
    count_handle = menu_handler.insert("Contar número de objetos")
    for obj in objects:
        menu_handler.insert(obj, parent=count_handle, callback=partial(Count, obj))

    # Menu de Missões
    mission_handle = menu_handler.insert("Missiões")
    for mission in missions:
        menu_handler.insert(mission, parent=mission_handle, callback=partial(Mission, mission))

def MenuMarker(marker):
    
    int_marker = InteractiveMarker()
    int_marker.header.frame_id = "base_link"
    int_marker.name = marker
    int_marker.pose.position.z = 1.2
    int_marker.scale = 0.2

    control = InteractiveMarkerControl()
    control.interaction_mode = InteractiveMarkerControl.BUTTON
    control.always_visible = True
    control.markers.append(Cube(int_marker))
    int_marker.controls.append(control)

    server.insert(int_marker) 

def Cube(cube):
    
    marker = Marker()   
        
    marker.type = Marker.CUBE
    marker.scale.x = cube.scale
    marker.scale.y = cube.scale
    marker.scale.z = cube.scale
    marker.color.r = 0.8
    marker.color.g = 0.8
    marker.color.b = 0.8
    marker.color.a = 1.0

    return marker

def Navigation(location, feedback):
    handle = feedback.menu_entry_id
    rospy.loginfo(f"A ir para: {location} (handle ID {handle})")
  
    if location == "Kitchen":
        spot = "3"
        movebase_client(spot)
    elif location == "Bedroom":
        spot = "1"
        movebase_client(spot)
    else:
        return
    

    # client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    # client.wait_for_server()

    # goal = MoveBaseGoal()
    # goal.target_pose.header.frame_id = "map"
    # goal.target_pose.header.stamp = rospy.Time.now()

    # if location == "Bedroom":
    #     goal.target_pose.pose.position.x = locations["Bedroom"][0]
    #     goal.target_pose.pose.position.y = locations["Bedroom"][1]
    #     goal.target_pose.pose.orientation.w = locations["Bedroom"][2]
    # elif location == "Kitchen":
    #     goal.target_pose.pose.position.x = locations["Kitchen"][0]
    #     goal.target_pose.pose.position.y = locations["Kitchen"][1]
    #     goal.target_pose.pose.orientation.w = locations["Kitchen"][2]
    # elif location == "Living Room":
    #     goal.target_pose.pose.position.x = locations["Living Room"][0]
    #     goal.target_pose.pose.position.y = locations["Living Room"][1]
    #     goal.target_pose.pose.orientation.w = locations["Living Room"][2]
    
    # else:
    #     return

    # client.send_goal(goal)
    # client.wait_for_result()

    # if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
    #     rospy.loginfo("Sucesso! Estou aqui!!")
    # else:
    #     rospy.loginfo("Sou um burro stressado, não consigo chegar ao destino")


def Photo(feedback):
    rospy.loginfo("Sorri!")
    #server.applyChanges()

def Detect(obj, feedback):
    handle = feedback.menu_entry_id
    rospy.loginfo(f"À procura de: {obj}")
    #server.applyChanges()

def Count(obj, feedback):
    handle = feedback.menu_entry_id
    rospy.loginfo(f"A contar número de: {obj}")
    #server.applyChanges()

def Mission(mission, feedback):
    handle = feedback.menu_entry_id
    rospy.loginfo("A executar missão: " + mission)
    #server.applyChanges()

if __name__ == '__main__':
    rospy.init_node("menu")
    
    server = InteractiveMarkerServer("menu")

    Menu()
    MenuMarker("marker")

    menu_handler.apply(server, "marker")
    server.applyChanges()

    rospy.spin()