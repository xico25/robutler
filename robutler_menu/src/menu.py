#!/usr/bin/env python3

import rospy
import actionlib
from interactive_markers.interactive_marker_server import *
from interactive_markers.menu_handler import *
from visualization_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from functools import partial
from goal import movebase_client
from camera import CameraNode
import threading

server = None
menu_handler = MenuHandler()
locations = [
    "Living Room",
    "Big Bedroom",
    "Kitchen",
    "Mid Bedroom",
    "Office"
]

objects = [
    "Portátil",
    "Cadeira"
]

missions = [
    "Procurar um portátil no escritório",
    "Contar o número de cadeiras na sala",
    "Verificar se está alguém no quarto grande",
    "Verificar se a mesa está levantada",
    "Verificar se a vóvó está viva na varanda",
    "Fotografar divisão",
    "Contar o número de cubos azuis",
    "Verificar se a TV tá ligada"
]

def Menu():

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
    int_marker.scale = 0.1

    control = InteractiveMarkerControl()
    control.interaction_mode = InteractiveMarkerControl.BUTTON
    control.always_visible = True
    control.markers.append(Sphere(int_marker))
    int_marker.controls.append(control)

    server.insert(int_marker) 

def Sphere(sphere):
    
    marker = Marker()   
        
    marker.type = Marker.SPHERE
    marker.scale.x = sphere.scale
    marker.scale.y = sphere.scale
    marker.scale.z = sphere.scale
    marker.color.r = 0.8
    marker.color.g = 0.8
    marker.color.b = 0.8
    marker.color.a = 0.3

    return marker

def Navigation(location, feedback):
    handle = feedback.menu_entry_id
    rospy.loginfo(f"A ir para: {location} (handle ID {handle})")
  
    if location == "Big Bedroom":
        spot = "3"
        movebase_client(spot)
    elif location == "Office":
        spot = "1"
        movebase_client(spot)
    elif location == "Mid Bedroom":
        spot = "2"
        movebase_client(spot)
    elif location == "Mid Bedroom" :
        spot = "4"
        movebase_client(spot)
    elif location == "Living Room" :
        spot = "5"
        movebase_client(spot)
    else:
        return

def Photo(feedback):
    handle = feedback.menu_entry_id
    rospy.loginfo("Sorri!")

    # Inicia a captura da imagem em uma nova thread
    CameraNode()

def Detect(obj, feedback):
    handle = feedback.menu_entry_id
    rospy.loginfo(f"À procura de: {obj}")
    #server.applyChanges()

def Count(obj, feedback):
    handle = feedback.menu_entry_id
    rospy.loginfo(f"A contar número de: {obj}")
    #server.applyChanges()

def Mission(mission, feedback, location):
    handle = feedback.menu_entry_id
    rospy.loginfo("A executar missão: " + mission)

    # if mission == "Fotografar Divisão":
    #     if location == "Kitchen":
    #         spot = "3"
    #         movebase_client(spot)






if __name__ == '__main__':
    rospy.init_node("menu")
    
    server = InteractiveMarkerServer("menu")

    Menu()
    MenuMarker("marker")

    menu_handler.apply(server, "marker")
    server.applyChanges()

    rospy.spin()