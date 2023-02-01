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
    bedroom = (0.17,3.53,1)
    bathroom = (0.17,3.53,1)
    gym = (0.17,3.53,1)
    kitchen = (0.17,3.53,1)

    
    if user_choice=="1":
        goal.target_pose.pose.position.x = bedroom[0]
        goal.target_pose.pose.position.y = bedroom[1]
        goal.target_pose.pose.orientation.w = bedroom[2]
    elif user_choice=="2":
        goal.target_pose.pose.position.x = bathroom[0]
        goal.target_pose.pose.position.y = bathroom[1]
        goal.target_pose.pose.orientation.w = bathroom[2]
    elif user_choice=="3":
        goal.target_pose.pose.position.x = kitchen[0]
        goal.target_pose.pose.position.y = kitchen[1]
        goal.target_pose.pose.orientation.w = kitchen[2]
    elif user_choice=="4":
        goal.target_pose.pose.position.x = gym[0]
        goal.target_pose.pose.position.y = gym[1]
        goal.target_pose.pose.orientation.w = gym[2]
   
    elif user_choice=="5":     
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
            print("Choose your location!(To enter coords mode type 5)\n1)bedroom\n2)bathroom\n3)kitchen\n4)gym\n5)coordinates")
            user_choice=input()
            if user_choice=="e":
                break
            rospy.init_node('movebase_client_py')
            result = movebase_client(user_choice)
            if result:
                rospy.loginfo("Goal execution done!")
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")