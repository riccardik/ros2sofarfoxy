# ros2sofarfoxy
## setup bridge

(on the ros2 pc) 
add to `/etc/hosts: IP_ADDRESS   COMPUTER_NAME` of the ros1 pc
(the same but inverse on the ros1 pc)

run:

    export ROS_MASTER_URI=http://192.168.1.195:11311 #(ip of the ros1 machine)
    source ~/ros2-ws/install/setup.bash #(path of the ros2 ws)
    ros2 run ros1_bridge dynamic_bridge

build the package and run the listener on a new terminal windows (optional):

    colcon build --packages-select examples_rclpy_minimal_subscriber
    ros2 run examples_rclpy_minimal_subscriber subscriber

(optional) build only one package

    colcon build --packages-select examples_rclpy_minimal_subscriber
    colcon build --packages-select gazebo_msgs

## Run 
on new terminal window run:

script to send point coords to ros1 (the coordinate of the desired position for the baster's left end effector)

    ros2 run examples_rclpy_minimal_subscriber publisher

script to move the coke can model in the ros1 gazebo simulation

    ros2 run examples_rclpy_minimal_subscriber move_coke


    