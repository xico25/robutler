#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def movebase_client(user_choice):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    office = (0,3,1)
    midbedroom = (-2.72,3.75,1)
    bigbedroom = (-6.10,3.00,1)
    kitchen = (0.17,3.53,1)
    livingroom =(-2.05,-3,70,0)

    
    if user_choice=="1":
        goal.target_pose.pose.position.x = office[0]
        goal.target_pose.pose.position.y = office[1]
        goal.target_pose.pose.orientation.w = office[2]
    elif user_choice=="2":
        goal.target_pose.pose.position.x = midbedroom[0]
        goal.target_pose.pose.position.y = midbedroom[1]
        goal.target_pose.pose.orientation.w = midbedroom[2]
    elif user_choice=="3":
        goal.target_pose.pose.position.x = bigbedroom[0]
        goal.target_pose.pose.position.y = bigbedroom[1]
        goal.target_pose.pose.orientation.w = bigbedroom[2]
    elif user_choice=="4":
        goal.target_pose.pose.position.x = kitchen[0]
        goal.target_pose.pose.position.y = kitchen[1]
        goal.target_pose.pose.orientation.w = kitchen[2]
   
    elif user_choice=="5":     
        goal.target_pose.pose.position.x = livingroom[0]
        goal.target_pose.pose.position.y = livingroom[1]
        goal.target_pose.pose.orientation.w = livingroom[2]
    
    elif user_choice=="6":     
        goal.target_pose.pose.position.x = float(input("x="))
        goal.target_pose.pose.position.y = float(input("y="))
        goal.target_pose.pose.orientation.w = float(input("w="))

        


    else:
        print("Choose Another Location")
        return
    
    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()
        

if __name__ == '__main__':
   
    while True: 
        try:
            print("Choose your location!(To enter coords mode type 5)\n1)office\n2)midbedroom\n3)kitchen\n4)gym\n5)coordinates\n6)Navigation")
            user_choice=input()
            if user_choice=="e":
                break
            rospy.init_node('movebase_client_py')
            result = movebase_client(user_choice)
            if result:
                rospy.loginfo("Goal execution done!")
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")