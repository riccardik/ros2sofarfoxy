# ros2sofarfoxy
## setup bridge

(on the ros2 pc) 
add to `/etc/hosts`: `IP_ADDRESS   COMPUTER_NAME` of the ros1 pc
(the same but inverse on the ros1 pc)

build the packages:
    
    colcon build --packages-select examples_rclpy_minimal_subscriber2
    colcon build --packages-select gazebo_msgs

run:

    export ROS_MASTER_URI=http://192.168.1.195:11311 #(ip of the ros1 machine)
    source ~/ros2-ws/install/setup.bash #(path of the ros2 ws)
    ros2 run ros1_bridge dynamic_bridge

run the listener on a new terminal windows (optional):

    ros2 run examples_rclpy_minimal_subscriber2 subscriber


## Run 
on new terminal window run:

script to send point coords to ros1 (the coordinate of the desired position for the baster's left end effector)

    ros2 run examples_rclpy_minimal_subscriber2 publisher

script to move the coke can model in the ros1 gazebo simulation

    ros2 run examples_rclpy_minimal_subscriber2 move_coke

## Launch file
    
    source ~/ros2-ws/install/setup.bash
    cd ~/ros2-ws/src/minimal_subscriber2/launch
    export ROS_MASTER_URI=http://192.168.1.195:11311
    ros2 launch launch.py 

### Publish on the position topic or on the state topic

    source ~/ros2-ws/install/setup.bash

    ros2 topic pubposition_toreach geometry_msgs/msg/Point "x: 0.5 
y: 0.5
z: 0" 


    ros2 topic pub /state_mobrob std_msgs/msg/Int32 "data: 1"

### Avviare se non funziona il launchfile   

Terminale 1, la macchina a stati:
    source ~/ros2-ws/install/setup.bash
    ros2 run examples_rclpy_minimal_subscriber2 state_machine

Terminale 2, publisher della posizione continuo

    source ~/ros2-ws/install/setup.bash
    ros2 pub position_toreach geometry_msgs/msg/Point "x: 0.5 y: 0.5 z: 0.5"

Terminale 3, publisher dello stato (1 fa graspare baxter)

    source ~/ros2-ws/install/setup.bash
    ros2 topic pub /state_mobrob std_msgs/msg/Int32 "data: 1"


Terminale 4, subscriber della posizione dell'ee di baxter

    source ~/ros2-ws/install/setup.bash
    ros2 topic sub /position_sub  geometry_msgs/msg/Point 


    