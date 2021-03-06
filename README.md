# ros2sofarfoxy
BANXTER PROJECT - SOFAR - Robotics Engineering UNIGE
## Installation and requirements
- Ubuntu 20.04 x64 (https://releases.ubuntu.com/20.04/)
- Ros1 Noetic (http://wiki.ros.org/noetic/Installation/Ubuntu, necessary to use the bridge)
- Ros2 Foxy (https://docs.ros.org/en/foxy/Installation.html)
- ros1_bridge-foxy (ros1 bridge, included in the repository but with the `colcon_build` disabled for that package, https://github.com/ros2/ros1_bridge/blob/master/README.md)

        sudo apt install ros-foxy-ros1-bridge

- baxter_common_ros2 (port of baxter messages for ros2, included, https://github.com/CentraleNantesRobotics/baxter_common_ros2)
- gazebo_ros_pkgs 

        sudo apt install ros-foxy-gazebo-ros*

## Configuration
This package will make use of the `ros1_bridge` package: to use it, is necessary to configure the host file of both the PC's that are running Ros1 and Ros2:
- on the Ros1 pc, open `/etc/hosts` with a text editor and add the following line: `IP_ADDRESS   COMPUTER_NAME`, where the IP address and the computer name are the ones of the Ros2 computer.
- on the Ros2 pc, add the ones of the Ros1 pc
If this pachage is used as a bridge between two simulations, one in Ros1 and one in Ros2, the name of the frame of the mobile robot has to be set in the file `./bridge_statem/banxter_bridge/repub_pose.py`, at the line:

      self.req.reference_frame="coke_can_robot"
the `coke_can_robot` has to be substituted with the name of the model of the robot in Gazebo.


## Build the packages
build the packages (i will assume `~/ros2-ws/` as the Current Ros2 workspace):
    
    source ~/ros2-ws/install/setup.bash 
    cd  ~/ros2-ws/
    colcon build --symlink-install
    colcon build --packages-select banxter_bridge
    colcon build --packages-select gazebo_msgs





## Run the package
Is possible to run the package launching the single nodes or by using a launch file.
### Run the single nodes
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
    
    export ROS_MASTER_URI=http://192.168.1.195:11311 #IP of the Ros1 machine
    export ROS_MASTER_URI=http://130.251.13.118:11311 
    source ~/ros2-ws/install/setup.bash #(path of the ros2 ws)
    cd ~/ros2-ws/src/bridge_statem/launch
    ros2 launch launch.py 

Launch the gazebo simulation:

    export GAZEBO_MODEL_PATH=/home/rick/ros2-ws/src/bridge_statem/models/:$GAZEBO_MODEL_PATH
    source ~/ros2-ws/install/setup.bash 
    cd ~/ros2-ws/src/bridge_statem/launch
    ros2 launch gazebo.launch.py 

## Using the package
The package allows to communicate from a ROS2 instance to a ROS1 instance, running on another pc (or in a virtual machine) to send commands directed to the simulation of a Baxter robot (running on ROS1 using Gazebo).

This package allows the position control of a 3D model (in this case a coke can) that will move in the environment: the Baxter robot is ideally positioned over a mobile robot that is navigating the environment, for this reason is necessary to send in the Ros1 simulation the position of the can relative to the robot (the can will move over time with respect to the fixed (in the simulation) robot).

This package will offer the support as a bridge between the two simulation, the mobile robot will publish its position in the environment, the position of the coke can relative to it will be comoputed and sent to ROS1. When the robot will reach the desired position, the state machine will change state and it will send a command to Baxter to reach the Coke can with its left end-effector(it is a model without physics and collision, just a placeholder to better visualize the goal).


### The state machine
The state machine has a very simple implementation, it allow for two possible states:
- `0` : the mobile robot is still moving towards the goal. The state machine will communicate to Ros1 the relative position of the coke can with respect to the Baxter robot.
- `1` : the mobile robot is arrived to the goal. When the transition from `0` to `1` happens, the state machine will communicate to the Baxter robot in Ros1 to reach the last received position of the Coke can.

### Interaction
This package is used as a bridge between a Ros1 simulation () and a Ros2 simulation, were a mobile robot is navigating the environment. In both simulation, is present a can of coke that has to represent the goal.
The position of the can in the Ros2 simulation is fixed, and the mobile robot is moving. In Ros1, the Baxter robot is fixed and the can will move with respect to it, depending on how the mobile robot moves.
To test the behavior, a gazebo simulation is provided (refer to the section "Testing the full package").




## Testing
Is possible to launch all the node separately for testing purposes.
### Publish on the position topic:
In this topic the position of coke can with respect to the mobile robot will be published:

    source ~/ros2-ws/install/setup.bash
    ros2 topic pub /position_toreach geometry_msgs/msg/Point "x: 0.5 
    y: 0.5
    z: 0" 
### Publish on the state topic:
In this topic the state of the robot will be published

    ros2 topic pub /state_mobrob std_msgs/msg/Int32 "data: 1"

### Spawn coke model on gazebo
In a terminal window launch gazebo

    ros2 launch gazebo_ros gazebo.launch.py

In a new terminal window call the model spawn

    ros2 run gazebo_ros spawn_entity.py -entity coke_can2 -x 0 -y 0 -z 0 -file /home/rick/ros2-ws/src/bridge_statem/models/coke_can2/model.sdf

### Testing the state machine

Terminal 1, the finite state machine:

    source ~/ros2-ws/install/setup.bash
    ros2 run banxter_bridge state_machine

Terminal 2, publishing the point destination for the coke can model, it will move in the Ros1 simulation if it was running

    source ~/ros2-ws/install/setup.bash
    ros2 pub position_toreach geometry_msgs/msg/Point "x: 0.5 y: 0.5 z: 0.5"

Terminal 3, publishing the state of the mobile robot to the state machine

    source ~/ros2-ws/install/setup.bash
    ros2 topic pub /state_mobrob std_msgs/msg/Int32 "data: 1"


Terminal 4, it will visualize the output of the state machine, this topic will be then passed to the Ros1 simulation and will contain the goal for the left end effector 

    source ~/ros2-ws/install/setup.bash
    ros2 topic sub /position_sub  geometry_msgs/msg/Point 

### Testing the bridge
On the Ros1 pc launch the Baster's simulation, then aunch the main launch file:

    export ROS_MASTER_URI=http://192.168.1.195:11311
    source ~/ros2-ws/install/setup.bash #(path of the ros2 ws)
    cd ~/ros2-ws/src/bridge_statem/launch
    ros2 launch launch.py 
 This launch file will also run the Bridge between Ros1 and Ros2.
 To test that the bridge is actually working is possible to publish the command to move the coke can in the Ros1 simulation:

    source ~/ros2-ws/install/setup.bash
    ros2 topic pub '/coke_can_coords geometry_msgs/msg/Point "x: 0.5 
    y: 0.5
    z: 0" 

We can then send another command to the Ros1 simulation: this will move the Baxter's left end effector's position:

    source ~/ros2-ws/install/setup.bash
    ros2 topic pub '/position_sub geometry_msgs/msg/Point "x: 0.5 
    y: 0.5
    z: 0" 


## Testing the full package

This package offers a Gazebo simulation to test if the package is working correctly.
The following command will launch a Gazebo simulation that will contain two cans of coke 's model, named `coke_can_robot` that will simulate the frame of the mobile robot that is navigating the environment and `coke_can` that will simulate the position of the end goal.

    export GAZEBO_MODEL_PATH=/home/rick/ros2-ws/src/bridge_statem/models/:$GAZEBO_MODEL_PATH
    source ~/ros2-ws/install/setup.bash 
    cd ~/ros2-ws/src/bridge_statem/launch
    ros2 launch gazebo.launch.py 


Then launch the main launch file, to initialize the necessary nodes:

    export ROS_MASTER_URI=http://130.251.13.118:11311 
    source ~/ros2-ws/install/setup.bash #(path of the ros2 ws)
    cd ~/ros2-ws/src/bridge_statem/launch
    ros2 launch launch.py 


The package will compute continously the relative position of the `coke_can` to the robot: this position is the one that will be published on the Ros1 simulation as the position for the model of coke and, in the end, as goal position for the end effector when the mobile robot has stopped.
We can now change the position of the `coke_can_robot`in Ros2 with the following command (using the Set Entity Gazebo service) and see how this affects the Ros1 simulation: the can will move with respect to the Baxter robot.

    ros2 service call /spwnd_obj/set_entity_state 'gazebo_msgs/SetEntityState' '{state: {name: "coke_can_robot", pose: {position: {x:2, y: 2}}}}'

If then we send a `1` command on the state topic, the Baxter robot in the Ros1 simulation will move the end effector in the position that the can is in:

    ros2 topic pub /state_mobrob std_msgs/msg/Int32 "data: 1"
    

## Generated topic and nodes
<img src="pictures/rosgraph.png" width="800">
Most of the topics and nodes shown in the image are the ones generated by the Baxter's simulation and the control SDK.
Here follow the description of the implemented nodes:
    
 
  
  - `republish_cancoord`: this node will continously read the position of the `coke_can` model with respect to the mobile robot frame and will communicate it as a Point message to the state machine using the topic `/position_toreach`
  - `state_machine`: this node contains the state machine, it will receive the position of the previous node in the topic `/position_toreach` and it will republish it on the topic `/coke_can_coords`. It will also receive the state of the mobile robot (topic `/state_mobrob`) and, as described before in the "State machine" section, when it will be necessary it will publish the last position received from `/position_toreach` to `/position_sub`: this will trigger the robot in the Ros1 simulation to move the end effector in that precise position.
  - `bridge_ros1`: this node will publish the necessary topic from Ros1 to Ros2 and viceversa: in this case, the topics `/position_sub` and `/coke_can_coords` are published to Ros1.
  
