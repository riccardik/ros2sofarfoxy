from launch import LaunchDescription
from launch_ros.actions import Node 

import launch
import launch.actions
import launch.substitutions
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import launch_ros.actions


def generate_launch_description():


    return LaunchDescription([
        Node(
            package='ros1_bridge',
            executable='dynamic_bridge',
            parameters=[{
                "bridge-all-topics": '',
            }],
            name='bridge_ros1', output='screen'
        ),
        Node(
            package='banxter_bridge',
            executable='state_machine',
            name='state_machine', output='screen'
        ), 
        Node(
            package='banxter_bridge',
            executable='client_gazebo_state',
            name='republish_cancoord', output='screen'
        ), 


    ])


    """  Node(
        package='examples_rclpy_minimal_subscriber2',
        executable='publisher',
        name='send_position', output='screen'
    ),
    Node(
        package='examples_rclpy_minimal_subscriber2',
        executable='subscriber',
        name='send_position', output='screen'
    ), """