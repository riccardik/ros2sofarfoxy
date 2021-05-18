from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros1_bridge',
            executable='dynamic_bridge',
            name='bridge_ros1'
        ),
        Node(
            package='examples_rclpy_minimal_subscriber',
            executable='publisher',
            name='send_position'
        ),
        Node(
            package='examples_rclpy_minimal_subscriber',
            executable='subscriber',
            name='send_position'
        ),
        
    ])