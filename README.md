# ros2sofarfoxy
BANXTER PROJECT - SOFAR - Robotics Engineering UNIGE
## Installation and requirements
- Ubuntu 20.04 x64 (https://releases.ubuntu.com/20.04/)
- Ros1 Noetic (http://wiki.ros.org/noetic/Installation/Ubuntu, necessary to use the bridge)
- Ros2 Foxy (https://docs.ros.org/en/foxy/Installation.html)
- ros1_bridge-foxy (ros1 bridge, included in the repository, https://github.com/ros2/ros1_bridge/blob/master/README.md)

    sudo apt install ros-foxy-ros1-bridge

- baxter_common_ros2 (port of baxter messages for ros2, included, https://github.com/CentraleNantesRobotics/baxter_common_ros2)
## Setup and build the package
### Setup bridge
(on the ros2 pc) 
add to `/etc/hosts`: `IP_ADDRESS   COMPUTER_NAME` of the ros1 pc
(the same but inverse on the ros1 pc)

build the packages:
    
    source ~/ros2-ws/install/setup.bash 
    cd  ~/ros2-ws/
    colcon build --symlink-install
    colcon build --packages-select banxter_bridge
    colcon build --packages-select gazebo_msgs
## Run the package
Is possible to run the package launching the single nodes or by using a launch file.
### Run single nodesl
- Run the bridge and the state machine:

    Run the single nodes:

        export ROS_MASTER_URI=http://192.168.1.195:11311 #(ip of the ros1 machine)
        source ~/ros2-ws/install/setup.bash #(path of the ros2 ws)
        ros2 run ros1_bridge dynamic_bridge
        ros2 run banxter_bridge state_machine
- On new terminal window run (optional, for testing purposes):

    script to send point coords to ros1 (the coordinate of the desired position for the baster's left end effector)

        ros2 run banxter_bridge publisher

    script to move the coke can model in the ros1 gazebo simulation

        ros2 run banxter_bridge move_coke


### Run the Launch file
Is possible to use a launch file to avoid using multiple terminal windows:
    
    export ROS_MASTER_URI=http://192.168.1.195:11311 
    source ~/ros2-ws/install/setup.bash #(path of the ros2 ws)
    cd ~/ros2-ws/src/bridge_statem/launch
    ros2 ros2 launch launch.py 

## Using the package
The package allows to communicate from a ROS2 instance to a ROS1 instance, running on another pc (or in a virtual machine) to send commands directed to the simulation of a Baxter robot (running on ROS1 using Gazebo).

This package allows the position control of a 3D model (in this case a coke can) that will move in the environment: the Baxter robot is ideally positioned over a mobile robot that is navigating the environment, for this reason is necessary to send in the Ros1 simulation the position of the can relative to the robot (the can will move over time with respect to the fixed (in the simulation) robot).

This package will offer the support as a bridge between the two simulation, the mobile robot will publish its position in the environment, the position of the coke can relative to it will be comoputed and sent to ROS1. When the robot will reach the desired position, the state machine will change state and it will send a command to Baxter to reach the Coke can with its left end-effector(it is a model without physics and collision, just a placeholder to better visualize the goal).

### The state machine
The state machine is a very simple implementation, it allow for two possible states:
- `0` : the mobile robot is still moving towards the goal. The state machine will communicate to Ros1 the relative position of the coke can with respect to the Baxter robot.
- `1` : the mobile robot is arrived to the goal. The state machine will communicate to the Baxter robot in Ros1 to reach the last received position of the Coke can.

### Publish on the position topic:
In this topic the position of coke can with respect to the mobile robot will be published:

    source ~/ros2-ws/install/setup.bash
    ros2 topic pub /position_toreach geometry_msgs/msg/Point "x: 0.5 
    y: 0.5
    z: 0" 

### Publish on the state topic:
In this topic the state of the robot will be published

    ros2 topic pub /state_mobrob std_msgs/msg/Int32 "data: 1"











### Avviare se non funziona il launchfile   

Terminale 1, la macchina a stati:

    source ~/ros2-ws/install/setup.bash
    ros2 run banxter_bridge state_machine

Terminale 2, publisher della posizione continuo

    source ~/ros2-ws/install/setup.bash
    ros2 pub position_toreach geometry_msgs/msg/Point "x: 0.5 y: 0.5 z: 0.5"

Terminale 3, publisher dello stato (1 fa graspare baxter)

    source ~/ros2-ws/install/setup.bash
    ros2 topic pub /state_mobrob std_msgs/msg/Int32 "data: 1"


Terminale 4, subscriber della posizione dell'ee di baxter

    source ~/ros2-ws/install/setup.bash
    ros2 topic sub /position_sub  geometry_msgs/msg/Point 


    