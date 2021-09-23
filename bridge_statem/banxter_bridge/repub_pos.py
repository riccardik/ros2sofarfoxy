import sys

from gazebo_msgs.srv import GetEntityState
from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)

import rclpy
from rclpy.node import Node
import time


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(GetEntityState, '/spwnd_obj/get_entity_state')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = GetEntityState.Request()
        self.publisher_pos = self.create_publisher(Point, '/position_toreach', 1)

    def send_request(self):
        
        self.req.name = "coke_can"
        self.req.reference_frame="coke_can_robot"

        


        self.future = self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)

    
    while True:
        minimal_client = MinimalClientAsync()
        minimal_client.send_request()

        while rclpy.ok():
            rclpy.spin_once(minimal_client)
            if minimal_client.future.done():
                try:
                    response = minimal_client.future.result()
                except Exception as e:
                    minimal_client.get_logger().info(
                        'Service call failed %r' % (e,))
                else:
                    """minimal_client.get_logger().info(
                        'Result of add_two_ints: for %d + %d = %d' %
                        (minimal_client.req.a, minimal_client.req.b, response.sum)) """
                    print(response)
                    minimal_client.publisher_pos.publish(response.state.pose.position)
                    time.sleep(1)
                break

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()