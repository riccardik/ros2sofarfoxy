import rclpy
from rclpy.node import Node
import time
#import roslib

from std_msgs.msg import String
#from gazebo_msgs.msg import ModelState


from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
) 
class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        #self.publisher_ = self.create_publisher(ModelState, '/gazebo/set_model_state', 1)
        self.publisher_ = self.create_publisher(Point, '/coke_can_coords', 1)
         
        timer_period = 3  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        #self.subscription = self.create_subscription(  String,"/ik_result",self.ik_res_callback,            1)
        self.i = 0

    
    def timer_callback(self):
        """
        This function will allow the user to input the desired coordinates for the coke's model
        
        """
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