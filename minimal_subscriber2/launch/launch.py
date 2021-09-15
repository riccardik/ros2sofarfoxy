from launch import LaunchDescription
from launch_ros.actions import Node 

import launch
import launch.actions
import launch.substitutions
import launch_ros.actions


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros1_bridge',
            executable='dynamic_bridge',
            name='bridge_ros1', output='screen'
        ),
        Node(
            package='examples_rclpy_minimal_subscriber2',
            executable='state_machine',
            name='state_machine', output='screen'
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