#!/usr/bin/env python3

import random

import rospy
import rospkg
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose, Point, Quaternion

rospy.init_node('insert_object',log_level=rospy.INFO)

# get an instance of RosPack with the default search paths
rospack = rospkg.RosPack()
package_path = rospack.get_path('psr_apartment_description') + '/description/models/'


#Add here mode poses
placements = []
placements.append({'pose':Pose(position=Point(x=-6.09, y=-1.94, z=0.775), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'dinning_bedroom', 'place': 'table'})
placements.append({'pose':Pose(position=Point(x=-6.09, y=-2.15, z=0.775), orientation=Quaternion(x=0,y=0,z=0,w=1)),
              'room':'dinning_room', 'place': 'table'})



model_names = ['cup_glass',"plate_1",]

# Add here several models. All should be added to the robutler_description package
model_name = random.choice(model_names)

f = open( package_path + model_name + '/model.sdf' ,'r')
sdff = f.read()

rospy.wait_for_service('gazebo/spawn_sdf_model')
spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)


model_placement = random.choice(placements)
name = model_name + '_in_' + model_placement['place'] + '_of_' + model_placement['room']
spawn_model_prox(name, sdff, model_name, model_placement['pose'], "world")