# PSR - Project 3 - Robutler - Your Butler Robot

Work done by:
- Carlos Gabriel Cardoso  nº 98504
- Francisco Bastos Lopes  nº 98511
- João Gomes Cruz         nº 99980

# Inicialize

First you need to make sure that you have ROS properly installed and working in the right version then
you must install all the python dependences with 

- Then you need to install all the model package needed
```bash
cd ~/catkin_ws/src/
git clone https://github.com/aws-robotics/aws-robomaker-small-house-world
git clone https://github.com/aws-robotics/aws-robomaker-hospital-world

```

# Simulation
- To start the Robutler you need to first:
```bash
roslaunch robutler_bringup gazebo.launch
```
This will launch the simulated enviroment. Right after this you need to run in the terminal :
```bash
roslaunch robutler_bringup bringup.launch
```
This will launch your robot ready to walk in the house!!


##  Object spawns in the house :
Here are some objects you can spawn in the house:
- Blue Cubes
`rosrun psr_apartment_description cube_b_spawn`
- Laptop
`rosrun psr_apartment_description laptop_spawn`
- Red Sphere
`rosrun psr_apartment_description sphere_red_spawn`
- Table Set
`rosrun psr_apartment_description table_set_spawn`



## To open the menu with missions:
You must run: `rosrun robutler_menu menu.py`

In the RViz you must select the topic with /update in the interative markers