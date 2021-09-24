import rclpy
from rclpy.node import Node
import time

from std_msgs.msg import String


from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
"""
Test node to see if the goal position to the end effector is correctly sent and received in Ros1
        
    """
class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Point, 'position_sub', 1)
        timer_period = 3  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.subscription = self.create_subscription(  String,"/ik_result",self.ik_res_callback,            1)
        self.i = 0

    def ik_res_callback(self, msg):
        print("ik_solver_response = ",msg.data)
    def timer_callback(self):
        msg = Point()
        print("insert x")
        msg.x=float(input())
        print("insert y")
        msg.y=float(input())
        print("insert z")
        msg.z=float(input())
        self.publisher_.publish(msg)
        #self.get_logger().info('Publishing: "%s"' % msg.data)
        time.sleep(1)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()