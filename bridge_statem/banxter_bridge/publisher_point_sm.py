import rclpy
from rclpy.node import Node
import time

from std_msgs.msg import String, Int32


from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)


"""

     This state machine will communicate to ROS1 the coordinates to whihc the can of coke has to be moved 
     If the states goes from 0 to 1, the last received coordinate is being published to Ros1 as the goal for the end effector
        
"""
position_can = Point()
class     StateMachine(Node):

    def __init__(self):
        super().__init__('state_m')
        self.sub_pos = self.create_subscription(Point, 'position_toreach',self.pos_callback,            1)
        self.pub_point_ = self.create_publisher(Point, 'position_sub', 1)
        timer_period = 3  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        self.subscription = self.create_subscription(  String,"/ik_result",self.ik_res_callback,            1)
        self.sub = self.create_subscription(  Int32,"/state_mobrob",self.state_mobrob_callback,            1)
        self.publisher_coke = self.create_publisher(Point, '/coke_can_coords', 1)
        self.i = 0
        self.state = 0
        self.prev_state = 0
        self.prev_pos = Point()
        


    def ik_res_callback(self, msg):
        print("ik_solver_response = ",msg.data)
    def state_mobrob_callback(self, msg):
        global position_can
        self.prev_state = self.state
        self.state = msg.data
        if self.state!= self.prev_state:
            print("state is ",msg.data)
            #if state = 1 stop and reach it
            if self.state == 1:
                time.sleep(1)
                self.pub_point_.publish(position_can)
                
    def pos_callback(self, msg):
        print("received_pos = ",msg)
        global position_can
        if msg!=position_can:
            position_can = msg
            self.publisher_coke.publish(msg)
        




    """ def timer_callback(self):
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
        self.i += 1 """


def main(args=None):
    rclpy.init(args=args)

    statem = StateMachine()

    rclpy.spin(statem)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    statem.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()