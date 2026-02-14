#!/usr/bin/env python3
import rclpy, signal, sys, math
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SimpleController(Node):
    def __init__(self):
        super().__init__('simple_controller')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.tick)
        self.t = 0.0

    def tick(self):
        msg = Twist()
        msg.linear.x = 0.2
        msg.angular.z = 0.25 * math.sin(self.t)
        self.pub.publish(msg)
        self.t += 0.1

def main():
    rclpy.init()
    node = SimpleController()
    def shutdown(signum, frame):
        node.get_logger().info('Shutting down')
        rclpy.shutdown()
        sys.exit(0)
    signal.signal(signal.SIGINT, shutdown)
    rclpy.spin(node)

if __name__ == '__main__':
    main()
