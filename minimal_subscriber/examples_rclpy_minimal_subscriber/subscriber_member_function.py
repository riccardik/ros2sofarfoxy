# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import sensor_msgs.msg as SensM
from geometry_msgs.msg import Point

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        #self.subscription = self.create_subscription(  SensM.JointState,"/robot/joint_states",self.listener_callback,            10)    
        
        self.sub_2 = self.create_subscription(  Point,"/left_endpoint_pos",self.endpoint_callback,            10)  
        # prevent unused variable warning
        self.subscription = self.create_subscription(  String,"/ik_result",self.ik_res_callback,            10)        
    def ik_res_callback(self, msg):
        print(msg)
    def listener_callback(self, msg):
        #self.get_logger().info('I heard: ',msg.name)
        print(msg.name)
        print(msg.position)
        #self.get_logger().info('I heard: "%s"' % msg.data)
    def endpoint_callback(self, msg):
        #self.get_logger().info('I heard: ',msg.name)
        print(msg)
        #self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()
    #print("init")
    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
